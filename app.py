from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import pandas as pd
import os

from retail_ai.recommendation import get_recommendations
from retail_ai.chatbot import get_chatbot_response
from retail_ai.inventory import analyze_inventory

app = Flask(__name__)
# Secret key is required for Flask session to work
app.secret_key = 'retailai-secret-key-2024'

# ── Load data at startup ──────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
try:
    products_df = pd.read_csv(os.path.join(DATA_DIR, 'products.csv'))
    sales_df    = pd.read_csv(os.path.join(DATA_DIR, 'sales.csv'))
except Exception as e:
    print(f"Error loading datasets: {e}")
    products_df = pd.DataFrame(columns=['product_id','name','category','price','stock','description','image_url'])
    sales_df    = pd.DataFrame(columns=['date','product_id','quantity_sold'])


# ── Helper: resolve a product dict by ID ─────────────────────────────────────
def get_product_by_id(product_id):
    """Return a product dict for the given product_id, or None if not found."""
    row = products_df[products_df['product_id'] == product_id]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


# ── Context processor: inject cart/wishlist counts into every template ────────
@app.context_processor
def inject_counts():
    """Makes cart_count and wishlist_count available in all templates."""
    cart      = session.get('cart', {})
    wishlist  = session.get('wishlist', [])
    return {
        'cart_count':     sum(item['qty'] for item in cart.values()),
        'wishlist_count': len(wishlist),
    }


# ── Storefront ────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    all_products    = products_df.to_dict('records')
    recommendations = get_recommendations(products_df, current_product_id=101, limit=4)
    return render_template('index.html', products=all_products, recommendations=recommendations)


# ── Product Detail ────────────────────────────────────────────────────────────
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return render_template('404.html'), 404
    recommendations = get_recommendations(products_df, current_product_id=product_id, limit=3)
    # Tell the template whether this product is already in cart / wishlist
    in_cart     = str(product_id) in session.get('cart', {})
    in_wishlist = product_id in session.get('wishlist', [])
    return render_template('product.html', product=product,
                           recommendations=recommendations,
                           in_cart=in_cart, in_wishlist=in_wishlist)


# ── Cart: view ────────────────────────────────────────────────────────────────
@app.route('/cart')
def cart():
    cart_data  = session.get('cart', {})
    cart_items = list(cart_data.values())
    subtotal   = sum(item['price'] * item['qty'] for item in cart_items)
    tax        = round(subtotal * 0.08, 2)   # 8 % tax
    total      = round(subtotal + tax, 2)
    return render_template('cart.html', cart_items=cart_items,
                           subtotal=round(subtotal, 2), tax=tax, total=total)


# ── Cart: add ─────────────────────────────────────────────────────────────────
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    cart = session.get('cart', {})
    pid  = str(product_id)

    if pid in cart:
        cart[pid]['qty'] += 1           # increment quantity if already in cart
    else:
        cart[pid] = {
            'product_id': product_id,
            'name':       product['name'],
            'price':      float(product['price']),
            'image_url':  product['image_url'],
            'category':   product['category'],
            'qty':        1,
        }

    session['cart']     = cart          # must reassign for Flask to detect change
    session.modified    = True
    new_count = sum(item['qty'] for item in cart.values())
    return jsonify({'success': True, 'message': f"{product['name']} added to cart!",
                    'cart_count': new_count})


# ── Cart: remove ──────────────────────────────────────────────────────────────
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    pid  = str(product_id)
    cart.pop(pid, None)
    session['cart']  = cart
    session.modified = True
    return redirect(url_for('cart'))


# ── Cart: update quantity ─────────────────────────────────────────────────────
@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    cart = session.get('cart', {})
    pid  = str(product_id)
    qty  = int(request.form.get('qty', 1))
    if pid in cart:
        if qty <= 0:
            cart.pop(pid)
        else:
            cart[pid]['qty'] = qty
    session['cart']  = cart
    session.modified = True
    return redirect(url_for('cart'))


# ── Wishlist: view ────────────────────────────────────────────────────────────
@app.route('/wishlist')
def wishlist():
    ids            = session.get('wishlist', [])
    wishlist_items = [get_product_by_id(pid) for pid in ids if get_product_by_id(pid)]
    return render_template('wishlist.html', wishlist_items=wishlist_items)


# ── Wishlist: toggle (add / remove) ──────────────────────────────────────────
@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    product  = get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    wishlist = session.get('wishlist', [])

    if product_id in wishlist:
        wishlist.remove(product_id)         # toggle off
        action  = 'removed'
        message = f"{product['name']} removed from wishlist."
    else:
        wishlist.append(product_id)         # toggle on
        action  = 'added'
        message = f"{product['name']} added to wishlist!"

    session['wishlist'] = wishlist
    session.modified    = True
    return jsonify({'success': True, 'action': action, 'message': message,
                    'wishlist_count': len(wishlist)})


# ── Wishlist: remove ──────────────────────────────────────────────────────────
@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
def remove_from_wishlist(product_id):
    wishlist = session.get('wishlist', [])
    if product_id in wishlist:
        wishlist.remove(product_id)
    session['wishlist'] = wishlist
    session.modified    = True
    return redirect(url_for('wishlist'))


# ── Wishlist → Cart ───────────────────────────────────────────────────────────
@app.route('/move_to_cart/<int:product_id>', methods=['POST'])
def move_to_cart(product_id):
    """Move an item from wishlist directly into the cart."""
    product  = get_product_by_id(product_id)
    wishlist = session.get('wishlist', [])
    cart     = session.get('cart', {})
    pid      = str(product_id)

    if product_id in wishlist:
        wishlist.remove(product_id)

    if pid not in cart and product:
        cart[pid] = {
            'product_id': product_id,
            'name':       product['name'],
            'price':      float(product['price']),
            'image_url':  product['image_url'],
            'category':   product['category'],
            'qty':        1,
        }

    session['wishlist'] = wishlist
    session['cart']     = cart
    session.modified    = True
    return redirect(url_for('cart'))


import random, string

def _order_ref():
    """Generate a short random order reference like RA-A3F9K."""
    return 'RA-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# ── Checkout: show form ───────────────────────────────────────────────────────
@app.route('/checkout')
def checkout():
    cart_data  = session.get('cart', {})
    if not cart_data:
        return redirect(url_for('cart'))          # nothing to check out
    cart_items = list(cart_data.values())
    subtotal   = sum(item['price'] * item['qty'] for item in cart_items)
    tax        = round(subtotal * 0.08, 2)
    total      = round(subtotal + tax, 2)
    return render_template('checkout.html', cart_items=cart_items,
                           subtotal=round(subtotal, 2), tax=tax, total=total)


# ── Checkout: process order ───────────────────────────────────────────────────
@app.route('/place_order', methods=['POST'])
def place_order():
    cart_data = session.get('cart', {})
    if not cart_data:
        return redirect(url_for('cart'))

    # Collect form data
    order = {
        'ref':     _order_ref(),
        'name':    request.form.get('name', ''),
        'email':   request.form.get('email', ''),
        'address': request.form.get('address', ''),
        'city':    request.form.get('city', ''),
        'zip':     request.form.get('zip', ''),
        'payment': request.form.get('payment', 'card'),
        'items':   list(cart_data.values()),
        'subtotal': round(sum(i['price'] * i['qty'] for i in cart_data.values()), 2),
    }
    order['tax']   = round(order['subtotal'] * 0.08, 2)
    order['total'] = round(order['subtotal'] + order['tax'], 2)

    # Save confirmation data and clear the cart
    session['last_order'] = order
    session['cart']       = {}
    session.modified      = True

    return redirect(url_for('order_confirmation'))


# ── Order confirmation ────────────────────────────────────────────────────────
@app.route('/order_confirmation')
def order_confirmation():
    order = session.get('last_order')
    if not order:
        return redirect(url_for('home'))
    return render_template('confirmation.html', order=order)


# ── Chatbot ───────────────────────────────────────────────────────────────────
@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data       = request.json
    user_query = data.get('query', '')
    if not user_query:
        return jsonify({'response': 'Please say something.'}), 400
    response = get_chatbot_response(user_query, products_df)
    return jsonify({'response': response})


# ── Admin / Inventory Dashboard ───────────────────────────────────────────────
@app.route('/admin')
def admin():
    insights = analyze_inventory(products_df, sales_df)
    return render_template('inventory.html', insights=insights)


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
