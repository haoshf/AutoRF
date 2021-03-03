import os

def Lib():
    Librarylist = []
    work = os.getcwd()
    file_dir = (work+'/Library').replace("\\", "/")
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            Lib = (('./Library'+file).replace("\\", "/"),file)
            Librarylist.append(Lib)
    return Librarylist