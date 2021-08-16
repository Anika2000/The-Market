from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = "hello"

db = SQLAlchemy(app)


#Create the database
#db.create_all()

#Database Models
class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    shoppingcart = db.relationship("Cart", backref="user", lazy=True)

    def __repr__(self): 
        return f"User is {self.username} with password {self.password}"


cart_items = db.Table( "cart_items", 
    db.Column("item_id", db.Integer, db.ForeignKey("item.id")), 
    db.Column("cart_id", db.Integer, db.ForeignKey("cart.id"))
)


class Item(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(20))
    carts_on_item_table = db.relationship("Cart", secondary=cart_items, backref="items", lazy=True)

    def __repr__(self): 
        return f"The item {self.id} is {self.name} and price is {self.price}, posted on {self.date_posted} in {self.category}"


class Cart(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items_on_cart_table = db.relationship("Item", secondary=cart_items, backref="carts", lazy=True)

    def __repr__(self):
        return f"This cart's id is {self.id} belonging to the user with id {self.user_id}"



# Views and Controllers
@app.route('/')
def index(): 
    if not session.get("username"): 
        return redirect("/login")
    return render_template("index.html")


@app.route('/shoppingcart')
def shoppingcart(): 
    user_name = session.get("username")
    user = User.query.filter_by(username=user_name).first()
    user_cart = Cart.query.filter_by(user_id=user.id).first()
    all_items_on_cart = user_cart.items
    total = 0
    for item in all_items_on_cart:
        total = total + item.price
    return render_template("cart.html", items=all_items_on_cart, name=user_name, total=total)



@app.route('/add', methods=["GET", "POST"])
def add(): 
    if request.method == "POST": 
        user_name = session.get("username")
        user = User.query.filter_by(username=user_name).first()
        user_cart = Cart.query.filter_by(user_id=user.id).first()
        item_id = request.form.get("item_id")
        item_to_add = Item.query.get(item_id)
        user_cart.items.append(item_to_add)
        db.session.commit()
        return redirect("/shoppingcart")
    else: 
        return render_template("error.html")



@app.route('/remove', methods=["GET", "POST"])
def remove(): 
    if request.method == "POST": 
        user_name = session.get("username")
        user = User.query.filter_by(username=user_name).first()
        user_cart = Cart.query.filter_by(user_id=user.id).first()
        item_id_rem = request.form.get("item_id_rem")
        item_to_remove = Item.query.get(item_id_rem)
        user_cart.items.remove(item_to_remove)
        db.session.commit()
        return redirect("/shoppingcart")
    else: 
        return render_template("error.html")



@app.route('/createlisting', methods=["GET", "POST"])
def create(): 
    if request.method == "POST": 
        #if product name is an empty string or no proce available return an error statement
        product_name = request.form.get("itemname")
        product_description = request.form.get("itemdescription")
        product_price = request.form.get("itemprice")
        product_category = request.form.get("itemcategory")
        new_item = Item(name=product_name, description=product_description, price=product_price, category=product_category)
        try: 
            db.session.add(new_item)
            db.session.commit()
            return render_template("create.html")
        except:
            return render_template("error.html")
    else: 
        return render_template("create.html")


@app.route('/shop/<category>')
def shop(category): 
    if category == "All": 
        all_items = Item.query.all()
    else: 
        all_items = Item.query.filter_by(category=category).all()
    return render_template("shop.html", items=all_items, header=category)


@app.route('/login', methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        username_login = request.form.get("usernamelogin") 
        password_login = request.form.get("passwordlogin")
        user_validate = User.query.filter_by(username=username_login).first()
        if user_validate is None: 
            return render_template("error.html")
        else: 
            pass_word = user_validate.password
            if pass_word == password_login: 
                session["username"] = username_login
                return redirect("/")
            else: 
                return render_template("error.html")
    else: 
        return render_template("login.html")



@app.route('/signup', methods=["GET", "POST"])
def signup(): 
    if request.method == "POST": 
        user_name = request.form.get("username")
        pass_word = request.form.get("password")
        if User.query.filter_by(username=user_name).first() is None: 
            new_user = User(username=user_name, password=pass_word)
            try: 
                db.session.add(new_user)
                db.session.commit()
                created_user = User.query.filter_by(username=user_name).first()
                new_cart = Cart(user_id=created_user.id)
                db.session.add(new_cart)
                db.session.commit()
                return render_template("login.html")
            except: 
                return render_template("signup.html", messages="There was an error with signing you up. Try Again")
        else: 
            return render_template("error.html")
    else: 
        return render_template("signup.html")
    


@app.route('/logout')
def logout(): 
    session.pop('username', None)
    return redirect("/login")