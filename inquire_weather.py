 #每次只能查询一个城市，使用EasyGUI模块
import easygui as g
from lxml import etree
import random
import pymongo
import requests
import sys



def get_mongodbmessage():
    
    message = {}
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client.china_city
    collection = db.province
    for each in collection.find():
        message[each['_id']]=each[each['_id']]
    return message



def url_open(city_code):

    url = 'http://www.weather.com.cn/weather/'+city_code+'.shtml'
    headers = {}
    '''head = {
        
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }'''
    user_agents = [
            
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
            ]
    agent=random.choice(user_agents)
    headers['User-Agent']=agent
    req = requests.get(url=url,headers=headers)
    html = req.content.decode('utf-8')
    return html



def get_weather(city_code):
    html = url_open(city_code)
    selector=etree.HTML(html)
    weather_text=[]
    for i in range(1,8):
        #日期
        weather_text.append('*********************************\n')
        data_x = '//*[@id="7d"]/ul/li['+str(i)+']/h1/text()'
        data = selector.xpath(data_x)
        weather_text.append('日期为：'+data[0]+'\n')
        
        #天气
        weather_x = '//*[@id="7d"]/ul/li['+str(i)+']/p[1]/text()'
        weather = selector.xpath(weather_x)
        weather_text.append('天气状况为：'+weather[0]+'\n')
        
        #温度
        t_hx='//*[@id="7d"]/ul/li['+str(i)+']/p[2]/*/text()'
        T_h = selector.xpath(t_hx)
        if len(T_h)==2:
            weather_text.append('最高温度为：'+T_h[0]+'\n')
            weather_text.append('最低温度为：'+T_h[1]+'\n')
        else:
            weather_text.append('温度为：'+T_h[0]+'\n')
        
        #风向
        wind_x = '//*[@id="7d"]/ul/li['+str(i)+']/p[3]/em/span/@title'
        wind_direct = selector.xpath(wind_x)
        win=set(wind_direct)
        
        if len(win)==2:
            weather_text.append('风向为：'+wind_direct[0]+'转'+wind_direct[-1]+'\n')
        else:
            weather_text.append('风向为：'+wind_direct[0]+'\n')
                            
        #风力
        wind_y = '//*[@id="7d"]/ul/li['+str(i)+']/p[3]/i/text()'
        wind = selector.xpath(wind_y)
        weather_text.append('风力为：'+wind[0] +'\n')
    weather_text.append('*********************************\n')
    return  weather_text



def city_weather():
    
    city = get_mongodbmessage()
    province_choice=g.choicebox('选择省份','天气查询',city.keys())
    city_choice = g.choicebox('选择城市','天气查询',city[province_choice].keys())
    g.textbox(city_choice+'七日内天气情况','天气查询',get_weather(city[province_choice][city_choice]))
    
    sys.exit()



if __name__=="__main__":

    city_weather()
    

