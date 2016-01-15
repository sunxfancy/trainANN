# encoding=utf-8
__author__ = 'sxf'

from PIL import Image
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import pickle

class Image2Text:
    # size参数描述了要识别的每一个切分后的字符大小,因为神经网络要求全部识别内容等向量长度,
    #  一般设置为能够包含其中切割后最大的字符即可
    # types参数表示最终神经网络要分的类别数,也即总共出现的所有可能的字符种类数
    def __init__(self, size=(8, 12), types=12):
        self.imgsize = size
        self.types = types
        self.ds = SupervisedDataSet(size[0] * size[1], types)
        self.net = buildNetwork(self.imgsize[0] * self.imgsize[1],
                                100,
                                types,
                                bias=True)

    def cutting(self, im):
        w, h = im.size
        data = im.getdata()
        cut_imgs = []

        vlast_sum = 0
        vbegin = 0
        vend = 0
        for i in xrange(h):
            vsum = 0
            for j in xrange(w):
                vsum += data[i * w + j]
            if vsum > 0 and vlast_sum == 0:
                vbegin = i
            if vsum == 0 and vlast_sum > 0:
                vend = i

                begin = 0
                end = 0
                last_sum = 0

                for j in xrange(w):
                    sum = 0
                    for i in xrange(vbegin, vend):
                        sum += data[i * w + j]

                    if sum > 0 and last_sum == 0:
                        begin = j
                    if sum == 0 and last_sum > 0:
                        end = j
                        cut_imgs.append(im.crop((begin, vbegin, end, vend)))
                        # print begin, vbegin, end, vend

                    last_sum = sum

            vlast_sum = vsum

        return cut_imgs

    def resize(self, im):
        img = Image.new('1', self.imgsize, 0)
        img.paste(im, (0, 0))
        return img

    def ann_addsample(self, input, output):
        myoutput = [0 for i in xrange(self.types)]
        myoutput[output] = 1
        self.ds.addSample(input, myoutput)

    def ann_clear(self):
        self.ds.clear()

    def ann_train(self):
        trainer = BackpropTrainer(self.net, self.ds,
                                  momentum=0.1,
                                  verbose=True,
                                  weightdecay=0.0001)
        trainer.trainUntilConvergence(maxEpochs=50, validationProportion=0.01)

    def ann_sim(self, input):
        output = self.net.activate(input)
        maxoutput = 0
        maxi = 0
        for i in range(len(output)):
            if maxoutput < output[i]:
                maxoutput = output[i]
                maxi = i
        return maxi

    def ann_save(self, path='ann.db'):
        fileObject = open(path, 'w')
        pickle.dump(self.net, fileObject)
        fileObject.close()

    def ann_load(self, path='ann.db'):
        try:
            with open(path, 'r') as data:
                self.net = pickle.load(data)
            return True
        except IOError as err:
            print("File Error:"+str(err)) #str()将对象转换为字符串
            return False

    def open_file(self, path):
        fp = open(path, "rb")
        im = Image.open(fp)
        return self.open(im)

    def open(self, im):

        # 二值化
        # im = im.convert('1')
        im = im.convert('L')
        im = im.point(lambda x: 255 if x > 196 else 0)
        im = im.convert('1')
        im = im.point(lambda i: 1 - i / 255)

        # 切割图片
        imgs = self.cutting(im)

        # 等大小化
        for i in range(len(imgs)):
            imgs[i] = self.resize(imgs[i])
            # imgs[i].save('a/{0}.bmp'.format(i), option={'progression': True, 'quality': 90, 'optimize': True})
        return imgs

if __name__ == '__main__':
    i2t = Image2Text()

    # 如果未加载成功的话，训练网络并将其存储下来
    if not i2t.ann_load():
        ydb = open('trainweb/y.db', 'r')
        lines = ydb.readlines()
        ydb.close()

        for i in xrange(len(lines)):
            # print lines[i]
            imgs = i2t.open_file('trainweb/{0}.png'.format(i))
            if len(imgs) == len(lines[i])-1:
                for j in xrange(len(imgs)):
                    if lines[i][j] == ':':
                        i2t.ann_addsample(imgs[j].getdata(), 11)
                    elif lines[i][j] == '-':
                        i2t.ann_addsample(imgs[j].getdata(), 10)
                    else:
                        i2t.ann_addsample(imgs[j].getdata(), int(lines[i][j]))
        i2t.ann_train()
        i2t.ann_save()

    imgs = i2t.open_file('a.png')
    for im in imgs:
        ans = i2t.ann_sim(im.getdata())
        if ans == 10:
            print '-',
        elif ans == 11:
            print ':',
        else:
            print ans,
