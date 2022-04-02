import librosa

def bpm_detect(file):
    y, sr = librosa.load(file)
    hop_length = 512
    # Compute local onset autocorrelation
    oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

    #times = librosa.times_like(oenv, sr=sr, hop_length=hop_length)
    #tempogram = librosa.feature.tempogram(onset_envelope=oenv, sr=sr,
    #                                      hop_length=hop_length)

    # Estimate the global tempo for display purposes
    tempo = librosa.beat.tempo(onset_envelope=oenv, sr=sr,
                            hop_length=hop_length)[0]
    print(tempo)
    return(tempo)

if __name__=="__main__":
    file='presets/samples/nico.wav'
    bpm_detect(file)