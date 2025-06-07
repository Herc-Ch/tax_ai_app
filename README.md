
# Tax AI App

A full-stack web application for AI-powered tax advice.  
Frontend: React.  
Backend: Flask (Python) with OpenAI integration.  
**Develop and run easily with Docker and Docker Compose.**

---

## 🚀 Quick Start (Docker Recommended)

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- An OpenAI API key (format: `sk-...`)

---

### 1. Clone the repository

```bash
git clone https://github.com/Herc-Ch/tax_ai_app.git
cd tax_ai_app
```

---

### 2. Setup your OpenAI API Key

Create a `.env` file in your project root with:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

> ⚠️ Never commit your `.env` file or API keys to public repositories!

---

### 3. Build and Run the App (all with Docker!)

```bash
docker compose up --build
```

- **Frontend:** [http://localhost:3000](http://localhost:3000)  
- **Backend API:** [http://localhost:5000](http://localhost:5000)


---

## 🐳 Docker Overview

- **Frontend:** Uses Node.js to build your React app, then serves with Nginx for production.
- **Backend:** Runs Flask, handles form data and connects to OpenAI for tax advice.
- **No Python/Node/npm install required on your machine** – all happens in the containers.

---

## 🔗 API Endpoints

Backend exposes endpoints at `http://localhost:5000/api/submit-tax`:

| Method | Endpoint                        | Description                                | Example Body (JSON)                            |
|--------|---------------------------------|--------------------------------------------|------------------------------------------------|
| POST   | /api/submit-tax                 | Submit new tax data                        | `{ "filing_status": "single", ... }`           |
| GET    | /api/submit-tax                 | Get all tax data submissions               | –                                              |
| PUT    | /api/submit-tax                 | Update tax data at a given index           | `{ "index": 0, "income": 1500, ... }`          |
| DELETE | /api/submit-tax?index=0         | Delete tax submission at given index       | –                                              |


**AI Advice:**  
POST `/api/ai-tax-advice` with your tax form fields to receive AI-generated advice.

---

## 🛠️ Local Development Without Docker (Optional/Advanced)

You do **NOT** need to install Node, Python, or pip if using Docker!  
But for advanced local development:

**Backend:**

```bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY=sk-your-openai-api-key
python app.py
```

**Frontend:**

```bash
npm install
npm start
```

---

## 🗂️ Project Structure

```text
tax-ai-app/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── public/
├── src/
├── package.json
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## 📝 Notes

- The backend stores data in memory (not persistent).
- For production: use HTTPS, proper secrets management, and persistent storage.
- All dependencies are installed inside containers when using Docker.

---
## 🛠 Continuous Integration (CI) Pipeline

This project uses **GitHub Actions** to automate the testing and validation process with every code change.

### ⚙️ How It Works

- **Trigger**: The CI pipeline runs automatically on every `push` or `pull request` to the `main` branch.
- **Steps**:
  1. **Checkout Code** – Retrieves the latest code from the repository.
  2. **Set Up Docker** – Installs Docker and Docker Compose for building and running services.
  3. **Build and Start Services** – Builds backend and frontend containers using `docker-compose`.
  4. **Run Backend Tests** – Executes Python unit tests using `pytest` inside the backend container.
  5. **Linting** – A separate job uses **Super-Linter** to check code quality and formatting for multiple languages (Python, JavaScript, CSS, Markdown, YAML, etc.).

### 🔐 Secrets

The pipeline uses the `OPENAI_API_KEY` stored as a GitHub Secret to run the backend in CI without exposing sensitive credentials.

**Happy tax filing with AI!**
