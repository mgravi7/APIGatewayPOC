from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
from decimal import Decimal
import os
import sys
sys.path.append('/app')

from models.product import Product, ProductCreate, ProductResponse
from shared.common import setup_logging, create_health_response

# Setup logging
logger = setup_logging("product-service")

app = FastAPI(
    title="Product Service",
    description="Microservice for managing products",
    version="1.0.0"
)

# Mock data for now (will be replaced with database)
products_db = [
    Product(
        id=1,
        name="Laptop",
        description="High-performance laptop for professionals",
        price=Decimal("999.99"),
        category="Electronics",
        stock_quantity=50,
        created_at=datetime.now()
    ),
    Product(
        id=2,
        name="Smartphone",
        description="Latest smartphone with advanced features",
        price=Decimal("699.99"),
        category="Electronics",
        stock_quantity=100,
        created_at=datetime.now()
    ),
    Product(
        id=3,
        name="Coffee Maker",
        description="Automatic coffee maker with timer",
        price=Decimal("89.99"),
        category="Appliances",
        stock_quantity=25,
        created_at=datetime.now()
    )
]

@app.get("/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return create_health_response("product-service")

@app.get("/products", response_model=List[ProductResponse])
def get_products():
    """Get all products"""
    logger.info(f"Fetching all products. Count: {len(products_db)}")
    return products_db

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """Get a specific product by ID"""
    logger.info(f"Fetching product with ID: {product_id}")
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        logger.warning(f"Product not found with ID: {product_id}")
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/category/{category}")
def get_products_by_category(category: str):
    """Get products by category"""
    logger.info(f"Fetching products by category: {category}")
    filtered_products = [p for p in products_db if p.category.lower() == category.lower()]
    logger.info(f"Found {len(filtered_products)} products in category: {category}")
    return filtered_products

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "product-service",
        "version": "1.0.0",
        "description": "Product management microservice"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8000))
    logger.info(f"Starting product service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)