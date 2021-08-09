import mysql.connector


# Function for create connetion with db
def db_connector():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="e_Shopping"
    )

    return conn


# Function for check email id exist for create account
def check_email_is_exist(email):
    conn = db_connector()

    select = ''' SELECT COUNT(email) FROM users WHERE email = %s '''
    value = (str(email),)
    cur = conn.cursor()
    cur.execute(select, value)

    usersCount = cur.fetchall()[0][0]
    return usersCount


def userCreateAccount(user_id, first_name, last_name, email, nic, mobile_number, psw):
    conn = db_connector()

    insert_data = ''' INSERT INTO users (user_id, first_name, last_name, email, nic, mobile_number, psw) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s) '''
    values = (str(user_id), str(first_name), str(last_name),
              str(email), str(nic), int(mobile_number), str(psw))
    cur = conn.cursor()
    cur.execute(insert_data, values)

    conn.commit()
    return cur.rowcount


def userLogin(email, psw):
    conn = db_connector()

    select = ''' SELECT user_id FROM users WHERE email = %s AND psw = %s '''
    values = (str(email), str(psw))
    cur = conn.cursor()
    cur.execute(select, values)

    userId = cur.fetchall()
    return userId


def getUserData(user_id):
    conn = db_connector()

    selectUserData = ''' SELECT first_name, last_name, email, nic, mobile_number, profile_pic 
                        FROM users WHERE user_id = %s '''
    values = (str(user_id),)
    cur = conn.cursor()
    cur.execute(selectUserData, values)

    userData = cur.fetchall()[0]

    userDataDict = {
        "First_name": userData[0],
        "Last_name": userData[1],
        "Email": userData[2],
        "NIC": userData[3],
        "Mobile": userData[4],
    }

    profile_pic = userData[5]

    return userDataDict, profile_pic


def userProfilePicUploadDb(user_id, Profile_Pictures):
    conn = db_connector()

    update_profile_picture = ''' UPDATE users SET profile_pic = %s WHERE user_id = %s '''

    values = (str(Profile_Pictures), str(user_id))
    cur = conn.cursor()
    cur.execute(update_profile_picture, values)

    conn.commit()
    # return cur.rowcount


def removeUserProfilePic(user_id):
    conn = db_connector()

    remove_profile_picture = ''' UPDATE users SET profile_pic = null WHERE user_id = %s '''

    values = (str(user_id),)
    cur = conn.cursor()
    cur.execute(remove_profile_picture, values)

    conn.commit()
    return cur.rowcount


def changeUserAccountPsw(user_id, newPsw):
    conn = db_connector()

    changePsw = ''' UPDATE users SET psw = %s WHERE user_id = %s '''

    values = (str(newPsw), str(user_id))
    cur = conn.cursor()
    cur.execute(changePsw, values)

    conn.commit()
    return cur.rowcount


##### Admin #####

# Function for admin login
def adminLogin(email, psw):
    conn = db_connector()

    select = ''' SELECT id, first_name, last_name FROM admin WHERE email = %s AND psw = %s '''
    values = (str(email), str(psw))
    cur = conn.cursor()
    cur.execute(select, values)

    adminDetails = cur.fetchall()
    return adminDetails


# Function for get users count
def getUsersCount():
    conn = db_connector()

    select = ''' SELECT COUNT(user_id) FROM users'''
    cur = conn.cursor()
    cur.execute(select)

    usersCount = cur.fetchall()[0][0]
    return usersCount


# Function for get purchase count
def getPurchasesDetailsAndCount(date):
    conn = db_connector()

    select = ''' SELECT purchase_id, users.user_id, CONCAT(users.first_name ,' ', users.last_name), 
                        COUNT(product_code), SUM(qty), SUM(price), purchase_date, delivered 
                    FROM purches INNER JOIN users ON users.user_id = purches.user_id 
                        WHERE purches.purchase_date = %s  GROUP BY purches.purchase_id '''

    value = (str(date),)
    cur = conn.cursor()
    cur.execute(select, value)

    purchaseDetails = cur.fetchall()

    select_count = ''' SELECT COUNT(DISTINCT(purchase_id)) FROM purches '''
    cur = conn.cursor()
    cur.execute(select_count)

    purchaseCount = cur.fetchall()[0][0]

    return purchaseCount, purchaseDetails


# Function for get purchase details
def getPurchasesDetails():
    conn = db_connector()

    select = ''' SELECT purchase_id, users.user_id, CONCAT(users.first_name ,' ', users.last_name), 
                        COUNT(product_code), SUM(qty), SUM(price), purchase_date, delivered 
                    FROM purches INNER JOIN users ON users.user_id = purches.user_id 
                        GROUP BY purches.purchase_id
                        ORDER BY purches.purchase_date '''

    cur = conn.cursor()
    cur.execute(select)

    purchaseDetails = cur.fetchall()
    return purchaseDetails


# Function for get purchase item details
def getPurchasesItemDetails(purchase_id, user_id):
    conn = db_connector()

    select = ''' SELECT purches.product_code, products.product_title, purches.product_colour, 
        purches.product_size, purches.qty, purches.price FROM purches 
        	INNER JOIN products ON products.product_code = purches.product_code
            	WHERE purches.purchase_id = %s '''

    value = (str(purchase_id),)
    cur = conn.cursor()
    cur.execute(select, value)
    purchaseDetails = cur.fetchall()

    select_user_data = ''' SELECT user_id, CONCAT( first_name,' ',last_name), mobile_number, email  
                                    FROM users WHERE user_id = %s '''

    value = (str(user_id),)
    cur = conn.cursor()
    cur.execute(select_user_data, value)
    userData = cur.fetchall()[0]

    return purchaseDetails, userData


# Function for get admin details
def getAdminData(adminId):
    conn = db_connector()

    selectAdminData = ''' SELECT first_name, last_name, email FROM admin WHERE id = %s '''
    values = (str(adminId),)
    cur = conn.cursor()
    cur.execute(selectAdminData, values)

    adminData = cur.fetchall()[0]

    adminDataDict = {
        "First_name": adminData[0],
        "Last_name": adminData[1],
        "Email": adminData[2],
    }

    return adminDataDict


# Function for update admin account details
def updateAdminAccountDetails(adminId, first_name, last_name):
    conn = db_connector()

    updateDetails = ''' UPDATE admin SET first_name = %s, last_name = %s WHERE id = %s '''

    values = (str(first_name), str(last_name), str(adminId))
    cur = conn.cursor()
    cur.execute(updateDetails, values)

    conn.commit()
    return cur.rowcount


# Function for update admin psw
def changeAdminAccountPsw(adminId, newPsw):
    conn = db_connector()

    chanegPsw = ''' UPDATE admin SET psw = %s WHERE id = %s '''

    values = (str(newPsw), str(adminId))
    cur = conn.cursor()
    cur.execute(chanegPsw, values)

    conn.commit()
    return cur.rowcount


# Function for check product is exist
def checkProductIsExist(product_code):
    conn = db_connector()

    select_product_count = ''' SELECT COUNT(product_code) FROM products WHERE product_code = %s '''
    values = (str(product_code),)

    cur = conn.cursor()
    cur.execute(select_product_count, values)

    product_count = cur.fetchall()[0][0]

    return product_count


# Function for add new product
def addNewProduct(product_code, product_title, product_category, product_sub_category, price, discount, description, current_date):
    conn = db_connector()

    insert_data = ''' INSERT INTO products 
            (product_code, product_title, product_category, product_sub_category, price, discount, description, added_date)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '''
    values = (str(product_code), str(product_title), str(product_category),
              str(product_sub_category), str(price), str(discount), str(description), str(current_date))

    cur = conn.cursor()
    cur.execute(insert_data, values)

    conn.commit()
    return cur.rowcount


# Function for get categories
def getProductCategories():
    conn = db_connector()

    select_category = ''' SELECT DISTINCT(product_category) FROM products '''

    cur = conn.cursor()
    cur.execute(select_category)

    product_categories = cur.fetchall()
    return product_categories


# Function for get sub categories
def getProductSubCategories():
    conn = db_connector()

    select_sub_category = ''' SELECT DISTINCT(product_sub_category) FROM products '''

    cur = conn.cursor()
    cur.execute(select_sub_category)

    product_sub_categories = cur.fetchall()
    return product_sub_categories


# Function for get product codes
def getProductCodes():
    conn = db_connector()

    select_product_codes = ''' SELECT DISTINCT(product_code) FROM products '''

    cur = conn.cursor()
    cur.execute(select_product_codes)

    product_codes = cur.fetchall()
    return product_codes


# Function for get product colours
def getProductColors():
    conn = db_connector()

    select_product_colors = ''' SELECT DISTINCT(product_colour) FROM product_details '''

    cur = conn.cursor()
    cur.execute(select_product_colors)

    product_colors = cur.fetchall()
    return product_colors


# Function for get product sizes
def getProductSizes():
    conn = db_connector()

    select_product_sizes = ''' SELECT DISTINCT(product_size) FROM product_sizes '''

    cur = conn.cursor()
    cur.execute(select_product_sizes)

    product_sizes = cur.fetchall()
    return product_sizes


# Function for get exist products and items
def getExistProductsAndItems():
    conn = db_connector()

    select_products = ''' SELECT products.product_code, products.product_title, product_details.product_colour, 
	product_sizes.product_size, product_sizes.product_qty, products.price, products.discount, products.added_date 
		FROM products INNER JOIN product_details ON products.product_code = product_details.product_code
        INNER JOIN product_sizes ON product_sizes.product_code = products.product_code AND 
        product_sizes.product_colour = product_details.product_colour
			 ORDER BY products.product_code '''

    cur = conn.cursor()
    cur.execute(select_products)

    products = cur.fetchall()
    return products


# Function for get exist products and items
def getUsersDetailsForView():
    conn = db_connector()

    select_users = ''' SELECT user_id, email, first_name, last_name, nic, mobile_number 
                                    FROM users ORDER BY user_id '''

    cur = conn.cursor()
    cur.execute(select_users)

    users = cur.fetchall()
    return users


# Function for check product is exist
def checkProductColorIsExist(product_code, color):
    conn = db_connector()

    select_product_count = ''' SELECT COUNT(*) FROM product_details WHERE product_code = %s AND product_colour = %s '''
    values = (str(product_code), str(color))

    cur = conn.cursor()
    cur.execute(select_product_count, values)

    product_count = cur.fetchall()[0][0]

    return product_count


# Function for get selected product details
def getProductDetails(product_code):
    conn = db_connector()

    select_product_details = ''' SELECT * FROM products WHERE product_code = %s '''

    value = (str(product_code),)
    cur = conn.cursor()
    cur.execute(select_product_details, value)

    products = cur.fetchall()[0]
    return products


# Function for add new product details with images, color, qty
def addNewProductImagesWithDetails(product_code, product_colour, image_1, image_2, image_3, image_4, image_5):
    conn = db_connector()

    insert_data = ''' INSERT INTO product_details 
            (product_code, product_colour, image_1, image_2, image_3, image_4, image_5)
         VALUES (%s, %s, %s, %s, %s, %s, %s) '''
    values = (str(product_code), str(product_colour),
              str(image_1), str(image_2), str(image_3), str(image_4), str(image_5))

    cur = conn.cursor()
    cur.execute(insert_data, values)

    conn.commit()
    return cur.rowcount


# Function for add new product details with images, color, qty
def addNewProductSizeDetails(product_code, product_colour, product_size, qty):
    conn = db_connector()

    insert_data = ''' INSERT INTO product_sizes 
            (product_code, product_colour, product_size, product_qty)
         VALUES (%s, %s, %s, %s) '''
    values = (str(product_code), str(product_colour),
              str(product_size), int(qty))

    cur = conn.cursor()
    cur.execute(insert_data, values)

    conn.commit()
    return cur.rowcount


# Function get product qty
def getProductQty(product_code, product_colour, product_size):
    conn = db_connector()

    select_qty = ''' SELECT product_qty FROM product_sizes WHERE product_code = %s 
                            AND product_colour = %s AND product_size = %s '''

    values = (product_code, product_colour, product_size)
    cur = conn.cursor()
    cur.execute(select_qty, values)

    product_qty = cur.fetchall()[0][0]
    return product_qty


# Function for update product qty
def updateProductQtyDetails(product_code, product_colour, product_size, qty, method):
    conn = db_connector()

    if method == "increase":
        qty_update = ''' UPDATE product_sizes 
                            SET product_qty = product_qty + %s
                            WHERE product_code = %s AND product_colour = %s AND product_size = %s '''

    else:
        qty_update = ''' UPDATE product_sizes 
                            SET product_qty = product_qty - %s
                            WHERE product_code = %s AND product_colour = %s AND product_size = %s '''

    values = (int(qty), str(product_code), str(
        product_colour), str(product_size))

    cur = conn.cursor()
    cur.execute(qty_update, values)

    conn.commit()
    return cur.rowcount


# Function for get selected product details
def getProductViewDetails():
    conn = db_connector()

    select_product_details = ''' SELECT products.product_code, products.product_title, products.product_category, products.price, 
                                    products.discount, product_details.image_1 
                                    FROM products INNER JOIN product_details 
                                        ON products.product_code = product_details.product_code 
                                        INNER JOIN product_sizes ON products.product_code = 				 
                                        product_sizes.product_code
                                        WHERE product_sizes.product_qty > 0
                                        GROUP BY product_code ORDER BY products.added_date '''

    cur = conn.cursor()
    cur.execute(select_product_details)
    products = cur.fetchall()

    select_product_categories = ''' SELECT DISTINCT(products.product_category)
                                    FROM products INNER JOIN product_details 
                                        ON products.product_code = product_details.product_code 
                                        INNER JOIN product_sizes 
                                        ON products.product_code = product_sizes.product_code 
                                        WHERE product_sizes.product_qty > 0
                                        GROUP BY products.product_category ORDER BY products.product_category '''

    cur = conn.cursor()
    cur.execute(select_product_categories)
    categories = cur.fetchall()

    return products, categories


# Function for get selected product details
def getProductItemsDetails(ids=None):
    conn = db_connector()
    categories = []
    if ids != None:
        ids.append("")
        select_product_categories = ''' SELECT DISTINCT(products.product_category)
                                        FROM products INNER JOIN product_details 
                                            ON products.product_code = product_details.product_code 
                                            INNER JOIN product_sizes 
                                            ON products.product_code = product_sizes.product_code 
                                            WHERE product_sizes.product_qty > 0
                                            AND products.product_code NOT IN {}
                                            GROUP BY products.product_category ORDER BY products.product_category '''.format(tuple(ids))

    else:
        select_product_categories = ''' SELECT DISTINCT(products.product_category)
                                        FROM products INNER JOIN product_details 
                                            ON products.product_code = product_details.product_code 
                                            INNER JOIN product_sizes 
                                            ON products.product_code = product_sizes.product_code 
                                            WHERE product_sizes.product_qty > 0
                                            AND products.product_code
                                            GROUP BY products.product_category ORDER BY products.product_category '''

    cur = conn.cursor()
    cur.execute(select_product_categories)
    categories = cur.fetchall()

    all_products = []
    for category in categories:
        if ids != None:
            select_product_details = ''' SELECT products.product_code, products.product_title, products.product_category, products.price, 
                                            products.discount, product_details.image_1 
                                            FROM products INNER JOIN product_details 
                                                ON products.product_code = product_details.product_code 
                                                INNER JOIN product_sizes ON products.product_code = 				 
                                                product_sizes.product_code
                                                WHERE product_sizes.product_qty > 0 AND products.product_category = %s
                                                AND products.product_code NOT IN {}
                                                GROUP BY product_code ORDER BY products.added_date LIMIT 8 '''.format(tuple(ids))

        else:
            select_product_details = ''' SELECT products.product_code, products.product_title, products.product_category, products.price, 
                                            products.discount, product_details.image_1 
                                            FROM products INNER JOIN product_details 
                                                ON products.product_code = product_details.product_code 
                                                INNER JOIN product_sizes ON products.product_code = 				 
                                                product_sizes.product_code
                                                WHERE product_sizes.product_qty > 0 AND products.product_category = %s
                                                GROUP BY product_code ORDER BY products.added_date LIMIT 8 '''

        cur = conn.cursor()
        cur.execute(select_product_details, (str(category[0]),))
        products = cur.fetchall()

        for item in products:
            all_products.append(item)

    return all_products, categories


# Function for get selected product details
def getSearchProductDetails(search):
    search = '%' + str(search) + '%'
    conn = db_connector()

    select_product_details = ''' SELECT products.product_code, products.product_title, products.product_category, products.price, 
                                    products.discount, product_details.image_1 
                                    FROM products INNER JOIN product_details 
                                        ON products.product_code = product_details.product_code 
                                        INNER JOIN product_sizes ON products.product_code = 				 
                                        product_sizes.product_code
                                        WHERE product_sizes.product_qty > 0 
                                        AND (products.product_title LIKE %s or products.product_category LIKE %s
                                             or products.product_sub_category LIKE %s)
                                        GROUP BY product_code ORDER BY products.added_date '''

    values = (str(search), str(search), str(search))
    cur = conn.cursor()
    cur.execute(select_product_details, values)
    products = cur.fetchall()

    return products


# Function for get selected product item details
def getProductItemDetails(product_code, product_color=None):
    conn = db_connector()

    # Get colours
    get_colors = ''' SELECT DISTINCT(product_colour) 
                        FROM product_sizes WHERE product_code = %s AND product_qty > 0 '''

    value = (str(product_code),)
    cur = conn.cursor()
    cur.execute(get_colors, value)
    colors = cur.fetchall()

    # Get sizes
    get_sizes = ''' SELECT DISTINCT(product_size) 
                        FROM product_sizes WHERE product_code = %s 
                            AND product_colour = %s AND product_qty > 0 '''

    if product_color == None:
        values = (str(product_code), str(colors[0][0]))
    else:
        values = (str(product_code), str(product_color))

    cur = conn.cursor()
    cur.execute(get_sizes, values)
    sizes = cur.fetchall()

    # Get details
    get_details = ''' SELECT products.product_code, products.product_title, products.product_category,
                        product_details.product_colour, products.price, products.discount, products.description,
                        product_details.image_1, product_details.image_2, product_details.image_3,
                        product_details.image_4, product_details.image_5
                        FROM products INNER JOIN product_details
                        ON products.product_code = product_details.product_code
                            WHERE products.product_code = %s AND product_details.product_colour = %s '''

    cur = conn.cursor()
    cur.execute(get_details, values)
    details = cur.fetchall()[0]

    # Get related products
    get_related_products = ''' SELECT products.product_code, products.product_title, products.product_category, products.price, 
                                    products.discount, product_details.image_1 
                                    FROM products INNER JOIN product_details 
                                        ON products.product_code = product_details.product_code 
                                        INNER JOIN product_sizes ON products.product_code = 				 
                                        product_sizes.product_code
                                        WHERE product_sizes.product_qty > 0 
                                        AND (products.product_category in (SELECT DISTINCT(products.product_category)
                                                FROM products INNER JOIN product_details
                                                ON products.product_code = product_details.product_code
                                                    WHERE products.product_code = %s)
                                        OR products.product_sub_category in (SELECT DISTINCT(products.product_sub_category)
                                                FROM products INNER JOIN product_details
                                                ON products.product_code = product_details.product_code
                                                    WHERE products.product_code = %s))
                                        GROUP BY product_code ORDER BY products.added_date
                                        LIMIT 8 '''

    values = (str(product_code), str(product_code))
    cur = conn.cursor()
    cur.execute(get_related_products, values)
    related_products = cur.fetchall()

    return colors, sizes, details, related_products


# Function for get selected product details
def getCartDetails(product_code, product_color):
    conn = db_connector()

    cart_details = ''' SELECT products.product_title, products.price, products.discount, product_details.image_1 FROM products INNER JOIN product_details 
                            ON product_details.product_code = products.product_code 
                                WHERE products.product_code = %s AND product_details.product_colour = %s '''

    values = (str(product_code), str(product_color))
    cur = conn.cursor()
    cur.execute(cart_details, values)
    details = cur.fetchall()[0]

    return details


# Function for add to wishlist
def addToWishlist(user_id, product_code):
    conn = db_connector()

    insert_data = ''' INSERT INTO wishlist 
            (user_id, product_code)
         VALUES (%s, %s) '''
    values = (str(user_id), str(product_code))

    cur = conn.cursor()
    cur.execute(insert_data, values)

    conn.commit()
    return cur.rowcount


# Function for remove from wishlist
def removeFromWishlist(user_id, product_code):
    conn = db_connector()

    remove_data = ''' DELETE FROM wishlist WHERE user_id = %s AND product_code = %s '''
    values = (str(user_id), str(product_code))

    cur = conn.cursor()
    cur.execute(remove_data, values)

    conn.commit()
    return cur.rowcount


# Function for check wishlist
def checkItemExistInWishlist(user_id, product_code):
    conn = db_connector()

    select_data = ''' SELECT COUNT(*) FROM wishlist WHERE user_id = %s AND product_code = %s '''
    values = (str(user_id), str(product_code))

    cur = conn.cursor()
    cur.execute(select_data, values)

    count = cur.fetchall()[0][0]
    return count


# Function for get wishlist data
def getWishlistData(user_id):
    conn = db_connector()

    select_data = ''' SELECT products.product_code, products.product_title, product_details.image_1, 
                        products.price, products.discount FROM products INNER JOIN product_details 
                        ON product_details.product_code = products.product_code
                        INNER JOIN product_sizes ON products.product_code = product_sizes.product_code
                        INNER JOIN wishlist ON wishlist.product_code = products.product_code
                        AND product_sizes.product_qty > 0 AND wishlist.user_id = %s GROUP BY products.product_code '''
    values = (str(user_id),)

    cur = conn.cursor()
    cur.execute(select_data, values)

    data = cur.fetchall()
    return data


# Function for clear wishlist
def clearWishlist(user_id):
    conn = db_connector()

    remove_data = ''' DELETE FROM wishlist WHERE user_id = %s '''
    values = (str(user_id),)

    cur = conn.cursor()
    cur.execute(remove_data, values)

    conn.commit()
    return cur.rowcount


# Function for get items count
def checkProductCountExist(product_code, product_colour, product_size):
    conn = db_connector()

    select_data = ''' SELECT product_qty FROM product_sizes
                        WHERE product_code = %s AND product_colour = %s AND product_size = %s '''
    values = (str(product_code), str(product_colour),
              str(product_size))

    cur = conn.cursor()
    cur.execute(select_data, values)

    data = cur.fetchall()[0][0]
    return data


# Function for decrease items count
def addToPurchase(purchase_id, user_id, product_code, product_colour, product_size, product_count, date):
    conn = db_connector()

    update_data = ''' UPDATE product_sizes SET product_qty = product_qty - %s WHERE
                         product_code = %s AND product_colour = %s AND product_size = %s '''
    values = (str(product_count), str(product_code), str(product_colour),
              str(product_size))

    cur = conn.cursor()
    cur.execute(update_data, values)

    conn.commit()

    get_data = ''' SELECT product_title, price, discount FROM products WHERE product_code =  %s '''
    values = (str(product_code), )

    cur = conn.cursor()
    cur.execute(get_data, values)
    data = cur.fetchall()[0]

    if data[2] == '':
        discount = 0
    else:
        discount = float(data[2])

    price = float(data[1]) - discount

    insert_data = ''' INSERT INTO purches 
            (purchase_id, user_id, product_code, product_colour, product_size, qty, price, purchase_date, delivered)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'no') '''
    values = (str(purchase_id), str(user_id), str(product_code), str(product_colour),
              str(product_size), str(product_count), str(price), str(date))

    cur = conn.cursor()
    cur.execute(insert_data, values)

    conn.commit()


# Function for get purchase
def getPurchaseDataForUser(user_id):
    conn = db_connector()

    select_data = ''' SELECT purchase_id, COUNT(product_code), SUM(qty), SUM(price), purchase_date, delivered 
            FROM purches WHERE user_id = %s GROUP BY purchase_id ORDER BY purchase_date'''
    value = (str(user_id),)

    cur = conn.cursor()
    cur.execute(select_data, value)

    data = cur.fetchall()
    return data


# Function for add to wishlist
def insertSearched(user_id, product_code, date):
    conn = db_connector()
    values = (str(user_id), str(product_code), str(date))

    select = ''' SELECT COUNT(*) FROM searched WHERE user_id = %s AND product_code = %s AND searched_date = %s '''
    cur = conn.cursor()
    cur.execute(select, values)

    if cur.fetchall()[0][0] < 1:

        insert_data = ''' INSERT INTO searched 
                (user_id, product_code, searched_date)
            VALUES (%s, %s, %s)  '''

        cur = conn.cursor()
        cur.execute(insert_data, values)

        conn.commit()


# Get previous viewed history
def searched_history(userid, date):
    conn = db_connector()

    select = ''' SELECT searched_date FROM searched WHERE user_id = %s AND searched_date != %s ORDER BY searched_date DESC LIMIT 1 '''
    values = (str(userid), str(date))

    cur = conn.cursor()
    cur.execute(select, values)

    date = cur.fetchall()

    if len(date) > 0:
        select = ''' SELECT products.product_category, products.product_sub_category, 
                        COUNT(products.product_sub_category) as c FROM searched
                        INNER JOIN products ON products.product_code = searched.product_code
                        WHERE searched.user_id = %s AND searched.searched_date = %s
                        GROUP BY products.product_sub_category ORDER BY c LIMIT 10 '''
        values = (str(userid), str(date[0][0]))

        cur = conn.cursor()
        cur.execute(select, values)

        searched_data = cur.fetchall()
        return searched_data

    return 'none'


# Get recommended items details
def get_recommended_items_details(category, sub_category):
    conn = db_connector()

    select = ''' SELECT products.product_code, products.product_title, products.product_category, products.price, 
                    products.discount, product_details.image_1 
                    FROM products INNER JOIN product_details 
                        ON products.product_code = product_details.product_code 
                        INNER JOIN product_sizes ON products.product_code = 				 
                        product_sizes.product_code
                        WHERE product_sizes.product_qty > 0
                        AND products.product_category = %s
                        AND products.product_sub_category = %s
                        GROUP BY product_code ORDER BY products.added_date LIMIT 10 '''
    values = (str(category), str(sub_category))

    cur = conn.cursor()
    cur.execute(select, values)

    data = cur.fetchall()
    return data


# Function for update delivery details
def updatePurchaseDelevery(purchaseCode):
    conn = db_connector()

    qty_purchase = """ UPDATE purches 
                        SET delivered = 'yes'
                        WHERE purchase_id = %s """

    values = (str(purchaseCode),)

    cur = conn.cursor()
    cur.execute(qty_purchase, values)

    conn.commit()
    return cur.rowcount


# Function for update product details
def updateProductDetails(product_title, product_code, product_category, product_sub_category, price,
                         discount, description):

    conn = db_connector()

    update_data = ''' UPDATE products SET
            product_title = %s, product_category = %s, 
                product_sub_category = %s, price = %s, discount = %s, description = %s
                    WHERE product_code = %s '''
    values = (str(product_title), str(product_category),
              str(product_sub_category), str(price), str(discount), str(description), str(product_code))

    cur = conn.cursor()
    cur.execute(update_data, values)

    conn.commit()
    return cur.rowcount


# Function for week purchase details
def selectWeekPurchasesData():
    conn = db_connector()

    select = """ SELECT purchase_date, SUM(price) FROM purches GROUP BY purchase_date ORDER BY purchase_date DESC LIMIT 7 """

    cur = conn.cursor()
    cur.execute(select)

    data = cur.fetchall()
    return data


# Function for month purchase details
def selectMonthPurchasesData():
    conn = db_connector()

    select = """ SELECT purchase_date, SUM(price) FROM purches GROUP BY purchase_date ORDER BY purchase_date DESC """

    cur = conn.cursor()
    cur.execute(select)

    data = cur.fetchall()
    return data


# Function for update user profile details
def updateUserProfileDetails(userid, fname, lname, nic, mobile_number):
    conn = db_connector()

    update_data = ''' UPDATE users SET first_name = %s, last_name = %s,
                                nic = %s, mobile_number = %s WHERE user_id = %s'''
    values = (str(fname), str(lname), str(nic),
              int(mobile_number), str(userid))

    cur = conn.cursor()
    cur.execute(update_data, values)

    conn.commit()
    return cur.rowcount
