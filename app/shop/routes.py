from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models import User, Product, db

shop = Blueprint('shop', __name__, template_folder='shoptemplates')

@shop.route('/products')
def getAllProducts():
    products = Product.query.all()
    return render_template('index.html', products = products)

@shop.route('/products/<int:product_id>')
def getOneProduct(product_id):
    product = Product.query.get(product_id)
    return render_template('oneproduct.html', product = product)

@shop.route('/cart')
@login_required
def getUserCart():
    if current_user.is_authenticated:
        cart = current_user.myCart()
    
    return render_template('cart.html', cart = cart)
    

@shop.route('/cart/add/<int:product_id>', methods=["GET", "POST"])
@login_required
def addToCart(product_id):
    product = Product.query.get(product_id)
    current_user.add(product)
    flash('Successfully added to Cart!', 'success')
    return redirect(url_for('shop.getAllProducts'))

@shop.route('/cart/remove/<int:product_id>', methods=["GET", "POST"])
@login_required
def removeFromCart(product_id):
    product = Product.query.get(product_id)
    cart_set = set()
    if current_user.is_authenticated:
        cart = current_user.cart.all()
        cart_set = {x.id for x in cart}
    
        if product.id in cart_set:
            current_user.delete(product)
            
    return redirect(url_for('shop.getAllProducts'))
    
@shop.route('/cart/deleteall')
@login_required
def deleteAll():
    if current_user.is_authenticated:
        flash('Your cart has been deleted!', 'success')
        current_user.deleteall()
        
    return render_template('cart.html')