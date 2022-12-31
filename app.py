from cgitb import reset
from symtable import Symbol
from unittest import result
from cs50 import SQL
from flask import Flask, current_app, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy import null
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
from flask import *
import sqlite3
import hashlib
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import g, request

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ehealth.db'
app.config['SECRET_KEY'] = "SOME VAL"
app.app_context().push()
db = SQLAlchemy(app)

db.create_all()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ehealth.db")

# Make sure API key is set
os.environ["API_KEY"] = 'pk_90e51ad10a4b49f2a18da659384551ee'
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template('index.html', firstName=firstName, noOfItems=noOfItems)


@app.route("/services")
def services():
    """Show portfolio of stocks"""
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template('services.html', firstName=firstName, noOfItems=noOfItems)


@app.route("/about")
def about():
    """Show portfolio of stocks"""
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template('about.html', firstName=firstName, noOfItems=noOfItems)


@app.route("/contact")
def contact():
    """Show portfolio of stocks"""
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template('contact.html', firstName=firstName, noOfItems=noOfItems)


def getLoginDetails():
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute(
                "SELECT id, firstName FROM users WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
            cur.execute(
                "SELECT count(productId) FROM cart WHERE userId = " + str(userId))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)


@app.route("/addToCart")
@login_required
def addToCart():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = int(request.args.get('productId'))
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = '" +
                    session['email'] + "'")
        id = cur.fetchone()[0]
        try:
            cur.execute(
                "INSERT INTO cart (userId, productId) VALUES (?, ?)", (id, productId))
            conn.commit()
            msg = "Added successfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    flash('Add to cart')
    return redirect(url_for('Product'))


@app.route("/cart")
@login_required
def cart():
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = '" + email + "'")
        id = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, cart WHERE products.productId = cart.productId AND cart.userId = " + str(id))
        products = cur.fetchall()

    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    totalPrice = round(totalPrice)

    return render_template("cart.html", firstName=firstName, noOfItems=noOfItems, products=products, totalPrice=totalPrice)


@app.route("/confirmOrder")
def confirmOrder():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = int(request.args.get('productId'))
    email = session['email']
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = '" + email + "'")
        id = cur.fetchone()[0]
        try:
            cur.execute(
                "INSERT INTO Confirm ( userId, productId) VALUES (?, ?)", (id, productId))
            conn.commit()
            msg = "Added successfully"
        except:
            conn.rollback()
            msg = "Error occured"

        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, Confirm WHERE products.productId = Confirm.productId AND Confirm.userId = " + str(id))
        products = cur.fetchall()
        try:
            cur.execute("DELETE FROM cart WHERE userId = " +
                        str(id) + " AND productId = " + str(productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    flash('Thanks for confirm order. We will send you between 2 days. In sha allah')
    return redirect(url_for('cart'))


@app.route("/history")
@login_required
def history():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = '" + email + "'")
        id = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, Confirm WHERE products.productId = Confirm.productId AND Confirm.userId = " + str(id))
        products = cur.fetchall()
    return render_template('confirmOrder.html', products=products,   noOfItems=noOfItems)


@app.route("/removeFromCart")
@login_required
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    productId = int(request.args.get('productId'))
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = '" + email + "'")
        id = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM cart WHERE userId = " +
                        str(id) + " AND productId = " + str(productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('cart'))


@app.route("/displayCategory")
def Product():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM products')
        itemData = cur.fetchall()
        cur.execute('SELECT * FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('display.html', firstName=firstName, noOfItems=noOfItems, itemData=itemData, categoryData=categoryData)


@app.route("/productDescription")
def productDescription():
    productId = request.args.get('productId')
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM products WHERE productId = ' + productId)
        productData = cur.fetchone()
    conn.close()
    return render_template('aboutproduct.html', firstName=firstName, data=productData, noOfItems=noOfItems)

# Admin Login


@app.route("/admin", methods=["GET", "POST"])
def admin():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        # admin = str(request.form.get("username"))

        if not request.form.get("username"):
            return apology("must provide username", 403)
        admin = str(request.form.get("username"))
        if admin != "admin":
            return apology("must provide valid username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to admin dashbord page
        return redirect("/admin/dashbord")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("admin_login.html")

# admin dashbord


@app.route("/admin/dashbord")
@login_required
def admin_dashbord():
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        loggedIn = True

        cur.execute(
            "SELECT count(id) FROM users ")
        noOfusers = cur.fetchone()[0]
        cur.execute(
            "SELECT count(categoryId) FROM categories")
        noOfcategories = cur.fetchone()[0]

        cur.execute(
            "SELECT count(cid) FROM Confirm")
        noOforder = cur.fetchone()[0]

        cur.execute(
            "SELECT * FROM Confirm")
        order = cur.fetchall()

        cur.execute(
            "SELECT * FROM products")
        products = cur.fetchall()
    conn.close()
    return render_template('addmin.html', products=products, order=order, noOforder=noOforder, noOfusers=noOfusers, noOfcategories=noOfcategories)

# admin Add products


@app.route("/admin/addProduct")
@login_required
def addProduct():
    with sqlite3.connect('ehealth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories")
        categories = cur.fetchall()
    conn.close()
    return render_template('addProducts.html', categories=categories)


@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price"))
        description = request.form.get("description")
        stock = int(request.form.get("stock"))
        categoryId = int(request.form.get("category"))

        # Uploading image procedure
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('ehealth.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO products (name, price, description, image, stock, categoryId) VALUES (?, ?, ?, ?, ?, ?)''',
                            (name, price, description, imagename, stock, categoryId))
                conn.commit()
                msg = "added successfully"
            except:
                msg = "error occured"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect(url_for('addProduct'))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        row = db.execute("SELECT * FROM users WHERE (email)= (?)",
                         (request.form.get("email")))
        session['email'] = request.form.get("email")

        # Ensure username exists and password is correct
        if len(row) != 1:
            return apology("invalid email", 403)

        rows = db.execute("SELECT * FROM users WHERE (username) =(?)",
                          (request.form.get("username")))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Log out


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Registration


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")
        address1 = request.form.get("address1")
        city = request.form.get("city")
        phone = request.form.get("phone")

        if not firstname:
            return apology("must provide firstname", 403)

        if not lastname:
            return apology("must provide lastname", 403)

        if not password:
            return apology("must provide password", 403)

        if not confirmation or password != confirmation:
            return apology("passwords do not match", 403)

        if not email:
            return apology("passwords do not match", 403)

        if not address1:
            return apology("Must provide valid address1", 403)

        if not city:
            return apology("Must provide valid city", 403)

        if not phone:
            return apology("Must provide valid phone", 403)

        hash = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (firstname,lastname,username, hash,email,address1,city,phone) VALUES (?,?,?,?,?,?,?,?)", firstname, lastname, username, hash, email, address1, city, phone)
            return redirect('/')
        except:
            return apology("Username already exists", 403)

    else:
        return render_template('register.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans
