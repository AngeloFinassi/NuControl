from time import strftime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import apology, login_required, read_file, categorize_dataframe
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os
import db

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if not name:
            return apology("Please insert a name", 403)
        if not password:
            return apology("Please insert a password", 403)
        
        row = db.execute("SELECT * FROM users WHERE name = ?", (name,), fetchone=True)
        
        if row is None or not check_password_hash(row["password"], password):
            return apology("Invalid username or password", 403)
        
        session["user_id"] = row["user_id"]
        print("Login Made")
        return redirect("/")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not name:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("Please confirm your password", 400)
        elif password != confirmation:
            return apology("Passwords do not match", 400)

        rows = db.execute("SELECT * FROM users WHERE name = ?", (name,), fetchall=True)
        if len(rows) > 0:
            return apology("Username already taken", 400)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, hash), commit=True)

        user = db.execute("SELECT user_id FROM users WHERE name = ?", (name,), fetchone=True)
        session["user_id"] = user["user_id"]
        return redirect("/")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    print("Logout made")
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    uploads_file = db.execute("SELECT filename, id FROM uploads WHERE user_id = ?", (user_id,), fetchall=True)

    return render_template("index.html", uploads=uploads_file, from_page="index")

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    user_id = session["user_id"]

    #Fillter the inputs
    if "file" not in request.files:
        return apology("Please insert a file", 403)
    
    file = request.files["file"]
    filename = secure_filename(file.filename.lower())
    
    base_filename = os.path.splitext(filename)[0]
    timestamp = datetime.now().strftime("%M%S")
    csv_filename = base_filename + '_' + timestamp + ".csv"

    df = read_file(file, filename)
    if df is None:
        return apology("Please insert a valid file", 403)
    
    #Save on database and add a copy on the filepath, to work later
    path = (f"users/uploads/user_{user_id}")
    
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, csv_filename)

    #Reset the file cursos before save, to prevent mistakes, exp: seek(0) to reset the pointer to the begginer part of the file
    df.to_csv(filepath, index=False)

    db.execute("INSERT INTO uploads (user_id, filename, filepath) VALUES (?, ?, ?)", (user_id, csv_filename, filepath), commit=True)
    print("Upload made")

    return redirect("/")

@app.route("/filetable", methods=["POST"])
@login_required
def filetable():
    user_id = session["user_id"]
    file_id = request.form.get("file_id")

    if not file_id:
        return apology("Please select a file", 400)

    try:
        file_id = int(file_id)
    except ValueError:
        return apology("Invalid file id", 400)

    row = db.execute("SELECT filename, filepath FROM uploads WHERE user_id = ? AND id = ?", (user_id, file_id), fetchone=True)
    if row is None:
        return apology("Any file found, please select another", 400)

    filename = row["filename"]
    file = row["filepath"]

    df = read_file(file, filename)

    if df is None:
        return apology("Error to read the file", 500)

    table_data = df.to_dict(orient="records")
    headers = df.columns.tolist()
    uploads_file = db.execute("SELECT filename, id FROM uploads WHERE user_id = ?", (user_id,), fetchall=True)

    return render_template("index.html", uploads=uploads_file, from_page="index", table_data=table_data, headers=headers, filename=filename)

@app.route("/delete_file", methods=["POST"])
@login_required
def delete_file():
    user_id = session["user_id"]
    file_id = request.form.get("file_id")

    if not file_id:
        return apology("Missing file", 400)

    row = db.execute("SELECT filepath FROM uploads WHERE user_id = ? AND id = ?", (user_id, file_id), fetchone=True)
    if row is None:
        return apology("Arquivo não encontrado", 404)

    filepath = row["filepath"]

    #delete from the stoarge
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
    except Exception as e:
        return apology(f"Erro to delete the file: {str(e)}", 500)

    #remove the file from database and the local folder
    db.execute("DELETE FROM uploads WHERE user_id = ? AND id = ?", (user_id, file_id), commit=True)

    flash("Arquivo deletado com sucesso!")
    return redirect("/")

from helpers import categorize_dataframe

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_id = session["user_id"]
    uploads_file = db.execute(
        "SELECT filename, id, filepath FROM uploads WHERE user_id = ?",
        (user_id,), fetchall=True
    )

    if not uploads_file:
        return render_template(
            "dashboard.html",
            dashboard_show=False,
            uploads=[],
            from_page="dashboard",
            labels=[],
            data=[]
        )

    if request.method == "POST":
        file_id = request.form.get("file_id")
        row = db.execute(
            "SELECT filename, filepath FROM uploads WHERE user_id = ? AND id = ?",
            (user_id, file_id), fetchone=True
        )
        if row is None:
            return apology("File not found", 400)
    else:
        row = uploads_file[0]

    df, category_sums = categorize_dataframe(
        read_file(row["filepath"], row["filename"])
    )

    labels = list(category_sums.keys())
    data   = list(category_sums.values())

    total_out = abs(df[df["valor"] < 0]["valor"].sum())
    total_in  = df[df["valor"] > 0]["valor"].sum()

    return render_template(
        "dashboard.html",
        dashboard_show=True,
        uploads=uploads_file,
        from_page="dashboard",
        labels=labels,
        data=data,
        total_out=round(total_out,2),
        total_in =round(total_in ,2)
    )