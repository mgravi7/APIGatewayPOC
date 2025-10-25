# APIGatewayPOC

> Production-ready API Gateway demonstration using Envoy, Keycloak, and FastAPI microservices

A proof-of-concept microservices application demonstrating API Gateway patterns with OAuth 2.0 authentication, JWT token validation, and role-based access control.

## Quick Start

**Get running in 5 minutes:** See [QUICK_START.md](QUICK_START.md)

**Full documentation:** Browse [docs/](docs/)

## Architecture

```
┌─────────────────────────────────────────────┐
│          API Gateway (Envoy)          │
│     Port 8080 (API) | Port 9901 (Admin)    │
│          + JWT Authentication   │
└──────────────────┬──────────────────────────┘
            │
        ┌──────────┴──────────┐
        │    │
┌───────────────┐    ┌───────────────────┐
│   Keycloak    │    │   Microservices   │
│   IAM/Auth    │    │  Customer/Product │
│  Port 8180    │    │  Ports 8001/8002  │
└───────────────┘    └───────────────────┘
```

## Features

- **API Gateway**: Envoy proxy with routing and load balancing
- **Authentication**: Keycloak OAuth 2.0 / OpenID Connect
- **Security**: JWT token validation, client secrets, RBAC
- **Microservices**: FastAPI-based customer and product services
- **Containerization**: Docker Compose orchestration
- **Production-Ready**: Security best practices and comprehensive documentation

## Documentation

### Essential Guides
- [Quick Start Guide](QUICK_START.md) - Get running in 5 minutes
- [Keycloak Setup](docs/setup/keycloak-setup.md) - Authentication configuration
- [Security Guide](docs/security/security-guide.md) - Security best practices
- [Quick Reference](docs/development/quick-reference.md) - Common commands

### By Topic
- **Security**: [docs/security/](docs/security/) - Authentication, secrets, production checklist
- **Development**: [docs/development/](docs/development/) - Developer guides and troubleshooting
- **Reports**: [reports/](reports/) - Project status and verification

[Browse all documentation →](docs/README.md)

## Quick Commands

```bash
# Start all services
docker-compose up -d

# Get access token
curl -X POST http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token \
  -d "client_id=test-client" \
  -d "username=testuser" \
  -d "password=testpass" \
  -d "grant_type=password"

# Access protected endpoint
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8080/customers

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

See [Quick Reference](docs/development/quick-reference.md) for more commands.

## API Endpoints

### Through API Gateway (Port 8080) - JWT Required

#### Customer Service
- `GET /customers` - List all customers
- `GET /customers/{id}` - Get customer by ID
- `GET /customers/health` - Health check

#### Product Service
- `GET /products` - List all products
- `GET /products/{id}` - Get product by ID
- `GET /products/category/{category}` - Filter by category
- `GET /products/health` - Health check

### Authentication
- **Keycloak Admin**: http://localhost:8180 (admin/admin)
- **Token Endpoint**: http://localhost:8180/realms/api-gateway-poc/protocol/openid-connect/token

## Security

This project implements enterprise-grade security:
- ✅ OAuth 2.0 / OpenID Connect authentication
- ✅ JWT token validation at API Gateway
- ✅ Client secret authentication
- ✅ Role-based access control (RBAC)
- ✅ Restricted redirect URIs
- ✅ Service-to-service authentication

**Important**: 
- Default secrets are for development only
- See [Security Guide](docs/security/security-guide.md) for production deployment
- Review [Production Checklist](docs/security/security-guide.md#production-security-checklist)

## Project Structure

```
APIGatewayPOC/
├── README.md              # This file
├── QUICK_START.md        # 5-minute getting started guide
├── docker-compose.yml           # Service orchestration
├── .env.example        # Environment variables template
│
├── docs/        # Documentation
│   ├── README.md           # Documentation index
│   ├── setup/        # Installation and setup guides
│   ├── security/      # Security documentation
│   └── development/ # Developer guides
│
├── reports/   # Status and verification reports
│   ├── project-status.md        # Current project status
│   └── verification-report.md  # Validation results
│
├── services/    # Microservices
│   ├── gateway/     # Envoy API Gateway
│   ├── keycloak/ # Keycloak IAM
│   ├── customer-service/        # Customer API
│   ├── product-service/         # Product API
│   └── shared/          # Shared utilities
│
├── tests/             # Integration tests
│   ├── test_customer_service.py
│   ├── test_product_service.py
│   └── integration/
│
└── scripts/        # Utility scripts
    ├── rotate-secrets.sh   # Secret rotation (Bash)
    ├── rotate-secrets.ps1    # Secret rotation (PowerShell)
    ├── start.sh       # Start services
    ├── stop.sh          # Stop services
    └── test.sh # Run tests
```

## Technology Stack

- **API Gateway**: Envoy Proxy v1.28
- **Authentication**: Keycloak 23.0
- **Backend**: FastAPI 0.104.1 (Python 3.11)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest, requests
- **Data Validation**: Pydantic 2.5.0

## Current Status

**Milestone**: Phase 2 - Keycloak Integration ✅ Complete

See [Project Status](reports/project-status.md) for details.

## Roadmap

- ✅ **Phase 1**: API Gateway & Microservices
- ✅ **Phase 2**: Keycloak Integration & Security
- 🔄 **Phase 3**: Database Integration (PostgreSQL)
- 📋 **Phase 4**: CRUD Operations
- 📋 **Phase 5**: Observability (Jaeger, Prometheus)
- 📋 **Phase 6**: Advanced Features (Rate limiting, caching)
- 📋 **Phase 7**: CI/CD & Kubernetes

## Troubleshooting

**Services won't start:**
```bash
docker-compose down
docker-compose up -d --build
```

**Authentication issues:**
- Verify Keycloak is running: `docker-compose logs keycloak`
- Check token hasn't expired (5 min default)
- See [Security Quick Reference](docs/security/quick-reference.md)

**Need more help?**
- Check [Quick Reference](docs/development/quick-reference.md)
- Review [Documentation](docs/README.md)
- See [Project Status](reports/project-status.md)

## Contributing

This is a learning/POC project. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

---

**Documentation**: [docs/](docs/) | **Quick Start**: [QUICK_START.md](QUICK_START.md) | **Security**: [docs/security/](docs/security/)

