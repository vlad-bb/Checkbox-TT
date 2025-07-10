Installation Guide
==================

System Requirements
-------------------

* Python 3.8 or higher
* PostgreSQL 12 or higher
* Docker (for database setup)

Installation Steps
------------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/vlad-bb/Checkbox-TT.git
    cd Checkbox-TT

2. Environment Setup
~~~~~~~~~~~~~~~~~~~~

Create a ``.env`` file based on ``env.example``:

.. code-block:: bash

    cp env.example .env

Edit the ``.env`` file with your database credentials and other configuration.

3. Database Setup
~~~~~~~~~~~~~~~~~

Start the PostgreSQL database using Docker:

.. code-block:: bash

    docker-compose up -d

4. Python Environment
~~~~~~~~~~~~~~~~~~~~~

Create and activate a virtual environment:

.. code-block:: bash

    # For macOS/Linux
    python -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

5. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install -r requirements.txt

6. Database Migrations
~~~~~~~~~~~~~~~~~~~~~~

Run database migrations using Alembic:

.. code-block:: bash

    alembic upgrade head

7. Start the Application
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python main.py

The application will be available at ``http://localhost:8000``

8. Access Documentation
~~~~~~~~~~~~~~~~~~~~~~~

* API Documentation: ``http://localhost:8000/docs``
* Alternative API Docs: ``http://localhost:8000/redoc``
* Health Check: ``http://localhost:8000/api/healthchecker``

Testing
-------

Run the test suite:

.. code-block:: bash

    pytest -v tests

Docker Deployment
-----------------

For production deployment, you can use the provided Dockerfile:

.. code-block:: bash

    docker build -t checkbox-tt .
    docker run -p 8000:8000 checkbox-tt

Environment Variables
---------------------

Required environment variables:

* ``DATABASE_URL`` - PostgreSQL connection string
* ``SECRET_KEY_JWT`` - JWT secret key
* ``ALGORITHM`` - JWT algorithm (default: HS256)
* ``HOST`` - Application host (default: localhost)
* ``PORT`` - Application port (default: 8000)

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Database Connection Error**
    - Ensure PostgreSQL is running
    - Check database credentials in ``.env``
    - Verify database exists

**Import Errors**
    - Ensure virtual environment is activated
    - Check all dependencies are installed
    - Verify Python path configuration

**Port Already in Use**
    - Change the PORT in ``.env`` file
    - Stop other applications using port 8000