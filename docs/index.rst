Checkbox-TT Documentation
=========================

Welcome to the Checkbox-TT documentation! This is a REST API for creating and viewing receipts (checks) with user registration and authorization.

Overview
--------

Checkbox-TT is a FastAPI-based REST API that provides:

* User registration and authentication
* Receipt/check creation with products
* Multiple output formats (HTML, TXT, QR code)
* PostgreSQL database integration
* Comprehensive API documentation

Features
--------

* **User Management**: Registration, login, JWT-based authentication
* **Receipt Creation**: Create receipts with multiple products and payment details
* **Multiple Views**: View receipts as HTML, plain text, or QR codes
* **Database Integration**: PostgreSQL with SQLAlchemy ORM
* **API Documentation**: Interactive Swagger/OpenAPI documentation
* **Testing**: Comprehensive test suite with pytest

Quick Start
-----------

1. Clone the repository::

    git clone https://github.com/vlad-bb/Checkbox-TT.git

2. Set up environment variables using `env.example` as a template

3. Start the PostgreSQL database::

    docker-compose up -d

4. Install dependencies::

    pip install -r requirements.txt

5. Run the application::

    python main.py

6. Access the API documentation at: http://localhost:8000/docs

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   api_reference
   user_guide
   development

API Reference
=============

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/main
   api/routes
   api/services
   api/repository
   api/database
   api/schemas

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

