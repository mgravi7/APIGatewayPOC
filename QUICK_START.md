# Quick Start Guide

Get the APIGatewayPOC running in 5 minutes.

## Prerequisites

- Docker Desktop installed and running
- Git (optional)

## Steps

### 1. Clone or Download
```bash
git clone https://github.com/mgravi7/APIGatewayPOC.git
cd APIGatewayPOC
```

### 2. Start Services
```bash
docker-compose up -d
```

### 3. Wait for Keycloak
```bash
docker-compose logs -f keycloak
# Wait for "Keycloak ... started"
# Press Ctrl+C to exit logs
```

### 4. Get Access Token
```bash
curl -X POST http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token \
  -d "client_id=test-client" \
  -d "username=testuser" \
  -d "password=testpass" \
  -d "grant_type=password"
```

### 5. Test Protected Endpoint
```bash
# Replace TOKEN with access_token from step 4
curl -H "Authorization: Bearer TOKEN" http://localhost:8080/customers
```

## Success!

You now have:
- API Gateway running on http://localhost:8080
- Keycloak authentication on http://localhost:8180
- Two microservices (Customer & Product)

## Next Steps

1. **Explore the APIs**: See [API Documentation](docs/api/)
2. **Understand Security**: Read [Security Guide](docs/security/security-guide.md)
3. **Start Development**: Check [Developer Guide](docs/development/quick-reference.md)

## Troubleshooting

Having issues? See [docs/development/quick-reference.md](docs/development/quick-reference.md) for troubleshooting tips.

## Full Documentation

See [docs/README.md](docs/README.md) for complete documentation.
