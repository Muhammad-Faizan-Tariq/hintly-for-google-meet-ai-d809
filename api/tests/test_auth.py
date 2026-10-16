"""
Test suite for authentication endpoints.

Tests:
- Invalid Google token returns 401
- Valid token creates user and returns JWT
- Token refresh
- Invalid JWT handling
"""

import pytest
from fastapi.testclient import TestClient
from api.index import app
from api.database import get_db
from api.models import User
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_db(monkeypatch):
    """Mock database session."""
    db = MagicMock(spec=Session)
    monkeypatch.setattr("api.routes.auth.get_db", lambda: db)
    return db


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_invalid_google_token_returns_401(self, client, mock_db):
        """Test that invalid Google token returns 401."""
        with patch("api.auth_utils.verify_google_token", return_value=None):
            response = client.post(
                "/api/auth/login",
                json={"google_token": "invalid_token"}
            )
            assert response.status_code == 401
            assert "token" in response.json().get("detail", "").lower()

    def test_valid_token_creates_user_and_returns_jwt(self, client, mock_db):
        """Test valid token creates user and returns JWT."""
        mock_payload = {
            "sub": "test_user_123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        with patch("api.auth_utils.verify_google_token", return_value=mock_payload):
            # Mock database operations
            mock_db.query(User).filter_by(google_id="test_user_123").first.return_value = None
            mock_db.add = MagicMock()
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            response = client.post(
                "/api/auth/login",
                json={"google_token": "valid_token"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "jwt_token" in data
            assert data["user"]["email"] == "test@example.com"
            assert len(data["jwt_token"]) > 0

    def test_existing_user_returns_jwt(self, client, mock_db):
        """Test that existing user gets JWT without duplication."""
        mock_payload = {
            "sub": "existing_user_123",
            "email": "existing@example.com",
            "name": "Existing User"
        }
        
        existing_user = MagicMock(spec=User)
        existing_user.id = "user_id_123"
        existing_user.google_id = "existing_user_123"
        existing_user.email = "existing@example.com"
        
        with patch("api.auth_utils.verify_google_token", return_value=mock_payload):
            mock_db.query(User).filter_by(google_id="existing_user_123").first.return_value = existing_user
            
            response = client.post(
                "/api/auth/login",
                json={"google_token": "valid_token"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "jwt_token" in data
            assert data["user"]["email"] == "existing@example.com"

    def test_invalid_jwt_returns_401(self, client):
        """Test that invalid JWT in headers returns 401."""
        response = client.get(
            "/api/meetings",
            headers={"Authorization": "Bearer invalid_jwt_token"}
        )
        assert response.status_code == 401

    def test_missing_auth_header_returns_401(self, client):
        """Test that missing auth header returns 401 for protected routes."""
        response = client.get("/api/meetings")
        assert response.status_code == 401

    def test_expired_jwt_returns_401(self, client, mock_db):
        """Test that expired JWT returns 401."""
        with patch("api.auth_utils.decode_jwt", return_value=None):
            response = client.get(
                "/api/meetings",
                headers={"Authorization": "Bearer expired_jwt"}
            )
            assert response.status_code == 401

    def test_malformed_auth_header_returns_401(self, client):
        """Test malformed Authorization header."""
        response = client.get(
            "/api/meetings",
            headers={"Authorization": "InvalidFormat token"}
        )
        assert response.status_code == 401

    def test_jwt_token_format_is_valid(self, client, mock_db):
        """Test that returned JWT has proper format."""
        mock_payload = {
            "sub": "format_test_user",
            "email": "format@example.com",
            "name": "Format Test"
        }
        
        with patch("api.auth_utils.verify_google_token", return_value=mock_payload):
            mock_db.query(User).filter_by(google_id="format_test_user").first.return_value = None
            mock_db.add = MagicMock()
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock()
            
            response = client.post(
                "/api/auth/login",
                json={"google_token": "valid_token"}
            )
            
            jwt_token = response.json()["jwt_token"]
            # JWT should have 3 parts separated by dots
            parts = jwt_token.split(".")
            assert len(parts) == 3, "JWT should have 3 parts (header.payload.signature)"
