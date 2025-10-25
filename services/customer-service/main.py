from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
import os
import sys
sys.path.append('/app')

from models.customer import Customer, CustomerCreate, CustomerResponse
from shared.common import setup_logging, create_health_response

# Setup logging
logger = setup_logging("customer-service")

app = FastAPI(
    title="Customer Service",
    description="Microservice for managing customers",
    version="1.0.0"
)

# Mock data for now (will be replaced with database)
customers_db = [
    Customer(
        id=1,
        name="Test User",
        email="test.user@example.com",
        phone="+1234567890",
        created_at=datetime.now()
    ),
    Customer(
        id=2,
        name="Admin User",
        email="admin.user@example.com",
        phone="+1234567891",
        created_at=datetime.now()
    ),
    Customer(
        id=3,
        name="Test UserCM",
        email="test.userCM@example.com",
        phone="+1234567892",
        created_at=datetime.now()
    ),
    Customer(
        id=4,
        name="Test UserPM",
        email="test.userPM@example.com",
        phone="+1234567893",
        created_at=datetime.now()
    ),
    Customer(
        id=5,
        name="Test UserPCM",
        email="test.userPCM@example.com",
        phone="+1234567894",
        created_at=datetime.now()
    ),
    Customer(
        id=6,
        name="John Doe",
        email="john.doe@example.com",
        phone="+1234567895",
        created_at=datetime.now()
    ),
    Customer(
        id=7,
        name="Jane Smith",
        email="jane.smith@example.com",
        phone="+1234567896",
        created_at=datetime.now()
    )
]

@app.get("/customers/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return create_health_response("customer-service")

@app.get("/customers", response_model=List[CustomerResponse])
def get_customers():
    """Get all customers"""
    logger.info(f"Fetching all customers. Count: {len(customers_db)}")
    return customers_db

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int):
    """Get a specific customer by ID"""
    logger.info(f"Fetching customer with ID: {customer_id}")
    customer = next((c for c in customers_db if c.id == customer_id), None)
    if not customer:
        logger.warning(f"Customer not found with ID: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8000))
    logger.info(f"Starting customer service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)