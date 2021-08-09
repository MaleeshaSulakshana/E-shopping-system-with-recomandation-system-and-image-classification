import os
import sys
from flask import Flask, render_template, send_file, redirect, send_from_directory, jsonify, json, url_for, request, session

sys.path.append(os.path.abspath('python/'))
import user
import admin

app = Flask(__name__)
app.secret_key = "EShopping"
app.static_folder = "templates/"


@app.route('/')
def index():
    return user.index()


# Rederect root for product page
@app.route('/product', methods=['GET', 'POST'])
def product():

    return user.product()


# Rederect root for product details page
@app.route('/product_details')
def product_details():
    return user.product_details()


# For add to cart
@app.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    return user.add_to_cart()


# For remove from cart
@app.route('/remove_item_from_cart', methods=['GET', 'POST'])
def remove_item_from_cart():
    return user.remove_item_from_cart()


# For clear cart
@app.route('/clear_cart')
def clear_cart():
    return user.clear_cart()


# For add check product and sizes is exist
@app.route('/check_product_sizes_is_exist_in_cart', methods=['GET', 'POST'])
def check_product_sizes_is_exist_in_cart():
    return user.check_product_sizes_is_exist_in_cart()


# Rederect root for sign in page
@app.route('/sign_in')
def sign_in():
    return user.sign_in()


# Rederect root for shopping cart page
@app.route('/cart')
def cart():
    return user.cart()


# Rederect root for cart complete
@app.route('/cart_complete', methods=['GET', 'POST'])
def cart_complete():
    return user.cart_complete()


# Rederect root for wishlist page
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    return user.wishlist()


# For add to wishlist
@app.route('/add_to_wishlist', methods=['GET', 'POST'])
def add_to_wishlist():
    return user.add_to_wishlist()


# For remove from wishlist
@app.route('/remove_item_from_wishlist', methods=['GET', 'POST'])
def remove_item_from_wishlist():
    return user.remove_item_from_wishlist()


# For remove from wishlist
@app.route('/clear_wishlist', methods=['GET', 'POST'])
def clear_wishlist():
    return user.clear_wishlist()


# Rederect root for profile page
@app.route('/profile')
def profile():
    return user.profile()


# Rederect root for user password change page
@app.route('/userChangePsw')
def userChangePsw():
    return user.userChangePsw()


# Rederect root for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Rederect root for admin page
@app.route('/Admin')
def Admin():
    return admin.Admin()


# Rederect root for admin login page
@app.route('/login')
def login():
    return admin.login()


# Rederect root for admin view_products page
@app.route('/view_products')
def view_products():
    return admin.view_products()


# Rederect root for admin add products page
@app.route('/add_product')
def add_product():
    return admin.add_product()


# Rederect root for admin add color, images and quantity page
@app.route('/add_imagesColorQty')
def add_imagesColorQty():
    return admin.add_imagesColorQty()


# Rederect root for admin add product sizes
@app.route('/add_product_sizes')
def add_product_sizes():
    return admin.add_product_sizes()


# Rederect root for admin update quantity page
@app.route('/update_product_qty')
def update_product_qty():
    return admin.update_product_qty()


# Rederect root for admin update product details page
@app.route('/update_product_details')
def update_product_details():
    return admin.update_product_details()


# Rederect root for admin view users list page
@app.route('/view_users_list')
def view_users_list():
    return admin.view_users_list()


# Rederect root for admin purchases view page
@app.route('/purchases')
def purchases():
    return admin.purchases()


# Rederect root for admin purchases view page
@app.route('/purchases_details', methods=['GET', 'POST'])
def purchases_details():
    return admin.purchases_details()


# Rederect root for admin profile view page
@app.route('/admin_profile')
def admin_profile():
    return admin.admin_profile()


# Rederect root for admin admin psw change page
@app.route('/admin_psw_change')
def admin_psw_change():
    return admin.admin_psw_change()


# For create new user account
@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    return user.createAccount()


# For login user account
@app.route('/userAccountLogin', methods=['GET', 'POST'])
def accountLogin():
    return user.accountLogin()


# For logout user account
@app.route('/userAccountLogout', methods=['GET', 'POST'])
def userAccountLogout():
    if 'userid' in session:
        session.pop('userid', None)

    if 'cart' in session:
        session.pop('cart', None)

    return redirect(url_for('index'))


# For upload user profile picture
@app.route('/userProfilePicUpload', methods=['GET', 'POST'])
def userProfilePicUpload():
    return user.userProfilePicUpload()


# For remove user profile picture
@app.route('/userProfilePictureRemove', methods=['GET', 'POST'])
def userProfilePictureRemove():
    return user.userProfilePictureRemove()


# For login user account
@app.route('/userAccountChangePsw', methods=['GET', 'POST'])
def userAccountChangePsw():
    return user.userAccountChangePsw()


# Admin
# For login admin account
@app.route('/adminAccountLogin', methods=['GET', 'POST'])
def adminAccountLogin():
    return admin.adminAccountLogin()


# For logout admin account
@app.route('/adminAccountLogout', methods=['GET', 'POST'])
def adminAccountLogout():
    if 'adminId' in session:
        session.pop('adminId', None)

    return redirect(url_for('login'))


# For admin account details update
@app.route('/adminAccountDetailsUpdate', methods=['GET', 'POST'])
def adminAccountDetailsUpdate():
    return admin.adminAccountDetailsUpdate()


# For admin account psw change
@app.route('/adminAccountPswChange', methods=['GET', 'POST'])
def adminAccountPswChange():
    return admin.adminAccountPswChange()


# For admin account psw change
@app.route('/addNewProduct', methods=['GET', 'POST'])
def addNewProduct():
    return admin.addNewProduct()


# For admin add new product details
@app.route('/addNewProductDetails', methods=['GET', 'POST'])
def addNewProductDetails():
    return admin.addNewProductDetails()


# For admin add new product details
@app.route('/addNewProductSize', methods=['GET', 'POST'])
def addNewProductSize():
    return admin.addNewProductSize()


# For admin add update product qty
@app.route('/updateProductQty', methods=['GET', 'POST'])
def updateProductQty():
    return admin.updateProductQty()


# For admin add update purchase delivery
@app.route('/updatePurchaseDelivery', methods=['GET', 'POST'])
def updatePurchaseDelivery():
    return admin.updatePurchaseDelivery()


# For getting prediction from classification model
@app.route('/detectDress', methods=['GET', 'POST'])
def detectDress():
    return user.detectDress()


# For update product details in admin side
@app.route('/updateProductDetails', methods=['GET', 'POST'])
def updateProductDetails():
    return admin.updateProductDetails()


# For update user profile details
@app.route('/updateUserProfileDetails', methods=['GET', 'POST'])
def updateUserProfileDetails():
    return user.updateUserProfileDetails()


# For get admin panel chart details
@app.route('/adminChartDetails', methods=['GET', 'POST'])
def adminChartDetails():
    return admin.adminChartDetails()


if __name__ == '__main__':
    app.run(debug=True)
