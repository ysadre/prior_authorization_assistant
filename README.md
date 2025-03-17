# Prior Authorization Assistant

This project is an AI-powered assistant that extracts prior authorization guidelines from payer PDFs and provides responses using ChatGPT.

The backend is built with FastAPI and handles PDF text extraction, vector search, and AI-driven query processing. The frontend is a simple React app that allows users to ask questions about prior authorization requirements.

To set up, install the required dependencies, run the FastAPI server, and start the React frontend.

🚀 How to Run the Project Locally

1️⃣ Prerequisites

Python Version: 3.9.7

Node.js and NPM Installed (Download here)

📌 Backend Setup (FastAPI)

1️⃣ Navigate to the Backend Directory

cd backend

2️⃣ Create a Virtual Environment (Optional but Recommended)

If you are using pyenv, activate the environment:

pyenv activate prior_auth_env

Otherwise, create and activate a virtual environment manually:

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Run the Backend

Start the FastAPI backend using Uvicorn:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

👉 The API will now be available at:➡️ http://127.0.0.1:8000/docs (Swagger UI)

📌 Frontend Setup (React)

1️⃣ Navigate to the Frontend Directory

cd frontend

2️⃣ Install Dependencies

npm install

3️⃣ Run the Frontend

npm start

👉 The React app will now be available at:➡️ http://localhost:3000

✅ You're All Set!

Now you can start working on the project locally. 🚀
