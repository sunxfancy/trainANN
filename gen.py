#coding=utf-8
__author__ = 'sxf'

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import *

def create_time_img(chars,
                    size = (95, 25),
                    mode = "RGB",
                    bg_color = (255, 255, 255),
                    fg_color = (0, 0, 0),
                    font_size = 18,
                    font_type = "upcel.ttf"):

    img = Image.new(mode, size, bg_color)    # 创建图形
    draw = ImageDraw.Draw(img)               # 创建画笔

    font = ImageFont.truetype(font_type, font_size)
    draw.text((3, 8), chars, font=font, fill=fg_color)

       # 图形扭曲参数
    # params = [1 - float(randint(1, 2)) / 500,
    #           0,
    #           0,
    #           0,
    #           1 - float(randint(1, 2)) / 500,
    #           float(randint(1, 2)) / 500,
    #           0.001,
    #           float(randint(1, 2)) / 500
    #           ]
    # img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲

    # img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）

    return img

train_data = [ '0000000000', '1111111111', '2222222222', '3333333333', '4444444444',
               '5555555555', '6666666666', '7777777777', '8888888888', '9999999999' ]

def gen():
    for i in range(10):
        img = create_time_img(train_data[i])
        img.save('train/{0}.jpg'.format(i), option={'progression': True, 'quality': 90, 'optimize': True})

    img = create_time_img('::::::::::')
    img.save('train/m.jpg', option={'progression': True, 'quality': 90, 'optimize': True})

    img = create_time_img('----------')
    img.save('train/l.jpg', option={'progression': True, 'quality': 90, 'optimize': True})
    img.save('train/l.jpg', option={'progression': True, 'quality': 90, 'optimize': True})

data = ['17:00-19:00', '8:30-9:30', '12:15-22:00', '13:54-16:47']

def gen_data():
    r = Random()
    db = open('train/y.db', 'w')
    for i in range(300):
        randlist = [r.randint(0, 9) for j in range(8)]
        text = '{0}{1}:{2}{3}-{4}{5}:{6}{7}'.format(randlist[0], randlist[1], randlist[2], randlist[3],
                                                    randlist[4], randlist[5], randlist[6], randlist[7])
        # print text
        db.write(text+'\n')
        img = create_time_img(text)
        img.save('train/{0}.bmp'.format(i), option={'progression': True, 'quality': 90, 'optimize': True})
    db.close()

if __name__ == '__main__':
    gen_data()
    # img = create_time_img('17:00-19:00')
    # img.save('a.bmp', option={'progression': True, 'quality': 90, 'optimize': True})