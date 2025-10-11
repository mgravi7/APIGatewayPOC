#!/bin/bash

# Script to run tests for the APIGatewayPOC application

echo "Running APIGatewayPOC Integration Tests"
echo "======================================"

# Check if services are running
echo "Checking if services are running..."
if ! curl -s http://localhost:8080/customers/health >/dev/null 2>&1; then
    echo "? Services are not running. Starting them first..."
    ./scripts/start.sh
    
    # Wait a bit more for services to stabilize
    echo "Waiting for services to stabilize..."
    sleep 20
fi

echo ""
echo "Installing test dependencies..."
pip install -r tests/requirements.txt

echo ""
echo "Running integration tests..."
echo "============================="

# Run tests with verbose output
python -m pytest tests/ -v --tb=short

echo ""
echo "Test run completed!"
echo ""
echo "To run specific test file:"
echo "pytest tests/test_customer_service.py -v"
echo "pytest tests/test_product_service.py -v"