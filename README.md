# APIGatewayPOC

A proof-of-concept microservices application demonstrating API Gateway patterns with Envoy and FastAPI.

## Overview
This is a learning project to demonstrate the use of an API Gateway in a microservices architecture.
The application consists of multiple microservices that communicate through an API Gateway,
which handles routing, authentication, and other cross-cutting concerns. We use Envoy as the API Gateway.

The microservices are built using FastAPI and Python.
The application is containerized using Docker and orchestrated with Docker Compose.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │     Envoy       │
│  (Port 8080)    │────│   (Port 9901)   │
└─────────────────┘    └─────────────────┘
         │                       │
         │              ┌────────┴────────┐
         │              │                 │
┌─────────────────┐  ┌─────────────────┐ 
│ Customer Service│  │ Product Service │ 
│   (Port 8001)   │  │   (Port 8002)   │ 
└─────────────────┘  └─────────────────┘ 
```

## Components
- **API Gateway (Envoy)**: Routes requests, handles load balancing
- **Customer Service (FastAPI)**: Manages customer data with REST API
- **Product Service (FastAPI)**: Manages product catalog with REST API
- **Shared Utilities**: Common logging and utility functions

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (for cloning the repository)

### Running the Application

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mgravi7/APIGatewayPOC.git
   cd APIGatewayPOC
   ```

2. **Start all services**:
   ```bash
   # Using the helper script (recommended)
   ./scripts/start.sh
   
   # Or manually with Docker Compose
   docker-compose up --build
   ```

3. **Verify services are running**:
   - API Gateway: http://localhost:8080
   - Envoy Admin: http://localhost:9901
   - Customer Service: http://localhost:8001
   - Product Service: http://localhost:8002

4. **Test the APIs**:
   ```bash
   # Get all customers through gateway
   curl http://localhost:8080/customers
   
   # Get all products through gateway
   curl http://localhost:8080/products
   
   # Get specific customer
   curl http://localhost:8080/customers/1
   
   # Get products by category
   curl http://localhost:8080/products/category/Electronics
   ```

### Running Tests

```bash
# Run integration tests
./scripts/test.sh

# Or manually
pip install -r tests/requirements.txt
pytest tests/ -v
```

### Stopping Services

```bash
# Using the helper script
./scripts/stop.sh

# Or manually
docker-compose down
```

## API Endpoints

### Through API Gateway (Port 8080)

#### Customer Service
- `GET /customers` - Get all customers
- `GET /customers/{id}` - Get customer by ID
- `GET /customers/health` - Health check

#### Product Service
- `GET /products` - Get all products
- `GET /products/{id}` - Get product by ID  
- `GET /products/category/{category}` - Get products by category
- `GET /products/health` - Health check

### Direct Service Access
- Customer Service: http://localhost:8001
- Product Service: http://localhost:8002

## Project Structure

```
APIGatewayPOC/
├── README.md
├── docker-compose.yml
├── .copilot-instructions.md
├── services/
│   ├── gateway/
│   │   ├── Dockerfile
│   │   └── envoy.yaml
│   ├── customer-service/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   └── models/
│   │       └── customer.py
│   ├── product-service/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   └── models/
│   │       └── product.py
│   └── shared/
│       └── common.py
├── tests/
│   ├── requirements.txt
│   ├── test_customer_service.py
│   └── test_product_service.py
└── scripts/
    ├── start.sh
    ├── stop.sh
    └── test.sh
```

## Development

### Adding a New Service

1. Create service directory: `services/new-service/`
2. Add `Dockerfile`, `requirements.txt`, `main.py`
3. Update `docker-compose.yml`
4. Update `services/gateway/envoy.yaml` for routing
5. Add tests in `tests/`

### Monitoring and Debugging

- **View logs**: `docker-compose logs -f [service-name]`
- **Envoy admin interface**: http://localhost:9901
- **Service health checks**: `curl http://localhost:8080/[service]/health`

## Future Enhancements

### Phase 1: Data Persistence
- [ ] Add PostgreSQL database
- [ ] Implement database models and connections
- [ ] Add data migration scripts

### Phase 2: CRUD Operations
- [ ] Add POST endpoints for creating resources
- [ ] Add PUT endpoints for updating resources  
- [ ] Add DELETE endpoints for removing resources
- [ ] Add input validation and error handling

### Phase 3: Security & Auth
- [ ] Implement JWT token authentication
- [ ] Integrate with Keycloak for identity management
- [ ] Add role-based access control

### Phase 4: Observability
- [ ] Add distributed tracing with Jaeger
- [ ] Implement metrics with Prometheus
- [ ] Add centralized logging
- [ ] Create monitoring dashboards

### Phase 5: Advanced Features
- [ ] Implement rate limiting in API Gateway
- [ ] Add caching with Redis
- [ ] Circuit breaker patterns
- [ ] API versioning strategy

### Phase 6: Deployment & CI/CD
- [ ] Create Kubernetes deployment manifests
- [ ] Set up CI/CD pipeline
- [ ] Add automated testing
- [ ] Production monitoring setup

### Phase 7: Frontend
- [ ] Create React-based UI
- [ ] Implement responsive design
- [ ] Add real-time features

## Technology Stack

- **API Gateway**: Envoy Proxy
- **Backend Services**: FastAPI (Python)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest, requests
- **Data Models**: Pydantic
- **Logging**: Python logging module

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests: `./scripts/test.sh`
6. Submit a pull request

## Troubleshooting

### Services won't start
- Ensure Docker Desktop is running
- Check port availability (8080, 8001, 8002, 9901)
- Run: `docker-compose down && docker-compose up --build`

### Tests failing
- Ensure services are running: `./scripts/start.sh`
- Check service health: `curl http://localhost:8080/customers/health`
- View logs: `docker-compose logs -f`

### Performance issues
- Check Envoy admin interface: http://localhost:9901
- Monitor resource usage: `docker stats`
- Review service logs for errors

## License

This project is licensed under the MIT License - see the LICENSE file for details.

