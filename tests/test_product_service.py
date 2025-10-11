"""
Integration tests for Product Service
"""
import pytest
import requests

# Configuration
GATEWAY_BASE_URL = "http://localhost:8080"
PRODUCT_SERVICE_URL = "http://localhost:8002"

class TestProductService:
    """Test product service endpoints"""
    
    def test_health_check_via_gateway(self):
        """Test health check through API Gateway"""
        response = requests.get(f"{GATEWAY_BASE_URL}/products/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "product-service"
    
    def test_health_check_direct(self):
        """Test health check directly to service"""
        response = requests.get(f"{PRODUCT_SERVICE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "product-service"
    
    def test_get_all_products_via_gateway(self):
        """Test getting all products through API Gateway"""
        response = requests.get(f"{GATEWAY_BASE_URL}/products")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) >= 3  # We have 3 mock products
        
        # Check first product structure
        product = products[0]
        assert "id" in product
        assert "name" in product
        assert "description" in product
        assert "price" in product
        assert "category" in product
        assert "stock_quantity" in product
        assert "created_at" in product
    
    def test_get_product_by_id_via_gateway(self):
        """Test getting specific product through API Gateway"""
        response = requests.get(f"{GATEWAY_BASE_URL}/products/1")
        assert response.status_code == 200
        product = response.json()
        assert product["id"] == 1
        assert product["name"] == "Laptop"
        assert product["category"] == "Electronics"
    
    def test_get_products_by_category(self):
        """Test getting products by category"""
        response = requests.get(f"{GATEWAY_BASE_URL}/products/category/Electronics")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) >= 2  # Laptop and Smartphone
        
        # All products should be in Electronics category
        for product in products:
            assert product["category"] == "Electronics"
    
    def test_get_products_by_nonexistent_category(self):
        """Test getting products by non-existent category"""
        response = requests.get(f"{GATEWAY_BASE_URL}/products/category/NonExistent")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) == 0
    
    def test_get_nonexistent_product(self):
        """Test getting non-existent product"""
        response = requests.get(f"{GATEWAY_BASE_URL}/products/999")
        assert response.status_code == 404
        error = response.json()
        assert "Product not found" in error["detail"]
    
    def test_product_service_root_endpoint(self):
        """Test root endpoint of product service"""
        response = requests.get(f"{GATEWAY_BASE_URL}/product-service/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "product-service"
        assert data["version"] == "1.0.0"