#!/bin/bash

# Setup script for APIGatewayPOC

echo "?? Setting up APIGatewayPOC..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "? Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "? Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "? Docker and Docker Compose are installed"

# Build all services
echo "?? Building all services..."
docker-compose build

echo "? Setup complete!"
echo ""
echo "To start the services, run:"
echo "  ./scripts/start.sh"
echo ""
echo "Or manually:"
echo "  docker-compose up -d"