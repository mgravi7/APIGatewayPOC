"""
Integration tests for Customer Service
"""
import pytest
import requests
import time

# Configuration
GATEWAY_BASE_URL = "http://localhost:8080"

class TestCustomerService:
    """Test customer service endpoints"""
    
    def test_health_check_via_gateway(self):
        """Test health check through API Gateway"""
        response = requests.get(f"{GATEWAY_BASE_URL}/customers/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "customer-service"
    
    def test_get_all_customers_via_gateway(self):
        """Test getting all customers through API Gateway"""
        response = requests.get(f"{GATEWAY_BASE_URL}/customers")
        assert response.status_code == 200
        customers = response.json()
        assert isinstance(customers, list)
        assert len(customers) >= 7  # We have 7 mock customers
        
        # Check first customer structure
        customer = customers[0]
        assert "id" in customer
        assert "name" in customer
        assert "email" in customer
        assert "created_at" in customer
    
    def test_get_customer_by_id_via_gateway(self):
        """Test getting specific customer through API Gateway"""
        response = requests.get(f"{GATEWAY_BASE_URL}/customers/6")
        assert response.status_code == 200
        customer = response.json()
        assert customer["id"] == 6
        assert customer["name"] == "John Doe"
        assert customer["email"] == "john.doe@example.com"
    
    def test_get_nonexistent_customer(self):
        """Test getting non-existent customer"""
        response = requests.get(f"{GATEWAY_BASE_URL}/customers/999")
        assert response.status_code == 404
        error = response.json()
        assert "Customer not found" in error["detail"]

@pytest.fixture(scope="session", autouse=True)
def wait_for_services():
    """Wait for services to be ready before running tests"""
    import time
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Check if gateway is responding
            response = requests.get(f"{GATEWAY_BASE_URL}/customers/health", timeout=5)
            if response.status_code == 200:
                print("Services are ready!")
                break
        except:
            pass
        
        retry_count += 1
        print(f"Waiting for services... ({retry_count}/{max_retries})")
        time.sleep(2)
    
    if retry_count >= max_retries:
        pytest.fail("Services did not start within the expected time")