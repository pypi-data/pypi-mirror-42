# ToDo-01
import os
import argparse
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
import numpy as np
import time

class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

# global ToDo-01
RESULT_DIR = "result"
IMG_WIDTH = 256
IMG_HEIGHT = 256
cwd = os.getcwd()

def vgg_model_maker(nb_classes):
    """
    In this case, use VGG16 except Fully Connected layer.
    Need to make FC for this model and put together them
    """

    # Load VGG16 not need fc include_top = False
    input_tensor = Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3))
    vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)

    # create FC layer
    top_model = Sequential()
    top_model.add(Flatten(input_shape=vgg16.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.5)) # ToDo
    top_model.add(Dense(nb_classes, activation='softmax'))

    # VGG16 + FC ---> new model
    model = Model(input=vgg16.input, output=top_model(vgg16.output))

    return model


def image_generator(classes, batch_size, train_data_dir, validation_data_dir, rotation):
    """
    load images and create dataset for training and validation
    """ 

    # training data
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        zoom_range=0.2,
        rotation_range = rotation,
        horizontal_flip=True,
        vertical_flip=True)

    # validation data
    validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        color_mode='rgb',
        classes=classes,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True)

    validation_generator = validation_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        color_mode='rgb',
        classes=classes,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True)

    return (train_generator, validation_generator)


def get_number_of_files(target_dir):
    dir_list = os.listdir(target_dir)
    sorted_list = sorted(dir_list)
    # print(sorted_list)
    # For Mac Users
    if sorted_list[0] == '.DS_Store':
        target = sorted_list[1]
    else:
        # print('here')
        target = sorted_list[0]
    # print('target :' + target)
    files_list = os.listdir(target_dir + '/' + target)
    # print(files_list)
    return len(files_list)


# resize images ---> 256x256
def resize_images(target_dir):
    print(Color.PURPLE + "start resizing images" + Color.END)
    print(Color.PURPLE + "finish resizing images" + Color.END)

# main
def main():
    parser = argparse.ArgumentParser(
        prog='ictrainer',
        usage='train a image classifier for keras',
        description='tool for training an image classifier',
        add_help = True 
        )
    parser.add_argument("--mode", dest="mode", help="choose one mode of 3 modes, train mode, test mode, and collect mode ", required=True)
    parser.add_argument("--classes", dest="classes", help="put your classname", type = str, nargs='*')
    parser.add_argument("--batch", dest="batch", help="batch size", default=15)
    parser.add_argument("--epoch", dest="epoch", help="epoch a big value takes so much time to train", default=30)
    parser.add_argument("--mname", dest="mname", help="your model name", default="myModel_")
    parser.add_argument("--lr", dest="lr", help="learning rate", default=1e-3)
    parser.add_argument("--momentum", dest="momentum", help="momentum: Parameter that accelerates SGD in the relevant direction and dampens oscillations.", default=0.9)
    parser.add_argument("--rotation", dest="rotation", help="image rotation for training", default=20)
    parser.add_argument("--keyword", dest="keyword", help="type keyword")
    parser.add_argument("-n", "--number", dest="number", help="number of total images", default=100)
    parser.add_argument("-t", "--target", dest="target", help="target folder")
    args = parser.parse_args()

    # args
    user_define_classes = args.classes # classes defined by user 
    batch = args.batch # batch size
    epoch = args.epoch # epoch size
    mname = args.mname  # model name
    input_lr = args.lr
    input_momentum = args.momentum
    input_rotation = args.rotation
    mode = args.mode # mode
    keyword = args.keyword
    max_num = int(args.number)
    target = args.target

    print('mode: ' + mode)
    if mode == 'collect':
        # mode image collect images
        from .image_collector import ImageCollector
        print(Color.CYAN + 'start image collecting mode' + Color.END)
        ic = ImageCollector(keyword, max_num)
        ic.get_images()
        print(Color.CYAN + 'end image collecting mode' + Color.END)

    elif mode == 'resize':
        # resize ToDo
        from .image_resizer import ImageResizer
        print(Color.GREEN + 'start image resize mode' + Color.END)
        ir = ImageResizer()
        ir.resize_image(cwd + '/dataset/' + target)
        print(Color.GREEN + 'end image resize mode' + Color.END)

    
    elif mode == 'train':
        # mode train train images
        
        print(Color.BLUE + 'start training mode' + Color.END)

        # create folder for result
        if not os.path.exists(RESULT_DIR):
            print(Color.YELLOW + 'You do not have result dir. I will create it for you!!!' + Color.END)
            os.mkdir(RESULT_DIR)

        classes = user_define_classes
        nb_classes = len(classes)

        # data folder path for train & validation
        train_data_dir = cwd + '/dataset/train'
        validation_data_dir = cwd + '/dataset/val'
        train_data_num = get_number_of_files(train_data_dir)
        validation_data_num = get_number_of_files(validation_data_dir)
        
        # print('train data num ' + str(train_data_num))
        # print('val data num ' + str(validation_data_num))


        # the amount of images
        # count the number of images
        nb_train_samples = train_data_num * nb_classes
        nb_validation_samples = validation_data_num * nb_classes

        # batch_size
        batch_size = batch
        nb_epoch = epoch
        # print('batch size ' + str(batch_size))
        # print('nb_epoch ' + str(nb_epoch))

        # start timer
        start = time.time()

        # create model
        vgg_model = vgg_model_maker(nb_classes)

        # freeze layers
        for layer in vgg_model.layers[:15]:
            layer.trainable = False

        # classes
        # optimizer lr(lerning rate) # parameter
        # lr: float >= 0. Learning rate.
        # momentum: float >= 0. Parameter that accelerates SGD in the relevant direction and dampens oscillations.
        # loss
        # metrics
        # 
        vgg_model.compile(loss='categorical_crossentropy',
            optimizer=optimizers.SGD(lr=input_lr, momentum=input_momentum),metrics=['accuracy'])

        # generator for images
        train_generator, validation_generator = image_generator(classes, batch_size, train_data_dir, validation_data_dir, input_rotation)

        # Fine-tuning
        history = vgg_model.fit_generator(
            train_generator,
            samples_per_epoch=nb_train_samples,
            nb_epoch=nb_epoch,
            validation_steps=20,
            validation_data=validation_generator
            # nb_val_samples=nb_validation_samples
            )

        # export model
        vgg_model.save_weights(os.path.join(RESULT_DIR, '{model_name}.h5'.format(model_name=mname)))

        process_time = int((time.time() - start) / 60)
        print(Color.BLUE + u'Finished training!!! This process took', process_time, u' minutes' + Color.END)

    else:
        print(Color.RED + 'you have not put mode name' + Color.END)


if __name__ == '__main__':
    main()