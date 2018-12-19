import urllib.request
import re
import os
def get_url():
    with open('logos.txt', 'r+') as source:
        url = [source.readline()]
        for line in source.readlines():
            line = line.strip('\n')
            url.append(line)
    return url


def get_name():
    url = get_url()
    Img_list = []
    index = 0
    for i in url:
        Img = re.findall('[lcs|icons]/(.*?.png)?', i)
        if len(Img) == 0 or Img[0] == '':
            Img = ['{}.jpg'.format(index)]
            # print(Img)b 3
            index += 1
        # print(Img[0])
        Img_list.append(''.join(Img))
    print(len(url))
    print(len(Img_list))
    for i in Img_list:
        print(i)
    return url,Img_list


def getImage():
    url,Img = get_name()
    file_path ='F:/Image'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for x, y in zip(url, Img):
        filename = os.path.join(file_path,y)
        try:
            urllib.request.urlretrieve(x,filename)
            print(filename)
        except Exception as e:
            print('{},{}没有图片生成'.format(x, y))
            continue


from PIL import Image
# 所有图片转成jpg
def to_jpg():
    file_path = 'F:/Image'
    for root, sub, files in os.walk(file_path):
        for file in files:
            file_name = os.path.join(root, file)
            # im = Image.open(file_name)
            # im = im.convert("RGB")
            # im.save(file_name)
            # print("{}-->rgb".format(file_name))
            newname = file.split('.')
            if newname[-1] == 'png':
                new_file = newname[0] + '.jpg'
                file_new = os.path.join(root, new_file)
                os.rename(file_name,file_new)
                print('{}--->{}'.format(file_name,file_new))
            # except Exception as e:
            #     shutil.move(file_path, 'F:/ftp3')
            #     print("{}-->remove".format(file_path))

from PIL import ImageFile


def split_img():
    file_path = 'F:/Image'
    rgbk_l = []
    other_l = []
    for root, sub, files in os.walk(file_path):
        for file in files:
            file_name = os.path.join(root, file)
            im = Image.open(file_name)
            if im == 'RGBK':
                rgbk_l.append(file_name)
            else:
                other_l.append(file_name)
    return rgbk_l, other_l

# 把RGBA通道变为RGB通道
def get_rgbk(rgbk_l):
    for i in rgbk_l:
        im = Image.open(i)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        r,g,b,a = im.split()
        im = Image.merge('RGB',(r,g,b))
        im.save(i)
        print("{}-->RGB".format(i))

# 其他的p可以直接convert
def get_other(other_l):
    for i in other_l:
        im=Image.open(i)
        im = im.convert("RGB")
        im.save(i)
        print("{}-->RGB".format(i))

if __name__ == '__main__':
    to_jpg()
    # A,B = split_img()
    # get_rgbk(A)
    # get_other(B)
