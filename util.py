import os
import random
import re
from datetime import datetime


# Function for get images folder root
def get_images_root(APP_ROOT):
    folder_path = os.path.join(APP_ROOT, 'templates/images/')
    return folder_path


# Function for genarate random number
def random_number():
    rand_no = str(random.randint(100000, 999999))
    return rand_no


# Function for get current date
def date_picker():
    current_datetime = datetime.now()
    date = str(current_datetime.strftime("%Y-%m-%d"))
    return date


# Function for get current date and time
def datetime_picker():
    current_datetime = datetime.now()
    date_time = str(current_datetime.strftime("%Y%m%d%H%M%S"))
    return date_time


# Validate email address
def emailValidate(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True

    else:
        return False


# Function for check string is float
def check_float(value):
    try:
        float(value)
        return True

    except ValueError:
        return False

# Check string is int


def RepresentsInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function for validate price


def priceValidation(value):

    if RepresentsInt(value) == False:
        if check_float(value) == False:
            return False

    return True
