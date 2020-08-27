import numpy as np
from tensorflow.keras.models import Sequential, Model, load_model
import librosa, soundfile
import norbert
from . import autoencoder

def snipify(audio):
    samplerate = 22050
    snips = []
    snipL = samplerate*5
    length = audio.shape[0]
    if length % snipL != 0:
        padding = (((length//snipL)+1)*snipL) - length
        audio = np.pad(audio, (0,padding), 'constant', constant_values=(0, 0))
        end = snipL
    for i in range(0,length,snipL):
        snips.append(audio[i:end])
        end = end + snipL
    return snips

def SPECify(snips):
    stfts = []
    specs = []
    hop_length = 1024
    n_fft = 4096
    for snip in snips:
        stft = librosa.stft(snip, n_fft=n_fft, hop_length=hop_length)
        stfts.append(stft)
        spec = np.abs(stft)
        specs.append(np.float32(spec.T))
    specs = np.array(specs)
    return specs, stfts

def separate(fileIn, fileOut, modelname):
    audio, samplerate = librosa.load(fileIn, sr=22050)
    snips = snipify(audio)
    specs, stfts = SPECify(snips)

    model = autoencoder.loadModel()
    model.load_weights(modelname)
    sourceSpecs = model.predict(specs)
    sourceaudio = np.array([])

    for i in range(0,sourceSpecs.shape[0]):
        sourceSpec = sourceSpecs[i].T
        stft = stfts[i]
        stft = np.expand_dims(stft, axis=2)
        sourceSpec = np.expand_dims(sourceSpec, axis=2)
        sourceSpec = np.expand_dims(sourceSpec, axis=3)
        print(sourceSpec.shape, stft.shape)
        resi = norbert.residual_model(sourceSpec, stft.astype(np.complex128), 1)
        sourceSpecNorbert = norbert.wiener(resi, stft.astype(np.complex128), 1, use_softmask=False)
        sourceSpecNorbert1 = sourceSpecNorbert[:,...,0,0]
        sourceaudio = np.append(sourceaudio,librosa.istft(sourceSpecNorbert1))

    soundfile.write(fileOut,sourceaudio,samplerate)

if __name__ == '__main__':
    modelname = "Music2SpeechLargeDB.h5"
    fileIn = "C:\Projects\Year4\FYP\open-unmix-pytorch-master\\SpeechMix.wav"
    fileOut = "C:\Projects\Year4\FYP\open-unmix-pytorch-master\\Besting.wav"
    separate(fileIn, fileOut, modelname)
