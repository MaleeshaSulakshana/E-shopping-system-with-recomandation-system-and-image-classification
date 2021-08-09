import os
import sys
import datetime
from flask import Flask, render_template, send_file, redirect, send_from_directory, jsonify, json, url_for, request, session

sys.path.append(os.path.abspath('python/'))
import db
import util

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# Function for return Admin
def Admin():
    if 'adminId' in session:
        date = util.date_picker()
        usersCount = db.getUsersCount()
        purchaseCount, purchaseDetails = db.getPurchasesDetailsAndCount(
            util.date_picker())
        adminDetails = db.getAdminData(session['adminId'])

        return render_template('Admin/index.html', adminName=adminDetails['First_name'] + " " + adminDetails['Last_name'],
                               date=date, usersCount=usersCount, purchaseCount=purchaseCount, purchaseDetails=purchaseDetails)

    else:
        return redirect(url_for('login'))


# Function for return admin login
def login():
    if 'adminId' in session:
        return render_template('Admin/index.html')

    else:
        return render_template('Admin/login.html')


# Function for return view_products
def view_products():
    if 'adminId' in session:

        adminDetails = db.getAdminData(session['adminId'])
        products = db.getExistProductsAndItems()
        return render_template('Admin/view_products.html',
                               adminName=adminDetails['First_name'] +
                               " " + adminDetails['Last_name'],
                               products=products)

    else:
        return redirect(url_for('login'))


# Function for return add_product
def add_product():
    if 'adminId' in session:

        product_categories = db.getProductCategories()
        select_sub_category = db.getProductSubCategories()
        adminDetails = db.getAdminData(session['adminId'])
        return render_template('Admin/add_product.html', adminName=adminDetails['First_name'] + " " + adminDetails['Last_name'],
                               product_categories=product_categories, select_sub_category=select_sub_category)

    else:
        return redirect(url_for('login'))


# Function for return add_imagesColorQty
def add_imagesColorQty():
    if 'adminId' in session:
        adminDetails = db.getAdminData(session['adminId'])
        product_codes = db.getProductCodes()
        product_colors = db.getProductColors()
        return render_template('Admin/add_imagesColorQty.html',
                               adminName=adminDetails['First_name'] +
                               " " + adminDetails['Last_name'],
                               product_codes=product_codes, product_colors=product_colors)

    else:
        return redirect(url_for('login'))


# Function for return add_product_sizes
def add_product_sizes():
    if 'adminId' in session:

        product_code = request.args.get('product_code', default=None)
        product_color = request.args.get('product_color', default=None)

        adminDetails = db.getAdminData(session['adminId'])
        product_codes = db.getProductCodes()
        product_colors = db.getProductColors()

        if product_code is None or product_color is None:

            return render_template('Admin/add_product_sizes.html',
                                   adminName=adminDetails['First_name'] +
                                   " " + adminDetails['Last_name'],
                                   product_codes=product_codes, product_colors=product_colors)

        else:
            return render_template('Admin/add_product_sizes.html',
                                   adminName=adminDetails['First_name'] +
                                   " " + adminDetails['Last_name'],
                                   product_item_code=product_code, product_item_color=product_color)

    else:
        return redirect(url_for('login'))


# Function for return update_product_qty
def update_product_qty():
    if 'adminId' in session:

        product_code = request.args.get('product_code', default=None)
        product_size = request.args.get('product_size', default=None)
        product_color = request.args.get('product_color', default=None)

        adminDetails = db.getAdminData(session['adminId'])
        product_codes = db.getProductCodes()
        product_colors = db.getProductColors()
        product_sizes = db.getProductSizes()

        if product_code is None or product_color is None or product_size is None:

            return render_template('Admin/update_product_qty.html',
                                   adminName=adminDetails['First_name'] +
                                   " " + adminDetails['Last_name'],
                                   product_codes=product_codes, product_colors=product_colors, product_sizes=product_sizes)

        else:
            return render_template('Admin/update_product_qty.html',
                                   adminName=adminDetails['First_name'] +
                                   " " + adminDetails['Last_name'],
                                   product_item_code=product_code, product_item_color=product_color, product_size=product_size)

    else:
        return redirect(url_for('login'))


# Function for return update_product_details
def update_product_details():
    if 'adminId' in session:
        product_code = request.args['product_code']

        adminDetails = db.getAdminData(session['adminId'])
        product_codes = db.getProductCodes()
        product_details = db.getProductDetails(product_code)
        return render_template('Admin/update_product_details.html',
                               adminName=adminDetails['First_name'] +
                               " " + adminDetails['Last_name'],
                               product_codes=product_codes, product_details=product_details)

    else:
        return redirect(url_for('login'))


# Function for return view_users_list
def view_users_list():
    if 'adminId' in session:

        adminDetails = db.getAdminData(session['adminId'])
        users = db.getUsersDetailsForView()
        return render_template('Admin/view_users_list.html',
                               adminName=adminDetails['First_name'] +
                               " " + adminDetails['Last_name'], users=users)
    else:
        return redirect(url_for('login'))


# Function return purchases
def purchases():
    if 'adminId' in session:

        adminDetails = db.getAdminData(session['adminId'])
        purchaseDetails = db.getPurchasesDetails()
        return render_template('Admin/purchases.html',
                               adminName=adminDetails['First_name'] +
                               " " + adminDetails['Last_name'], purchaseDetails=purchaseDetails)

    else:
        return redirect(url_for('login'))


# Function for return purchases_details
def purchases_details():
    if 'adminId' in session:

        adminDetails = db.getAdminData(session['adminId'])
        purchase_id = request.args.get('purchase_id', default=None)
        user_id = request.args.get('user_id', default=None)
        date = request.args.get('date', default=None)
        is_delivered = request.args.get('is_delivered', default=None)
        total = request.args.get('total', default=None)

        if purchase_id is None or user_id is None:
            return redirect(url_for('purchases'))

        else:
            purchaseDetails, userData = db.getPurchasesItemDetails(
                purchase_id, user_id)

        return render_template('Admin/purchases_details.html',
                               adminName=adminDetails['First_name'] +
                               " " + adminDetails['Last_name'], purchase_id=purchase_id,
                               userData=userData, purchaseDetails=purchaseDetails,
                               date=date, is_delivered=is_delivered, total=total)

    else:
        return redirect(url_for('login'))


# Function for return admin_profile
def admin_profile():
    if 'adminId' in session:
        adminDetails = db.getAdminData(session['adminId'])
        return render_template('Admin/admin_profile.html', adminName=adminDetails['First_name'] + " " + adminDetails['Last_name'],
                               adminDetails=adminDetails)

    else:
        return redirect(url_for('login'))


# Function for return admin_psw_change
def admin_psw_change():
    if 'adminId' in session:
        return render_template('Admin/admin_psw_change.html')

    else:
        return redirect(url_for('login'))


# Function for return adminAccountLogin
def adminAccountLogin():
    if request.method == "POST":
        txtAdminLoginUsername = request.form['txtAdminLoginUsername']
        txtAdminLoginPsw = request.form['txtAdminLoginPsw']

        # Validate email address
        if util.emailValidate(txtAdminLoginUsername) == False:
            return jsonify({'error_msg': "Invalid email address"})

        # Login
        else:
            adminDetails = db.adminLogin(
                txtAdminLoginUsername, txtAdminLoginPsw)
            if len(adminDetails) < 1:
                return jsonify({'error_msg': "Email or password invalid. Try again!"})

            else:
                session['adminId'] = adminDetails[0][0]
                return jsonify({'redirect': url_for("Admin")})

    else:
        return redirect(url_for('login'))


# Function for return adminAccountDetailsUpdate
def adminAccountDetailsUpdate():
    if 'adminId' in session:
        if request.method == "POST":
            txtAdminFirstName = request.form['txtAdminFirstName']
            txtAdminLastName = request.form['txtAdminLastName']

            if db.updateAdminAccountDetails(session['adminId'], txtAdminFirstName, txtAdminLastName) < 1:
                return jsonify({'error_msg': "Some Error Occur. Try Again!"})

            else:
                return jsonify({'redirect': url_for("admin_profile")})

        else:
            return redirect(url_for('admin_profile'))

    else:
        return redirect(url_for('login'))


# Function for return adminAccountPswChange
def adminAccountPswChange():
    if 'adminId' in session:
        if request.method == "POST":
            txtAdminChangePswEmail = request.form['txtAdminChangePswEmail']
            txtAdminChangePsw = request.form['txtAdminChangePsw']
            txtAdminChangeNewPsw = request.form['txtAdminChangeNewPsw']
            txtAdminChangeReNewPsw = request.form['txtAdminChangeReNewPsw']

            # Validate email address
            if util.emailValidate(txtAdminChangePswEmail) == False:
                return jsonify({'error_msg': "Invalid email address"})

            # Validate psw length
            elif len(txtAdminChangeNewPsw) < 8:
                return jsonify({'error_msg': "Your Password password weak"})

            # Validate psw and confirm psw
            elif txtAdminChangeNewPsw != txtAdminChangeReNewPsw:
                return jsonify({'error_msg': "Password and confirm password not matched"})

            # Re check authentication and update psw
            else:
                adminDetails = db.adminLogin(
                    txtAdminChangePswEmail, txtAdminChangePsw)
                if len(adminDetails) < 1:
                    return jsonify({'error_msg': "Email or password invalid. Try again!"})

                else:
                    if db.changeAdminAccountPsw(session['adminId'], txtAdminChangeNewPsw) < 1:
                        return jsonify({'error_msg': "Some Error Occur. Try Again!"})
                    else:
                        session.pop('adminId', None)
                        return jsonify({'redirect': url_for("login")})

        else:
            return redirect(url_for('admin_psw_change'))

    else:
        return redirect(url_for('login'))


# Function for return addNewProduct
def addNewProduct():
    if 'adminId' in session:
        if request.method == "POST":
            txtProductTitle = request.form['txtProductTitle']
            txtProductCode = request.form['txtProductCode']
            selectProductCategory = request.form['selectProductCategory']
            selectProductSubCategory = request.form['selectProductSubCategory']
            txtProductPrice = request.form['txtProductPrice']
            txtProductPriceDiscount = request.form['txtProductPriceDiscount']
            txtProductDescription = request.form['txtProductDescription']
            current_date = util.date_picker()

            if (len(txtProductTitle) == 0 or len(txtProductCode) == 0 or len(selectProductCategory) == 0 or
                    len(selectProductSubCategory) == 0 or len(txtProductPrice) == 0 or len(txtProductDescription) == 0):
                return jsonify({'error_msg': "Fields are empty"})

            # Validate price
            elif util.priceValidation(txtProductPrice) == False:
                return jsonify({'error_msg': "Price only containe numbers"})

            # Validate discount price
            elif len(txtProductPriceDiscount) != 0:
                if util.priceValidation(txtProductPriceDiscount) == False:
                    return jsonify({'error_msg': "Discount Price only containe numbers"})

            # Check product code is exist
            if db.checkProductIsExist(txtProductCode) != 0:
                return jsonify({'error_msg': txtProductCode + " ,This Product Code Exist. Try Again!"})

            elif db.addNewProduct(txtProductCode, txtProductTitle, selectProductCategory,
                                  selectProductSubCategory, txtProductPrice, txtProductPriceDiscount,
                                  txtProductDescription, current_date) < 1:

                return jsonify({'error_msg': "Some Error Occur. Try Again!"})

            else:
                return jsonify({'success_msg': "New Product Added Success!"})

        else:
            return redirect(url_for('admin_psw_change'))

    else:
        return redirect(url_for('login'))


# Function for return addNewProductDetails
def addNewProductDetails():
    if 'adminId' in session:
        if request.method == "POST":
            txtProductCode = request.form.get('txtProductCode')
            txtProductColor = request.form.get('txtProductColor')
            uploadProductImageOne = request.files.get('uploadProductImageOne')
            uploadProductImageTwo = request.files.get('uploadProductImageTwo')
            uploadProductImageThree = request.files.get(
                'uploadProductImageThree')
            uploadProductImageFour = request.files.get(
                'uploadProductImageFour')
            uploadProductImageFive = request.files.get(
                'uploadProductImageFive')

            if (len(txtProductCode) == 0 or len(txtProductColor) == 0 or uploadProductImageOne == None):
                return jsonify({'error_msg': "Fields are empty"})

            # Check product code is exist
            elif db.checkProductColorIsExist(txtProductCode, txtProductColor) > 0:
                return jsonify({'error_msg': txtProductCode + " ,This product with colour exist. Try Again!"})

            # Save product image 1
            image_root = util.get_images_root(APP_ROOT)
            img_name = uploadProductImageOne.filename
            filename, file_extension = os.path.splitext(img_name)
            image1_name = str(txtProductCode) + "_" + \
                str(txtProductColor) + "_1" + str(file_extension)
            uploadProductImageOne.save(
                image_root + "/product_images/" + image1_name)

            if uploadProductImageTwo != None:
                img_name = uploadProductImageTwo.filename
                filename, file_extension = os.path.splitext(img_name)
                image2_name = str(txtProductCode) + "_" + \
                    str(txtProductColor) + "_2" + str(file_extension)
                uploadProductImageTwo.save(
                    image_root + "/product_images/" + image2_name)

            else:
                image2_name = None

            if uploadProductImageThree != None:
                img_name = uploadProductImageThree.filename
                filename, file_extension = os.path.splitext(img_name)
                image3_name = str(txtProductCode) + "_" + \
                    str(txtProductColor) + "_3" + str(file_extension)
                uploadProductImageThree.save(
                    image_root + "/product_images/" + image3_name)

            else:
                image3_name = None

            if uploadProductImageFour != None:
                img_name = uploadProductImageFour.filename
                filename, file_extension = os.path.splitext(img_name)
                image4_name = str(txtProductCode) + "_" + \
                    str(txtProductColor) + "_4" + str(file_extension)
                uploadProductImageFour.save(
                    image_root + "/product_images/" + image4_name)

            else:
                image4_name = None

            if uploadProductImageFive != None:
                img_name = uploadProductImageFive.filename
                filename, file_extension = os.path.splitext(img_name)
                image5_name = str(txtProductCode) + "_" + \
                    str(txtProductColor) + "_5" + str(file_extension)
                uploadProductImageFive.save(
                    image_root + "/product_images/" + image5_name)

            else:
                image5_name = None

            if db.addNewProductImagesWithDetails(txtProductCode, txtProductColor,
                                                 image1_name, image2_name, image3_name, image4_name, image5_name) < 1:

                return jsonify({'error_msg': "Some Error Occur. Try Again!"})

            else:
                return jsonify({'success_msg': "Product details added successful!"})

        else:
            return redirect(url_for('add_imagesColorQty'))

    else:
        return redirect(url_for('login'))


# Function for return addNewProductSize
def addNewProductSize():
    if 'adminId' in session:
        if request.method == "POST":
            txt_product_code = request.form.get('txt_product_code')
            txt_product_color = request.form.get('txt_product_color')
            txt_product_size = request.form.get('txt_product_size')
            txt_qty = request.form.get('txt_qty')

            if (len(txt_product_code) == 0 or len(txt_product_color) == 0 or len(txt_product_size) == 0 or len(txt_qty) == 0):
                return jsonify({'error_msg': "Fields are empty"})

            # Check product code is exist
            elif db.checkProductColorIsExist(txt_product_code, txt_product_color) < 1:
                return jsonify({'error_msg': txt_product_code + " ,This product with colour exist. Try Again!"})

            txt_product_size = str(txt_product_size).upper()
            if db.addNewProductSizeDetails(txt_product_code, txt_product_color,
                                           txt_product_size, txt_qty) < 1:

                return jsonify({'error_msg': "Some Error Occur. Try Again!"})

            else:
                return jsonify({'success_msg': "Product details added successful!"})

        else:
            return redirect(url_for('add_product_sizes'))

    else:
        return redirect(url_for('login'))


# Function for return updateProductQty
def updateProductQty():
    if 'adminId' in session:
        if request.method == "POST":
            txt_product_code = request.form.get('txt_product_code')
            txt_product_color = request.form.get('txt_product_color')
            txt_product_size = request.form.get('txt_product_size')
            txt_new_qty = request.form.get('txt_new_qty')
            checkQty = request.form.get('checkQty')

            if (len(txt_product_code) == 0 or len(txt_product_color) == 0 or len(txt_product_size) == 0
                    or len(txt_new_qty) == 0 or len(checkQty) == 0):
                return jsonify({'error_msg': "Fields are empty"})

            # Check product code is exist
            elif db.checkProductColorIsExist(txt_product_code, txt_product_color) < 1:
                return jsonify({'error_msg': txt_product_code + " and " + txt_product_color +
                                " ,This product with colour not exist. Try Again!"})

            if checkQty == 'decrease':
                if db.getProductQty(txt_product_code, txt_product_color, txt_product_size) < int(txt_new_qty):
                    return jsonify({'error_msg': "Cannot decrease product qty. Qty less than you value. Try Again!"})

            if db.updateProductQtyDetails(txt_product_code, txt_product_color, txt_product_size, txt_new_qty, checkQty) < 1:

                return jsonify({'error_msg': "Some Error Occur. Try Again!"})

            else:
                return jsonify({'success_msg': "Product qty update successful!"})

        else:
            return redirect(url_for('update_product_qty'))

    else:
        return redirect(url_for('login'))


# Function for return updateProductQty
def updatePurchaseDelivery():
    if 'adminId' in session:
        if request.method == "POST":
            purchaseCode = str(request.form.get('purchaseCode')
                               ).replace('Purchases ID : ', "")

            if db.updatePurchaseDelevery(purchaseCode) < 1:

                return jsonify({'error_msg': "Some Error Occur. Try Again!"})

        return jsonify({'redirect': url_for('purchases')})

    else:
        return redirect(url_for('login'))


# Function for return updateProductQty
def updateProductDetails():
    if 'adminId' in session:
        if request.method == "POST":
            txtProductTitle = request.form.get('txtProductTitle')
            txtProductCode = request.form.get('txtProductCode')
            selectProductCategory = request.form.get('selectProductCategory')
            selectProductSubCategory = request.form.get(
                'selectProductSubCategory')
            txtProductPrice = request.form.get('txtProductPrice')
            txtProductPriceDiscount = request.form.get(
                'txtProductPriceDiscount')
            txtProductDescription = request.form.get('txtProductDescription')

            if (len(txtProductTitle) == 0 or len(txtProductCode) == 0 or len(selectProductCategory) == 0
                    or len(selectProductSubCategory) == 0 or len(txtProductPrice) == 0):
                return jsonify({'error_msg': "Fields are empty"})

            # Validate price
            elif util.priceValidation(txtProductPrice) == False:
                return jsonify({'error_msg': "Price only containe numbers"})

            # Validate discount price
            elif len(txtProductPriceDiscount) != 0:
                if util.priceValidation(txtProductPriceDiscount) == False:
                    return jsonify({'error_msg': "Discount Price only containe numbers"})

            # Check product code is exist
            if db.checkProductIsExist(txtProductCode) < 1:
                return jsonify({'error_msg': txtProductCode + " ,This Product Code Not Exist. Try Again!"})

            elif db.updateProductDetails(txtProductTitle, txtProductCode, selectProductCategory, selectProductSubCategory,
                                         txtProductPrice, txtProductPriceDiscount, txtProductDescription) < 1:

                return jsonify({'error_msg': "Some Error Occur. Try Again!"})

            else:
                return jsonify({'success_msg': "Product details update successful!"})

        else:
            return redirect(url_for('update_product_details'))

    else:
        return redirect(url_for('login'))


# Function for return admin chart details
def adminChartDetails():
    if request.method == "POST":
        week_details = db.selectWeekPurchasesData()
        month_details = db.selectMonthPurchasesData()

        days = []
        day_values = []
        for i in week_details:
            d = str(i[0])
            days.append(d.split('-')[-1])
            day_values.append(int(i[1]))

        week = [days, day_values]

        month_tuple = []
        for m in month_details:
            month = str(m[0]).split('-')
            month_tuple.append(
                [str(month[0] + ',' + month[1]), month[1], m[1]])

        values = set(map(lambda x: x[1], month_tuple))
        newlist = [[[y[2], y[1], y[0]] for y in month_tuple if y[1] == x]
                   for x in values]

        months = []
        month_values = []
        for c, val in enumerate(newlist):
            if c < 12:
                months.append(datetime.date(
                    1900, int(val[0][1]), 1).strftime('%B'))
                month_values.append(sum([float(i[0]) for i in val]))
            else:
                break

        month = [months, month_values]
        return jsonify({'week': week, 'month': month})
