import os
import cv2
from matplotlib import pyplot as plt
import tensorflow as tf
import numpy as np
from FindPhotos import findPhotos
def makeModel(query1:str, query2:str, model_name:str):


    #first find data

    findPhotos(query1, query2)
    
    datadir = "data"


    #first check if all of the photos provided are readable by cv2

    for image_class in os.listdir(datadir):
        for image in os.listdir(os.path.join(datadir, image_class)):
            image_path = os.path.join(datadir, image_class, image)
            try:
                img = cv2.imread(image_path)
            except:
                print("I am deleting " + image_path)
                os.remove(image_path)


    #lets load the data via tensorflow
    data = tf.keras.utils.image_dataset_from_directory('data')
    data_iterator = data.as_numpy_iterator()



    #preprocessing

    #first lets scale the data
    data = data.map(lambda x,y: (x/255, y))

    #split the data
    train_size = int(len(data)*0.7)
    val_size = int(len(data)*0.2)
    test_size = int(len(data)*0.2)


    train = data.take(train_size)
    val = data.skip(train_size).take(val_size)
    test = data.skip(train_size + val_size).take(test_size)


    #time to build the model
    from tensorflow import keras
    from keras import layers

    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)),
        layers.MaxPooling2D(),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D(),

        layers.Flatten(),

        layers.Dense(256, activation='relu'),
        layers.Dense(1, activation="sigmoid")   # Binary classification with sigmoid activation
    ])

    
    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])


    #now let's train the model
    logdir = 'logs'
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir = logdir)

    hist = model.fit(train, epochs=10, validation_data = val, callbacks = [tensorboard_callback])


    #lets plot the performance of the data
    fig = plt.figure()
    plt.plot(hist.history['loss'], color = 'green', label = 'loss')
    plt.plot(hist.history['val_loss'], color = 'red', label = 'val_loss')
    plt.legend(loc = 'upper left')
    plt.show()

    #lets evaluate the performance 

    accuracy = 0
    for batch in test.as_numpy_iterator():
        test_loss, test_acc = model.evaluate(batch[0], batch[1])
        accuracy += test_acc
    print('Test accuracy:', accuracy/len(test))



    #Save the model
    model.save(os.path.join('models', model_name))


makeModel("Charmander", "Squirtle", "Charmander vs Squirtle")
