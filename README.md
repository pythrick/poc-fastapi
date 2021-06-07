# PoC FastAPI

## Required Features
- [ ] Few endpoints (create, read, update, delete)
- [x] Authentication with JWT
- [x] Authorization based on users role and permission
- [x] Error handling of the errors in one place
- [x] CORS
- [x] Handling standard readiness and liveness request (they don't require auth)
- [ ] Example of Swagger using FastAPI approach that covers different use cases and has enough comments
- [x] Integration with NewRelic
- [ ] Wrap some features named above to a middleware (if it doesn't)
- [ ] Description of benefits of the async feature of the FastAPI
- [x] Configuration of the app should be handled using pyhocon package

## Added on my own taste:
- [x] Linters formatting/validations (black, isort, flake8, mypy)
- [x] Pre-commit validations
- [x] Docker w/ docker-compose
- [x] Entrypoint script
- [x] Migrations with Alembic
- [x] 100% code coverage
- [x] Makefile
- [x] Pagination

## Installation instructions
### Requirements
- Docker
- docker-compose

### Init project
```shell
make init
```

### Start API
```shell
make run
```
