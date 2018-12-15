import os.path

def inputFilepath(text):
    while True:
        path = input(text)
        if os.path.isfile(path):
            return path
        print("Invalid file path")
