import os
import sys
import random
from flask import Flask, render_template, send_file, redirect, send_from_directory, jsonify, json, url_for, request, session

sys.path.append(os.path.abspath('python/'))
# sys.path.append(os.path.abspath('dress_classification/'))
import db
import dress_classification.Predictions as predictions
import util

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# Function for return index page
def index():

    if 'userid' in session:

        result = db.searched_history(session['userid'], util.date_picker())
        if result != 'none':
            random.shuffle(result)

            random_items = []
            for i, item in enumerate(result):
                if i < 5:
                    random_items.append(item)
                else:
                    break

            items = []
            for item in random_items:
                data = db.get_recommended_items_details(item[0], item[1])
                for sub_item in data:
                    items.append(sub_item)

            random.shuffle(items)

            if len(items) != 0:
                final_recommended_items = []
                if len(items) > 20:
                    for i, product in enumerate(items):
                        if i < 20:
                            final_recommended_items.append(product)
                        else:
                            break

                else:
                    final_recommended_items = items

                ids = []
                for i in final_recommended_items:
                    ids.append(i[0])

                all_products, categories = db.getProductItemsDetails(ids)

                return render_template('index.html', products=all_products, categories=categories, recommend=final_recommended_items)

    all_products, categories = db.getProductItemsDetails()
    return render_template('index.html', products=all_products, categories=categories)


# Function for return product page
def product():

    search_item = request.args.get('search', default=None)

    if search_item is not None:
        products = db.getSearchProductDetails(search_item)
        return render_template('product.html', search=search_item, products=products)

    if request.method == "POST":
        search = str(request.form.get('txt_product_search'))
        products = db.getSearchProductDetails(search)
        return render_template('product.html', search=search, products=products)

    else:
        products, categories = db.getProductViewDetails()
        return render_template('product.html', categories=categories, products=products)


# Function for check product is exist in cart
def check_product_exist_in_cart(cart, product_code, product_color, product_size):
    is_exist_cart = 'no'

    for i, cart_item in enumerate(cart):
        if (cart_item['product_code'] == str(product_code)
            and cart_item['product_color'] == str(product_color)
                and cart_item['product_size'] == str(product_size)):
            is_exist_cart = 'yes'

            return is_exist_cart, i

    return is_exist_cart, ''


# Function for return product details page
def product_details():

    product_code = request.args.get('product_code', default=None)
    product_color = request.args.get('product_color', default=None)

    if product_code is None:
        return redirect(url_for('index'))
    else:
        if product_color is None:
            colors, sizes, details, related_products = db.getProductItemDetails(
                product_code, product_color=None)

            product_color = details[3]

        else:
            colors, sizes, details, related_products = db.getProductItemDetails(
                product_code, product_color)

        images = []
        for i in details[7:]:
            if i != 'None':
                images.append(i)

        is_exist_cart = 'no'
        item_count = 'no'
        if 'cart' in session:
            cart = session['cart']

            is_exist_cart, i = check_product_exist_in_cart(
                cart, str(product_code), str(product_color), str(sizes[0][0]))

            if is_exist_cart == 'yes':
                item_count = str(cart[i]['product_count'])

        is_exist_wishlist = 'no'
        if 'userid' in session:
            if db.checkItemExistInWishlist(session['userid'], product_code) > 0:
                is_exist_wishlist = 'yes'

            db.insertSearched(session['userid'],
                              product_code, util.date_picker())

        return render_template('product-detail.html', colors=colors, sizes=sizes, details=details,
                               images=images, is_exist_cart=is_exist_cart, item_count=item_count,
                               related_products=related_products, is_exist_wishlist=is_exist_wishlist)


# Function for return adding cart
def add_to_cart():
    if request.method == "POST":
        product_code = request.form['product_code']
        product_color = request.form['product_color']
        product_size = request.form['product_size']
        product_count = request.form['product_count']

        if 'userid' in session:

            item = {
                "product_code": product_code,
                "product_color": product_color,
                "product_size": product_size,
                "product_count": product_count,
            }

            if 'cart' in session:
                cart = session['cart']
                is_exist_cart, i = check_product_exist_in_cart(
                    cart, product_code, product_color, product_size)

                if is_exist_cart == 'yes':
                    cart.pop(i)
                    session['cart'] = cart
                    return jsonify({'cart_remove_success_msg': "Product removed from cart"})

                else:
                    cart.append(item)
                    session['cart'] = cart
                    return jsonify({'cart_added_success_msg': "Product added to cart"})

            else:
                session['cart'] = [item]

            return jsonify({'cart_added_success_msg': "Product added to cart"})

        else:
            return jsonify({'error_msg': "You are not logged in!"})

    else:
        return redirect(url_for('sign_in'))


# Function for remove cart items
def remove_item_from_cart():

    product_code = request.args.get('product_code')
    product_color = request.args.get('product_color')
    product_size = request.args.get('product_size')

    if product_code is not None or product_color is not None or product_size is not None:

        if 'userid' in session:

            if 'cart' in session:
                cart = session['cart']
                is_exist_cart, i = check_product_exist_in_cart(
                    cart, product_code, product_color, product_size)

                if is_exist_cart == 'yes':
                    cart.pop(i)
                    session['cart'] = cart

    return redirect(url_for('cart'))


# Function for return clear cart
def clear_cart():

    if 'userid' in session:
        if 'cart' in session:
            session.pop('cart', None)

    return redirect(url_for('cart'))


# Function for return check_product_sizes_is_exist_in_cart
def check_product_sizes_is_exist_in_cart():
    if request.method == "POST":
        product_code = request.form['product_code']
        product_color = request.form['product_color']
        product_size = request.form['product_size']

        if 'cart' in session:
            cart = session['cart']
            is_exist_cart, i = check_product_exist_in_cart(
                cart, product_code, product_color, product_size)

            if is_exist_cart == 'yes':
                return jsonify({'item': str(cart[i]['product_count'])})

            else:
                return jsonify({'item_not_found': "ADD TO CART"})

        else:
            return jsonify({'item_not_found': "ADD TO CART"})

    return jsonify({'item_not_found': "ADD TO CART"})


# Function for return sign_in
def sign_in():
    if 'userid' in session:
        return redirect(url_for('index'))
    else:
        return render_template('sign-in.html')


# Function for return cart
def cart():
    if 'userid' in session:
        if 'cart' in session:
            cart = session['cart']
            cart_details = []
            total_price = 0

            for item in cart:
                details = db.getCartDetails(
                    str(item['product_code']), str(item['product_color']))

                if details[2] == '':
                    discount = 0
                else:
                    discount = float(details[2])

                cart_details.append({
                    'product_code': item['product_code'],
                    'product_color': item['product_color'],
                    'product_count': item['product_count'],
                    'product_size': item['product_size'],
                    'product_title': details[0],
                    'product_icon': details[3],
                    'product_price': (float(details[1]) - discount),
                    'product_discount': discount,
                    'total': int(item['product_count']) * (float(details[1]) - discount)
                })

                total_price += float(int(item['product_count'])
                                     * (float(details[1]) - discount))

            return render_template('shoping-cart.html', cart_details=cart_details, total_price=total_price)

        return render_template('shoping-cart.html')

    else:
        return redirect(url_for('sign_in'))


# Function for return cart_complete
def cart_complete():

    if request.method == "POST":
        cart_msg = request.form['cart_msg']
        date = util.date_picker()
        date_time = util.datetime_picker()
        rnd_number = util.random_number()

        purchase_id = date_time + rnd_number

        if cart_msg == 'yes':

            if 'userid' in session:

                if 'cart' in session:
                    cart = session['cart']

                    for item in cart:
                        count = db.checkProductCountExist(item['product_code'], item['product_color'],
                                                          item['product_size'])

                        if count < int(item['product_count']):
                            return jsonify({'count_error': str(item['product_code']) + " Product " +
                                            str(item['product_size']) + " size our store have " + str(count) + " count only"})

                    for item in cart:
                        db.addToPurchase(purchase_id, session['userid'], item['product_code'], item['product_color'],
                                         item['product_size'], item['product_count'], date)

                    session.pop('cart', None)
                    return jsonify({'redirect': url_for("index")})

    return redirect(url_for('cart'))


# Function for return wishlist
def wishlist():
    if 'userid' in session:

        wishlist_data_list = db.getWishlistData(session['userid'])

        if len(wishlist_data_list) == 0:
            return render_template('wishlist.html')

        else:
            wishlist_data = []
            for item in wishlist_data_list:

                if item[4] == '':
                    discount = 0
                else:
                    discount = float(item[4])

                wishlist_data.append({
                    'product_code': item[0],
                    'product_title': item[1],
                    'product_icon': item[2],
                    'product_price': (float(item[3]) - discount)
                })

            return render_template('wishlist.html', wishlist_data=wishlist_data)

    else:
        return redirect(url_for('sign_in'))


# Function for return add_to_wishlist
def add_to_wishlist():

    if 'userid' in session:

        if request.method == "POST":
            product_code = request.form['product_code']

            if db.checkItemExistInWishlist(session['userid'], product_code) > 0:

                if db.removeFromWishlist(session['userid'], product_code) < 1:
                    return jsonify({'error_msg': "Some error occur"})

                else:
                    return jsonify({'removed_success_msg': "Product removed from wishlist"})

            else:
                if db.addToWishlist(session['userid'], product_code) < 1:
                    return jsonify({'error_msg': "Some error occur"})

                else:
                    return jsonify({'add_success_msg': "Product added to wishlist"})

        return jsonify({'error_msg': "Some error occur"})

    else:
        return redirect(url_for('sign_in'))


# Function for return remove_item_from_wishlist
def remove_item_from_wishlist():

    if 'userid' in session:
        product_code = request.args.get('product_code')

        if product_code is not None:

            db.removeFromWishlist(session['userid'], product_code)

        return redirect(url_for('wishlist'))

    else:
        return redirect(url_for('sign_in'))


# Function for return clear_wishlist
def clear_wishlist():

    if 'userid' in session:

        db.clearWishlist(session['userid'])

        return redirect(url_for('wishlist'))

    else:
        return redirect(url_for('sign_in'))


# Function for return profile
def profile():
    if 'userid' in session:
        userData, profile_pic = db.getUserData(session['userid'])
        purchase_data = db.getPurchaseDataForUser(session['userid'])

        if profile_pic != None:
            return render_template('profile.html', data=userData, profile_pic=profile_pic, purchase_data=purchase_data)
        else:
            return render_template('profile.html', data=userData, purchase_data=purchase_data)

    else:
        return redirect(url_for('index'))


# Function for return userChangePsw
def userChangePsw():
    if 'userid' in session:
        return render_template('change_psw.html')

    else:
        return redirect(url_for('index'))


# Function for return createAccount
def createAccount():
    if request.method == "POST":
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        nic = request.form['nic']
        mobile_number = request.form['mobile']
        psw = request.form['psw']
        confirm_psw = request.form['cpsw']

        if (len(first_name) == 0 or len(last_name) == 0 or len(email) == 0
                or len(nic) == 0 or len(mobile_number) == 0 or len(psw) == 0 or len(confirm_psw) == 0):
            return jsonify({'error_msg': "Fields are empty!"})

        # Validate 10 charaters nic number
        elif len(nic) == 10:
            nic_char = nic[-1].lower()
            nic_numbers = nic[0:-1]

            if nic_char not in ['v', 'x']:
                return jsonify({'error_msg': "NIC not valid"})
            elif util.RepresentsInt(nic_numbers) == False:
                return jsonify({'error_msg': "NIC not valid"})

        # Validate email address
        if util.emailValidate(email) == False:
            return jsonify({'error_msg': "Invalid email address"})

        # Validate nic number length 10 or 12
        elif len(nic) not in [10, 12]:
            return jsonify({'error_msg': "NIC not valid"})

        # Mobile number length validate
        elif len(mobile_number) != 10:
            return jsonify({'error_msg': "Mobile number contains 10 numbers"})

        # Mobile number validate only number
        elif util.RepresentsInt(mobile_number) == False:
            return jsonify({'error_msg': "Mobile number only contains numbers"})

        elif len(psw) < 8:
            return jsonify({'error_msg': "Your password weak"})

        # Validate psw and confirm psw
        elif psw != confirm_psw:
            return jsonify({'error_msg': "Password and confirm password not matched"})

        else:
            # Genarate random key and create user id
            random_no = util.random_number()
            user_id = first_name + str(random_no)

            # Check exist email
            if db.check_email_is_exist(str(email)) > 0:
                return jsonify({'error_msg': email + " This email has account"})

            # Create user account
            else:
                if db.userCreateAccount(user_id, first_name, last_name, email, nic, mobile_number, psw) < 1:

                    return jsonify({'error_msg': "Account create failed. Try again!"})

                else:
                    session['userid'] = user_id

                    return jsonify({'redirect': url_for("index")})

    return jsonify({'redirect': url_for("index")})


# Function for return accountLogin
def accountLogin():
    if request.method == "POST":
        loginEmail = request.form['loginEmail']
        loginPsw = request.form['loginPsw']

        if (len(loginEmail) == 0 or len(loginPsw) == 0):
            return jsonify({'error_msg': "Fields are empty!"})

        # Validate email address
        elif util.emailValidate(loginEmail) == False:
            return jsonify({'error_msg': "Invalid email address"})

        # Login
        else:
            userId = db.userLogin(loginEmail, loginPsw)
            if len(userId) == 0:
                return jsonify({'error_msg': "Email or password invalid. Try again!"})

            else:
                session['userid'] = userId[0][0]
                return jsonify({'redirect': url_for("index")})


# Function for return userProfilePicUpload
def userProfilePicUpload():
    if 'userid' in session:
        if request.method == "POST":

            # Save Uploaded image
            for images in request.files.getlist("upload_profile_image"):
                image_root = util.get_images_root(APP_ROOT)
                img_name = images.filename
                filename, file_extension = os.path.splitext(img_name)
                new_file_name = str(session['userid']) + str(file_extension)
                img = '/'.join([image_root +
                                "/Profile_Pictures", new_file_name])
                images.save(img)

                db.userProfilePicUploadDb(
                    str(session['userid']), new_file_name)

        return redirect(url_for('profile'))

    else:
        return redirect(url_for('index'))


# Function for return userProfilePictureRemove
def userProfilePictureRemove():

    if 'userid' in session:
        if db.removeUserProfilePic(session['userid']) < 1:
            return redirect(url_for('profile'))

        else:
            return redirect(url_for('profile'))

    else:
        return redirect(url_for('index'))


# Function for return userAccountChangePsw
def userAccountChangePsw():
    if 'userid' in session:
        if request.method == "POST":
            changePswEmail = request.form['changePswEmail']
            currentPsw = request.form['currentPsw']
            newPsw = request.form['newPsw']
            reNewPsw = request.form['reNewPsw']

            if len(changePswEmail) or len(currentPsw) or len(newPsw) or len(reNewPsw):
                return jsonify({'error_msg': "Fields are empty!"})

            # Validate email address
            if util.emailValidate(changePswEmail) == False:
                return jsonify({'error_msg': "Invalid email address"})

            # Validate psw length
            elif len(newPsw) < 8:
                return jsonify({'error_msg': "Your Password password weak"})

            # Validate psw and confirm psw
            elif newPsw != reNewPsw:
                return jsonify({'error_msg': "Password and confirm password not matched"})

            # Change password
            else:
                userId = db.userLogin(changePswEmail, currentPsw)
                if len(userId) == 0:
                    return jsonify({'error_msg': "Email or password invalid. Try again!"})

                else:

                    if db.changeUserAccountPsw(session['userid'], newPsw) < 1:
                        return jsonify({'error_msg': "Some error occur. Try again!"})

                    else:
                        session.pop('userid', None)
                        return jsonify({'redirect': url_for("sign_in")})

    else:
        return redirect(url_for('index'))


# Function for return detectDress
def detectDress():
    if request.method == "POST":
        uploaded_image = request.files.get('uploaded_image')

        if uploaded_image == None:
            return jsonify({'error_msg': "Image not Uploaded"})

        else:

            # Save image
            root = str(APP_ROOT) + '/classification_images/' + \
                util.datetime_picker() + util.random_number() + '/'

            image_root = root + 'images/'

            if not os.path.exists(image_root):
                os.makedirs(image_root)

            img_name = uploaded_image.filename
            uploaded_image.save(
                image_root + img_name)

            try:
                result = predictions.dress_detection_model_prediction(
                    APP_ROOT, root)
                result['REDIRECT'] = url_for(
                    'product', search=result['PREDICTED_CLASS'].lower())

                return jsonify({'result': result})

            except Exception as e:
                return jsonify({'error_msg': "Some error occur"})

    else:
        return jsonify({'error_msg': "Some error occur"})


# Function for return updateUserProfileDetails
def updateUserProfileDetails():
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        nic = request.form.get('nic')
        mobile_number = str(request.form.get('mobile'))

        if (len(fname) == 0 or len(lname) == 0 or len(nic) == 0 or len(mobile_number) == 0):
            return jsonify({'error_msg': "Fields are empty"})

        # # Validate 10 charaters nic number
        # if len(nic) == 10:
        #     nic_char = nic[-1].lower()
        #     nic_numbers = nic[0:-1]

        #     if nic_char not in ['v', 'x']:
        #         return jsonify({'error_msg': "NIC not valid"})
        #     elif util.RepresentsInt(nic_numbers) == False:
        #         return jsonify({'error_msg': "NIC not valid"})

        # # Validate nic number length 10 or 12
        # elif len(nic) not in [10, 12]:
        #     return jsonify({'error_msg': "NIC not valid"})

        # # Mobile number length validate
        # elif len(mobile_number) != 10:
        #     return jsonify({'error_msg': "Mobile number contains 10 numbers"})

        # # Mobile number validate only number
        # elif util.RepresentsInt(mobile_number) == False:
        #     return jsonify({'error_msg': "Mobile number only contains numbers"})

        elif db.updateUserProfileDetails(session['userid'], fname, lname, nic, mobile_number) < 1:

            return jsonify({'error_msg': "Some Error Occur. Try Again!"})

        else:
            return jsonify({'success_msg': "Profile details update successful!"})

    else:
        return jsonify({'error_msg': "Some error occur"})
