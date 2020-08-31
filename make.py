import os
import random
import numpy as np
import librosa

def readWav(path):
    x = []
    y = []
    for r, d, f in os.walk(path):
        for file in f:
            # try:
            if ".wav" in file:
                print("Reading: ",file)
                audio, samplerate = librosa.load(os.path.join(r,file), sr=22050)
                yield(audio,file)

def snipify(source, dest):
    samplerate = 22050
    snipL = samplerate*5
    namecnt = 1
    for audio, name in readWav(source):
        length = audio.shape[0]
        if length % snipL != 0:
            padding = (((length//snipL)+1)*snipL) - length
            audio = np.pad(audio, (0,padding), 'constant', constant_values=(0, 0))
        end = snipL
        for i in range(0,length,snipL):
            snip = audio[i:end]
            end = end + snipL
            print("Writing snippet")
            librosa.output.write_wav(os.path.join(dest,"Noise-"+str(namecnt).zfill(5)+".wav"),snip,samplerate)
            namecnt += 1

def STFTify(audio, dest, name):
    hop_length = 1024
    n_fft = 4096
    stft = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length)
    spec = np.abs(stft)
    print("Saving Spectrogram")
    np.save(os.path.join(dest, name[0:-4]),spec.T)

def Noiseify(source, noise, speechDest, mixDest):
    samplerate = 22050
    amp = [0.1,0.2,0.3,0.4,0.5]
    for audio, file in readWav(source):
        rand = random.choice(range(1,65424))
        noisefile,_ = librosa.load(os.path.join(noise,"Noise-"+str(rand).zfill(5)+".wav"), sr=22050)
        mix = audio + (noisefile*random.choice(amp))
        STFTify(audio, speechDest, file)
        STFTify(mix, mixDest, "Mix-"+file[6:])

if __name__ == '__main__':
    snipify("E:\DataSets\\noise","E:\DataSets\dev-clean\\noiseSnips")
    Noiseify("E:\DataSets\clean\speechSnips","E:\DataSets\dev-clean\\noiseSnips","E:\DataSets\dev-clean\SpeechNP","E:\DataSets\dev-clean\MixNP")
