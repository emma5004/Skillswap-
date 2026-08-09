from flask import Flask, render_template, request, redirect, session, send_from_directory
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "skill_swap_secret_key"

# ==================================================
# DATABASE
# ==================================================

DATABASE = "skill_swap_users.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():

    conn = get_db()

    # USERS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            about TEXT DEFAULT '',
            profile_picture TEXT DEFAULT ''
        )
    """)

    # SKILLS USERS CAN TEACH
    conn.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            skill TEXT NOT NULL,
            category TEXT DEFAULT '',
            level TEXT DEFAULT '',
            description TEXT DEFAULT ''
        )
    """)

    # SKILLS USERS WANT TO LEARN
    conn.execute("""
        CREATE TABLE IF NOT EXISTS learning_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            skill TEXT NOT NULL,
            category TEXT DEFAULT '',
            level TEXT DEFAULT '',
            description TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()


init_database()


# ==================================================
# PROFILE PICTURE SETTINGS
# ==================================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    return render_template("home.html")


# ==================================================
# SIGN UP
# ==================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        if not name or not email:

            return render_template(
                "signup.html",
                error="Please enter your name and email."
            )

        conn = get_db()

        existing_user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        if existing_user:

            conn.close()

            return render_template(
                "signup.html",
                error="An account with this email already exists."
            )

        conn.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                about,
                profile_picture
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                "",
                ""
            )
        )

        conn.commit()
        conn.close()

        session["name"] = name
        session["email"] = email
        session["profile_picture"] = ""

        return redirect("/dashboard")

    return render_template("signup.html")


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        if not email:

            return render_template(
                "login.html",
                error="Please enter your email."
            )

        conn = get_db()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        conn.close()

        if user is None:

            return render_template(
                "login.html",
                error="Account not found. Please sign up first."
            )

        session["name"] = user["name"]
        session["email"] = user["email"]
        session["profile_picture"] = user["profile_picture"]

        return redirect("/dashboard")

    return render_template("login.html")


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
def dashboard():

    email = session.get("email")

    if not email:

        return redirect("/login")

    conn = get_db()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    skills = conn.execute(
        """
        SELECT *
        FROM skills
        WHERE user_email = ?
        ORDER BY id DESC
        """,
        (email,)
    ).fetchall()

    learning_goals = conn.execute(
        """
        SELECT *
        FROM learning_goals
        WHERE user_email = ?
        ORDER BY id DESC
        """,
        (email,)
    ).fetchall()

    conn.close()

    if user is None:

        return redirect("/login")

    session["name"] = user["name"]
    session["profile_picture"] = user["profile_picture"]

    return render_template(
        "dashboard.html",
        name=user["name"],
        skills=skills,
        learning_goals=learning_goals
    )


# ==================================================
# FIND SKILLS
# ==================================================

@app.route("/browse")
def browse():

    conn = get_db()

    skills = conn.execute(
        """
        SELECT
            skills.*,
            users.name
        FROM skills
        JOIN users
        ON skills.user_email = users.email
        ORDER BY skills.id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "browse.html",
        skills=skills
    )


# ==================================================
# ADD SKILL I CAN TEACH
# ==================================================

@app.route("/add-skill", methods=["GET", "POST"])
def add_skill():

    email = session.get("email")

    if not email:

        return redirect("/login")

    if request.method == "POST":

        skill = request.form.get(
            "skill",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        level = request.form.get(
            "level",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        if not skill:

            return render_template(
                "teach_skill.html",
                error="Please enter the skill you want to teach."
            )

        conn = get_db()

        conn.execute(
            """
            INSERT INTO skills
            (
                user_email,
                skill,
                category,
                level,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                email,
                skill,
                category,
                level,
                description
            )
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("teach_skill.html")


# ==================================================
# LEARN SKILL
# ==================================================

@app.route("/learn-skill", methods=["GET", "POST"])
def learn_skill():

    email = session.get("email")

    if not email:

        return redirect("/login")

    if request.method == "POST":

        skill = request.form.get(
            "skill",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        level = request.form.get(
            "level",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        if not skill:

            return render_template(
                "learn_skill.html",
                error="Please enter a skill."
            )

        conn = get_db()

        conn.execute(
            """
            INSERT INTO learning_goals
            (
                user_email,
                skill,
                category,
                level,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                email,
                skill,
                category,
                level,
                description
            )
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("learn_skill.html")


# ==================================================
# PROFILE
# ==================================================

@app.route("/profile")
def profile():

    email = session.get("email")

    if not email:

        return redirect("/login")

    conn = get_db()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    skills = conn.execute(
        """
        SELECT *
        FROM skills
        WHERE user_email = ?
        ORDER BY id DESC
        """,
        (email,)
    ).fetchall()

    learning_goals = conn.execute(
        """
        SELECT *
        FROM learning_goals
        WHERE user_email = ?
        ORDER BY id DESC
        """,
        (email,)
    ).fetchall()

    conn.close()

    if user is None:

        return redirect("/login")

    session["profile_picture"] = user["profile_picture"]

    return render_template(
        "profile.html",
        name=user["name"],
        email=user["email"],
        about=user["about"],
        profile_picture=user["profile_picture"],
        skills=skills,
        learning_goals=learning_goals
    )


# ==================================================
# EDIT PROFILE
# ==================================================

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    email = session.get("email")

    if not email:

        return redirect("/login")

    conn = get_db()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    if user is None:

        conn.close()

        return redirect("/login")

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        new_email = request.form.get(
            "email",
            ""
        ).strip().lower()

        about = request.form.get(
            "about",
            ""
        ).strip()

        if not name or not new_email:

            conn.close()

            return render_template(
                "edit_profile.html",
                name=name,
                email=new_email,
                about=about
            )

        duplicate = conn.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            AND id != ?
            """,
            (
                new_email,
                user["id"]
            )
        ).fetchone()

        if duplicate:

            conn.close()

            return render_template(
                "edit_profile.html",
                name=name,
                email=new_email,
                about=about,
                error="That email is already being used."
            )

        # Update the user
        conn.execute(
            """
            UPDATE users
            SET name = ?,
                email = ?,
                about = ?
            WHERE id = ?
            """,
            (
                name,
                new_email,
                about,
                user["id"]
            )
        )

        # Keep the user's skills connected to the new email
        conn.execute(
            """
            UPDATE skills
            SET user_email = ?
            WHERE user_email = ?
            ""
