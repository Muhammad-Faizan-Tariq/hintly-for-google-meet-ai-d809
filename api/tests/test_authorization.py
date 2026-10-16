"""
Test suite for authorization and access control.

Tests:
- User A cannot read user B's meetings (403)
- User A cannot append to user B's meeting transcript
- User A cannot end user B's meeting
- User A cannot stream user B's meeting hints
- User A cannot list user B's meetings
- Cross-user access attempt returns proper error
"""

import pytest
from fastapi.testclient import TestClient
from api.index import app
from api.models import User, Meeting
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock
from datetime import datetime


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
def user_a():
    """Create mock user A."""
    user = MagicMock(spec=User)
    user.id = "user_a_123"
    user.email = "user_a@example.com"
    user.google_id = "google_a_123"
    return user


@pytest.fixture
def user_b():
    """Create mock user B."""
    user = MagicMock(spec=User)
    user.id = "user_b_456"
    user.email = "user_b@example.com"
    user.google_id = "google_b_456"
    return user


@pytest.fixture
def user_b_meeting(user_b):
    """Create meeting owned by user B."""
    meeting = MagicMock(spec=Meeting)
    meeting.id = "meeting_b_789"
    meeting.user_id = user_b.id  # Owned by user B
    meeting.title = "User B's Meeting"
    meeting.transcript = "Some transcript"
    meeting.started_at = datetime.utcnow()
    meeting.ended_at = None
    return meeting


class TestAuthorization:
    """Test authorization and access control."""

    def test_user_a_cannot_read_user_b_meeting(self, client, mock_db, user_a, user_b, user_b_meeting):
        """Test that user A cannot read user B's meeting."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_a_123"}):
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            # Meeting belongs to user_b, so user_a's query returns None
            mock_db.query(Meeting).filter_by(id="meeting_b_789", user_id="user_a_123").first.return_value = None
            
            response = client.get(
                "/api/meetings/meeting_b_789",
                headers={"Authorization": "Bearer user_a_token"}
            )
            
            assert response.status_code == 404
            assert "not found" in response.json().get("detail", "").lower()

    def test_user_a_cannot_append_to_user_b_meeting(self, client, mock_db, user_a, user_b, user_b_meeting):
        """Test that user A cannot append transcript to user B's meeting."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_a_123"}):
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            # User A shouldn't find user B's meeting
            mock_db.query(Meeting).filter_by(id="meeting_b_789", user_id="user_a_123").first.return_value = None
            
            response = client.post(
                "/api/meetings/meeting_b_789/transcript",
                headers={"Authorization": "Bearer user_a_token"},
                json={"chunk": "This is user A's chunk"}
            )
            
            assert response.status_code == 404

    def test_user_a_cannot_end_user_b_meeting(self, client, mock_db, user_a, user_b, user_b_meeting):
        """Test that user A cannot end user B's meeting."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_a_123"}):
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            mock_db.query(Meeting).filter_by(id="meeting_b_789", user_id="user_a_123").first.return_value = None
            
            response = client.post(
                "/api/meetings/meeting_b_789/end",
                headers={"Authorization": "Bearer user_a_token"}
            )
            
            assert response.status_code == 404

    def test_user_a_cannot_stream_user_b_hints(self, client, mock_db, user_a, user_b, user_b_meeting):
        """Test that user A cannot stream hints for user B's meeting."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_a_123"}):
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            mock_db.query(Meeting).filter_by(id="meeting_b_789", user_id="user_a_123").first.return_value = None
            
            response = client.get(
                "/api/meetings/meeting_b_789/hints/stream",
                headers={"Authorization": "Bearer user_a_token"}
            )
            
            assert response.status_code == 404

    def test_user_a_cannot_list_user_b_meetings(self, client, mock_db, user_a, user_b, user_b_meeting):
        """Test that user A's list only shows user A's meetings."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_a_123"}):
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            # Return empty list for user_a - no meetings owned by user_a
            mock_db.query(Meeting).filter_by(user_id="user_a_123").all.return_value = []
            
            response = client.get(
                "/api/meetings",
                headers={"Authorization": "Bearer user_a_token"}
            )
            
            assert response.status_code == 200
            meetings = response.json()
            assert len(meetings) == 0
            # Verify user_b's meeting is not included
            for meeting in meetings:
                assert meeting["user_id"] != "user_b_456"

    def test_user_a_can_only_see_own_meetings(self, client, mock_db, user_a):
        """Test that user A can only see their own meetings."""
        user_a_meeting_1 = MagicMock(spec=Meeting)
        user_a_meeting_1.id = "meeting_a_111"
        user_a_meeting_1.user_id = "user_a_123"
        user_a_meeting_1.title = "User A Meeting 1"
        
        user_a_meeting_2 = MagicMock(spec=Meeting)
        user_a_meeting_2.id = "meeting_a_222"
        user_a_meeting_2.user_id = "user_a_123"
        user_a_meeting_2.title = "User A Meeting 2"
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_a_123"}):
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            mock_db.query(Meeting).filter_by(user_id="user_a_123").all.return_value = [user_a_meeting_1, user_a_meeting_2]
            
            response = client.get(
                "/api/meetings",
                headers={"Authorization": "Bearer user_a_token"}
            )
            
            assert response.status_code == 200
            meetings = response.json()
            assert len(meetings) == 2
            # All returned meetings should belong to user_a
            for meeting in meetings:
                assert meeting["user_id"] == "user_a_123"

    def test_cross_user_access_returns_403_or_404(self, client, mock_db, user_a, user_b, user_b_meeting):
        """Test that cross-user access returns appropriate error."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_a_123"}):
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            mock_db.query(Meeting).filter_by(id="meeting_b_789", user_id="user_a_123").first.return_value = None
            
            response = client.get(
                "/api/meetings/meeting_b_789",
                headers={"Authorization": "Bearer user_a_token"}
            )
            
            # Should return 404 (not found) rather than 403 (forbidden) for security
            # This prevents leaking information about meeting existence
            assert response.status_code in [403, 404]

    def test_user_cannot_modify_without_ownership(self, client, mock_db, user_a, user_b_meeting):
        """Test that user cannot modify meeting they don't own."""
        user_a = MagicMock(spec=User)
        user_a.id = "user_a_123"
        user_a.google_id = "google_a_123"
        
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_a_123"}):
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            # The query filters by both id and user_id, so owned check happens naturally
            mock_db.query(Meeting).filter_by(id="meeting_b_789", user_id="user_a_123").first.return_value = None
            
            response = client.post(
                "/api/meetings/meeting_b_789/transcript",
                headers={"Authorization": "Bearer user_a_token"},
                json={"chunk": "unauthorized chunk"}
            )
            
            assert response.status_code == 404

    def test_user_b_can_access_own_meeting(self, client, mock_db, user_b, user_b_meeting):
        """Test that user B can access their own meeting."""
        with patch("api.auth_utils.decode_jwt", return_value={"sub": "google_b_456"}):
            mock_db.query(User).filter_by(google_id="google_b_456").first.return_value = user_b
            mock_db.query(Meeting).filter_by(id="meeting_b_789", user_id="user_b_456").first.return_value = user_b_meeting
            
            response = client.get(
                "/api/meetings/meeting_b_789",
                headers={"Authorization": "Bearer user_b_token"}
            )
            
            assert response.status_code == 200
            meeting = response.json()
            assert meeting["id"] == "meeting_b_789"
            assert meeting["user_id"] == "user_b_456"

    def test_different_users_get_different_lists(self, client, mock_db, user_a, user_b):
        """Test that different users get different meeting lists."""
        user_a_meeting = MagicMock(spec=Meeting)
        user_a_meeting.id = "meeting_a_111"
        user_a_meeting.user_id = "user_a_123"
        
        user_b_meeting = MagicMock(spec=Meeting)
        user_b_meeting.id = "meeting_b_789"
        user_b_meeting.user_id = "user_b_456"
        
        with patch("api.auth_utils.decode_jwt") as mock_decode:
            # First call as user A
            mock_decode.return_value = {"sub": "google_a_123"}
            mock_db.query(User).filter_by(google_id="google_a_123").first.return_value = user_a
            mock_db.query(Meeting).filter_by(user_id="user_a_123").all.return_value = [user_a_meeting]
            
            response_a = client.get(
                "/api/meetings",
                headers={"Authorization": "Bearer user_a_token"}
            )
            
            # Reset mock for user B call
            mock_db.reset_mock()
            mock_decode.return_value = {"sub": "google_b_456"}
            mock_db.query(User).filter_by(google_id="google_b_456").first.return_value = user_b
            mock_db.query(Meeting).filter_by(user_id="user_b_456").all.return_value = [user_b_meeting]
            
            response_b = client.get(
                "/api/meetings",
                headers={"Authorization": "Bearer user_b_token"}
            )
            
            assert response_a.status_code == 200
            assert response_b.status_code == 200
            
            meetings_a = response_a.json()
            meetings_b = response_b.json()
            
            # User A should only see their meeting
            assert len(meetings_a) == 1
            assert meetings_a[0]["id"] == "meeting_a_111"
            
            # User B should only see their meeting
            assert len(meetings_b) == 1
            assert meetings_b[0]["id"] == "meeting_b_789"
