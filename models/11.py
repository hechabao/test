from fontTools.ttLib import TTFont

# 加载字体文件：
font = TTFont('ebf320e5 (1).woff')

# 转为xml文件：
font.saveXML('maoyan3.xml')


dicts_num = {'uniF13A': 6, 'uniE428': 3, 'uniF60B': 7, 'uniF680': 1, 'uniF7DB': 5, 'uniEBED': 9,
             'uniECD3': 0, 'uniEFC7': 4, 'uniEF36': 2, 'uniE705': 8}

dicts_num = {'uniEB13': 6, 'uniE990': 3, 'uniE1E9': 7, 'uniF738': 1, 'uniF71B': 5, 'uniF3AF': 9,
                        'uniEF55': 0, 'uniEA19': 4, 'uniED14': 2, 'uniED67': 8}

dicts_num = {'uniEFA3': 6, 'uniEE52': 3, 'uniEECB': 7, 'uniF8BF': 1, 'uniF867': 5, 'uniF639': 9,
                        'uniE7C1': 0, 'uniF8E7': 4, 'uniE2E8': 2, 'uniEEE9': 8}

dicts_num = {'uniEFA3': 6, 'uniEE52': 3, 'uniEECB': 7, 'uniF8BF': 1, 'uniF867': 5, 'uniF639': 9,
                        'uniE7C1': 0, 'uniF8E7': 4, 'uniE2E8': 2, 'uniEEE9': 8}


# import requests
# from models import XinXi,Count,db,DianYing
# from sqlalchemy import or_, and_
# import re
# from bs4 import BeautifulSoup
#
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#         "Referer": "https://accounts.douban.com/",
#             }
#
# movies = list(set([i.name for i in XinXi.query.all()]))
# print(movies)
# for movie_name in movies:
#     url = 'https://movie.douban.com/j/subject_suggest?q={}'.format(movie_name)
#     h1 = requests.get(url=url,headers=headers,verify=False)
#     print(h1.json())
#     if h1.json():
#         datas = {}
#         datas['movie'] = movie_name
#         movie_url = 'https://movie.douban.com/subject/{}/?from=showing'.format(h1.json()[0]['id'])
#         datas['url'] = movie_url
#         datas['id'] = str(h1.json()[0]['id'])
#         print(movie_url)
#         h1 = requests.get(url=movie_url, headers=headers, verify=False)
#         score = re.findall('"ratingValue": "(.*?)"',h1.text)
#         if score:
#             datas['score'] = score[0]
#         else:
#             datas['score'] = 0
#         soup = BeautifulSoup(h1.text, 'html.parser')
#         datas['director'] = soup.select('div#info span.attrs')[0].text
#         attrs1 =  soup.select('div#info span.attrs')[1].select('a')
#         if len(attrs1) == 3:
#             datas['actor1'] = attrs1[0].text
#             datas['actor2'] = attrs1[1].text
#             datas['actor3'] = attrs1[2].text
#         elif len(attrs1) == 2:
#             datas['actor1'] = attrs1[0].text
#             datas['actor2'] = attrs1[1].text
#             datas['actor3'] = ''
#         elif len(attrs1) == 1:
#             datas['actor1'] = attrs1[0].text
#             datas['actor2'] = ''
#             datas['actor3'] = ''
#         else:
#             datas['actor1'] = ''
#             datas['actor2'] = ''
#             datas['actor3'] = ''
#         try:
#             datas['num'] = soup.select('a.rating_people > span')[0].text
#             datas['star5'] = int(
#                 float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[0].text).replace('%', '')))
#             datas['star4'] = int(
#                 float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[1].text).replace('%', '')))
#             datas['star3'] = int(
#                 float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[2].text).replace('%', '')))
#             datas['star2'] = int(
#                 float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[3].text).replace('%', '')))
#             datas['star1'] = int(
#                 float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[4].text).replace('%', '')))
#         except:
#             datas['num'] = 0
#             datas['star5'] = 0
#             datas['star4'] = 0
#             datas['star3'] = 0
#             datas['star2'] = 0
#             datas['star1'] = 0
#
#         datas['short'] = soup.select('div.mod-hd > h2 a')[0].text.replace('全部', '').replace('条', '').strip()
#         writer = soup.select('div#info > span')[1].text.strip()
#         if '编剧' in writer:
#             writer = writer.split(': ')[-1]
#         else:
#             writer = ''
#         datas['writer'] = writer
#         info = soup.select('div#info')[0].text
#         types2 = re.findall('类型:(.*)', info)
#         if types2:
#             type1 = str(types2[0]).split('/')[0].strip()
#             if len(str(types2[0]).split('/')) >= 2:
#                 type2 = str(types2[0]).split('/')[-1].strip()
#             else:
#                 type2 = ''
#         else:
#             type1 = ''
#             type2 = ''
#         datas['type1'] = type1
#         datas['type2'] = type2
#         regions = re.findall('制片国家/地区:(.*)', info)
#         if regions:
#             region = regions[0].strip()
#         else:
#             region = ''
#         datas['region'] = region
#         times = re.findall('片长:(.*)', info)
#         if times:
#             time1 = str(times[0]).replace('分钟', '').strip()
#             time2 = re.findall('(\d+)', time1)
#             if time2:
#                 time1 = time2[0]
#             else:
#                 time1 = ''
#         else:
#             time1 = ''
#         datas['time'] = time1
#         dates = re.findall('上映日期:(.*)', info)
#         if dates:
#             da1 = re.findall('(\d{4}-\d{2}-\d{2})', dates[0])
#             if da1:
#                 year = str(da1[0]).split('-')[0]
#                 month = str(da1[0]).split('-')[1]
#             else:
#                 year = ''
#                 month = ''
#         else:
#             year = ''
#             month = ''
#         datas['year'] = year
#         datas['month'] = month
#         print(datas)
#         if not DianYing.query.filter(and_(DianYing.movie == datas['movie'], DianYing.url == datas['url'], )).all():
#             db.session.add(
#                 DianYing(
#                     movie=datas['movie'],
#                     score=datas['score'],
#                     num=datas['num'],
#                     star5=datas['star5'],
#                     star4=datas['star4'],
#                     star3=datas['star3'],
#                     star2=datas['star2'],
#                     star1=datas['star1'],
#                     short=datas['short'],
#                     director=datas['director'],
#                     writer=datas['writer'],
#                     actor1=datas['actor1'],
#                     actor2=datas['actor2'],
#                     actor3=datas['actor3'],
#                     type1=datas['type1'],
#                     type2=datas['type2'],
#                     region=datas['region'],
#                     year=datas['year'],
#                     month=datas['month'],
#                     time=datas['time'],
#                     url=datas['url'],
#                 )
#             )
#             db.session.commit()
#
#
#
#     break
#
#
#
