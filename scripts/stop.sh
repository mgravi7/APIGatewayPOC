#!/bin/bash

# Script to stop the APIGatewayPOC application

echo "Stopping APIGatewayPOC microservices..."
echo "======================================="

# Stop all services
docker-compose down

echo ""
echo "? All services stopped!"
echo ""
echo "To clean up completely (remove containers, networks, and volumes):"
echo "docker-compose down -v --remove-orphans"
echo ""
echo "To remove all images:"
echo "docker-compose down --rmi all"