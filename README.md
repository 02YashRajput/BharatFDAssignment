# Available at: https://bharatfdassignment.onrender.com
# FAQ API

This project provides an API for managing and retrieving Frequently Asked Questions (FAQs) in multiple languages. It supports automatic translation of FAQ content and caches the results for faster retrieval.

## Features

- **Get FAQs in English**: Retrieves FAQs in English by default or when no language is specified.
- **Get FAQs in Other Languages**: Supports retrieving FAQs in any specified language, with automatic translation if a translation is not available in the database.
- **Caching**: FAQ responses are cached to improve performance, reducing the need for repeated translation calls.
- **Dynamic Language Support**: New languages can be added dynamically, and translations will be created using Google Translate if not already available.

## Requirements

- Python 3.x
- Django 3.x or later
- Django Rest Framework
- Googletrans (Google Translate API client)
- Redis 

## Installation

### Step 1: Clone the Repository

  ```bash
  git clone https://github.com/02YashRajput/BharatFDAssignment
  cd BharatFDAssignment
  ```
### Step 2: Create and Activate a Virtual Environment
On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create a .env file

```bash
touch .env
```

### Step 5: Add the following variables to the .env file

```bash
DB_USER= <your_username>
DB_PASSWORD= <your_password>
DB_HOST= <your_host>
DB_NAME= <your_database_name>
REDIS_URL= <your_redis_url>
```

### Step 6: Move to the server directory

```bash
cd server
```

### Step 7: Apply Database Migrations
Run the migrations to set up the database:

```bash
python manage.py migrate
```

### Step 8: Run the Development Server

```bash
python manage.py runserver
```
Your application will now be accessible at your_domain

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

