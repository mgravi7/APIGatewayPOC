# Keycloak Service

This directory contains the Keycloak configuration for the API Gateway POC project.

## Overview

Keycloak is an open-source Identity and Access Management (IAM) solution that provides:
- Single Sign-On (SSO)
- OAuth 2.0 and OpenID Connect support
- User Federation
- Identity Brokering
- Social Login

## Configuration

### Dockerfile
- Based on the latest official Keycloak image (Quarkus-based)
- Runs in development mode for easier testing
- Automatically imports the realm configuration on startup

### Default Credentials

**Admin Console:**
- URL: http://localhost:8180
- Username: `admin`
- Password: `admin`

**Test Users:**
- Username: `testuser` / Password: `testpass` (roles: user, customer-manager)
- Username: `adminuser` / Password: `adminpass` (roles: user, admin, customer-manager, product-manager)

## Realm Configuration

The `realm-export.json` file contains the pre-configured realm `api-gateway-poc` with:

### Clients
- **api-gateway**: Main gateway client for token validation
- **customer-service**: Bearer-only client for customer service
- **product-service**: Bearer-only client for product service
- **test-client**: Public client for testing (supports direct grant flow)

### Roles
- `user`: Basic user role
- `admin`: Administrator role
- `customer-manager`: Can manage customer data
- `product-manager`: Can manage product data

## Testing Authentication

### Get Access Token (Password Grant)

```bash
curl -X POST http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=test-client" \
  -d "username=testuser" \
  -d "password=testpass" \
  -d "grant_type=password"
```

### Access Protected Endpoints

```bash
# Use the access_token from previous response
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://localhost:8080/customers
```

## Endpoints

- **Admin Console**: http://localhost:8180
- **Realm Endpoint**: http://localhost:8180/realms/api-gateway-poc
- **JWKS Endpoint**: http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/certs
- **Token Endpoint**: http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token
- **UserInfo Endpoint**: http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/userinfo

## Environment Variables

The following environment variables are used:

- `KC_BOOTSTRAP_ADMIN_USERNAME`: Admin username (replaces deprecated `KEYCLOAK_ADMIN`)
- `KC_BOOTSTRAP_ADMIN_PASSWORD`: Admin password (replaces deprecated `KEYCLOAK_ADMIN_PASSWORD`)
- `KC_HTTP_PORT`: HTTP port (default: 8080)
- `KC_HOSTNAME_STRICT`: Disable strict hostname checking for development
- `KC_HTTP_ENABLED`: Enable HTTP (not just HTTPS)
- `KC_HEALTH_ENABLED`: Enable health endpoints
- `KC_METRICS_ENABLED`: Enable metrics endpoints

## Production Considerations

For production deployments, you should:
1. Use PostgreSQL instead of H2 database
2. Enable HTTPS/TLS
3. Set strong admin passwords
4. Configure proper hostname settings
5. Enable strict hostname validation
6. Configure rate limiting and brute force protection
7. Set appropriate token lifespans
8. Use secrets management for sensitive data

## Customizing the Realm

To modify the realm configuration:
1. Access the admin console at http://localhost:8180
2. Login with admin credentials
3. Make your changes in the UI
4. Export the realm: Realm Settings ? Action ? Partial Export
5. Replace `realm-export.json` with the exported configuration

## Troubleshooting

### Container won't start
- Check if port 8180 is already in use
- Review logs: `docker-compose logs keycloak`

### Realm not imported
- Verify `realm-export.json` is valid JSON
- Check container logs for import errors
- Ensure the realm file is properly mounted

### Token validation fails
- Verify JWKS endpoint is accessible from gateway
- Check token expiration time
- Ensure correct realm and client configuration

### Deprecation Warnings
If you see warnings about deprecated environment variables:
- Use `KC_BOOTSTRAP_ADMIN_USERNAME` instead of `KEYCLOAK_ADMIN`
- Use `KC_BOOTSTRAP_ADMIN_PASSWORD` instead of `KEYCLOAK_ADMIN_PASSWORD`
- Remove `KC_HOSTNAME_STRICT_HTTPS` (deprecated in favor of newer hostname options)
