import time
import traceback


import requests
from models import XinXi,Count,db,DianYing
from sqlalchemy import or_, and_
import re
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        "Referer": "https://accounts.douban.com/",
        "Cookie": '''viewed="36104107"; bid=zhRj5Sk1hkA; gr_user_id=342170f3-3cea-4f34-8d0a-b7e16b57ca4c; __gads=ID=a5a90a51a6616ff4-2279c08c23da0085:T=1677237844:RT=1677237844:S=ALNI_MZPt9X7Ym0dHMY00rLA1MdV_BmH-g; ll="118281"; __yadk_uid=dUaN7hRBqGnoNQno1SpdAjyFzFZfPJ3z; _vwo_uuid_v2=D8DE89F2725DCB4D3CD4678A1CAEFC3AF|9405ac4f39d15de604bee6a66832a8e4; _ga_RXNMP372GL=GS1.1.1678171945.1.0.1678171945.60.0.0; dbcl2="167247563:mU2WmLC2+FY"; push_noty_num=0; push_doumail_num=0; _ga=GA1.2.1121846458.1677237845; __utmz=30149280.1678523115.9.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16724; __utmz=223695111.1678523139.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/doulist/116238969/; ct=y; ck=gB5W; frodotk_db="44f0fc0ce3996c23ced2f426aacc4469"; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1678614479%2C%22https%3A%2F%2Fwww.douban.com%2Fdoulist%2F116238969%2F%22%5D; _pk_id.100001.4cf6=8d96792c0e804e8c.1678085199.4.1678614479.1678523649.; _pk_ses.100001.4cf6=*; __utma=30149280.1121846458.1677237845.1678523115.1678614479.10; __utmb=30149280.0.10.1678614479; __utmc=30149280; __utma=223695111.1121846458.1677237845.1678523139.1678614479.4; __utmb=223695111.0.10.1678614479; __utmc=223695111; __gpi=UID=00000bcb74c248dd:T=1677237844:RT=1678614481:S=ALNI_MaFGf2GzFQaA3QZ9yBBwhntuFHSEA'''
}

movies = list(set([i.name for i in XinXi.query.all()]))
print(movies)
for movie_name in movies:
    time.sleep(3)
    url = 'https://movie.douban.com/j/subject_suggest?q={}'.format(movie_name)
    print(url)
    h1 = requests.get(url=url,headers=headers,verify=False)
    print(h1.json())
    if h1.json():
        try:
            datas = {}
            datas['movie'] = movie_name
            movie_url = 'https://movie.douban.com/subject/{}/?from=showing'.format(h1.json()[0]['id'])
            datas['url'] = movie_url
            datas['id'] = str(h1.json()[0]['id'])
            print(movie_url)
            h1 = requests.get(url=movie_url, headers=headers, verify=False)
            score = re.findall('"ratingValue": "(.*?)"',h1.text)
            if score:
                datas['score'] = score[0]
                if not datas['score']:
                    datas['score'] = 0
            else:
                datas['score'] = 0
            soup = BeautifulSoup(h1.text, 'html.parser')
            datas['director'] = soup.select('div#info span.attrs')[0].text
            attrs1 =  soup.select('div#info span.attrs')[1].select('a')
            if len(attrs1) == 3:
                datas['actor1'] = attrs1[0].text
                datas['actor2'] = attrs1[1].text
                datas['actor3'] = attrs1[2].text
            elif len(attrs1) == 2:
                datas['actor1'] = attrs1[0].text
                datas['actor2'] = attrs1[1].text
                datas['actor3'] = ''
            elif len(attrs1) == 1:
                datas['actor1'] = attrs1[0].text
                datas['actor2'] = ''
                datas['actor3'] = ''
            else:
                datas['actor1'] = ''
                datas['actor2'] = ''
                datas['actor3'] = ''
            try:
                datas['num'] = soup.select('a.rating_people > span')[0].text
                datas['star5'] = int(
                    float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[0].text).replace('%', '')))
                datas['star4'] = int(
                    float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[1].text).replace('%', '')))
                datas['star3'] = int(
                    float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[2].text).replace('%', '')))
                datas['star2'] = int(
                    float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[3].text).replace('%', '')))
                datas['star1'] = int(
                    float(datas['num']) / 100 * float(str(soup.select('span.rating_per')[4].text).replace('%', '')))
            except:
                datas['num'] = 0
                datas['star5'] = 0
                datas['star4'] = 0
                datas['star3'] = 0
                datas['star2'] = 0
                datas['star1'] = 0

            datas['short'] = soup.select('div.mod-hd > h2 a')[0].text.replace('全部', '').replace('条', '').strip().split(' ')[0]
            writer = soup.select('div#info > span')[1].text.strip()
            if '编剧' in writer:
                writer = writer.split(': ')[-1]
            else:
                writer = ''
            datas['writer'] = writer
            info = soup.select('div#info')[0].text
            types2 = re.findall('类型:(.*)', info)
            if types2:
                type1 = str(types2[0]).split('/')[0].strip()
                if len(str(types2[0]).split('/')) >= 2:
                    type2 = str(types2[0]).split('/')[-1].strip()
                else:
                    type2 = ''
            else:
                type1 = ''
                type2 = ''
            datas['type1'] = type1
            datas['type2'] = type2
            regions = re.findall('制片国家/地区:(.*)', info)
            if regions:
                region = regions[0].strip()
            else:
                region = ''
            datas['region'] = region
            times = re.findall('片长:(.*)', info)
            if times:
                time1 = str(times[0]).replace('分钟', '').strip()
                time2 = re.findall('(\d+)', time1)
                if time2:
                    time1 = time2[0]
                else:
                    time1 = '0'
            else:
                time1 = '0'
            datas['time'] = time1
            dates = re.findall('上映日期:(.*)', info)
            if dates:
                da1 = re.findall('(\d{4}-\d{2}-\d{2})', dates[0])
                if da1:
                    year = str(da1[0]).split('-')[0]
                    month = str(da1[0]).split('-')[1]
                else:
                    year = ''
                    month = ''
            else:
                year = ''
                month = ''
            datas['year'] = year
            datas['month'] = month
            print(datas)
            if not DianYing.query.filter(and_(DianYing.movie == datas['movie'], DianYing.url == datas['url'], )).all():
                db.session.add(
                    DianYing(
                        movie=datas['movie'],
                        score=datas['score'],
                        num=datas['num'],
                        star5=datas['star5'],
                        star4=datas['star4'],
                        star3=datas['star3'],
                        star2=datas['star2'],
                        star1=datas['star1'],
                        short=datas['short'],
                        director=datas['director'],
                        writer=datas['writer'],
                        actor1=datas['actor1'],
                        actor2=datas['actor2'],
                        actor3=datas['actor3'],
                        type1=datas['type1'],
                        type2=datas['type2'],
                        region=datas['region'],
                        year=datas['year'],
                        month=datas['month'],
                        time=datas['time'],
                        url=datas['url'],
                    )
                )
                db.session.commit()
        except:
            print(traceback.format_exc())
            continue


