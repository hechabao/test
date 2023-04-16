import random
import requests
import datetime
import time
import re
import hashlib
import urllib3
import cn2an
urllib3.disable_warnings()



start_date = datetime.datetime.strptime('2021-01-01','%Y-%m-%d')

session = requests.session()

dicts_num = {'unie9d7': 6, 'unie744': 3, 'unieedc': 7, 'unie4f1': 1, 'unie8ac': 5, 'unieabe': 9, 'unif5f4': 0, 'unif1cc': 4, 'unif6c0': 2, 'unie80f': 8}

def jiexi(jiexi):
    i = jiexi.replace('&#x', 'uni').lower()
    strs = ''
    for ii in i.split(';'):
        if ii:
            if ii.strip().startswith('.'):
                strs += '.' + str(dicts_num.get(ii[1:].strip()))
            else:
                strs += str(dicts_num.get(str(ii.strip())))
    return strs


if __name__ == '__main__':
    while True:
        time.sleep(2)
        date = start_date.strftime('%Y-%m-%d')
        url = 'https://piaofang.maoyan.com/dashboard/movie?date={}'.format(date)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        }
        h1 = session.get(url=url,headers=headers,verify=False)
        appdate = re.findall('"uuid":"(.*?)"',h1.text)
        if appdate:
            uuid = appdate[0]
        else:
            continue

        ajax_url = 'https://piaofang.maoyan.com/dashboard-ajax/movie'
        timeStamp = int(time.time()*1000)
        index = int(random.random()*1000+1)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Referer":url,
            "Host": "piaofang.maoyan.com",
            "Cookie": "_lxsdk_cuid=17dd826610bc8-074a4c1f433b7a-4303066-144000-17dd826610cc8; _lxsdk=6D282530619D11ECAC62E53058C173478FBB1B70FC5D4803AA91E36436E0191A; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1640008934,1640053263,1640183474; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1640183477; __mta=216471081.1640009073181.1640053309514.1640183486387.5; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=17de2fe1eab-747-3f8-810%7C%7C6"
        }

        singkey = 'method=GET&timeStamp={}&User-Agent=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk2LjAuNDY2NC4xMTAgU2FmYXJpLzUzNy4zNg==&index={}&channelId=40009&sVersion=2&key=A013F70DB97834C0A5492378BD76C53A'.format(timeStamp,index)
        date1 = start_date.strftime('%Y%m%d')
        m = {
            "showDate": date1,
            "orderType": "0",
            "uuid": uuid,
            "timeStamp": timeStamp,
            "User-Agent": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk2LjAuNDY2NC4xMTAgU2FmYXJpLzUzNy4zNg==",
            "index": index,
            "channelId": "40009",
            "sVersion": "2",
            "signKey": hashlib.md5(singkey.encode('utf-8')).hexdigest()
        }
        h2 = session.get(url=ajax_url,headers=headers,params=m,verify=False)
        dict_info = h2.json()

        Count_piaofang = dict_info['movieList']['nationBoxInfo']['nationBoxSplitUnit']['num']
        Count_piaofang = jiexi(Count_piaofang)
        try:
            float(Count_piaofang)
        except:
            continue
        print(Count_piaofang)
        Count_piaofang = Count_piaofang + dict_info['movieList']['nationBoxInfo']['nationBoxSplitUnit']['unit']
        for resu in dict_info['movieList']['list']:
            name = resu['movieInfo']['movieName']
            movieId = resu['movieInfo']['movieId']
            days = resu['movieInfo']['releaseInfo']
            piaofang = jiexi(resu['splitBoxSplitUnit']['num']) + resu['splitBoxSplitUnit']['unit']
            print(name,movieId,days,piaofang)

        start_date = start_date + datetime.timedelta(days=1)