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

    # SWAP REQUESTS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS swap_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_email TEXT NOT NULL,
            receiver_email TEXT NOT NULL,
            skill_id INTEGER NOT NULL,
            my_skill TEXT NOT NULL,
            message TEXT DEFAULT '',
            status TEXT DEFAULT 'pending'
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

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()

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
                error="An account with this email already exists. Please login."
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

        email = request.form.get("email", "").strip().lower()

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

    if user is None:

        conn.close()
        session.clear()

        return redirect("/login")

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

    session["name"] = user["name"]
    session["email"] = user["email"]
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

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    level = request.args.get("level", "").strip()

    conn = get_db()

    query = """
        SELECT
            skills.*,
            users.name
        FROM skills
        JOIN users
        ON skills.user_email = users.email
        WHERE 1 = 1
    """

    params = []

    if search:

        query += """
            AND (
                skills.skill LIKE ?
                OR skills.description LIKE ?
            )
        """

        search_value = "%" + search + "%"

        params.append(search_value)
        params.append(search_value)

    if category:

        query += """
            AND skills.category = ?
        """

        params.append(category)

    if level:

        query += """
            AND skills.level = ?
        """

        params.append(level)

    query += """
        ORDER BY skills.id DESC
    """

    skills = conn.execute(
        query,
        params
    ).fetchall()

    categories = conn.execute(
        """
        SELECT DISTINCT category
        FROM skills
        WHERE category != ''
        ORDER BY category
        """
    ).fetchall()

    levels = conn.execute(
        """
        SELECT DISTINCT level
        FROM skills
        WHERE level != ''
        ORDER BY level
        """
    ).fetchall()

    conn.close()

    return render_template(
        "browse.html",
        skills=skills,
        categories=categories,
        levels=levels,
        search=search,
        selected_category=category,
        selected_level=level
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

        skill = request.form.get("skill", "").strip()
        category = request.form.get("category", "").strip()
        level = request.form.get("level", "").strip()
        description = request.form.get("description", "").strip()

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

        skill = request.form.get("skill", "").strip()
        category = request.form.get("category", "").strip()
        level = request.form.get("level", "").strip()
        description = request.form.get("description", "").strip()

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

        conn
# ==================================================
# ADVERTISE YOUR BRAND
# ==================================================

@app.route("/advertise", methods=["GET", "POST"])
def advertise():

    user_id = current_user_id()

    if not user_id:
        return redirect("/login")

    if request.method == "POST":

        brand_name = request.form.get("brand_name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        contact = request.form.get("contact", "").strip()
        website = request.form.get("website", "").strip()

        if not brand_name:
            return render_template(
                "advertise.html",
                error="Please enter your brand name."
            )

        image_filename = ""

        if "image" in request.files:

            image = request.files["image"]

            if image and image.filename:

                filename = secure_filename(image.filename)

                image_filename = filename

                image.save(
                    os.path.join(
                        UPLOAD_FOLDER,
                        filename
                    )
                )

        conn = get_db()

        conn.execute(
            """
            INSERT INTO advertisements
            (
                user_id,
                brand_name,
                category,
                description,
                contact,
                website,
                image
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                brand_name,
                category,
                description,
                contact,
                website,
                image_filename
            )
        )

        conn.commit()
        conn.close()

        return redirect("/advertisements")

    return render_template("advertise.html")


# ==================================================
# VIEW ADVERTISEMENTS
# ==================================================

@app.route("/advertisements")
def advertisements():

    conn = get_db()

    ads = conn.execute(
        """
        SELECT
            advertisements.*,
            users.username
        FROM advertisements
        JOIN users
        ON advertisements.user_id = users.id
        ORDER BY advertisements.id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "advertisements.html",
        ads=ads
        )
