import os
import json
from json import JSONEncoder
import numpy as np
import face_recognition


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


data = []
for b in os.listdir('photos/astrum_students'):

    for p in os.listdir(f'photos/astrum_students/{b}'):
        name = p.split(".")[0]
        # path = f"dars-2/photos/{b}/{p}"
        path = f"photos/astrum_students/{b}/{p}"
        pic = face_recognition.load_image_file(path)
        encode_pic = face_recognition.face_encodings(pic)[0]

        d = {'name': name,
             'path': path,
             'dir': b,
             'encode': encode_pic}

        data.append(d)

encodedNumpyData = json.dumps(data, cls=NumpyArrayEncoder)

with open("astrum_students.json", "w") as outfile:
    outfile.write(encodedNumpyData)
