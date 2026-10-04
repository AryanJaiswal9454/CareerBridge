# CareerBridge

CareerBridge is a full-stack career growth platform designed to help users build strong professional profiles, manage resumes, explore career opportunities, and get guided support for career planning and interview preparation.

The project combines a Django REST API backend with a React + Vite frontend to provide a modern, scalable experience for users who want to improve their job readiness and career trajectory.

## Overview

CareerBridge brings together the following key capabilities:

- User account creation and authentication
- Professional profile management
- Resume upload and document handling
- Career/job matching and recommendations
- Roadmap planning for career progression
- Interview preparation support
- Learning and resource discovery
- Modern responsive web interface

## Tech Stack

### Frontend
- React
- Vite
- JavaScript
- React Router
- Axios
- Recharts
- Firebase

### Backend
- Python
- Django
- Django REST Framework
- MySQL
- JWT Authentication
- CORS support
- Python-dotenv
- AI/GenAI integration support

## Project Structure

```bash
CareerBridge/
├── backend/
│   ├── accounts/
│   ├── careers/
│   ├── careerbridge/
│   ├── interviews/
│   ├── matching/
│   ├── profiles/
│   ├── resources/
│   ├── resumes/
│   ├── roadmap/
│   ├── manage.py
│   ├── requirements.txt
│   └── careerbridge_backup.sql
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── .gitignore
│   ├── .oxlintrc.json
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── .gitignore
└── README.md
```

## Features

### 1. User Accounts
Secure user registration, login, and profile-based access for personalized actions.

### 2. Profile Management
Users can maintain and update professional details such as skills, experience, education, and career goals.

### 3. Resume Management
Support for resume-related workflows, including document upload and processing.

### 4. Career Matching
Career recommendations and matching logic based on user profiles and interests.

### 5. Roadmap Planning
Structured career development paths to help users plan their next steps.

### 6. Interview Preparation
Modules designed to support interview readiness and career growth.

### 7. Resource Hub
Centralized access to learning materials and career resources.

## Backend Apps

The backend is organized into functional Django apps:

- `accounts` – authentication and user account management
- `profiles` – user profiles and career metadata
- `resumes` – resume handling and document support
- `careers` – career-related logic and job opportunity data
- `matching` – recommendation and matching engine
- `roadmap` – career roadmap planning
- `interviews` – interview preparation features
- `resources` – educational and career resources

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- Node.js 18+
- npm or yarn
- MySQL server
- Virtual environment tool (`venv` or `virtualenv`)

## Backend Setup

1. Navigate to the backend folder:

```bash
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `backend` directory with required variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=careerbridge
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=CareerBridge AI <noreply@careerbridge.ai>
```

5. Run database migrations:

```bash
python manage.py migrate
```

6. Start the Django development server:

```bash
python manage.py runserver
```

The backend will typically run at:

```bash
http://localhost:8000
```

## Frontend Setup

1. Navigate to the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The frontend will run at:

```bash
http://localhost:5173
```

## Build for Production

Frontend:

```bash
cd frontend
npm run build
```

To preview the production build:

```bash
npm run preview
```

## Environment Notes

- The backend uses `django-environ` style environment variables via `python-dotenv`.
- The project is configured for local development and uses `localhost` for frontend access.
- MySQL is used as the default database backend.

## Usage

Once the backend and frontend are running:

- Create an account or sign in
- Complete your profile
- Upload your resume
- Explore career suggestions and tracks
- Review roadmap guidance
- Prepare for interviews with available resources

## Roadmap

Planned improvements may include:

- Better AI-powered career recommendations
- Enhanced resume parsing and analysis
- More detailed interview coaching tools
- User dashboards and stats
- Improved job search and matching logic
- Deployment support for production environments

## Contributing

Contributions are welcome. If you want to contribute:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request with a clear description

## Notes

This project appears to be under active development and may evolve as new features and integrations are added.

## Contact

For questions or collaboration, you can reach out through the project owner or repository maintainer.

---

If you'd like, I can also create:
- a more polished GitHub-style README with badges and screenshots
- a project-specific README tailored for recruiters
- a shorter version for a portfolio or submission
- the exact README.md file content ready to be pushed into your repo
