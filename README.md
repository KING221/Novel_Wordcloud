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
  
    ```story_with_attr = [(x.word, x.flag) for x in psg.cut(file) if len(x.word) >= 2] ```
    
    这里用了一个列表存储起了《火焰杯》小说里的所有词+词性。```psg.cut(file)```是默认词性标注分词器（其实是```jieba.posseg```，但在引用部分为了方便，所以写成了```psg```），使用了for循环，针对单个词+词性，然后用了if语句排除掉长度<2的词（的地得你我他……）。```（x.word, x.flag）```是固定写法。
    
  ```f.write('{0}\t{1}\n'.format(x[0],x[1]) ```是写入本地txt。这里用了字符串格式化```format```，把前面的```｛0｝```与后面的```x[0]```关联起来；把前面的```｛1｝```与后面的```x[1]```关联起来。
  
  那么```x[0]```，```x[1]```，x到底是什么呢？我用了```print```方法之后，看到了单个```x```是```[ '太冷' , 'ns' ]```，```x```是分词列表，这个列表里包含了一个单词以及这个单词的词性。```x[0]```是列表里的第一个元素，根据上面的代码可知```x[0]```代表了word，那么```x[1]```自然是词性，flag。
