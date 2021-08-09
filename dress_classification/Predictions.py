from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import numpy as np
import pandas as pd
import json
import pickle
import shutil


def dress_detection_model_prediction(APP_ROOT, test):
    # Read json
    folder_path = APP_ROOT + "/dress_classification/"
    with open(folder_path + "/config.json", "r") as read_file:
        json_data = json.load(read_file)

    print(test)

    # Get data from json
    test_data = test
    img_width = int(json_data['img_width'])
    img_height = int(json_data['img_height'])
    model_path = folder_path + "/" + str(json_data['model'])
    pickle_path = folder_path + "/" + str(json_data['pickle'])

    # Load model
    model = keras.models.load_model(model_path)

    # Genarate data for prediction
    predict_datagen = ImageDataGenerator(rescale=1. / 255)
    predict_generator = predict_datagen.flow_from_directory(
        test_data,
        shuffle=False,
        target_size=(img_height, img_width))

    # Get prediction
    predictions = model.predict_generator(predict_generator)
    predicted_class_indices = np.argmax(predictions, axis=1)

    # Load init_dict pickle
    init_dic = pickle.load(open(pickle_path, 'rb'))
    swap_dict = dict([(value, key) for key, value in init_dic.items()])

    # Get true name in the predictions
    predClassArray = []
    for class_indices in predicted_class_indices:
        predClassArray.append(swap_dict.get(class_indices))

    # Calculate score of the predictions
    predPercentArray = []
    for predPercentage in predictions:
        predPercentArray.append("{0:0.1f}".format(
            (np.max(predPercentage) / np.sum(predPercentage) * 100)))

    # Create dataframe for prediction results
    prediction = pd.DataFrame({'IMAGE_NAME': predict_generator.filenames,
                               'PREDICTED_CLASS': predClassArray, 'ACCURACY': predPercentArray})

    result = {}
    for index, row in prediction.iterrows():
        result = {'PREDICTED_CLASS': str(row['PREDICTED_CLASS']).replace("_", " ").upper(),
                  'ACCURACY': float(row['ACCURACY'])}

    # Remove folder
    shutil.rmtree(test_data[:-1])

    return result
