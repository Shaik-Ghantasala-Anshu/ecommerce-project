from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'secret123'

# 12 Products
products = [
    {"id": 1, "name": "Shoes", "price": 999, "image": "shoes.jpg"},
    {"id": 2, "name": "Watch", "price": 1999, "image": "watch.jpg"},
    {"id": 3, "name": "Bag", "price": 1499, "image": "bag.jpg"},
    {"id": 4, "name": "T-Shirt", "price": 599, "image": "tshirt.jpg"},
    {"id": 5, "name": "Headphones", "price": 1299, "image": "headphones.jpg"},
    {"id": 6, "name": "Sunglasses", "price": 799, "image": "sunglasses.jpg"},
    {"id": 7, "name": "Laptop", "price": 49999, "image": "laptop.jpg"},
    {"id": 8, "name": "Mobile", "price": 19999, "image": "mobile.jpg"},
    {"id": 9, "name": "Bottle", "price": 299, "image": "bottle.jpg"},
    {"id": 10, "name": "Backpack", "price": 1199, "image": "backpack.jpg"},
    {"id": 11, "name": "Keyboard", "price": 899, "image": "keyboard.jpg"},
    {"id": 12, "name": "Mouse", "price": 499, "image": "mouse.jpg"}
]

users = {}

@app.route('/')
def home():
    return render_template('index.html', products=products)

# -------- REGISTER --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users[request.form['username']] = request.form['password']
        return redirect('/login')
    return render_template('register.html')

# -------- LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u in users and users[u] == p:
            session['user'] = u
            return redirect('/')
    return render_template('login.html')

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('cart', None)
    return redirect('/')

# -------- ADD TO CART --------
@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(pid)
    session.modified = True
    return redirect('/')

# -------- REMOVE FROM CART --------
@app.route('/remove_from_cart/<int:pid>')
def remove_from_cart(pid):
    if 'cart' in session and pid in session['cart']:
        session['cart'].remove(pid)
        session.modified = True
    return redirect('/cart')

# -------- CLEAR CART --------
@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect('/cart')

# -------- CART --------
@app.route('/cart')
def cart():
    items = []
    total = 0
    for pid in session.get('cart', []):
        for p in products:
            if p['id'] == pid:
                items.append(p)
                total += p['price']
    return render_template('cart.html', items=items, total=total)

if __name__ == '__main__':
    app.run(debug=True)

