import requests
import numpy as np
import os
import cv2
import time
import json

requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False
headers = {"Accept": "application/json"}

def imread(path, site='JD', server='http://192.168.1.10:8888/', file_limits=10):
#     tt = time.time()
    if "." in path:
        r = s.get(os.path.join(server, site, path))
        x = cv2.imdecode(np.fromstring(r.content, dtype='uint8'), 1)
    else:
        r = s.get(os.path.join(server, site, path, "?limit=%d"%file_limits), headers=headers)
        resp_json = json.loads(r.text)
        imgs = []
        x = []
        for entry in resp_json['Entries']:
            imgs.append(entry['FullPath'])
        for img in imgs:
            img = img[1:]
            r = s.get(os.path.join(server, img))
            xx = cv2.imdecode(np.fromstring(r.content, dtype='uint8'), 1)
            x.append(xx)
#     print(time.time()-tt)
    return x
