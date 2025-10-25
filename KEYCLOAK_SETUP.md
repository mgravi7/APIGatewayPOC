# Keycloak Integration - Quick Start Guide

## Getting Started

### 1. Start All Services
```bash
docker-compose up -d --build
```

### 2. Wait for Keycloak to be Ready
Monitor the logs to ensure Keycloak is fully started:
```bash
docker-compose logs -f keycloak
```
Wait until you see: "Keycloak ... started"

### 3. Access Keycloak Admin Console
- **URL**: http://localhost:8180
- **Username**: admin
- **Password**: admin

## Testing Authentication

### Option 1: Get Access Token (Direct Grant Flow)

```bash
curl -X POST http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=test-client" \
  -d "username=testuser" \
  -d "password=testpass" \
  -d "grant_type=password"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "token_type": "Bearer"
}
```

### Option 2: Using Admin User

```bash
curl -X POST http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=test-client" \
  -d "username=adminuser" \
  -d "password=adminpass" \
  -d "grant_type=password"
```

## Testing Protected Endpoints

### 1. Try Accessing Without Token (Should Fail)
```bash
curl -v http://localhost:8080/customers
```
**Expected**: 401 Unauthorized - Jwt is missing

### 2. Access With Valid Token (Should Succeed)
```bash
# First, get the token and extract it
TOKEN=$(curl -s -X POST http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=test-client" \
  -d "username=testuser" \
  -d "password=testpass" \
  -d "grant_type=password" | jq -r '.access_token')

# Use the token to access protected endpoints
curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/customers
```

### 3. Test Product Service
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/products
```

## Verifying JWT Token

You can decode and verify your JWT token at https://jwt.io or using:

```bash
# Decode JWT (requires jq)
echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null | jq .
```

## Available Test Users

| Username   | Password   | Roles                                    |
|------------|-----------|------------------------------------------|
| testuser   | testpass  | user, customer-manager                   |
| adminuser  | adminpass | user, admin, customer-manager, product-manager |

## Useful Commands

### View All Service Logs
```bash
docker-compose logs -f
```

### View Keycloak Logs Only
```bash
docker-compose logs -f keycloak
```

### View Gateway Logs Only
```bash
docker-compose logs -f gateway
```

### Restart Keycloak
```bash
docker-compose restart keycloak
```

### Stop All Services
```bash
docker-compose down
```

### Rebuild and Restart
```bash
docker-compose down
docker-compose up -d --build
```

## Important Endpoints

### Keycloak
- **Admin Console**: http://localhost:8180
- **Realm Info**: http://localhost:8180/realms/api-gateway-poc
- **Token Endpoint**: http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token
- **JWKS (Public Keys)**: http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/certs
- **UserInfo**: http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/userinfo

### API Gateway
- **Gateway**: http://localhost:8080
- **Admin Interface**: http://localhost:9901

### Services (Direct Access - Bypass Gateway)
- **Customer Service**: http://localhost:8001
- **Product Service**: http://localhost:8002

## Troubleshooting

### Issue: "401 Unauthorized" even with token
**Solutions:**
1. Verify token hasn't expired (default: 5 minutes)
2. Check that Keycloak is accessible from gateway container:
   ```bash
   docker-compose exec gateway ping keycloak
   ```
3. Verify JWKS endpoint is accessible:
   ```bash
   docker-compose exec gateway curl http://keycloak:8080/realms/api-gateway-poc/protocol/openid-connect/certs
   ```

### Issue: Keycloak container exits immediately
**Solutions:**
1. Check logs: `docker-compose logs keycloak`
2. Verify port 8180 is not in use
3. Ensure realm-export.json is valid JSON

### Issue: Gateway can't validate tokens
**Solutions:**
1. Wait for Keycloak health check to pass
2. Check gateway logs for JWT filter errors
3. Verify Envoy configuration syntax

### Issue: Services not starting
**Solutions:**
1. Check if all required ports are available
2. Ensure Docker has enough resources
3. Review individual service logs

## Next Steps

1. **Implement Role-Based Access Control (RBAC)**
   - Add role checks in Envoy configuration
   - Implement fine-grained authorization

2. **Add Service-to-Service Authentication**
   - Configure services to validate tokens
   - Implement client credentials flow

3. **Production Hardening**
   - Add PostgreSQL for Keycloak
   - Enable HTTPS/TLS
   - Configure proper secrets management
   - Set up monitoring and alerting

4. **Advanced Features**
   - Social login integration
   - Multi-factor authentication
   - Custom themes
   - User federation (LDAP/Active Directory)
