# make a prediction for a new image.
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from sklearn.metrics import classification_report

# load and prepare the image


def load_image(filename):
    # load the image
    img = load_img(filename, grayscale=True, target_size=(28, 28))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 1 channel
    img = img.reshape(1, 28, 28, 1)
    # prepare pixel data
    img = img.astype('float32')
    img = img / 255.0
    return img

# load an image and predict the class


def run_example():
    # classes
    classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress',
               'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    # load the image
    img = load_image('test.jpeg')
    # load model
    model = load_model('ResNet56v2.h5')
    # predict the class
    result = model.predict(img)
    result = np.argmax(result, axis=1)
    for key in result:
        print('predicted class: %s' % classes[key])


# entry point, run the example
run_example()
