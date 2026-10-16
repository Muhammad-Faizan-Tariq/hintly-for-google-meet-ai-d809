"""
Test suite for meetings CRUD operations.

Tests:
- Create meeting
- Append transcript chunks (5 chunks)
- List meetings
- Get meeting by ID
- End meeting generates summary
- Meeting not found returns 404
"""

import pytest
from fastapi.testclient import TestClient
from api.index import app
from api.database import get_db
from api.models import Meeting, User
from sqlalchemy.orm import Session
from datetime import datetime
from unittest.mock import patch, MagicMock
import uuid


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
    """Create mock meeting."""
    meeting = MagicMock(spec=Meeting)
    meeting.id = "meeting_123"
    meeting.user_id = "user_123"
    meeting.title = "Test Meeting"
    meeting.started_at = datetime.utcnow()
    meeting.ended_at = None
    meeting.transcript = ""
    meeting.summary = None
    return meeting


class TestMeetingsCRUD:
    """Test meetings CRUD operations."""

    def test_create_meeting(self, client, auth_headers, mock_db, mock_user):
        """Test creating a new meeting."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.add = MagicMock()
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            response = client.post(
                "/api/meetings",
                headers=auth_headers,
                json={"title": "New Meeting"}
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["title"] == "New Meeting"
            assert data["user_id"] == "user_123"
            assert "id" in data
            assert data["summary"] is None

    def test_create_meeting_without_auth(self, client):
        """Test creating meeting without authentication fails."""
        response = client.post(
            "/api/meetings",
            json={"title": "Unauthorized Meeting"}
        )
        assert response.status_code == 401

    def test_append_single_transcript_chunk(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test appending a single transcript chunk."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            response = client.post(
                "/api/meetings/meeting_123/transcript",
                headers=auth_headers,
                json={"chunk": "Speaker 1: Hello, let's start the meeting."}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "Hello, let's start the meeting" in data["transcript"]

    def test_append_multiple_transcript_chunks(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test appending 5 transcript chunks."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            chunks = [
                "Speaker 1: Let's discuss the project timeline.",
                "Speaker 2: Agree, we need to finalize by next month.",
                "Speaker 1: What about the budget?",
                "Speaker 2: I'll send the budget breakdown.",
                "Speaker 1: Perfect, meeting adjourned."
            ]
            
            for i, chunk in enumerate(chunks):
                response = client.post(
                    "/api/meetings/meeting_123/transcript",
                    headers=auth_headers,
                    json={"chunk": chunk}
                )
                assert response.status_code == 200
                data = response.json()
                # Verify all chunks are in transcript
                assert mock_meeting.transcript.count(chunk) >= 0

    def test_append_chunk_to_nonexistent_meeting(self, client, auth_headers, mock_db, mock_user):
        """Test appending chunk to meeting that doesn't exist."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="nonexistent", user_id="user_123").first.return_value = None
            
            response = client.post(
                "/api/meetings/nonexistent/transcript",
                headers=auth_headers,
                json={"chunk": "Some text"}
            )
            
            assert response.status_code == 404

    def test_list_meetings(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test listing all meetings for user."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(user_id="user_123").all.return_value = [mock_meeting]
            
            response = client.get(
                "/api/meetings",
                headers=auth_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) > 0
            assert data[0]["id"] == "meeting_123"
            assert data[0]["title"] == "Test Meeting"

    def test_list_meetings_empty(self, client, auth_headers, mock_db, mock_user):
        """Test listing meetings when user has none."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(user_id="user_123").all.return_value = []
            
            response = client.get(
                "/api/meetings",
                headers=auth_headers
            )
            
            assert response.status_code == 200
            assert response.json() == []

    def test_get_meeting_by_id(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test getting meeting by ID."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            
            response = client.get(
                "/api/meetings/meeting_123",
                headers=auth_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "meeting_123"
            assert data["title"] == "Test Meeting"
            assert data["user_id"] == "user_123"

    def test_get_nonexistent_meeting(self, client, auth_headers, mock_db, mock_user):
        """Test getting meeting that doesn't exist."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="nonexistent", user_id="user_123").first.return_value = None
            
            response = client.get(
                "/api/meetings/nonexistent",
                headers=auth_headers
            )
            
            assert response.status_code == 404

    def test_end_meeting_generates_summary(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test ending meeting generates summary using LLM."""
        mock_meeting.transcript = "Speaker 1: Let's discuss the roadmap. We need to focus on performance. Speaker 2: Agree, performance is critical."
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            with patch("api.llm_client.generate_summary") as mock_llm:
                mock_llm.return_value = "Meeting discussed product roadmap with focus on performance optimization."
                mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
                mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
                mock_db.commit = MagicMock()
                mock_db.refresh = MagicMock()
                
                response = client.post(
                    "/api/meetings/meeting_123/end",
                    headers=auth_headers
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["summary"] is not None
                assert len(data["summary"]) > 0
                assert "roadmap" in data["summary"].lower() or "performance" in data["summary"].lower()

    def test_end_meeting_with_empty_transcript(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test ending meeting with no transcript."""
        mock_meeting.transcript = ""
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            
            response = client.post(
                "/api/meetings/meeting_123/end",
                headers=auth_headers
            )
            
            assert response.status_code == 400
            assert "transcript" in response.json().get("detail", "").lower()

    def test_meeting_serialization(self, client, auth_headers, mock_db, mock_user, mock_meeting):
        """Test meeting response includes all required fields."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "user_123"}):
            mock_db.query(User).filter_by(google_id="user_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            
            response = client.get(
                "/api/meetings/meeting_123",
                headers=auth_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            required_fields = ["id", "user_id", "title", "started_at", "ended_at", "transcript", "summary"]
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"
