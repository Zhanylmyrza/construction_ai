
# AI-Powered Construction Task Manager

## Overview

This project simulates an AI-powered construction task manager using **FastAPI** and integrates with the **Gemini Pro API** to generate tasks for construction projects. The project includes API endpoints to create and retrieve projects, stores data in an **SQLite** database, and supports background task simulation for task completion.

## Features

- **Create a new project** by providing project details (name, location).
- **Generate a list of construction tasks** for the project using **Gemini Pro API**.
- **Store and retrieve project and task data** using an **SQLite database**.
- **Simulate task completion** using **background processing** (Bonus).
- **Unit tests** to verify API functionality (Bonus).

## Installation

### Prerequisites

Make sure you have Python 3.8+ installed. You also need `pip` to install dependencies.

### Steps to Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Zhanylmyrza/construction_ai.git
   cd construction_ai
   ```

2. Create a virtual environment and activate it:

   - On Windows:
     ```bash
     python -m venv myenv
     .\myenv\Scripts\activate
     ```
   - On MacOS/Linux:
     ```bash
     python3 -m venv myenv
     source myenv/bin/activate
     ```

3. Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

5. Create the SQLite database:
   ```bash
   python app/database.py
   ```

### Environment Variables

You need to set your **Gemini Pro API Key** as an environment variable. Create a `.env` file in the root of the project and add the following line:

```bash
GEMINI_API_KEY=your_api_key_here
```

You can get your **Gemini Pro API Key** from [Gemini API Docs](https://ai.google.dev/gemini-api/docs).

## API Usage

### Create a New Project

- **Endpoint:** `POST /projects/`
- **Description:** Create a new construction project and generate associated tasks.

**Request Body:**
```json
{
  "project_name": "Restaurant",
  "location": "San Francisco"
}
```

**Response:**
```json
{
  "id": 1,
  "project_name": "Restaurant",
  "location": "San Francisco",
  "status": "processing",
  "tasks": [
    {"name": "Find land", "status": "pending"},
    {"name": "Get permits", "status": "pending"},
    {"name": "Hire contractors", "status": "pending"}
  ]
}
```

### Retrieve Project Details

- **Endpoint:** `GET /projects/{project_id}`
- **Description:** Retrieve the details of a specific project by its ID.

**Response:**
```json
{
  "id": 1,
  "project_name": "Restaurant",
  "location": "San Francisco",
  "status": "in_progress",
  "tasks": [
    {"name": "Find land", "status": "completed"},
    {"name": "Get permits", "status": "pending"}
  ]
}
```



## Project Structure

```plaintext
construction_ai/
│── app/
│   ├── main.py         # FastAPI entry point
│   ├── models.py       # Database models
│   ├── database.py     # SQLite connection
│   ├── schemas.py      # Pydantic schemas
│   ├── services.py     # Gemini API task generation
│   ├── routes.py       # API endpoints
│── requirements.txt    # Dependencies
│── README.md           # Documentation
```

## Dependencies

- FastAPI
- SQLAlchemy
- Pydantic
- httpx (for Gemini Pro API requests)
- pytest (for testing)

Install them by running:

```bash
pip install -r requirements.txt
```

