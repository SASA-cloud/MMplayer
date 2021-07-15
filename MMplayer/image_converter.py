import os
from PIL import Image
import shutil
import sys 



def image_converter(dataset_dir):
    # Define the input and output image
    output_jpg = os.path.join(dataset_dir, 'jpg')
    output_png = os.path.join(dataset_dir, 'png')
    if not os.path.exists(output_jpg):
        os.mkdir(output_jpg)
    if not os.path.exists(output_png):
        os.mkdir(output_png)


    jpgfiles = []
    pngfiles = []
    image_list = os.listdir(dataset_dir)
    jpgfiles = [os.path.join(dataset_dir, x) for x in image_list if x.endswith('.jpg') or x.endswith('.jpeg')]
    pngfiles = [os.path.join(dataset_dir, x) for x in image_list if x.endswith('.png')]
    for index, jpg in enumerate(jpgfiles):
        if index > 100000:
            break
        try:
            sys.stdout.write('\r>>Converting image %d/100000'%(index))
            sys.stdout.flush()
            im = Image.open(jpg)
            png = os.path.splitext(jpg)[0]+".png"
            im.save(png)
            shutil.move(png, output_png)
        except IOError as e:
            print('could not read:', jpg)
            print('error', e)
            print('skip it\n')

    for index, png in enumerate(pngfiles):
        if index > 100000:
            break
        try:
            sys.stdout.write('\r>>Converting image %d/100000' % (index))
            sys.stdout.flush()
            im = Image.open(png)
            jpg = os.path.splitext(png)[0] + ".jpg"
            im = im.convert("RGB")
            im.save(jpg)
            shutil.move(jpg, output_jpg)
        except IOError as e:
            print('could not read:', png)
            print('error', e)
            print('skip it\n')

    sys.stdout.write('\nConvert Over!\n')
    sys.stdout.flush()

if __name__ == '__main__':
    current_dir = os.getcwd()
    print(current_dir)
    data_dir = 'C:\\Users\\清羽凌空\\Desktop\\多媒体\\database\\pic'

    image_converter(data_dir)
