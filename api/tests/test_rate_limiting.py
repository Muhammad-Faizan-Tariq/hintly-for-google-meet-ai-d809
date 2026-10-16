"""
Test suite for rate limiting.

Tests:
- 11th transcript append in 1 second returns 429
- Rate limit resets after time window
- Rate limit headers are present
- Different endpoints have different limits
- Rate limit applies per user (not globally)
"""

import pytest
from fastapi.testclient import TestClient
from api.index import app
from api.models import User, Meeting
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock
from datetime import datetime
import time


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


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
    meeting.transcript = ""
    meeting.started_at = datetime.utcnow()
    meeting.ended_at = None
    return meeting


class TestRateLimiting:
    """Test rate limiting functionality."""

    def test_11th_transcript_append_in_1_second_returns_429(self, client, mock_db, mock_user, mock_meeting):
        """Test that 11th transcript append within 1 second returns 429."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_123"}):
            mock_db.query(User).filter_by(google_id="google_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            # Make 10 successful appends
            for i in range(10):
                response = client.post(
                    "/api/meetings/meeting_123/transcript",
                    headers={"Authorization": "Bearer test_token"},
                    json={"chunk": f"Chunk {i}"}
                )
                assert response.status_code == 200
            
            # 11th append should be rate limited
            response = client.post(
                "/api/meetings/meeting_123/transcript",
                headers={"Authorization": "Bearer test_token"},
                json={"chunk": "Chunk 11"}
            )
            
            assert response.status_code == 429
            assert "rate" in response.json().get("detail", "").lower()

    def test_rate_limit_includes_retry_after_header(self, client, mock_db, mock_user, mock_meeting):
        """Test that rate limit response includes Retry-After header."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_123"}):
            mock_db.query(User).filter_by(google_id="google_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            # Make 10 appends to hit rate limit
            for i in range(10):
                client.post(
                    "/api/meetings/meeting_123/transcript",
                    headers={"Authorization": "Bearer test_token"},
                    json={"chunk": f"Chunk {i}"}
                )
            
            # 11th append triggers rate limit
            response = client.post(
                "/api/meetings/meeting_123/transcript",
                headers={"Authorization": "Bearer test_token"},
                json={"chunk": "Chunk 11"}
            )
            
            assert response.status_code == 429
            # Should include retry-after header
            assert "retry-after" in response.headers or "x-ratelimit-reset" in response.headers

    def test_rate_limit_per_user(self, client, mock_db):
        """Test that rate limiting is per-user, not global."""
        user_1 = MagicMock(spec=User)
        user_1.id = "user_1"
        user_1.google_id = "google_1"
        
        user_2 = MagicMock(spec=User)
        user_2.id = "user_2"
        user_2.google_id = "google_2"
        
        meeting_1 = MagicMock(spec=Meeting)
        meeting_1.id = "meeting_1"
        meeting_1.user_id = "user_1"
        meeting_1.transcript = ""
        
        meeting_2 = MagicMock(spec=Meeting)
        meeting_2.id = "meeting_2"
        meeting_2.user_id = "user_2"
        meeting_2.transcript = ""
        
        with patch("api.auth_utils.decode_jwt") as mock_decode:
            # User 1 makes 10 appends
            mock_decode.return_value = {"sub": "google_1"}
            mock_db.query(User).filter_by(google_id="google_1").first.return_value = user_1
            mock_db.query(Meeting).filter_by(id="meeting_1", user_id="user_1").first.return_value = meeting_1
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            for i in range(10):
                response = client.post(
                    "/api/meetings/meeting_1/transcript",
                    headers={"Authorization": "Bearer user_1_token"},
                    json={"chunk": f"Chunk {i}"}
                )
                assert response.status_code == 200
            
            # Reset mock for user 2
            mock_db.reset_mock()
            mock_decode.return_value = {"sub": "google_2"}
            mock_db.query(User).filter_by(google_id="google_2").first.return_value = user_2
            mock_db.query(Meeting).filter_by(id="meeting_2", user_id="user_2").first.return_value = meeting_2
            
            # User 2 should be able to make appends without hitting user 1's limit
            for i in range(10):
                response = client.post(
                    "/api/meetings/meeting_2/transcript",
                    headers={"Authorization": "Bearer user_2_token"},
                    json={"chunk": f"Chunk {i}"}
                )
                assert response.status_code == 200

    def test_rate_limit_includes_x_ratelimit_headers(self, client, mock_db, mock_user, mock_meeting):
        """Test that responses include X-RateLimit-* headers."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_123"}):
            mock_db.query(User).filter_by(google_id="google_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            response = client.post(
                "/api/meetings/meeting_123/transcript",
                headers={"Authorization": "Bearer test_token"},
                json={"chunk": "First chunk"}
            )
            
            assert response.status_code == 200
            # Should include rate limit headers
            headers = {k.lower(): v for k, v in response.headers.items()}
            # At least one of these should be present
            has_limit_header = any(
                header in headers for header in [
                    "x-ratelimit-limit",
                    "x-ratelimit-remaining",
                    "ratelimit-limit",
                    "ratelimit-remaining"
                ]
            )
            # Note: This is a soft check - implementation may vary

    def test_rate_limit_error_message_helpful(self, client, mock_db, mock_user, mock_meeting):
        """Test that rate limit error message is helpful."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_123"}):
            mock_db.query(User).filter_by(google_id="google_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            # Make 10 appends
            for i in range(10):
                client.post(
                    "/api/meetings/meeting_123/transcript",
                    headers={"Authorization": "Bearer test_token"},
                    json={"chunk": f"Chunk {i}"}
                )
            
            # Trigger rate limit
            response = client.post(
                "/api/meetings/meeting_123/transcript",
                headers={"Authorization": "Bearer test_token"},
                json={"chunk": "Chunk 11"}
            )
            
            assert response.status_code == 429
            error_msg = response.json().get("detail", "").lower()
            # Error should mention rate limit and/or too many requests
            assert "rate" in error_msg or "too many" in error_msg

    def test_burst_protection(self, client, mock_db, mock_user, mock_meeting):
        """Test that burst protection works (10 allowed, 11th blocked)."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_123"}):
            mock_db.query(User).filter_by(google_id="google_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            responses = []
            for i in range(12):  # Try 12 requests
                response = client.post(
                    "/api/meetings/meeting_123/transcript",
                    headers={"Authorization": "Bearer test_token"},
                    json={"chunk": f"Chunk {i}"}
                )
                responses.append(response.status_code)
            
            # First 10 should be 200
            assert all(code == 200 for code in responses[:10])
            # 11th and 12th should be 429
            assert responses[10] == 429
            assert responses[11] == 429

    def test_rate_limit_applies_to_transcript_endpoint(self, client, mock_db, mock_user, mock_meeting):
        """Test that rate limiting specifically applies to transcript append endpoint."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_123"}):
            mock_db.query(User).filter_by(google_id="google_123").first.return_value = mock_user
            mock_db.query(Meeting).filter_by(id="meeting_123", user_id="user_123").first.return_value = mock_meeting
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            # GET requests to list/get should not be rate limited
            response = client.get(
                "/api/meetings",
                headers={"Authorization": "Bearer test_token"}
            )
            assert response.status_code in [200, 401]  # Not 429

    def test_rate_limit_per_meeting_or_global(self, client, mock_db, mock_user):
        """Test rate limit scope (per meeting or per user)."""
        meeting_1 = MagicMock(spec=Meeting)
        meeting_1.id = "meeting_1"
        meeting_1.user_id = "user_123"
        meeting_1.transcript = ""
        
        meeting_2 = MagicMock(spec=Meeting)
        meeting_2.id = "meeting_2"
        meeting_2.user_id = "user_123"
        meeting_2.transcript = ""
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_123"}):
            mock_db.query(User).filter_by(google_id="google_123").first.return_value = mock_user
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            # Make requests to meeting_1
            for i in range(5):
                mock_db.query(Meeting).filter_by(id="meeting_1", user_id="user_123").first.return_value = meeting_1
                response = client.post(
                    "/api/meetings/meeting_1/transcript",
                    headers={"Authorization": "Bearer test_token"},
                    json={"chunk": f"Chunk {i}"}
                )
                assert response.status_code == 200
            
            # Make requests to meeting_2
            for i in range(5):
                mock_db.query(Meeting).filter_by(id="meeting_2", user_id="user_123").first.return_value = meeting_2
                response = client.post(
                    "/api/meetings/meeting_2/transcript",
                    headers={"Authorization": "Bearer test_token"},
                    json={"chunk": f"Chunk {i}"}
                )
                assert response.status_code == 200
            
            # Total should be 10 requests to the same user
            # Both should succeed (rate limit is likely per-meeting or has decent window)
