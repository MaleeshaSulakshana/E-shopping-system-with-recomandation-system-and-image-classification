# Import library files

import tensorflow as tf
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import os
import json
import time
import logging
import sys
import pickle


def genarate_date_time():
    t = time.localtime()
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S", t)

    return current_time


date_time = genarate_date_time()

# Log file
log_folder_name = "Log_" + date_time + "/"
logpath = "logs/" + log_folder_name
log_file_name = "log_" + date_time + ".log"
log_file_source = logpath + log_file_name

# Output json
output_json_name = "json_" + date_time
output_json_path = "output_Jsons/" + output_json_name + "/"
output_json_source = output_json_path + output_json_name + ".json"

# Model save
model_name = "model_" + date_time
best_model_path = "best_model/" + model_name
best_model_source = best_model_path + "/" + model_name + ".h5"

# Pickle file
pickle_folder = "pickle_" + date_time + "/"
pickles_save_name = "train_generator_pickle/" + pickle_folder
pickle_path = pickles_save_name + "pickle_classes.pkl"

# Create folders
if not os.path.exists(logpath):
    os.makedirs(logpath)

if not os.path.exists(output_json_path):
    os.makedirs(output_json_path)

if not os.path.exists(best_model_path):
    os.makedirs(best_model_path)

if not os.path.exists(pickles_save_name):
    os.makedirs(pickles_save_name)


logging.basicConfig(filename=log_file_source,
                    format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Process Started \n \n')


logging.basicConfig(filename=log_file_source, filemode='w',
                    format='%(asctime)s - %(message)s', level=logging.INFO)


class warning:
    def __init__(self):
        return log_file_name
        logging.warning()


# Load argument json
with open("config.json", "r") as read_file:
    userData = json.load(read_file)


class Payload(object):
    def __init__(self, userData):
        self.__dict__ = json.loads(userData)


config = Payload(json.dumps(userData))


# Initializing Basic Parameters
train_data_dir = config.train_data_dir
img_width = int(config.img_width)
img_height = int(config.img_height)
batch_size = int(config.batch_size)
validation_split = float(config.validation_split)
epochs = int(config.epochs)
best_model_saving_destination = config.best_model_saving_destination

# Getting the Number of Classes for Training
list = os.listdir(train_data_dir)
numOfClasses = len(list)

# Initialize Base Models' pre-trained weights from imagenet
model = VGG19(weights='imagenet', include_top=False,
              input_shape=(img_width, img_height, 3))
logging.warning(model)
print("=============== Base Model Loaded Successfully ===============")

# Select layers from weight model
for layer in model.layers[:-5]:
    layer.trainable = False

# Set input and output layers
top_layers = model.output
top_layers = Flatten()(top_layers)
top_layers = Dense(numOfClasses, activation="softmax")(top_layers)

custom_Model = Model(inputs=model.input, outputs=top_layers)

# Add Keras Generators
train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   validation_split=validation_split)  # set validation split

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training')  # set as training data

validation_generator = train_datagen.flow_from_directory(
    train_data_dir,  # same directory as training data
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation')  # set as validation data

print("=============== Generators Loaded Successfully ===============")

# Create class dictionary
init_dic = dict(train_generator.class_indices.items())

# Save init_dict in pickle
pickle.dump(init_dic, open(pickle_path, 'wb'))
swap_dict = dict([(value, key) for key, value in init_dic.items()])

# Compile model
base_learning_rate = 0.00001
custom_Model.compile(loss='categorical_crossentropy',
                     optimizer=tf.keras.optimizers.Adam(
                         lr=base_learning_rate, clipnorm=0.001),
                     metrics=['accuracy'])


# Save our model using specified conditions
cp = ModelCheckpoint(best_model_source, monitor='val_acc', verbose=1,
                     save_best_only=False, save_weights_only=False, mode='auto', period=1)

# # Set early stopping
es = EarlyStopping(monitor='val_acc', min_delta=0,
                   patience=10, verbose=1, mode='auto')

print("=============== Model Evaluation Started ===============")

final_Model = ''

# Model traning
try:
    final_Model = custom_Model.fit_generator(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        callbacks=[cp]
        # callbacks=[es, cp]
    )

except:
    logging.error(
        "Exception occurred system will exit soon \n \n", exc_info=True)
    sys.exit(1)


# Get the history from fit_Generator Dictionary, then assign each Confident Accuracy Values & Validation Accuracy Values into separate arrays:
con_acc = final_Model.history['acc']
val_acc = final_Model.history['val_acc']

# Output JSON file params:
output_data = {}
output_data['Best Confident Accuracy(%)'] = round(max(con_acc) * 100)
output_data['Best Validation Accuracy(%)'] = round(max(val_acc) * 100)
output_data['Best Model Path'] = best_model_source
output_data['Swapped Indicies'] = swap_dict

with open(output_json_source, 'w') as outfile:
    json.dump(output_data, outfile)

logging.warning(final_Model)

# Logging info(end time)
logging.basicConfig(filename=log_file_source,
                    format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Process Ended \n \n')

print("=============== Model Evaluation Successfully Completed ===============")
