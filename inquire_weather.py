 #每次只能查询一个城市，使用EasyGUI模块
import easygui as g
from lxml import etree
import random
import pymongo
import requests
import sys
from tkinter import *


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


class Application(Frame):
    def __init__(self, city,master=None):
        self.city=city
        
        
        Frame.__init__(self, master,bg='white')
        self.width,self.height=self.master.maxsize()
        self.choice_city = StringVar()
        self.choice_city.set("上海")
        self.choice_pro = StringVar()
        self.choice_pro.set("上海")
        self.pack(expand=YES,fill=BOTH)
        self.window_init()
        self.fm1()
        self.fm2()
        self.fm3()

    
    def window_init(self):
        self.master.title('天气预报—中国天气网')
        self.master.bg='white'
        
        #self.master.geometry("{}x{}".format(self.width, self.height))



    def choice_text1(self):
            self.choice_pro.set(self.choiceprovince.get(ACTIVE))
            self.choicecity.delete(0,END)
            for i,each in enumerate(self.city[self.choice_pro.get()].keys()):
                self.choicecity.insert(END,each)
                
            #print(choice_pro)
    def choice_text2(self):
            self.choice_city.set(self.choicecity.get(ACTIVE))
            self.city_weather.delete(0,END)
            for i,each in enumerate(get_weather(self.city[self.choice_pro.get()][self.choice_city.get()])):
                self.city_weather.insert(END,each)
            
            #print(choice_city)
        
    def fm1(self):
        self.fm1=Frame(self,bg='white')
        self.fm1.pack(side='left',expand='no',fill='both',padx=5, pady=5)
        
        self.titleLabe1=Label(self.fm1,text="选择省份",fg = "white",bg='blue')
        self.titleLabe1.pack(side='top',fill='x')

        self.choicebutton1=Button(self.fm1,text='确定',command=self.choice_text1)
        self.choicebutton1.pack(side='bottom', fill='x')

        self.scrollbar1=Scrollbar(self.fm1)
        self.scrollbar1.pack(side='right',fill='y')
        
        self.choiceprovince=Listbox(self.fm1,yscrollcommand=self.scrollbar1.set)
        self.choiceprovince.pack(side='left',fill='y')
        for i,each in enumerate(self.city.keys()):
            self.choiceprovince.insert(END,each)   

        

    def fm2(self):
        
        self.fm2=Frame(self,bg='white')
        self.fm2.pack(side='left',expand='no',fill='both',padx=5, pady=5)
        
        self.titleLabe2=Label(self.fm2,text="选择城市",fg = "white",bg='blue')
        self.titleLabe2.pack(side='top',fill='x')

        
        self.label=Label(self.fm2,textvariable=self.choice_pro)
        self.label.pack(fill='x')

        
        self.choicebutton2=Button(self.fm2,text='确定',command=self.choice_text2)
        self.choicebutton2.pack(side='bottom', fill='x')

        self.scrollbar2=Scrollbar(self.fm2)
        self.scrollbar2.pack(side='right',fill='y')
        
        self.choicecity=Listbox(self.fm2,yscrollcommand=self.scrollbar2.set)
        self.choicecity.pack(side='left',fill='y')
        for i,each in enumerate(self.city[self.choice_pro.get()].keys()):
                self.choicecity.insert(END,each)
        
        

    def fm3(self):
        self.fm3=Frame(self,bg='white')
        self.fm3.pack(side='right',expand='yes',fill='both',padx=5, pady=5)
        
        self.titleLabe3=Label(self.fm3,text="城市天气预报（7日内）",fg = "white",bg='blue')
        self.titleLabe3.pack(side='top',fill='x')

        
        self.labe2=Label(self.fm3,textvariable=self.choice_pro)
        self.labe2.pack(side='top',fill='x')
        self.labe3=Label(self.fm3,textvariable=self.choice_city)
        self.labe3.pack(side='top',fill='x')

        self.choicebutton3=Button(self.fm3,text='退出',command=self.quit)
        self.choicebutton3.pack(side='bottom', fill='x')
     
        
        self.scrollbar3=Scrollbar(self.fm3)
        self.scrollbar3.pack(side='right', fill='y')
        
        self.city_weather=Listbox(self.fm3,yscrollcommand=self.scrollbar3.set)
        self.city_weather.pack(side='left', expand='yes',fill='both')
        for i,each in enumerate(get_weather(self.city[self.choice_pro.get()][self.choice_city.get()])):
                self.city_weather.insert(END,each)



def city_weather():
    
    city = get_mongodbmessage()
    app = Application(city)
    app.mainloop()
    
    '''
    province_choice=g.choicebox('选择省份','天气查询',city.keys())
    city_choice = g.choicebox('选择城市','天气查询',city[province_choice].keys())
    g.textbox(city_choice+'七日内天气情况','天气查询',get_weather(city[province_choice][city_choice]))
    '''
    sys.exit()



if __name__=="__main__":

    city_weather()
    

