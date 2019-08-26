#!/usr/bin/python
# -*- coding: UTF-8 -*-
#适用于Py2
import jieba
from collections import Counter
import jieba.posseg as psg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator

def cut_cache():
    file = open(u'F:\王国图书馆\[01] Harry Potter\哈利·波特 人文版（TXT）\哈利·波特与火焰杯.txt', "r").read()
    story_with_attr = [(x.word, x.flag) for x in psg.cut(file) if len(x.word)>=2]
    with open("F:\\HP4-OUT2-1.txt", "w+") as f:
        print("writing to txt...")
        for x in story_with_attr:
            f.write("{0}\t{1}\n".format(x[0],x[1]))
    f.close()

def read_result():
    story_with_attr = []
    with open("F:\\HP4-OUT2-1.txt","r")as f:
        for x in f.readlines():
            x = x.decode('utf-8')
            pair = x.split()
            if len(pair)<2:
                continue
            else:
                story_with_attr.append((pair[0],pair[1]))
    return story_with_attr

def built_attr_dict(story_with_attr):
    attr_dict = {}
    for x in story_with_attr:
       attr_dict[x[0]] = x[1]
    return attr_dict

def get_topn(words,topn,attr_dict):
    c = Counter(words).most_common(topn)
    top_words_with_freq = {}
    with open('F:\\RESULT.txt',"w+") as f :
        for x in c:
            f.write('{0}\t{1}\t{2}\n'.format(x[0], x[1], attr_dict[x[0]]))
            top_words_with_freq[x[0]] = x[1]
    return top_words_with_freq

#生成词云
def gen_world_cloud(img_bg_path, font_path, background_color,
                    top_words_with_freq, save_path):
    img_bg = imread(img_bg_path)
    wc = WordCloud(font_path = font_path,
    background_color = background_color,
    max_words = 500,
    mask = img_bg,
    max_font_size=50,
    random_state=30,
    width = 1000,
    margin = 5,
    height = 700)
    wc.generate_from_frequencies(top_words_with_freq)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    wc.to_file(save_path)

def main():
    cut_cache()
    story_with_attr = read_result()
    attr_dict = built_attr_dict(story_with_attr)
    stop_attr = ['r','c','d','v','m','t']
    words = [x[0] for x in story_with_attr if x[1] not in stop_attr]
    background_color = 'white'
    top_words_with_freq = get_topn(words = words, topn = 500, attr_dict = attr_dict)
    gen_world_cloud(u"F:\\微信图片_20180703185344.jpg",
                    u"F:\文件存档\字体库\SourceHanSansCN-Bold.otf",
                    background_color , top_words_with_freq,
                    'F:\HP4_WC2.png')
    print("done!")

if __name__ == '__main__':
    main()
