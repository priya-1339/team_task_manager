# 🗂 Team Task Manager

A full-stack web app built with **Flask + MongoDB** that lets teams manage projects and tasks with role-based access control (Admin / Member).

---

## 🚀 Live Demo

🔗 [Live URL here](#) <!-- Replace with your Railway URL -->

---

## ✨ Features

- 🔐 Signup / Login with hashed passwords (bcrypt)
- 👥 Role-based access control — Admin & Member
- 📁 Project creation and management
- ✅ Task creation, assignment & status tracking
- 📊 Dashboard with stats — Total, Pending, In Progress, Done, Overdue
- 🔴 Overdue task highlighting
- 🎯 Priority levels — Low / Medium / High
- 👁 Password show/hide toggle
- 🗑 Delete tasks (Admin only)

---

## 👥 Roles

| Feature | Admin | Member |
|---|---|---|
| Create Project | ✅ | ❌ |
| Create Task & Assign | ✅ | ❌ |
| View all tasks | ✅ | ❌ |
| View own tasks | ✅ | ✅ |
| Advance task status | ✅ | ✅ (own tasks only) |
| Delete task | ✅ | ❌ |

---

## 📁 Project Structure

```
team_task_manager/
├── app.py
├── requirements.txt
├── Procfile
├── .env               ← you create this (not committed)
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── create_project.html
    └── create_task.html
```

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/team-task-manager.git
cd team-task-manager
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/taskmanager?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-here
```

### 5. Run the app
```bash
python app.py
```
Visit: http://127.0.0.1:5000

---

## ☁️ MongoDB Atlas Setup

1. Go to https://cloud.mongodb.com → Sign up / Login
2. Create a **free M0 cluster**
3. Create a **database user** with username & password
4. Under **Network Access** → Add IP → **Allow from anywhere** (`0.0.0.0/0`)
5. Click **Connect** → **Drivers** → Copy the connection string
6. Replace `<password>` with your actual password
7. Paste into `.env` as `MONGO_URI`

---

## 🚂 Deploy to Railway

1. Push your code to GitHub (without `.env`)
2. Go to https://railway.app → **New Project** → **Deploy from GitHub repo**
3. Add environment variables in Railway dashboard:
   - `MONGO_URI` = your Atlas connection string
   - `SECRET_KEY` = any random string
4. Railway auto-detects the `Procfile` and deploys with gunicorn
5. Your app will be live at a `.railway.app` URL

---

## 🛠 Tech Stack

- **Backend** — Python, Flask
- **Database** — MongoDB Atlas (via Flask-PyMongo)
- **Auth** — Flask-Bcrypt (password hashing), Flask Sessions
- **Frontend** — HTML, Bootstrap 5, CSS
- **Deployment** — Railway + Gunicorn

---

## 📦 Dependencies

```
Flask
Flask-Bcrypt
Flask-PyMongo
pymongo
python-dotenv
gunicorn
dnspython
```
