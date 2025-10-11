#!/bin/bash

# Script to start the APIGatewayPOC application

echo "Starting APIGatewayPOC microservices..."
echo "=================================="

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "Building and starting services with Docker Compose..."
docker-compose up --build -d

echo ""
echo "Waiting for services to be ready..."
sleep 15

echo ""
echo "Service Status:"
echo "================"

# Check each service
echo "Checking Gateway (Envoy)..."
if curl -s http://localhost:9901/ready >/dev/null 2>&1; then
    echo "? Gateway (Envoy) - Ready"
else
    echo "? Gateway (Envoy) - Not ready"
fi

echo "Checking Customer Service..."
if curl -s http://localhost:8001/health >/dev/null 2>&1; then
    echo "? Customer Service - Ready"
else
    echo "? Customer Service - Not ready"
fi

echo "Checking Product Service..."
if curl -s http://localhost:8002/health >/dev/null 2>&1; then
    echo "? Product Service - Ready"
else
    echo "? Product Service - Not ready"
fi

echo ""
echo "Available Endpoints:"
echo "==================="
echo "?? API Gateway: http://localhost:8080"
echo "?? Envoy Admin: http://localhost:9901"
echo "?? Customer Service (direct): http://localhost:8001"
echo "?? Product Service (direct): http://localhost:8002"
echo ""
echo "Example API calls through gateway:"
echo "• GET http://localhost:8080/customers"
echo "• GET http://localhost:8080/products"
echo "• GET http://localhost:8080/customers/1"
echo "• GET http://localhost:8080/products/1"
echo ""
echo "To view logs: docker-compose logs -f [service-name]"
echo "To stop services: ./scripts/stop.sh"