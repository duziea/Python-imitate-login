import requests
import json
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy
import matplotlib.pyplot as plt


def get_qq_comment():

    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?'

    data = {
        # "biztype": "1",
        # "topid": "237773700",
        # "cmd": "6",
        # "needmusiccrit": "0",
        # "pagesize": "200",

        "biztype": "1",
        "topid": "215830524",
        "cmd": "6",
        "needmusiccrit": "0",
        "pagesize": "200",

    }

    response = requests.get(url, params=data)
    print(response)
    comments = json.loads(response.text)
    comment = comments['comment']
    commentlist = comment['commentlist']
    commentlist2 = []
    comment3 = ''
    for i in commentlist:
        dic={}
        dic['rootcommentcontent'] = i['rootcommentcontent']
        dic['nick'] = i['nick']
        dic['praisenum'] = i['praisenum']
        dic['time'] = i['time']
        commentlist2.append(dic)
        comment3 += i['rootcommentcontent']

    print(len(commentlist2))
    # with open('qqmusic/shuohaobuku.json', 'w',encoding='utf-8') as f:
    #     json.dump(commentlist2,f,ensure_ascii=False)
    with open('qqmusic/waitwaitwait.json', 'w',encoding='utf-8') as f:
        json.dump(commentlist2,f,ensure_ascii=False)

    return comment3

def getwd(comment3):
    # img_path = r'qqmusic\cover.jpg'
    img_path = r'qqmusic\kun.jpg'
    cut_text = ''.join(jieba.cut(comment3))
    background_image = numpy.array(Image.open(img_path))
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf", # 字体
                          background_color = 'white', # 背景色
                          max_words = 100, # 最大显示单词数
                          max_font_size = 60, # 频率最大单词字体大小
                        #   stopwords = stopwords, # 过滤噪声词
                          mask = background_image # 自定义显示的效果图
                        ).generate(cut_text)
    image = wordcloud.to_image()
    image.show()



if __name__ == "__main__":
    comment3 = get_qq_comment()
    getwd(comment3)