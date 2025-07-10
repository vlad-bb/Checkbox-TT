Development Guide
=================

Project Structure
-----------------

.. code-block::

    Checkbox-TT/
    ├── main.py                 # FastAPI application entry point
    ├── requirements.txt        # Python dependencies
    ├── alembic.ini            # Database migration configuration
    ├── docker-compose.yml     # Docker services configuration
    ├── env.example            # Environment variables template
    ├── src/                   # Source code
    │   ├── conf/              # Configuration modules
    │   ├── database/          # Database models and connection
    │   ├── filters/           # FastAPI filters
    │   ├── repository/        # Data access layer
    │   ├── routes/            # API route handlers
    │   ├── schemas/           # Pydantic models
    │   ├── services/          # Business logic
    │   ├── static/            # Static files
    │   └── templates/         # Jinja2 templates
    ├── tests/                 # Test suite
    ├── alembic/               # Database migration files
    └── docs/                  # Documentation

Architecture
------------

The application follows a layered architecture:

**Presentation Layer (Routes)**
  - FastAPI route handlers
  - Request/response validation
  - Authentication middleware

**Business Logic Layer (Services)**
  - Authentication service
  - Check processing service
  - Business rules implementation

**Data Access Layer (Repository)**
  - Database queries
  - Data mapping
  - Transaction management

**Data Layer (Database)**
  - SQLAlchemy models
  - PostgreSQL database
  - Alembic migrations

Setting Up Development Environment
----------------------------------

1. Fork and Clone
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/your-username/Checkbox-TT.git
    cd Checkbox-TT

2. Create Branch
~~~~~~~~~~~~~~~~

.. code-block:: bash

    git checkout -b feature/your-feature-name

3. Install Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install -r requirements.txt
    pip install pytest pytest-asyncio pytest-dotenv

4. Set Up Pre-commit Hooks
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install pre-commit
    pre-commit install

Testing
-------

Running Tests
~~~~~~~~~~~~~

Run all tests:

.. code-block:: bash

    pytest

Run with coverage:

.. code-block:: bash

    pytest --cov=src tests/

Run specific test file:

.. code-block:: bash

    pytest tests/test_route_auth.py

Test Structure
~~~~~~~~~~~~~~

Tests are organized by functionality:

- ``test_route_auth.py`` - Authentication endpoints
- ``test_route_check.py`` - Check CRUD operations
- ``test_route_check_view.py`` - Check viewing endpoints

Writing Tests
~~~~~~~~~~~~~

Example test structure:

.. code-block:: python

    import pytest
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    def test_create_user():
        response = client.post("/api/auth/signup", json={
            "username": "testuser",
            "business_name": "Test Business",
            "email": "test@example.com",
            "password": "testpassword"
        })
        assert response.status_code == 201

Database Migrations
-------------------

Creating Migrations
~~~~~~~~~~~~~~~~~~~

After modifying database models:

.. code-block:: bash

    alembic revision --autogenerate -m "Description of changes"

Applying Migrations
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    alembic upgrade head

Rolling Back Migrations
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    alembic downgrade -1

Code Style
----------

The project follows PEP 8 style guidelines:

Formatting
~~~~~~~~~~

Use tools like ``black`` and ``isort``:

.. code-block:: bash

    pip install black isort
    black .
    isort .

Linting
~~~~~~~

Use ``flake8`` for linting:

.. code-block:: bash

    pip install flake8
    flake8 src/

Type Hints
~~~~~~~~~~

Use type hints for better code documentation:

.. code-block:: python

    from typing import List, Optional
    from pydantic import BaseModel

    async def get_checks(user_id: int) -> List[Check]:
        ...

Documentation
~~~~~~~~~~~~~

Follow Google-style docstrings:

.. code-block:: python

    def create_check(user_id: int, check_data: CheckRequest) -> Check:
        """Create a new check for a user.
        
        Args:
            user_id: The ID of the user creating the check
            check_data: The check data from the request
            
        Returns:
            The created check object
            
        Raises:
            ValueError: If check data is invalid
        """

API Design Guidelines
---------------------

RESTful Principles
~~~~~~~~~~~~~~~~~~

- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Use plural nouns for collections (``/checks``)
- Use consistent naming conventions
- Return appropriate HTTP status codes

Response Format
~~~~~~~~~~~~~~~

Consistent JSON response structure:

.. code-block:: python

    {
        "id": 1,
        "created_at": "2024-01-01T12:00:00Z",
        "data": {...}
    }

Error Handling
~~~~~~~~~~~~~~

Use FastAPI's HTTPException:

.. code-block:: python

    from fastapi import HTTPException, status

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

Contributing
------------

1. Follow the coding standards
2. Write tests for new features
3. Update documentation
4. Create descriptive commit messages
5. Submit pull requests for review

Performance Considerations
--------------------------

Database Queries
~~~~~~~~~~~~~~~~

- Use appropriate indexes
- Avoid N+1 query problems
- Use eager loading for related data
- Implement pagination for large datasets

Caching
~~~~~~~

Consider caching for:
- Frequently accessed data
- Expensive computations
- Static content

Async Programming
~~~~~~~~~~~~~~~~~

- Use async/await for I/O operations
- Don't block the event loop
- Use appropriate connection pooling

Security Best Practices
-----------------------

Authentication
~~~~~~~~~~~~~~

- Use strong JWT secrets
- Implement token expiration
- Use refresh tokens
- Hash passwords properly

Input Validation
~~~~~~~~~~~~~~~~

- Validate all input data
- Sanitize user inputs
- Use Pydantic models for validation
- Implement rate limiting

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

- Store secrets in environment variables
- Use different configurations for environments
- Never commit secrets to version control

Deployment
----------

Production Checklist
~~~~~~~~~~~~~~~~~~~~

- [ ] Use HTTPS
- [ ] Set proper CORS policies
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Use production database
- [ ] Set environment variables
- [ ] Configure reverse proxy
- [ ] Set up backup strategy

Docker Deployment
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    docker build -t checkbox-tt .
    docker run -d -p 8000:8000 --env-file .env checkbox-tt

Monitoring
~~~~~~~~~~

Consider implementing:
- Health checks
- Application metrics
- Error tracking
- Performance monitoring