import os
import numpy as np
from tensorflow.keras.models import Sequential, Model, load_model
import librosa, librosa.display
import norbert
import autoencoder

# Create actual wav sample
def PreProcess(filepath):
    audio, samplerate = librosa.load(filepath, sr=22050)
    snip = audio[0:samplerate*5]
    hop_length = 1024
    n_fft = 4096
    stft = librosa.stft(snip, n_fft=n_fft, hop_length=hop_length)

    spec = np.abs(stft)

    x = []
    x.append(np.float32(spec.T))
    x = np.array(x)
    return x, stft

def PostProcess(Y, stft):
    stft = np.expand_dims(stft, axis=2)
    Y = np.expand_dims(Y.T, axis=3)
    resi = norbert.residual_model(Y, stft.astype(np.complex128), 1)
    YNorbert = norbert.wiener(resi, stft.astype(np.complex128), 1, use_softmask=False)
    YNorbert1 = YNorbert[:,...,0,0]
    Yaudio = librosa.istft(YNorbert1)
    return Yaudio


testdir = "C:\Projects\Year4\FYP\TFsep\\test files\\"
file = "NoisyV-00007.wav"
filepath = os.path.join(testdir,file)
X, stft = PreProcess(filepath)

model = autoencoder.loadModel()
model.load_weights('Music2SpeechLargeDB.h5')
Y = model.predict(X)

audio = PostProcess(Y, stft)
librosa.output.write_wav(testdir+"Cleaned-"+file,audio,22050)
