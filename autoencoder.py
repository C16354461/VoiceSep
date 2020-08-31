# import tensorflow as tf
# import os, random, pickle
import numpy as np
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, LSTM, Input, TimeDistributed, BatchNormalization # Dropout,


def loadSamples():
    with open('E:\DataSets\dev-clean\SpeechNPvalid.pkl', 'rb') as f:
        ValidCleanNP = pickle.load(f)
    with open('E:\DataSets\dev-clean\MixNPvalid.pkl', 'rb') as f:
        ValidMixNP = pickle.load(f)
    with open('E:\DataSets\dev-clean\SpeechNP.pkl', 'rb') as f:
        TrainCleanNP = pickle.load(f)
    with open('E:\DataSets\dev-clean\MixNP.pkl', 'rb') as f:
        TrainMixNP = pickle.load(f)

    i = 0
    ValidSamples = []
    for file in ValidMixNP:
        ValidSamples.append([file,ValidCleanNP[i]])
        i += 1

    i = 0
    TrainSamples = []
    for file in TrainMixNP:
        TrainSamples.append([file,TrainCleanNP[i]])
        i += 1

    return TrainSamples, ValidSamples

def generator(samples, Xpath, Ypath, batch_size):
    num_samples = len(samples)
    random.shuffle(samples)
    while True:
        for start in range(0, num_samples,batch_size):
            batch_samples = samples[start:start+batch_size]
            X = []
            Y = []
            for sample in batch_samples:
                X.append(np.load(os.path.join(Xpath,sample[0])))
                Y.append(np.load(os.path.join(Ypath,sample[1])))
            X = np.array(X)
            Y = np.array(Y)

            yield X, Y

def loadModel():
    model = Sequential()

    model.add(LSTM(1024,input_shape=(108, 2049 ), return_sequences=True))
    model.add(BatchNormalization())

    model.add(LSTM(1024, return_sequences=True))
    model.add(BatchNormalization())

    model.add(LSTM(1024, return_sequences=True))

    model.add(TimeDistributed(Dense(2049)))
    opt = Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss='mse')
    return model

def Train():
    TrainSamples, ValidSamples = loadSamples()
    Trainxpath = "E:\DataSets\dev-clean\MixNP"
    Trainypath = "E:\DataSets\dev-clean\SpeechNP"
    Validxpath = "E:\DataSets\dev-clean\MixNPvalid"
    Validypath = "E:\DataSets\dev-clean\SpeechNPvalid"
    batch = 25
    TrainGen = generator(TrainSamples,Trainxpath,Trainypath,batch_size=batch)
    ValidGen = generator(ValidSamples,Validxpath,Validypath,batch_size=batch)
    model = loadModel()
    model.summary()
    model.load_weights('Noisey2SpeechLargeDB.h5')

    checkpoint = ModelCheckpoint('Noisey2SpeechLargeDB2.h5', save_best_only=True, monitor='val_loss', mode='auto')

    model.fit(TrainGen, steps_per_epoch=len(TrainSamples)//batch,
     epochs=10,callbacks=[checkpoint],validation_data=ValidGen,
     validation_steps=len(ValidSamples)//batch)

if __name__ == '__main__':
    Train()
