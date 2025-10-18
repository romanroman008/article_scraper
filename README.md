📰 ## Django Article Scraper

A simple Django application for scraping articles from given URLs and storing them in a PostgreSQL database.
The collected data is accessible through the /articles/ JSON endpoint.

🚀 ## Features

Scrape articles from any given URL

Store data in PostgreSQL

REST API endpoint to access scraped articles

Easy to run locally or via Docker

🧩 Requirements

Python 3.11+

PostgreSQL 13+

(optional) Docker

⚙️ Local Installation
git clone <repository-url>
cd <repository-folder>

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

🗃️ Database Setup

Install PostgreSQL

You can follow the guide here:
👉 https://www.w3schools.com/postgresql/postgresql_getstarted.php

Create a database user

CREATE USER your_user
  WITH LOGIN
  PASSWORD 'your_password';


Create a database

CREATE DATABASE your_db_name
  WITH OWNER = your_user;


Grant privileges

GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;

⚙️ Environment Configuration

Generate a new Django secret key:

python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"


Then create a .env file in your project root:

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DJANGO_SECRET_KEY=your_generated_secret_key

🏃 Running the Project

Make sure your virtual environment is activated and your .env file is configured.

python manage.py makemigrations
python manage.py migrate
python manage.py runserver


The application will be available at:
👉 http://127.0.0.1:8000/

🧾 Scraping Articles

To scrape articles, run:

python manage.py scrape --url <url1> <url2> <url3> ...


If no URLs are provided, the scraper will use default URLs defined in the project.

📡 API Endpoints
Method	Endpoint	Description	Example
GET	/articles/	Returns all scraped articles	curl http://127.0.0.1:8000/articles/
GET	/articles/<id>/	Returns a single article by ID	curl http://127.0.0.1:8000/articles/1/
GET	/articles/?source=<domain>	Returns articles filtered by source domain	curl "http://127.0.0.1:8000/articles/?source=bbc.com"

Example response:

[
  {
    "id": 1,
    "title": "BBC News: Django simplifies web scraping",
    "url": "https://www.bbc.com/news/example-article",
    "source": "bbc.com",
    "scraped_at": "2025-10-18T10:00:00Z"
  }
]

🐳 Docker Setup (optional)

You can run the entire project — including the PostgreSQL database, Django app, and scraper — using Docker and Docker Compose.

1️⃣ Build and start the containers
docker compose up --build


This command builds the images and starts all defined containers.

Alternatively, to start them in detached mode (in the background):

docker compose up -d


This will:

Launch the PostgreSQL database

Run the Django application

Automatically apply migrations (if configured in the Dockerfile/entrypoint)

2️⃣ Run the scraper

Once the containers are up, you can run the scraper command inside the running environment:

docker compose run --rm scraper --url <url1> <url2> <url3>


The --rm flag removes the container after execution.
If no URLs are provided, the scraper will use the default URLs defined in the codebase.

3️⃣ Stop the containers

To stop and remove containers, networks, and volumes:

docker compose down
