from wordcloud import WordCloud
import jieba,os
import PIL.Image as image11
import numpy as np
from models.models import db,DianYing


def chinese_jieba(text):
    wordlist_jieba = jieba.cut(text)
    space_wordlist = ''.join(wordlist_jieba)
    return space_wordlist

def daoyan():
    mask = np.array(image11.open("11.jpg"))
    datas = DianYing.query.all()
    strs = ''
    for data in datas:
        strs += data.director

    text = chinese_jieba(strs)

    font_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))) + os.sep + 'data' + os.sep + 'simfang.ttf'
    wordcloud = WordCloud(font_path=font_path,mask=mask,
                              background_color=None, mode="RGBA", width=800,
                               height=400, max_words=50, min_font_size=8).generate(text)
    image = wordcloud.to_image()
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'static/ciyun' + os.sep + '{}.png'.format('director')
    image.save(path)

def writer():
    mask = np.array(image11.open("11.jpg"))
    datas = DianYing.query.all()
    strs = ''
    for data in datas:
        strs += data.writer

    text = chinese_jieba(strs)

    font_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))) + os.sep + 'data' + os.sep + 'simfang.ttf'
    wordcloud = WordCloud(font_path=font_path,mask=mask,
                              background_color=None, mode="RGBA", width=800,
                               height=400, max_words=50, min_font_size=8).generate(text)
    image = wordcloud.to_image()
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'static/ciyun' + os.sep + '{}.png'.format('writer')
    image.save(path)

def actor():
    mask = np.array(image11.open("11.jpg"))
    datas = DianYing.query.all()
    strs = ''
    for data in datas:
        strs += data.actor1 +' ' + data.actor2 +  ' ' + data.actor3  +' '

    text = chinese_jieba(strs)

    font_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))) + os.sep + 'data' + os.sep + 'simfang.ttf'
    wordcloud = WordCloud(font_path=font_path,mask=mask,
                              background_color=None, mode="RGBA", width=800,
                               height=400, max_words=50, min_font_size=8).generate(text)
    image = wordcloud.to_image()
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'static/ciyun' + os.sep + '{}.png'.format('actor')
    image.save(path)


def region():
    mask = np.array(image11.open("11.jpg"))
    datas = DianYing.query.all()
    strs = ''
    for data in datas:
        strs += data.region + ' '

    text = chinese_jieba(strs)

    font_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))) + os.sep + 'data' + os.sep + 'simfang.ttf'
    wordcloud = WordCloud(font_path=font_path,mask=mask,
                              background_color=None, mode="RGBA", width=800,
                               height=400, max_words=50, min_font_size=8).generate(text)
    image = wordcloud.to_image()
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'static/ciyun' + os.sep + '{}.png'.format('region')
    image.save(path)


if __name__ == '__main__':
    daoyan()
    writer()
    actor()
    region()