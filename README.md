# Available at: https://bharatfdassignment.onrender.com
# FAQ API

This project provides an API for managing and retrieving Frequently Asked Questions (FAQs) in multiple languages. It supports automatic translation of FAQ content and caches the results for faster retrieval.

## Features

- **Get FAQs in English**: Retrieves FAQs in English by default or when no language is specified.
- **Get FAQs in Other Languages**: Supports retrieving FAQs in any specified language, with automatic translation if a translation is not available in the database.
- **Caching**: FAQ responses are cached to improve performance, reducing the need for repeated translation calls.
- **Dynamic Language Support**: New languages can be added dynamically, and translations will be created using Google Translate if not already available.

## Requirements
- Docker

## Installation
### Method 1: Using docker-compose with Image Pull (Automatic)
#### Step 1: Add the following variables to the .env file

```bash
DB_USER= <your_db_user>
DB_PASSWORD= <your_db_password>
DB_HOST= <yout_db_host>
DB_NAME= <your_db_name>
REDIS_URL = <yout_redis_url>
```

### Step 2: Create docker-compose.yml
```yml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  redis:
    image: redis:alpine
    networks:
      - backend

  web:
    image: yash02rajput/bharatfdassignment:latest
    command: python server/manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    networks:
      - backend
    env_file:
      - <path_to_env_file>

volumes:
  postgres_data:

networks:
  backend:
    driver: bridge

```

#### Step 3: Build and Run the Docker Containers

Now, run the following command:

```bash
docker-compose up --build
``` 
This method will automatically pull the yash02rajput/bharatfdassignment:latest image if it's not already on your system.

### Method 2: Using docker-compose with Image Build (Manual)

#### Step 1: Clone the Repository

  ```bash
  git clone https://github.com/02YashRajput/BharatFDAssignment
  cd BharatFDAssignment
  ```

#### Step 2: Add the following variables to the .env file

```bash
DB_USER= <your_db_user>
DB_PASSWORD= <your_db_password>
DB_HOST= <yout_db_host>
DB_NAME= <your_db_name>
REDIS_URL = <yout_redis_url>
```

#### Step 3: Build and Run the Docker Containers
Once you have cloned the repository, navigate to the project directory and run the following command to build and start the services defined in the docker-compose.yml file:

```bash
docker-compose up --build
```

Your application will now be accessible at http://0.0.0.0:8000

## API Endpoints
### 1. Get All FAQs
#### Request
```bash
http://0.0.0.0:8000/api/faqs/ 
```
Optional Query Parameter: lang – The language code (e.g., en, hi, bn). If not provided, the default language is English (en).

#### Response
- 200 OK – Returns a list of FAQs. If the requested language translation is available, it will return the translated FAQs. Otherwise, it will try to convert the FAQs to the requested language using Google Translate and return the translated content.
- If the requested language cannot be translated (e.g., due to a failed API call), the API will fall back to returning the FAQs in English.



  ```json
  [
      {
          "question": "What is Django?",
          "answer": "Django is a Python web framework."
      },
      {
          "question": "What is the purpose of this API?",
          "answer": "This API provides FAQ translation services."
      }
  ]
  ```
#### Language Fallback Behavior:

If the requested language is not present in the database, the API will attempt to convert the FAQ content into the requested language using Google Translate. If the translation fails, the content will fall back to the default English language (i.e., en). In case of translation failure, the FAQ content will be returned in English.

## Testing

To test the API, you can use pytest. The project includes tests for the following cases:

- Retrieving FAQs in English.
- Retrieving FAQs in other languages (e.g., French).
- Retrieving FAQs with a nonexistent language code.
- Testing model behavior and database interactions. This includes testing save functions on the models.

### Run Tests

```bash
pytest
```

