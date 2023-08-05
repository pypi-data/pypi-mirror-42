import requests
import numpy as np
import os
import cv2
import time
from multiprocessing import Pool

requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

def imread(path, site='JD', server='http://192.168.1.10:8888/'):
#     tt = time.time()
    r = s.get(os.path.join(server, site, path))
    x = cv2.imdecode(np.fromstring(r.content, dtype='uint8'), 1)
#     print(time.time()-tt)
    return x
