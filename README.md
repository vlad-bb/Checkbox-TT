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