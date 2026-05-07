# app.py

from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")


mongo = PyMongo(app)
bcrypt = Bcrypt(app)
with app.app_context():
    mongo.db.users.create_index("email", unique=True)
    mongo.db.tasks.create_index("assigned_to")


# ── Helper: login required ──────────────────────────────────────────────────

def login_required():
    return 'user' not in session


# ── HOME ────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return redirect('/login')


# ── SIGNUP ──────────────────────────────────────────────────────────────────

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        name     = request.form['name'].strip()
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        admin_key = request.form.get('admin_key', '').strip()
        role = 'admin' if admin_key == os.getenv('ADMIN_SECRET_KEY') else 'member'

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')

        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('signup.html')

        if mongo.db.users.find_one({"email": email}):
            flash('Email already registered. Please login.', 'danger')
            return render_template('signup.html')

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed,
            "role": role,
            "created_at": datetime.utcnow()
        })
        flash('Account created! Please login.', 'success')
        return redirect('/login')

    return render_template('signup.html')


# ── LOGIN ───────────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']

        user = mongo.db.users.find_one({"email": email})

        if not user:
            flash('Email not registered. Please sign up.', 'danger')
        elif not bcrypt.check_password_hash(user['password'], password):
            flash('Incorrect password. Please try again.', 'danger')
        else:
            session['user']  = user['name']
            session['email'] = user['email']
            session['role']  = user['role']
            session['uid']   = str(user['_id'])
            return redirect('/dashboard')

    return render_template('login.html')


# ── LOGOUT ──────────────────────────────────────────────────────────────────

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ── DASHBOARD ───────────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    if login_required():
        return redirect('/login')

    role = session['role']

    # Admins see all tasks; members see only their own
    if role == 'admin':
        tasks = list(mongo.db.tasks.find({"created_by": session['email']}).sort("created_at", -1))
    else:
        tasks = list(mongo.db.tasks.find({"assigned_to": session['email']}).sort("created_at", -1))

    now = datetime.utcnow()

    total_tasks     = len(tasks)
    completed_tasks = sum(1 for t in tasks if t['status'] == 'Done')
    pending_tasks   = sum(1 for t in tasks if t['status'] == 'Pending')
    progress_tasks  = sum(1 for t in tasks if t['status'] == 'In Progress')

    # Overdue: due_date passed and not Done
    overdue_tasks = 0
    for t in tasks:
        try:
            due = datetime.strptime(t['due_date'], '%Y-%m-%d')
            if due < now and t['status'] != 'Done':
                overdue_tasks += 1
                t['overdue'] = True
            else:
                t['overdue'] = False
        except Exception:
            t['overdue'] = False

    if role == 'admin':
        projects = list(mongo.db.projects.find({"created_by": session['email']}))
    else:
        projects = list(mongo.db.projects.find())

    return render_template(
        'dashboard.html',
        user=session['user'],
        role=role,
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        progress_tasks=progress_tasks,
        overdue_tasks=overdue_tasks,
        projects=projects
    )


# ── CREATE PROJECT (Admin only) ─────────────────────────────────────────────

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if login_required():
        return redirect('/login')
    if session['role'] != 'admin':
        flash('Only admins can create projects.', 'danger')
        return redirect('/dashboard')

    if request.method == 'POST':
        project_name = request.form['project_name'].strip()
        description  = request.form.get('description', '').strip()

        if not project_name:
            flash('Project name is required.', 'danger')
            return render_template('create_project.html')

        if mongo.db.projects.find_one({"project_name": project_name}):
            flash('A project with that name already exists.', 'danger')
            return render_template('create_project.html')

        mongo.db.projects.insert_one({
            "project_name": project_name,
            "description": description,
            "created_by": session['email'],
            "created_at": datetime.utcnow()
        })
        flash(f'Project "{project_name}" created!', 'success')
        return redirect('/dashboard')

    return render_template('create_project.html')


# ── CREATE TASK (Admin only) ─────────────────────────────────────────────────

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if login_required():
        return redirect('/login')
    if session['role'] != 'admin':
        flash('Only admins can create tasks.', 'danger')
        return redirect('/dashboard')

    users    = list(mongo.db.users.find({}, {"password": 0}))
    projects = list(mongo.db.projects.find())

    if request.method == 'POST':
        title       = request.form['title'].strip()
        description = request.form.get('description', '').strip()
        assigned_to = request.form['assigned_to']   # email of assignee
        due_date    = request.form['due_date']
        project_id  = request.form.get('project_id', '')
        priority    = request.form.get('priority', 'Medium')

        if not title or not assigned_to or not due_date:
            flash('Title, assignee, and due date are required.', 'danger')
            return render_template('create_task.html', users=users, projects=projects)

        task_data = {
            "title": title,
            "description": description,
            "assigned_to": assigned_to,
            "status": "Pending",
            "priority": priority,
            "due_date": due_date,
            "created_by": session['email'],
            "created_at": datetime.utcnow()
        }
        if project_id:
            task_data["project_id"] = project_id

        mongo.db.tasks.insert_one(task_data)
        flash(f'Task "{title}" created and assigned!', 'success')
        return redirect('/dashboard')

    return render_template('create_task.html', users=users, projects=projects)


# ── UPDATE STATUS ────────────────────────────────────────────────────────────

@app.route('/update_status/<task_id>', methods=['POST'])
def update_status(task_id):
    if login_required():
        return redirect('/login')

    try:
        oid = ObjectId(task_id)
    except Exception:
        flash('Invalid task ID.', 'danger')
        return redirect('/dashboard')

    task = mongo.db.tasks.find_one({"_id": oid})
    if not task:
        flash('Task not found.', 'danger')
        return redirect('/dashboard')

    # Members can only update tasks assigned to them
    if session['role'] != 'admin' and task['assigned_to'] != session['email']:
        flash('You can only update your own tasks.', 'danger')
        return redirect('/dashboard')

    status_flow = {"Pending": "In Progress", "In Progress": "Done", "Done": "Done"}
    new_status  = status_flow.get(task['status'], "Done")

    mongo.db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
    )
    flash(f'Task status updated to "{new_status}".', 'success')
    return redirect('/dashboard')


# ── DELETE TASK (Admin only) ──────────────────────────────────────────────────

@app.route('/delete_task/<task_id>' , methods=['POST'])
def delete_task(task_id):
    if login_required():
        return redirect('/login')
    if session['role'] != 'admin':
        flash('Only admins can delete tasks.', 'danger')
        return redirect('/dashboard')

    try:
        oid = ObjectId(task_id)
    except Exception:
        flash('Invalid task ID.', 'danger')
        return redirect('/dashboard')

    mongo.db.tasks.delete_one({"_id": oid})
    flash('Task deleted.', 'success')
    return redirect('/dashboard')


# ── RUN ───────────────────────────────────────────────────────────────────────

@app.route('/health')
def health():
    return {"status": "ok"}
@app.errorhandler(404)
def not_found(e):
    return "Page not found", 404

@app.errorhandler(500)
def server_error(e):
    return "Something went wrong", 500

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "false").lower() == "true")