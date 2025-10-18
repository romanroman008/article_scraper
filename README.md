# 📰 **Django Article Scraper**

A simple **Django** application for **scraping articles from given URLs** and storing them in a **PostgreSQL** database.  
The collected data is accessible through the `/articles/` JSON endpoint.

---

## 🚀 **Features**

- Scrape articles from any given URL  
- Store data in PostgreSQL  
- REST API endpoint to access scraped articles  
- Easy to run locally or via Docker  

---

## 🧩 **Requirements**

- Python **3.11+**  
- PostgreSQL **13+**  
- Django **5.2.7**  
- Django REST Framework **3.16.1**  
- psycopg[binary] **3.2.10**  
- python-dotenv **1.1.1**  
- dj-database-url **3.0.1**  
- requests **2.32.5**  
- beautifulsoup4 **4.14.2**  
- dateparser **1.2.2**  
- gunicorn *(for production deployment)*  
- whitenoise *(for serving static files in production)*  
- *(optional)* Docker  
---

## ⚙️ **Local Installation**

```bash
git clone <repository-url>
cd <repository-folder>

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🗃️ **Database Setup**

### 1️⃣ Install PostgreSQL  
Follow the guide here:  
👉 [PostgreSQL Setup Guide](https://www.w3schools.com/postgresql/postgresql_getstarted.php)

### 2️⃣ Create a database user
```sql
CREATE USER your_user
  WITH LOGIN
  PASSWORD 'your_password';
```

### 3️⃣ Create a database
```sql
CREATE DATABASE your_db_name
  WITH OWNER = your_user;
```

### 4️⃣ Grant privileges
```sql
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;
```

---

## ⚙️ **Environment Configuration**

Generate a new Django secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

Then create a `.env` file in your project root:
```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DJANGO_SECRET_KEY=your_generated_secret_key
```

---

## 🏃 **Running the Project**

Make sure your virtual environment is activated and your `.env` file is configured:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The application will be available at:  
👉 **http://127.0.0.1:8000/**

---

## 🧾 **Scraping Articles**

Run the scraper manually:

```bash
python manage.py scrape --url <url1> <url2> <url3> ...
```

If no URLs are provided, the scraper will use **default URLs** defined in the project.

---

## 📡 **API Endpoints**

| **Method** | **Endpoint** | **Description** | **Example** |
|-------------|--------------|------------------|--------------|
| **GET** | `/articles/` | Returns all scraped articles | `curl http://127.0.0.1:8000/articles/` |
| **GET** | `/articles/<id>/` | Returns a single article by ID | `curl http://127.0.0.1:8000/articles/1/` |
| **GET** | `/articles/?source=<domain>` | Returns articles filtered by source domain | `curl "http://127.0.0.1:8000/articles/?source=bbc.com"` |

**Example JSON response:**
```json
[
  {
    "id": 1,
    "title": "BBC News: Django simplifies web scraping",
    "url": "https://www.bbc.com/news/example-article",
    "source": "bbc.com",
    "scraped_at": "2025-10-18T10:00:00Z"
  }
]
```

---

## 🐳 **Docker Setup (optional)**

You can run the entire project — including the **PostgreSQL database**, **Django app**, and **scraper** — using Docker and Docker Compose.

### 1️⃣ Build and start the containers
```bash
docker compose up --build
```

This command builds the images and starts all defined containers.  
To run in detached mode (in the background):

```bash
docker compose up -d
```

This will:
- Launch the PostgreSQL database  
- Run the Django application  
- Automatically apply migrations (if configured in the entrypoint)  

### 2️⃣ Run the scraper
```bash
docker compose run --rm scraper --url <url1> <url2> <url3>
```
The `--rm` flag removes the container after execution.  
If no URLs are provided, the scraper will use the default ones defined in the code.

### 3️⃣ Stop the containers
```bash
docker compose down
```
