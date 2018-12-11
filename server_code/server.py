from flask import Flask, request
from pymongo import MongoClient
import os
import pandas as pd
from tensorflow.python.keras.models import load_model
from PIL import Image
import numpy as np
from process_data import *
import re
import datetime

# Connect to the MongoDB

client = MongoClient('mongodb://18.209.62.51/cool_db')
db = client.smartwatch_db

UPLOAD_FOLDER = '/home/ec2-user/pictures'

# load classification model
model = load_model('ss_img_reg_model_final.h5')
model._make_predict_function()

#load food database

food_dict = pd.read_csv('/home/ec2-user/data/food_data.csv')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# define processing functions
def resize(path, dim=384):
    """
    resize the image and convert it into a standard RGB format
    :param path:
    :param dim:
    :return:
    """
    try:
        im = Image.open(path)
        # Anti-alias is a high quality downsampling method
        if im.size != (dim, dim):
            im = im.resize((dim, dim), Image.ANTIALIAS)
            imResize = im.convert('RGB')
        return np.array(imResize)
    except:
        "File not found!"
        return None


def classify_food(filepath,
                  model):
    """
    uses a neural network to classify the data
    :param filepath:
    :return:
    """
    print('classify food now...')
    print(filepath)
    x = resize(filepath)
    p = model.predict(np.expand_dims(x, 0))
    categories = ['Vegetables', 'Beef', 'Cheese', 'Bread', 'Desserts']
    c = categories[p.argmax()]
    print('classify food done')

    return c

def calculate_weight(pressure):
    """
    Takes in the pressure measurement
    :param pressure:
    :return: weight in gram
    """

    return 3.6

def get_calories_percentage(db):
    data = pd.DataFrame(list(db.spoondata_user.find()),
                        columns=['timestamp', 'food', 'foodtype', 'weight',
                                 'calories', 'temperature'])
    data['timestamp'] = pd.to_datetime(data.timestamp)
    calories = data[(data.timestamp.dt.date ==
                     datetime.datetime.now().date())].sum().calories
    return int((calories / 2700) * 100)

def get_no_of_bites(db):
    data = pd.DataFrame(list(db.spoondata_user.find()),
                        columns=['timestamp', 'food', 'foodtype', 'weight',
                                 'calories', 'temperature'])
    data['timestamp'] = pd.to_datetime(data.timestamp)
    bites = data[(data.timestamp.dt.date ==
                     datetime.datetime.now().date())].shape[0]
    return int(bites)


def process_classify_data(filepath, dict, food_dict, model):
    """
    Takes in an observation of the food, and cleans it
    :param filepath:
    :param dict:
    :param food_dict:
    :return:
    """

    timestamp = str(dict['timestamp'])
    food = classify_food(filepath, model)
    foodtype = food_dict[food_dict.name == food]['group'].values[0]
    weight = calculate_weight(float(dict['pressure']))
    calories_standard = food_dict[food_dict.name == food]['calories'].values[0]
    calories = round(weight * calories_standard / 100,2)
    temperature = float(dict['temp'])
    # takes an impage as input and creates a datapoint for a user

    return {'timestamp': timestamp,
            'food': food,
            'foodtype': foodtype,
            'weight': weight,
            'calories': calories,
            'temperature': temperature}


@app.route('/')
def hello_world():
    return 'Hello, Morgan!'


@app.route('/latest_id/', methods=['POST', 'GET'])
def get_latest_number():
    l = os.listdir(UPLOAD_FOLDER)
    l.sort()
    try:
        g = re.match('img([0-9]*)\.', l[-1])
        return g.group(1)
    except:
        return 0

@app.route('/save_picture/', methods=['POST', 'GET'])
def save_request1():
    if 'file' not in request.files:
        print('No file part')
        return ""
    file = request.files['file']
    filename = file.filename

    if file.filename == '':
        print('No selected file')
        return ""
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER' ], filename))
        print('picture saved')
        return "Picture Saved"
    else:
        return ""

@app.route('/save_picture_label/', methods=['POST', 'GET'])
def save_request_label():
    if 'file' not in request.files:
        print('No file part')
        return ""
    file = request.files['file']
    filename = file.filename

    if file.filename == '':
        print('No selected file')
        return ""
    if file:
        x = filename.split("_")

        file.save(os.path.join(app.config['UPLOAD_FOLDER/'+x[0]], x[1]))
        print('picture saved')
        return "Picture Saved"
    else:
        return ""


@app.route('/accelerometer/', methods=['POST', 'GET'])
def save_accelerometer():
    data = request.json
    result = db.spoondata_accel.insert_one(data)
    print(data)


    return "Data saved"



@app.route('/save_data/', methods=['POST', 'GET'])
def save_request2():
    data = request.json
    print(data['filepath'])
    result = db.spoondata_raw.insert_one(data)
    clean_data = process_classify_data(UPLOAD_FOLDER + '/' + data['filepath'],
                                       data,
                                       food_dict=food_dict,
                                       model=model)
    result2 = db.spoondata_user.insert_one(clean_data)
    cal_perc = get_calories_percentage(db)
    bites = get_no_of_bites(db)
    clean_data['cal_perc'] = cal_perc
    clean_data['bites'] = bites
    print(clean_data)
    clean_data.pop('_id')

    return str(clean_data)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=4028)

