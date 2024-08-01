from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import re
import os

class UserManager:
    def __init__(self, file_path='user_data.csv'):
        self.file_path = file_path
        self.initialize_file()

    def initialize_file(self):
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['email', 'password'])

    def is_valid_email(self, email):
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

    def is_valid_password(self, password):
        return len(password) > 8

    def save_user(self, email, password):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, password])

    def is_user_exists(self, email):
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email:
                    return True
        return False

    def authenticate_user(self, email, password):
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == email and row[1] == password:
                        return True
            return False
        except FileNotFoundError:
            print("User data file not found")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'your_secret_key'
        self.user_manager = UserManager()

        self.configure_routes()

    def configure_routes(self):
        @self.app.route("/")
        def home():
            return render_template("home.html")

        @self.app.route('/about')
        def about():
            return render_template('about.html')

        @self.app.route('/contact')
        def contact():
            return render_template('contact.html')

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                email = request.form['email']
                password = request.form['password']
                if not email or not password:
                    flash("Fields cannot be empty.")
                elif not self.user_manager.is_valid_email(email):
                    flash("Invalid email address.")
                elif not self.user_manager.is_valid_password(password):
                    flash("Password must be more than 8 characters.")
                elif self.user_manager.is_user_exists(email):
                    flash("Email already registered.")
                else:
                    self.user_manager.save_user(email, password)
                    return redirect(url_for('login'))
            return render_template('register.html')

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                email = request.form['email']
                password = request.form['password']
                if self.user_manager.authenticate_user(email, password):
                    flash("Login successful!", "success")
                    return redirect(url_for('success'))
                else:
                    flash("Invalid email or password.", "danger")
                    return redirect(url_for('login'))
            return render_template('login.html')

        @self.app.route('/success')
        def success():
            return render_template("success.html")

    def run(self):
        self.app.run(debug=True, port=7000)

if __name__ == '__main__':
    app = FlaskApp()
    app.run()
