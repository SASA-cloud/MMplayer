import os
import time
from PIL import Image

def image_size_change(PicPath, length, width):
  objectPath = os.path.join(PicPath, 'resize')  # 输出文件夹地址
  if not os.path.exists(objectPath):
    os.mkdir(objectPath)
  pic = os.listdir(PicPath)
  count = 1
  for i in pic:
    if i.endswith('.jpg') or i.endswith('.jpeg'):
      file = os.path.join(PicPath, i)
      im = Image.open(file)
      out = im.resize((length, width))
      listStr = [str(int(time.time())), str(count)]
      fileName = ''.join(listStr)
      out = out.convert("RGB")
      out.save(objectPath+os.sep+'%s.jpg' % fileName)
      count = count + 1

if __name__ == "__main__":
  PicPath = 'C:/Users/清羽凌空/Desktop/多媒体/database/pic'
  objectPath = 'C:/Users/清羽凌空/Desktop/多媒体/data/pic_trans'
  length = input()
  length = int(length)
  width = input()
  width = int(width)
  image_size_change(PicPath,length, width)