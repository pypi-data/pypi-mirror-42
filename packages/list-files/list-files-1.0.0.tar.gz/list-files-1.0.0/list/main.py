import os
import hashlib

class PrintFilesOfDir:
  def __init__(self,path):
    self.path=path
    self.attr={}
  def printfiles(self):
    for file in os.listdir(self.path):
      filename=os.path.join(self.path,file)
      if(os.path.isdir(filename)):
        print filename+" isdir"
        continue
      print(filename)
      self.attr[file]=self.generate(filename)
      print(self.attr[file])
  def assignattr(self):
    pass
  def generate(self,name):
    blocksize=65536
    hasher=hashlib.md5()
    with open(name,'rb') as file:
      buf=file.read(blocksize)
      while len(buf)>0:
        hasher.update(buf)
        buf=file.read(blocksize)
    return hasher.hexdigest() 
if __name__=='__main__':
  p=PrintFilesOfDir("/home/ubuntu/Downloads")
  p.printfiles()
