from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from config import Config
from models import db, User, Category, Product, CartItem, Order, OrderItem
from flask_mail import Mail, Message

# 1. App initialization
app = Flask(__name__)
app.config.from_object(Config)

# 2. Mail Configuration (Yahan apni Asli Gmail ID likhein)
# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mfareedsajjad@gmail.com'
app.config['MAIL_PASSWORD'] = 'upmfcolxhvpthlrc'  # App Password bina spaces ke
app.config['MAIL_DEFAULT_SENDER'] = 'mfareedsajjad@gmail.com'

mail = Mail(app)

# 3. Mail Initialize
mail = Mail(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ───────────────────────── Helpers ─────────────────────────

def get_cart_count():
    if current_user.is_authenticated:
        return sum(item.quantity for item in current_user.cart_items)
    return 0

def get_cart_total():
    if current_user.is_authenticated:
        return sum(item.subtotal() for item in current_user.cart_items)
    return 0

@app.context_processor
def inject_globals():
    return {
        "cart_count": get_cart_count(),
        "categories": Category.query.all(),
        "year": datetime.now().year,
    }


# ───────────────────────── Public Routes ─────────────────────────

@app.route("/")
def home():
    featured = Product.query.filter_by(is_featured=True, is_active=True).limit(5).all()
    latest = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(8).all()
    trending = Product.query.filter(Product.badge.in_(["Hot", "Trending", "Popular"])).limit(6).all()
    new_products = Product.query.filter(Product.badge == "New").limit(6).all()
    deals = Product.query.filter(Product.badge.in_(["Sale", "Deal"])).limit(6).all()
    bestsellers = Product.query.filter(Product.badge.in_(["Bestseller", "Best Seller"])).limit(4).all()
    all_products = Product.query.filter_by(is_active=True).order_by(Product.id.desc()).limit(12).all()

    occasions = [
        {"name": "Eid Collection", "image": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=300&fit=crop"},
        {"name": "Wedding Wear", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&h=300&fit=crop"},
        {"name": "Office Wear", "image": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=300&fit=crop"},
        {"name": "Casual Daily", "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=500&h=300&fit=crop"},
    ]

    return render_template(
        "index.html",
        featured=featured,
        latest=latest,
        trending=trending,
        new_products=new_products,
        deals=deals,
        bestsellers=bestsellers,
        all_products=all_products,
        occasions=occasions,
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    return render_template("product.html", product=product, related=related)


@app.route("/category/<int:category_id>")
def category_page(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id, is_active=True).all()
    return render_template("category.html", category=category, products=products)


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    products = []
    if q:
        products = Product.query.filter(
            Product.is_active == True,
            db.or_(
                Product.name.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%")
            )
        ).all()
    return render_template("search.html", products=products, query=q)


# ───────────────────────── Auth Routes ─────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not all([name, email, password]):
            flash("Please fill all required fields.", "danger")
            return render_template("auth/register.html")
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return render_template("auth/register.html")

        user = User(name=name, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Welcome {name}! Account created successfully.", "success")
        return redirect(url_for("home"))
    return render_template("auth/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f"Welcome back, {user.name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))
        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


# ───────────────────────── Cart Routes ─────────────────────────

@app.route("/cart")
@login_required
def cart():
    items = current_user.cart_items
    total = sum(item.subtotal() for item in items)
    return render_template("cart.html", items=items, total=total)


@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if product.stock < 1:
        flash("Sorry, this product is out of stock.", "warning")
        return redirect(request.referrer or url_for("home"))

    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash(f"'{product.name}' added to cart!", "success")
    return redirect(request.referrer or url_for("home"))


@app.route("/update_cart/<int:item_id>", methods=["POST"])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    qty = int(request.form.get("quantity", 1))
    if qty < 1:
        db.session.delete(item)
    else:
        item.quantity = qty
    db.session.commit()
    flash("Cart updated.", "success")
    return redirect(url_for("cart"))


@app.route("/remove_from_cart/<int:item_id>")
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart"))


# ───────────────────────── Checkout & Orders ─────────────────────────

@app.route("/checkout", methods=["GET", "POST"])
@login_required 
def checkout():
    items = current_user.cart_items
    if not items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart"))
    total = sum(item.subtotal() for item in items)

    if request.method == "POST":
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()
        city = request.form.get("city", "").strip()
        notes = request.form.get("notes", "").strip()

        if not address or not phone:
            flash("Address and phone are required.", "danger")
            return render_template("checkout.html", items=items, total=total)

        order = Order(
            user_id=current_user.id,
            total=total,
            shipping_address=address,
            phone=phone,
            city=city,
            notes=notes,
            payment_method="Cash on Delivery",
            status="Pending"
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            db.session.add(order_item)
            item.product.stock = max(0, item.product.stock - item.quantity)

        # clear cart
        for item in items:
            db.session.delete(item)

        db.session.commit()

        # --- EMAIL NOTIFICATION START ---
        try:
            msg = Message(
                subject=f"Order Confirmation - Markaz Clone #{order.id}",
                recipients=[current_user.email]
            )
            msg.body = f"""
            Assalam-o-Alaikum,

            Aap ka order successfully place ho gaya hai!

            Order Details:
            ----------------------------------
            Order ID: #{order.id}
            Total Amount: Rs. {order.total}
            Payment Method: Cash on Delivery
            Shipping Address: {order.shipping_address}, {order.city}

            Hum aap ka order jald dispatch kar dein ge.

            Shukriya,
            Markaz Clone Team
            """
            mail.send(msg)
        except Exception as e:
            print("Email sending failed:", e)
        # --- EMAIL NOTIFICATION END ---

        flash(f"Order #{order.id} placed successfully! Pay Cash on Delivery.", "success")
        return redirect(url_for("order_detail", order_id=order.id))

    return render_template("checkout.html", items=items, total=total)


@app.route("/orders")
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("orders.html", orders=orders)


@app.route("/order/<int:order_id>")
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    return render_template("order_detail.html", order=order)


# ───────────────────────── Admin Routes ─────────────────────────

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access required.", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    stats = {
        "products": Product.query.count(),
        "orders": Order.query.count(),
        "users": User.query.count(),
        "pending": Order.query.filter_by(status="Pending").count(),
        "revenue": db.session.query(db.func.sum(Order.total)).filter(Order.status != "Cancelled").scalar() or 0,
    }
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()
    return render_template("admin/dashboard.html", stats=stats, recent_orders=recent_orders)


@app.route("/admin/products")
@login_required
@admin_required
def admin_products():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template("admin/products.html", products=products)


@app.route("/admin/product/add", methods=["GET", "POST"])
@login_required
@admin_required
def admin_add_product():
    categories = Category.query.all()
    if request.method == "POST":
        product = Product(
            name=request.form["name"],
            description=request.form.get("description", ""),
            price=int(request.form["price"]),
            old_price=int(request.form["old_price"]) if request.form.get("old_price") else None,
            image=request.form.get("image", ""),
            badge=request.form.get("badge") or None,
            rating=float(request.form.get("rating", 4.5)),
            stock=int(request.form.get("stock", 50)),
            category_id=int(request.form["category_id"]),
            is_featured=bool(request.form.get("is_featured")),
            is_active=True
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("admin_products"))
    return render_template("admin/product_form.html", product=None, categories=categories)


@app.route("/admin/product/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form.get("description", "")
        product.price = int(request.form["price"])
        product.old_price = int(request.form["old_price"]) if request.form.get("old_price") else None
        product.image = request.form.get("image", "")
        product.badge = request.form.get("badge") or None
        product.rating = float(request.form.get("rating", 4.5))
        product.stock = int(request.form.get("stock", 50))
        product.category_id = int(request.form["category_id"])
        product.is_featured = bool(request.form.get("is_featured"))
        product.is_active = bool(request.form.get("is_active"))
        db.session.commit()
        flash("Product updated!", "success")
        return redirect(url_for("admin_products"))
    return render_template("admin/product_form.html", product=product, categories=categories)


@app.route("/admin/product/delete/<int:product_id>")
@login_required
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "info")
    return redirect(url_for("admin_products"))


@app.route("/admin/orders")
@login_required
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=orders)


@app.route("/admin/order/<int:order_id>/status", methods=["POST"])
@login_required
@admin_required
def admin_update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get("status")
    if status in ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]:
        order.status = status
        db.session.commit()
        flash(f"Order #{order.id} status updated to {status}.", "success")
    return redirect(url_for("admin_orders"))


# ───────────────────────── Init ─────────────────────────
with app.app_context():
    admin_user = User.query.filter_by(email="admin@markaz.pk").first()
    if admin_user:
        admin_user.password = generate_password_hash("admin123")
        admin_user.is_admin = True
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)