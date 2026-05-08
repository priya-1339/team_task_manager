# 🗂 Team Task Manager

A full-stack web application built with **Flask + MongoDB** featuring role-based access control (Admin / Member), project & task management, and a live dashboard.

---

## 🚀 Live Demo

🔗 [Live URL](https://your-app.railway.app) ← replace with your Railway URL

---

## ✨ Features

- 🔐 Secure Signup / Login with bcrypt password hashing
- 👥 Role-based access control (Admin / Member)
- 📁 Project creation and management
- ✅ Task creation, assignment & status tracking (Pending → In Progress → Done)
- 📊 Dashboard with live stats: Total, Pending, In Progress, Done, Overdue
- ⚠️ Overdue task highlighting
- 🔑 Admin registration protected by secret key
- 🗑 Delete tasks (Admin only)
- 🔁 Password show/hide toggle
- ✔️ Confirm password validation

---

## 📁 Project Structure

```
team_task_manager/
├── app.py                  ← Main Flask application
├── requirements.txt        ← Python dependencies
├── Procfile                ← Railway/gunicorn deployment config
├── .env                    ← Environment variables (not committed)
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

### 1. Clone the repository
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
MONGO_URI=mongodb+srv://priyadarshini:dL-a8w-t2xsmcJK@cluster0.ejqfo7d.mongodb.net/taskmanager?retryWrites=true&w=majority
SECRET_KEY=some-long-random-string-here
ADMIN_SECRET_KEY=TaskManager@Secret99
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
3. Create a database user (username & password)
4. Under **Network Access** → Add IP → Allow from anywhere (`0.0.0.0/0`)
5. Click **Connect** → **Drivers** → Copy connection string
6. Replace `<password>` with your actual password
7. Paste into your `.env` as `MONGO_URI`

---

## 🚂 Deploy to Railway

1. Push your code to GitHub (without `.env`)
2. Go to https://railway.app → New Project → Deploy from GitHub repo
3. Add environment variables in Railway dashboard:
   - `MONGO_URI` = your Atlas connection string
   - `SECRET_KEY` = any random strong string
   - `ADMIN_SECRET_KEY` = your chosen admin registration key
4. Railway auto-detects the `Procfile` and deploys with gunicorn
5. Your app will be live at a `.railway.app` URL

---

## 👥 Roles & Access

| Feature | Admin | Member |
|---|---|---|
| Signup with Admin Key | ✅ | ❌ |
| Create Project | ✅ | ❌ |
| Create Task | ✅ | ❌ |
| View own tasks & projects | ✅ | ✅ |
| Advance task status | ✅ | ✅ (own tasks only) |
| Delete task | ✅ | ❌ |

### How Admin Registration Works
- On the signup page, select **Admin** from the role dropdown
- An **Admin Key** field appears — enter the secret key
- If the key matches `ADMIN_SECRET_KEY` in your environment → account is created as Admin
- If key is wrong or blank → account is created as Member
- This ensures admin access cannot be self-assigned without the secret key

---

## 🔐 Security Features

- Passwords hashed with **bcrypt**
- Credentials loaded from **environment variables** (never hardcoded)
- Admin role protected by **secret key**
- Status/delete routes use **POST** (not GET)
- Invalid ObjectId requests handled with **try/except**
- Database indexes on `email` and `assigned_to` for performance

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MongoDB Atlas (via Flask-PyMongo) |
| Auth | Flask-Bcrypt, Flask Session |
| Frontend | HTML, Bootstrap 5, CSS |
| Deployment | Railway + Gunicorn |

---

## 📦 Dependencies

```
Flask==3.1.3
Flask-Bcrypt==1.0.1
Flask-PyMongo==3.0.1
pymongo==4.17.0
python-dotenv==1.2.2
gunicorn==26.0.0
dnspython==2.8.0
```
