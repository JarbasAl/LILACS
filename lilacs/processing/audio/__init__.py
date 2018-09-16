import requests


def classify_audio(wav_file, engine="MAX-Audio-Classifier"):
    # source  https://github.com/IBM/MAX-Audio-Classifier
    url = "http://207.154.234.38:5008/model/predict"

    with open(wav_file, 'rb') as file:
        file_form = {'audio': (wav_file, file, 'audio/wav')}
        r = requests.post(url=url, files=file_form)
    return r.json()


if __name__ == "__main__":
    w = "Cop Car Siren-SoundBible.com-1231381021.wav"
    print(classify_audio(w)) # emergency vehicle
    w = "normal_shotgun_-Soundeffects-1522730314.wav"
    print(classify_audio(w)) # gunshot, gunfire
    w = "pno-cs.wav"
    print(classify_audio(w)) # music