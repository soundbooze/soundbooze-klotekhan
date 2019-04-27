import pycurl
import certifi
from StringIO import StringIO
import re
import os
import numpy as np

# pip install youtube-dl
QUERY = "https://www.youtube.com/results?search_query=" + "mike+portnoy+isolated+drum"
WATCH = "https://www.youtube.com/watch?v=" 

buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, QUERY)
c.setopt(c.WRITEDATA, buffer)
c.setopt(c.CAINFO, certifi.where())
c.perform()
c.close()

body = buffer.getvalue()
splitBody = body.split(' ')

f = []
for i in range(len(splitBody)):
    s = str(splitBody[i])
    if len(s) > 1:
        r = re.search("\/watch\?v", s)
        if r:
            f.append(i)

foundvid = []
for i in f:
    s = splitBody[i].split("=")
    f = s[2]
    if not re.search(';list', f):
        foundvid.append(s[2][:-1])

urlvid = []
for f in foundvid:
    urlvid.append(WATCH + f)

urlvid = np.unique(urlvid)

for i in range(len(urlvid)):
    os.system("./youtube-dl -x --audio-format mp3 " + urlvid[i] + " -o mp3/" + str(i) + ".wav")

# bot-chopper - dataZ builder

#generate from isolated
#generate from poly
#generate from rnd(hybrid)
