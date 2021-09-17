import os
def loadfile(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
        f.close()
        return data

