# HealthTrack - Personal Health Dashboard 🩺

A comprehensive health tracking application that helps users monitor their wellness journey.

## Features

- 📊 Interactive health metrics dashboard
- 💪 Workout logging and tracking
- 🍽️ Meal and nutrition tracking
- 😴 Sleep quality monitoring
- 💧 Hydration tracking
- 📝 Medical history and doctor's notes
- 🔔 Smart reminders and notifications
- 📱 Smart device integration (Fitbit, Apple Health)

## Tech Stack

### Backend
- Django
- Django REST Framework
- PostgreSQL
- Celery for background tasks

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Recharts for data visualization
- React Query for data fetching

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL
- Redis (for Celery)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create `.env` files in both frontend and backend directories:

### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/healthtrack
REDIS_URL=redis://localhost:6379/0
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 