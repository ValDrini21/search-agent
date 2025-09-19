import os
import pytest
import requests
import jwt
from dotenv import load_dotenv
import time

class TestAgentFlow:
    """Test the complete search agent flow"""

    def setup_method(self):
        """Setup for each test"""
        self.base_url = "http://localhost:8000"
        # Load .env file from the root directory
        load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
        self.jwt_secret = os.getenv("JWT_SECRET")

        if not self.jwt_secret:
            pytest.skip("JWT_SECRET not found in .env file")

    def create_test_token(self):
        """Create a valid JWT token for testing"""
        payload = {
            "id": 123,
            "username": "test_user",
            "email": "test@example.com",
            "tier": "premium"
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    def test_health_endpoint(self):
        """Test health endpoint works"""
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("✅ Health endpoint works")

    def test_protected_endpoint_without_auth(self):
        """Test that protected endpoints require authentication"""
        response = requests.post(f"{self.base_url}/run")
        assert response.status_code == 401
        assert "Authorization header required" in response.json()["error"]
        print("✅ Protected endpoint correctly requires auth")

    def test_complete_agent_flow(self):
        """Test complete flow: session creation + agent execution"""
        token = self.create_test_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Test 1: Create session
        print("🔧 Testing session creation...")
        session_data = {
            "state": {
                "user_id": 123,
                "session_id": "test_session_123"
            }
        }

        session_response = requests.post(
            f"{self.base_url}/apps/search_agent/users/123/sessions/test_session_123",
            json=session_data,
            headers=headers
        )

        # Accept both 200/201 (created) and 400 (already exists)
        assert session_response.status_code in [200, 201, 400], f"Session creation failed: {session_response.text}"
        print("✅ Session created or already exists")

        # Test 2: Run agent
        print("🤖 Testing agent execution...")
        agent_data = {
            "app_name": "search_agent",
            "user_id": "123",
            "session_id": "test_session_123",
            "new_message": {
                "role": "user",
                "parts": [{
                    "text": "Are Google services down or up? Please check the current status."
                }]
            },
            "streaming": False
        }

        agent_response = requests.post(
            f"{self.base_url}/run",
            json=agent_data,
            headers=headers
        )

        assert agent_response.status_code == 200, f"Agent execution failed: {agent_response.text}"
        response_data = agent_response.json()
        assert response_data is not None, "No response data received"

        print(f"✅ Agent executed successfully!")
        print(f"📝 Response: {response_data}")

        # Don't return anything to avoid the warning
        # return response_data  # Remove this line

if __name__ == "__main__":
    # Run tests directly
    test = TestAgentFlow()
    test.setup_method()

    try:
        test.test_health_endpoint()
        test.test_protected_endpoint_without_auth()
        test.test_complete_agent_flow()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
