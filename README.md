# 📚 MAD-2 Library Management System

This project is a full-stack library management system built using **Flask (Python)** for the backend and **Vue.js** for the frontend. It includes features like user authentication, book management, feedback, wishlist, cart system, background tasks using **Celery**, and email testing with **MailHog**.

---

## ⚙️ Prerequisites

- Python 3.10 or newer
- Node.js and npm
- Redis
- Go (for MailHog)

---

## 🐍 Backend Setup

1. **Clone the repository**

```bash
git clone https://github.com/ArnoldMathew1998/MAD-2-library-project.git
cd MAD-2-library-project/Backend
```

2. **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the Flask server**

```bash
python3 app.py
```

---

## 🌐 Frontend Setup (Vue.js)

1. Navigate to the frontend folder (adjust path if needed):

```bash
cd ../Frontend
```

2. Install dependencies

```bash
npm install
```

3. Run the frontend

```bash
npm run serve
```

---

## 🛠️ Redis Setup

Install and start the Redis server:

```bash
sudo apt install redis-server
sudo service redis-server start
```

---

## ⏳ Celery + Celery Beat

In separate terminals (while your virtual environment is active):

**Run Celery Worker:**

```bash
celery -A app.celery_app worker --loglevel=info
```

**Run Celery Beat Scheduler:**

```bash
celery -A app.celery_app beat --loglevel=info
```

---

## 📧 MailHog for Email Testing

1. **Install Go (if not already installed):**

```bash
sudo apt install golang-go
```

2. **Install MailHog**

```bash
go install github.com/mailhog/MailHog@latest
```

3. **Run MailHog**

```bash
~/go/bin/MailHog
```

Then visit: [http://localhost:8025](http://localhost:8025)

---

## ✅ You're Ready!

Your backend will be running at: [http://127.0.0.1:5000](http://127.0.0.1:5000)  
Frontend will be live at: [http://localhost:8080](http://localhost:8080) (default Vue port)  
Emails will show up at: [http://localhost:8025](http://localhost:8025)

---

## 📝 License

This project is for academic purposes (MAD-2 Project). Feel free to extend it!

```

---

Let me know if you'd like to add screenshots, demo video links, or deployment instructions too!
