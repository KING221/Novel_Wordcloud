# Novel_Wordcloud
基于py2的小说词云创建
## 流程图
![pic](https://github.com/KING221/Novel_Wordcloud/blob/master/词频统计.png)
## 进行分词，得到缓存
```
import jieba
import jieba.posseg as psg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#对小说文本进行分词，分词后的内容存储到本地缓存文件txt里。
def cut_cache():
    file = open(u"F:\王国图书馆\[01] Harry Potter\哈利·波特 人文版（TXT）\哈利·波特与火焰杯.txt","r").read()
    story_with_attr = [(x.word, x.flag)
                   for x in psg.cut(file)
                   if len(x.word) >= 2]
    print(len(story_with_attr))
    with open('F:\\HP4-out.txt',"w+")as f:
        for x in story_with_attr:
            #print x
            f.write('{0}\t{1}\n'.format(x[0],x[1]))
```
  引入部分```jieba.posseg```可以对分词的词性进行分析。上面的函数，是「分词+词云」的第一步，对文本进行分词，并且添加词性（方便进一步筛选），写进本地txt，作为缓存文件（因为文本量太大了，不可能每次都重新读取，这样很花时间，所以需要一个缓存）。

```
story_with_attr = [(x.word, x.flag) for x in psg.cut(file) if len(x.word) >= 2] 
```
    
  这里用了一个列表存储起了《火焰杯》小说里的所有词+词性。```psg.cut(file)```是默认词性标注分词器（其实是```jieba.posseg```，但在引用部分为了方便，所以写成了```psg```），使用了for循环，针对单个词+词性，然后用了if语句排除掉长度<2的词（的地得你我他……）。```（x.word, x.flag）```是固定写法。
    
  ```f.write('{0}\t{1}\n'.format(x[0],x[1]) ```是写入本地txt。这里用了字符串格式化```format```，把前面的```｛0｝```与后面的```x[0]```关联起来；把前面的```｛1｝```与后面的```x[1]```关联起来。
  
  那么```x[0]```，```x[1]```，x到底是什么呢？我用了```print```方法之后，看到了单个```x```是```[ '太冷' , 'ns' ]```，```x```是分词列表，这个列表里包含了一个单词以及这个单词的词性。```x[0]```是列表里的第一个元素，根据上面的代码可知```x[0]```代表了word，那么```x[1]```自然是词性，flag。

## 读取缓存，生成列表
```
#读取缓存文件txt的内容，并且把该部分内容进行筛选，存储到列表里。
def read_result():
    story_with_attr = []
    wiht open("F:\\HP4-OUT2.txt","r")as f:
        for x in f.readlines():
            x = x.decode('utf-8')
            pair = x.split()
            if len(pair)<2:
                continue
            else:
            story_with_attr.append((pair[0] , pair[1]))
    return story_with_attr
```

得到缓存文件后，对这些缓存文件进行清洗，录入到列表里。这部分函数开头定义了一个“单词+词性”列表，然后for循环缓存文件内容，将里面的东西解码成utf-8，防止生成词云出错。

接着对全体x——也就是那个缓存文件的数据（此时还是空格分开的形式），进行```split```方法。```print pair```之后会得到['单词' , '词性']的组合。```split```通过空格、制表符、换行符等进行分割字符串，分隔开的字符串之间有逗号，并且用一个列表存储数据。

计算```pair```的长度，如果小于2，说明词和词性两者里少了一个，舍弃这个数据，具体到代码里就是```continue```跳出本次循环，进入下一次循环。

如果>=2，说明这个数据就是要找的，把```pair[0]```——也就是```split```之后得到的列表的第一项单词，添加到存储用的列表里；把```pair[1]```——```split```之后得到的第二项词性，同样添加到列表里。

## 将列表转为字典
```
#将词性列表进行处理，转为词性字典，用于词性筛选。
def built_attr_dict(story_with_attr):
    attr_dict = {}
    for x in story_with_attr:
       attr_dict[x[0]] = x[1]
    return attr_dict
```
这个字典，也就是```attr_dict```存储了词和词性，对于之后的词性筛选有帮助。

在这里用了一个for循环和定义句式，将```x[0]```和```x[1]```进行了绑定，之后得出的字典是```attr_dict｛x[0] : x[1]｝```。

## 统计词频
```
def get_topn(words,topn,attr_dict):
    c = Counter(words).most_common(topn)
    with open('F:\\RESULT.txt',"w+") as f :
        for x in c:
            f.write('{0}\t{1}\t{2}\n'.format(x[0], x[1], attr_dict[x[0]]))
```
计数器用于统计words里的词频topn，我在main()函数里设定传入的参数是```get_topn(words = words, topn = 500, attr_dict = attr_dict)```，所以会统计word里前500个单词的词频。注意写入文件里的```attr_dict[x[0]]```，这是词性;写入的分别是 单词/次数/词性。

本段代码传入的words是x[0]，也就是单词，但对x[0]做了一个限制： ``` words = [x[0] for x in story_with_attr if x[1] not in stop_attr]```。```stop_attr```用于筛选词汇，它是一个在main()函数里的列表。

还记得最后写入txt的三个东西吗？最后一个是词性，源自词性字典。我的步骤是：先空着stop_attr列表，执行一次脚本——得到txt，对照着txt上词性字典的词性——筛选词汇（因为有些无意义的词），将这个词的词性手动填入```stop_attr```——执行脚本，重复步骤——直到txt的单词大部分都有意义。

## 词云
```
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator

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
    print "done!"
    
    
```
大部分都是定义内容，定义词云的样式。注意```main```部分，传入函数里，我没有写```‘a=b’```这样的形式，因为如果你写了一个只会，其他的都要写，可能会出错。

所以我把定义部分放在前面，就是```background_color```那里。

传入的图片，必须是黑白分明的那种，不能有灰色，否则python会渲染出错，它会将灰色也当作黑色。我选用的图片是：

![PIC](https://github.com/KING221/Novel_Wordcloud/blob/master/black.png)

生成的词云是：


![PIC](https://github.com/KING221/Novel_Wordcloud/blob/master/词云图.png)
