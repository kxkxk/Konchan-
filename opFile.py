import os
import time
def mkPath():
    if(os.path.isdir("./pic") == False):
        os.mkdir("./pic")
    return "./pic"
def strTime():
    name = time.strftime('%M%S%Y%m%d%H',time.localtime(time.time()))
    return name
def mkNewFord(name):
    if(os.path.isdir(name) == False):
        os.mkdir("./pic/"+name)
    return "./pic/"+name+"/"
