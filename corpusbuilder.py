import glob, os, sys
from pathlib import Path
import re
def build(path):
    full_corpus = ""
    nonascii = bytearray(range(0x80, 0x100))
    for file in glob.glob(path,recursive=True):
        f = open(file,"rb")
        file_data = f.read()
        file_data = file_data.translate(None,nonascii).decode("utf-8")
        full_corpus += file_data
        f.close()
    print("Size of corpus:",sys.getsizeof(full_corpus)/1024/1024,"MB")
    full_corpus = full_corpus.replace("\n"," ")
    full_corpus = full_corpus.replace("\r"," ")
    full_corpus = re.sub("[^A-Za-z0-9,.?!:;\-—_ ]+","",full_corpus)
    full_corpus = re.sub("\\s{2,}","",full_corpus)
    return full_corpus
