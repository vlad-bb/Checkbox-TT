# Checkbox-TT
REST API для створення та перегляду чеків з реєстрацією та авторизацією користувачів.

## Steps to run app

### Clone repository
```git clone https://github.com/vlad-bb/Checkbox-TT.git```

### Create file .env and fill credentials like in file env.example

### Activate Docker

### Run Docker Compose with Postgres DB
```docker-compose up -d```

### Create virtual enviroment
```python -m venv .venv```

### Activate virtual enviroment
#### for macos/linux
```source .venv/bin/activate```
#### for Windows
```.venv\Scripts\activate```

### Install packages from requirements.txt
```pip install -r requirements.txt```

### Run FastApi App
```python main.py```

### Follow next link
```http://localhost:8000/docs```

### Exit and close app
```docker-compose down```



## Run tests
```pytest -v tests```

## Documentation

This project includes comprehensive Sphinx documentation with API reference, user guide, and development information.

### Building Documentation

1. Install documentation dependencies:
```bash
pip install -r requirements-docs.txt
```

2. Build HTML documentation:
```bash
cd docs
make html
```

Or use the build script:
```bash
./build_docs.sh
```

3. Open documentation:
```bash
open docs/_build/html/index.html
```

### Documentation Contents

- **Installation Guide**: Complete setup instructions
- **User Guide**: API usage examples and workflows  
- **API Reference**: Auto-generated documentation from source code
- **Development Guide**: Contributing guidelines and architecture overview

The documentation is automatically generated from docstrings in the source code and includes:
- FastAPI route documentation
- Database models and schemas
- Service layer functions
- Repository pattern implementations