from flask import Flask, render_template,request,url_for,flash
from models import User
from config import Config
from extensions import db

app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username").strip()
        password=request.form.get("password").strip()
        email=request.form.get("email").strip()
        role=request.form.get("role")

        if not username:
            flash("username is required","error")
            return render_template("register.html")
        if len(password)<4:
            flash("password should be greater than or equal to 4 characters","error")
            return render_template("register.html")
        if not email or "@" not in email:
            flash("enter a proper email address","error")
            return render_template("register.html")
        if role not in ["student","teacher"]:
            flash("Enter a proper role","error")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("User already exists","error")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("Email already exists","error")
            return render_template("register.html")
        try:
            user=User(
            username=username,
            password=password,
            email=email,
            role=role,
            )
            db.session.add(user)
            db.session.commit()
            flash("Registration successfull","Success")
            return render_template("home.html")
        
        except Exception:
            db.session.rollback()
            flash("Something went wrong, please try again.","error")
            return render_template("register.html")
    return render_template("register.html")




if __name__ == "__main__":
    app.run(debug=True)