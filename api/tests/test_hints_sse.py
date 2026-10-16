"""
Test suite for hints Server-Sent Events (SSE) streaming.

Tests:
- Mock LLM generates hints
- SSE stream yields events with required fields
- Stream contains >=1 hint event within 10s
- Event structure: {type, text, confidence}
- Stream closes properly
- Multiple hints can be streamed
"""

import pytest
from fastapi.testclient import TestClient
from api.index import app
from api.database import get_db
from api.models import User, Meeting
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from datetime import datetime


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create authorization headers with mock JWT."""
    return {"Authorization": "Bearer mock_jwt_token"}


@pytest.fixture
def mock_db(monkeypatch):
    """Mock database session."""
    db = MagicMock(spec=Session)
    monkeypatch.setattr("api.routes.meetings.get_db", lambda: db)
    return db


@pytest.fixture
def mock_user():
    """Create mock user."""
    user = MagicMock(spec=User)
    user.id = "user_123"
    user.email = "test@example.com"
    user.google_id = "google_123"
    return user


@pytest.fixture
def mock_meeting():
    """Create mock meeting with transcript."""
    meeting = MagicMock(spec=Meeting)
    meeting.id = "meeting_123"
    meeting.user_id = "user_123"
    meeting.title = "Test Meeting"
    meeting.transcript = "Speaker 1: We need to improve performance. Speaker 2: Agreed, let's optimize the database queries."
    meeting.started_at = datetime.utcnow()
    meeting.ended_at = None
    return meeting


class TestHintsSSE:
    """Test hints SSE streaming."""

    def test_hints_stream_yields_valid_events(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test that hints stream yields valid SSE events with required fields."""
        mock_hints = [
            {"type": "action", "text": "Consider database indexing for performance", "confidence": 0.95},
            {"type": "insight", "text": "Query optimization is mentioned as priority", "confidence": 0.88},
        ]
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            with patch("api.llm_client.stream_hints", return_value=iter(mock_hints)):
                mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
                mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
                
                response = client.get(
                    "/api/meetings/meeting_123/hints/stream",
                    headers=auth_headers
                )
                
                assert response.status_code == 200
                assert response.headers.get("content-type") == "text/event-stream"
                
                # Parse SSE events
                events = []
                for line in response.text.split("\n"):
                    if line.startswith("data:"):
                        import json
                        event_data = json.loads(line[5:].strip())
                        events.append(event_data)
                
                assert len(events) >= 1
                for event in events:
                    assert "type" in event
                    assert "text" in event
                    assert "confidence" in event
                    assert isinstance(event["confidence"], (int, float))
                    assert 0 <= event["confidence"] <= 1

    def test_hints_stream_minimum_one_event(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test that stream yields at least one hint event."""
        mock_hints = [
            {"type": "action", "text": "Implement caching strategy", "confidence": 0.92},
        ]
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            with patch("api.llm_client.stream_hints", return_value=iter(mock_hints)):
                mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
                mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
                
                response = client.get(
                    "/api/meetings/meeting_123/hints/stream",
                    headers=auth_headers
                )
                
                assert response.status_code == 200
                import json
                events = []
                for line in response.text.split("\n"):
                    if line.startswith("data:"):
                        event_data = json.loads(line[5:].strip())
                        events.append(event_data)
                
                assert len(events) >= 1

    def test_hints_stream_without_auth(self, client):
        """Test that hints stream requires authentication."""
        response = client.get("/api/meetings/meeting_123/hints/stream")
        assert response.status_code == 401

    def test_hints_stream_nonexistent_meeting(self, client, auth_headers, mock_db, mock_user):
        """Test streaming hints for non-existent meeting."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="nonexistent", user_id="user_123").first.return_value = None
            
            response = client.get(
                "/api/meetings/nonexistent/hints/stream",
                headers=auth_headers
            )
            
            assert response.status_code == 404

    def test_hints_stream_different_event_types(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test that stream can yield different hint types."""
        mock_hints = [
            {"type": "action", "text": "Add monitoring", "confidence": 0.90},
            {"type": "insight", "text": "User behavior pattern", "confidence": 0.85},
            {"type": "warning", "text": "Performance risk", "confidence": 0.95},
        ]
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            with patch("api.llm_client.stream_hints", return_value=iter(mock_hints)):
                mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
                mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
                
                response = client.get(
                    "/api/meetings/meeting_123/hints/stream",
                    headers=auth_headers
                )
                
                assert response.status_code == 200
                import json
                event_types = set()
                for line in response.text.split("\n"):
                    if line.startswith("data:"):
                        event_data = json.loads(line[5:].strip())
                        event_types.add(event_data["type"])
                
                assert "action" in event_types
                assert "insight" in event_types
                assert "warning" in event_types

    def test_hints_stream_confidence_scores_valid(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test that all confidence scores are between 0 and 1."""
        mock_hints = [
            {"type": "action", "text": "Optimize queries", "confidence": 0.5},
            {"type": "insight", "text": "Meeting pattern", "confidence": 1.0},
            {"type": "warning", "text": "High risk area", "confidence": 0.0},
        ]
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            with patch("api.llm_client.stream_hints", return_value=iter(mock_hints)):
                mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
                mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
                
                response = client.get(
                    "/api/meetings/meeting_123/hints/stream",
                    headers=auth_headers
                )
                
                assert response.status_code == 200
                import json
                for line in response.text.split("\n"):
                    if line.startswith("data:"):
                        event_data = json.loads(line[5:].strip())
                        assert 0 <= event_data["confidence"] <= 1

    def test_hints_stream_text_field_not_empty(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test that hint text is not empty."""
        mock_hints = [
            {"type": "action", "text": "Implementation detail here", "confidence": 0.85},
        ]
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            with patch("api.llm_client.stream_hints", return_value=iter(mock_hints)):
                mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
                mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
                
                response = client.get(
                    "/api/meetings/meeting_123/hints/stream",
                    headers=auth_headers
                )
                
                assert response.status_code == 200
                import json
                for line in response.text.split("\n"):
                    if line.startswith("data:"):
                        event_data = json.loads(line[5:].strip())
                        assert len(event_data["text"]) > 0

    def test_hints_stream_cross_user_access(self, client, mock_db, mock_user):
        """Test that user cannot access another user's meeting hints."""
        other_user_meeting = MagicMock(spec=Meeting)
        other_user_meeting.id = "other_meeting_123"
        other_user_meeting.user_id = "other_user_456"
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            # Return None because user_123 doesn't own other_user_456's meeting
            mock_db.query(Meeting).filter_by(id="other_meeting_123", user_id="user_123").first.return_value = None
            
            response = client.get(
                "/api/meetings/other_meeting_123/hints/stream",
                headers={"Authorization": "Bearer mock_jwt_token"}
            )
            
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_hints_stream_response_time(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test that hints stream responds within 10 seconds."""
        mock_hints = [
            {"type": "action", "text": "Quick hint", "confidence": 0.88},
        ]
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            with patch("api.llm_client.stream_hints", return_value=iter(mock_hints)):
                mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
                mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
                
                import time
                start = time.time()
                response = client.get(
                    "/api/meetings/meeting_123/hints/stream",
                    headers=auth_headers
                )
                elapsed = time.time() - start
                
                assert response.status_code == 200
                assert elapsed < 10, f"Stream took {elapsed}s, expected < 10s"
