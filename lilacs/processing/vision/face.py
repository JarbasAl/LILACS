import requests
from os.path import abspath
import base64


def face_analysis(face_picture, engine="deepface_demo"):
    url = "https://api.deepface.ir/analysis"
    with open(face_picture, 'rb') as f:
        files = {'file': (face_picture, f.read(), 'image/jpeg')}
    # TODO test if token expires
    r = requests.post(url, files=files, data={"token": "0113b67e-213b-4167-a95c-0689b73288be"})
    return r.json()["data"]


def face_age(face_picture, engine="MAX-Facial-Age-Estimator"):
    # source  https://github.com/IBM/MAX-Facial-Age-Estimator
    url = "http://207.154.234.38:5005/model/predict"
    with open(face_picture, 'rb') as f:
        files = {'image': f.read()}
    r = requests.post(url, files=files)
    return r.json()["predictions"]


def animate_eyes(face_picture, mode=None, engine="deepwarp_demo"):
    # https://github.com/ddtm/deep-smile-warp
    face_picture = abspath(face_picture)
    modes = ["roll", "scroll", "cross", "shift"]
    if mode is None:
        res = []
        for m in modes:
            res += animate_eyes(face_picture, m, engine)
        return res
    mode = mode.lower()
    assert mode in modes
    url = "http://163.172.78.19/process"
    with open(face_picture, 'rb') as f:
        files = {'file': (face_picture, f.read(), 'image/jpeg')}
    r = requests.post(url, data={"action": mode}, files=files)
    url = r.headers["location"]
    done = False
    # check if ready
    while not done:
        r = requests.get(url)
        if r.json()["state"] != "PROGRESS":
            done = True
            data = base64.decodebytes(bytes(r.json()["result"].split("base64,")[1], encoding="utf-8"))
            with open(face_picture+"_"+mode+".mp4", "wb") as f:
                f.write(data)
    return [face_picture+"_"+mode+".mp4"]


def face_emotion(face_picture, engine="deepface_demo"):
    url = "https://api.deepface.ir/emotion"
    with open(face_picture, 'rb') as f:
        files = {'file': (face_picture, f.read(), 'image/jpeg')}
    r = requests.post(url, files=files, data={"token": "0113b67e-213b-4167-a95c-0689b73288be"})
    return r.json()["data"]


class LILACSFace(object):
    def __init__(self, bus=None):
        self.bus = bus

    def face_age(self, face_picture, engine="MAX-Facial-Age-Estimator"):
        return face_age(face_picture, engine)

    def face_emotion(self, face_picture, engine="deepface_demo"):
        return face_emotion(face_picture, engine)

    def face_analysis(self, face_picture, engine="deepface_demo"):
        return face_analysis(face_picture, engine)

    def animate_eyes(self, face_picture, mode=None, engine="deepwarp_demo"):
        return animate_eyes(face_picture, mode, engine)


if __name__ == "__main__":

    LILACS = LILACSFace()

    picture = "sasha.jpg"

    data = LILACS.face_analysis(picture)
    print(data)

    data = LILACS.face_emotion(picture)
    print(data)

    data = LILACS.face_age(picture)
    print(data)

    files = LILACS.animate_eyes(picture)
    print(files)
