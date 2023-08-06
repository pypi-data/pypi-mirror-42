import keras
import keras.backend as K
import numpy as np
from keras.datasets import fashion_mnist
from keras_adabound import AdaBound


(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

x_train = np.expand_dims(x_train.astype(K.floatx()) / 255, axis=-1)
x_test = np.expand_dims(x_test.astype(K.floatx()) / 255, axis=-1)

y_train, y_test = np.expand_dims(y_train, axis=-1), np.expand_dims(y_test, axis=-1)

train_num = round(x_train.shape[0] * 0.9)
x_train, x_valid = x_train[:train_num, ...], x_train[train_num:, ...]
y_train, y_valid = y_train[:train_num, ...], y_train[train_num:, ...]


def get_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Dropout(input_shape=(28, 28, 1), rate=0.3, name='Input-Dropout'))
    model.add(keras.layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same', name='Conv-1'))
    model.add(keras.layers.MaxPool2D(pool_size=2, name='Pool-1'))
    model.add(keras.layers.Dropout(rate=0.2, name='Dropout-1'))
    model.add(keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', padding='same', name='Conv-2'))
    model.add(keras.layers.MaxPool2D(pool_size=2, name='Pool-2'))
    model.add(keras.layers.Dropout(rate=0.2, name='Dropout-2'))
    model.add(keras.layers.Flatten(name='Flatten'))
    model.add(keras.layers.Dense(units=256, activation='relu', name='Dense'))
    model.add(keras.layers.Dropout(rate=0.2, name='Dense-Dropout'))
    model.add(keras.layers.Dense(units=10, activation='softmax', name='Softmax'))
    return model


model = get_model()
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)
model.fit(
    x=x_train,
    y=y_train,
    epochs=3,
    validation_data=(x_valid, y_valid),
    callbacks=[keras.callbacks.EarlyStopping(monitor='val_acc', patience=2)]
)
adam_score = model.evaluate(x_test, y_test)
print('Score of Adam:\t%.4f' % adam_score[1])


model = get_model()
model.compile(
    optimizer=AdaBound(),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)
model.fit(
    x=x_train,
    y=y_train,
    epochs=3,
    validation_data=(x_valid, y_valid),
    callbacks=[keras.callbacks.EarlyStopping(monitor='val_acc', patience=2)]
)
ada_bound_score = model.evaluate(x_test, y_test)
print('Score of Adam:\t%.4f' % adam_score[1])
print('Score of AdaBound:\t%.4f' % ada_bound_score[1])