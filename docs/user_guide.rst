User Guide
==========

Authentication
--------------

User Registration
~~~~~~~~~~~~~~~~~

Register a new user account:

.. code-block:: bash

    curl -X POST "http://localhost:8000/api/auth/signup" \
         -H "Content-Type: application/json" \
         -d '{
           "username": "john_doe",
           "business_name": "John's Store",
           "email": "john@example.com",
           "password": "secure_password"
         }'

User Login
~~~~~~~~~~

Login to get access tokens:

.. code-block:: bash

    curl -X POST "http://localhost:8000/api/auth/login" \
         -H "Content-Type: application/json" \
         -d '{
           "email": "john@example.com",
           "password": "secure_password"
         }'

Response includes:
- ``access_token`` - Use for API requests
- ``refresh_token`` - Use to refresh access token
- ``token_type`` - Always "bearer"

Using Authentication
~~~~~~~~~~~~~~~~~~~~

Include the access token in API requests:

.. code-block:: bash

    curl -X GET "http://localhost:8000/api/check/" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

Working with Receipts
---------------------

Creating a Receipt
~~~~~~~~~~~~~~~~~~

Create a new receipt with products:

.. code-block:: bash

    curl -X POST "http://localhost:8000/api/check/" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "products": [
             {
               "name": "Apple",
               "price": 1.50,
               "quantity": 3
             },
             {
               "name": "Bread",
               "price": 2.00,
               "quantity": 1
             }
           ],
           "payment": {
             "type": "cash",
             "amount": 10.00
           }
         }'

Receipt Fields
~~~~~~~~~~~~~~

**Products Array**
  - ``name`` (string, required) - Product name
  - ``price`` (number, required) - Unit price
  - ``quantity`` (number, required) - Quantity purchased

**Payment Object**
  - ``type`` (string, required) - Payment method ("cash" or "cashless")
  - ``amount`` (number, required) - Amount paid

Viewing Receipts
~~~~~~~~~~~~~~~~

**List All Receipts**

.. code-block:: bash

    curl -X GET "http://localhost:8000/api/check/" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

**Get Specific Receipt**

.. code-block:: bash

    curl -X GET "http://localhost:8000/api/check/1" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

Receipt Formats
---------------

HTML Format
~~~~~~~~~~~

View receipt as HTML page:

.. code-block:: bash

    curl -X GET "http://localhost:8000/check/1/html" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

Text Format
~~~~~~~~~~~

Get receipt as plain text:

.. code-block:: bash

    curl -X GET "http://localhost:8000/check/1/txt" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

QR Code
~~~~~~~

Generate QR code for receipt:

.. code-block:: bash

    curl -X GET "http://localhost:8000/check/1/qr" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

Filtering Receipts
------------------

You can filter receipts using query parameters:

**Filter by Date Range**

.. code-block:: bash

    curl -X GET "http://localhost:8000/api/check/?created_at__gte=2024-01-01&created_at__lte=2024-12-31" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

**Filter by Payment Type**

.. code-block:: bash

    curl -X GET "http://localhost:8000/api/check/?payment_type=cash" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

**Filter by Amount Range**

.. code-block:: bash

    curl -X GET "http://localhost:8000/api/check/?total__gte=10&total__lte=100" \
         -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

Error Handling
--------------

Common Error Responses
~~~~~~~~~~~~~~~~~~~~~~

**401 Unauthorized**
  - Missing or invalid authentication token
  - Token has expired

**404 Not Found**
  - Receipt does not exist
  - Invalid endpoint

**422 Validation Error**
  - Invalid request data
  - Missing required fields

**409 Conflict**
  - Email already exists during registration

Example Error Response:

.. code-block:: json

    {
      "detail": "Invalid authentication credentials"
    }

Rate Limiting
-------------

The API implements rate limiting to prevent abuse. If you exceed the rate limit, you'll receive a 429 Too Many Requests response.

Best Practices
--------------

Security
~~~~~~~~

1. Store access tokens securely
2. Use HTTPS in production
3. Refresh tokens before expiration
4. Use strong passwords

Performance
~~~~~~~~~~~

1. Use filtering to limit large result sets
2. Implement pagination for large datasets
3. Cache frequently accessed data
4. Use appropriate HTTP methods

Data Validation
~~~~~~~~~~~~~~~

1. Validate all input data
2. Handle decimal precision for monetary values
3. Ensure positive values for prices and quantities
4. Validate email formats