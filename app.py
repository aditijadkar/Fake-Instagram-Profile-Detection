from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import joblib
from scrape_instagram import get_instagram_data

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "your_secret_key"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Load trained model
model = joblib.load("models/fake_detector.pkl")

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        insta_username = request.form["username"]
        insta_data = get_instagram_data(insta_username)

        if "error" in insta_data:
            if insta_data["error"] in ["Profile not found", "Rate limit reached. Please try again in a few minutes."]:
                return render_template("not_found.html", error=insta_data["error"])
            else:
                return render_template("error.html", error=insta_data["error"])

        feature_vector = [[
            insta_data["profile_pic"],
            insta_data["nums_length_username"],
            insta_data["fullname_words"],
            insta_data["nums_length_fullname"],
            insta_data["name_equals_username"],
            insta_data["description_length"],
            insta_data["external_url"],
            insta_data["private"],
            insta_data["posts"],
            insta_data["followers"],
            insta_data["following"]
        ]]

        prediction = model.predict(feature_vector)[0]
        score = model.predict_proba(feature_vector)[0][1] * 100

        return render_template(
            "result.html",
            username=insta_username,
            score=score,
            insta_data=insta_data,
            is_fake=prediction
        )

    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
