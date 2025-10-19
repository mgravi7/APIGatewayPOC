import requests
import pytest
import time

# Wait for services to be ready
time.sleep(5)

BASE_URL = "http://localhost:8080"

def test_gateway_routing():
    """Test that the gateway routes requests correctly"""
    
    # Test customer service through gateway
    response = requests.get(f"{BASE_URL}/customers")
    assert response.status_code == 200
    customers = response.json()
    assert isinstance(customers, list)
    assert len(customers) > 0
    
    # Test product service through gateway
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0

def test_customer_service_health():
    """Test customer service health endpoint"""
    response = requests.get(f"{BASE_URL}/customers/health")
    assert response.status_code == 200
    health_data = response.json()
    assert health_data["status"] == "healthy"
    assert health_data["service"] == "customer-service"

def test_product_service_health():
    """Test product service health endpoint"""
    response = requests.get(f"{BASE_URL}/products/health")
    assert response.status_code == 200
    health_data = response.json()
    assert health_data["status"] == "healthy"
    assert health_data["service"] == "product-service"

def test_customer_by_id():
    """Test getting specific customer"""
    response = requests.get(f"{BASE_URL}/customers/1")
    assert response.status_code == 200
    customer = response.json()
    assert customer["id"] == 1
    assert "name" in customer
    assert "email" in customer

def test_product_by_id():
    """Test getting specific product"""
    response = requests.get(f"{BASE_URL}/products/1")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == 1
    assert "name" in product
    assert "price" in product

def test_products_by_category():
    """Test getting products by category"""
    response = requests.get(f"{BASE_URL}/products/category/Electronics")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    # Check that all returned products are in Electronics category
    for product in products:
        assert product["category"] == "Electronics"