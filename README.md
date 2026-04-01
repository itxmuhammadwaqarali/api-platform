# API Platform for Third-Party Developers

Welcome to the API Platform! This is a personal project I built to explore modern API development, security, and integrations. It's designed to be scalable and developer-friendly, much like platforms such as Stripe or Twilio.

This platform lets developers manage API keys, access APIs securely, and handles rate limiting to prevent abuse—all while integrating FastAPI for the gateway and Django for the backend.

---

## Features

### ✅ What's Already Built
- **FastAPI API Gateway**
  - Manages incoming API requests smoothly.
  - Uses middleware to validate API keys.
  - Implements rate limiting with Redis to stop overuse.
  - Includes a `/v1/test-key` endpoint for quick API key testing.

- **Django Developer Portal**
  - Keeps track of API keys and developer accounts.
  - Uses PostgreSQL as the database.

- **Webhooks**
  - Sends async webhooks when rate limits get hit.

- **Redis Integration**
  - Stores request counts for rate limiting.

---

### 🚀 Future Plans
- Add billing and monetization based on API key usage.
- Build usage analytics and dashboards.
- Generate SDKs for different programming languages.
- Support API versioning.
- Create a full UI for the developer portal.

---

## Tech Stack

- **API Gateway:** FastAPI
- **Developer Portal & Models:** Django
- **Database:** PostgreSQL
- **Cache & Rate Limiting:** Redis
- **Webhooks:** Async tasks
- **Python Version:** 3.12

---

## Project Structure

```
api-platform/
├─ services/
│  ├─ api-gateway/          # FastAPI Gateway
│  │  ├─ app/
│  │  │  ├─ api/            # API routers
│  │  │  ├─ core/           # Configs, Redis client
│  │  │  ├─ middleware/     # API key & rate limit middleware
│  │  │  └─ main.py
│  ├─ developer_portal/     # Django project for developers
│  │  ├─ developer_portal/
│  │  │  └─ settings.py
├─ README.md
├─ requirements.txt
```

---

## Installation

1. Clone the repo:
   ```bash
   git clone git@github.com:itxmuhammadwaqarali/api-platform.git
   cd api-platform
   ```

2. Set up a virtual environment and install the dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Get PostgreSQL and Redis running, then update `settings.py` with your configs.

4. Run the Django migrations:
   ```bash
   cd services/developer_portal
   python manage.py migrate
   ```

5. Fire up the FastAPI Gateway:
   ```bash
   cd services/api-gateway
   uvicorn app.main:app --reload
   ```

---

## Usage

- **Add your API key** to the request headers:
  ```
  X-API-Key: YOUR_API_KEY
  ```

- **Test your API key** with:
  ```
  GET /v1/test-key
  ```

- If you hit the rate limit, you'll get:
  ```
  HTTP 429 - Rate limit exceeded
  ```

---

## Notes

This is a hands-on project I created to learn about **API key authentication**, **rate limiting**, **integrating FastAPI with Django**, and **webhooks**. It's a work in progress, with more features on the roadmap for future updates.
