import os
if not os.path.isdir("./OANC"):
  os.system("curl https://www.anc.org/OANC/OANC-1.0.1-UTF8.zip -o OANC-1.0.1-UTF8.zip")
  os.system("unzip OANC-1.0.1-UTF8.zip")
import bptokenizer
