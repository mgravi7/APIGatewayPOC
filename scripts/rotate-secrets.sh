#!/bin/bash

# Keycloak Client Secret Rotation Script
# This script helps rotate client secrets in Keycloak

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
KEYCLOAK_URL="${KEYCLOAK_URL:-http://localhost:8180}"
REALM="${REALM:-api-gateway-poc}"
ADMIN_USER="${ADMIN_USER:-admin}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"

echo -e "${GREEN}=== Keycloak Client Secret Rotation Tool ===${NC}"
echo ""

# Function to generate a secure random secret
generate_secret() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-32
}

# Function to get admin token
get_admin_token() {
    echo -e "${YELLOW}Getting admin access token...${NC}"
    local token=$(curl -s -X POST "${KEYCLOAK_URL}/realms/master/protocol/openid-connect/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${ADMIN_USER}" \
      -d "password=${ADMIN_PASSWORD}" \
        -d "grant_type=password" \
        -d "client_id=admin-cli" | jq -r '.access_token')
    
    if [ "$token" == "null" ] || [ -z "$token" ]; then
        echo -e "${RED}Failed to get admin token. Check credentials.${NC}"
   exit 1
    fi
    
    echo "$token"
}

# Function to get client UUID
get_client_uuid() {
    local client_id=$1
    local token=$2
    
    local uuid=$(curl -s -X GET "${KEYCLOAK_URL}/admin/realms/${REALM}/clients" \
   -H "Authorization: Bearer ${token}" | jq -r ".[] | select(.clientId==\"${client_id}\") | .id")
    
    if [ -z "$uuid" ]; then
        echo -e "${RED}Client '${client_id}' not found${NC}"
        exit 1
    fi
    
    echo "$uuid"
}

# Function to update client secret
update_client_secret() {
 local client_id=$1
    local new_secret=$2
    local token=$3
    
    echo -e "${YELLOW}Updating secret for client: ${client_id}${NC}"
    
    local uuid=$(get_client_uuid "$client_id" "$token")
    
    local response=$(curl -s -X POST "${KEYCLOAK_URL}/admin/realms/${REALM}/clients/${uuid}/client-secret" \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json" \
        -d "{\"type\":\"secret\",\"value\":\"${new_secret}\"}")
    
    echo -e "${GREEN}? Secret updated for ${client_id}${NC}"
}

# Function to display menu
show_menu() {
    echo ""
  echo "Select an option:"
    echo "1) Rotate api-gateway secret"
    echo "2) Rotate customer-service secret"
    echo "3) Rotate product-service secret"
    echo "4) Rotate ALL confidential client secrets"
    echo "5) Generate secure secret (display only)"
    echo "6) Exit"
    echo ""
}

# Function to rotate specific client
rotate_client() {
    local client_id=$1
    local token=$(get_admin_token)
    local new_secret=$(generate_secret)
    
    update_client_secret "$client_id" "$new_secret" "$token"
  
    echo ""
    echo -e "${GREEN}=== New Secret ===${NC}"
    echo -e "Client: ${YELLOW}${client_id}${NC}"
    echo -e "Secret: ${GREEN}${new_secret}${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANT:${NC} Save this secret! Update your environment variables:"
    echo ""
    
    case $client_id in
        "api-gateway")
            echo "API_GATEWAY_CLIENT_SECRET=${new_secret}"
            ;;
 "customer-service")
  echo "CUSTOMER_SERVICE_CLIENT_SECRET=${new_secret}"
       ;;
        "product-service")
            echo "PRODUCT_SERVICE_CLIENT_SECRET=${new_secret}"
   ;;
    esac
    
    echo ""
}

# Function to rotate all clients
rotate_all() {
    echo -e "${YELLOW}Rotating ALL confidential client secrets...${NC}"
    echo ""
    
    local token=$(get_admin_token)
    
  # api-gateway
    local gateway_secret=$(generate_secret)
    update_client_secret "api-gateway" "$gateway_secret" "$token"
    
    # customer-service
  local customer_secret=$(generate_secret)
 update_client_secret "customer-service" "$customer_secret" "$token"
    
    # product-service
    local product_secret=$(generate_secret)
    update_client_secret "product-service" "$product_secret" "$token"
    
    echo ""
    echo -e "${GREEN}=== All Secrets Rotated ===${NC}"
    echo ""
    echo -e "${YELLOW}Copy these to your .env file:${NC}"
    echo ""
    echo "API_GATEWAY_CLIENT_SECRET=${gateway_secret}"
    echo "CUSTOMER_SERVICE_CLIENT_SECRET=${customer_secret}"
    echo "PRODUCT_SERVICE_CLIENT_SECRET=${product_secret}"
    echo ""
    echo -e "${RED}IMPORTANT: Restart all services after updating environment variables!${NC}"
    echo ""
}

# Main menu loop
while true; do
    show_menu
    read -p "Enter choice [1-6]: " choice
    
    case $choice in
      1)
   rotate_client "api-gateway"
            ;;
        2)
            rotate_client "customer-service"
     ;;
        3)
            rotate_client "product-service"
            ;;
        4)
    rotate_all
          ;;
   5)
          secret=$(generate_secret)
          echo ""
         echo -e "${GREEN}Generated secure secret:${NC}"
     echo "$secret"
            echo ""
            ;;
        6)
            echo "Exiting..."
            exit 0
            ;;
        *)
         echo -e "${RED}Invalid option. Please try again.${NC}"
  ;;
    esac
done
