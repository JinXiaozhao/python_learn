# config
#my_sender = ''  # 发件人邮箱账号
#my_pass = ''  # 发件人邮箱密码
#my_name = " "  # 发件人邮箱昵称
# recipients = ''  # 收件人邮箱账号
#re_name = ' '  # 收件人邮箱昵称
#mail_subject = "天气预报"  # 邮件的主题，也可以说是标题
import pymongo
import random
import requests
import time
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from tkinter import *
import traceback

# 获取城市代码


def get_mongodbmessage():
    message = {}
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client.china_city
    collection = db.province
    for each in collection.find():
        message[each['_id']] = each[each['_id']]
    return message

# 爬取城市天气网页


def url_open(city_code):
    url = 'http://www.weather.com.cn/weather/' + city_code + '.shtml'
    headers = {}
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
    agent = random.choice(user_agents)
    headers['User-Agent'] = agent
    try:
        req = requests.get(url=url, headers=headers)
    except:
        time.sleep(1)
        req = requests.get(url=url, headers=headers)
    html = req.content.decode('utf-8')
    return html


# 获取城市天气信息
def get_weather(city_code):
    html = url_open(city_code)
    selector = etree.HTML(html)
    weather_text = []
    for i in range(1, 8):
        # 日期
        weather_text.append('*********************************\n')
        data_x = '//*[@id="7d"]/ul/li[' + str(i) + ']/h1/text()'
        data = selector.xpath(data_x)
        weather_text.append('日期为：' + data[0] + '\n')

        # 天气
        weather_x = '//*[@id="7d"]/ul/li[' + str(i) + ']/p[1]/text()'
        weather = selector.xpath(weather_x)
        weather_text.append('天气状况为：' + weather[0] + '\n')

        # 温度
        t_hx = '//*[@id="7d"]/ul/li[' + str(i) + ']/p[2]/*/text()'
        T_h = selector.xpath(t_hx)
        if len(T_h) == 2:
            weather_text.append('最高温度为：' + T_h[0] + '\n')
            weather_text.append('最低温度为：' + T_h[1] + '\n')
        else:
            weather_text.append('温度为：' + T_h[0] + '\n')

        # 风向
        wind_x = '//*[@id="7d"]/ul/li[' + str(i) + ']/p[3]/em/span/@title'
        wind_direct = selector.xpath(wind_x)
        win = set(wind_direct)

        if len(win) == 2:
            weather_text.append('风向为：' + wind_direct[0] + '转' + wind_direct[-1] + '\n')
        else:
            weather_text.append('风向为：' + wind_direct[0] + '\n')

        # 风力
        wind_y = '//*[@id="7d"]/ul/li[' + str(i) + ']/p[3]/i/text()'
        wind = selector.xpath(wind_y)
        weather_text.append('风力为：' + wind[0] + '\n')
    weather_text.append('*********************************\n')
    return weather_text


# 发送天气邮件
def mail(sender_mail, sender_key,
         mail_title, recipients_mail,
         weather_text, province, city):

    my_sender = sender_mail
    recipients = recipients_mail
    my_pass = sender_key
    mail_subject = mail_title

    re_name = ' '
    my_name = ' '
    mail_text = province + ' ' + city + '\n' + ' '.join(weather_text)
    print(mail_text)
    ret = True
    msg = MIMEMultipart()
    main_text = MIMEText(mail_text, 'plain', 'utf-8')
    msg.attach(main_text)
    msg['From'] = formataddr([my_name, my_sender])
    msg['To'] = formataddr([re_name, recipients])
    msg['Subject'] = mail_subject

    try:
        server = smtplib.SMTP_SSL("smtp.163.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [recipients, ], msg.as_string())
        server.quit()
    except:
        ret = False
    return ret

# 界面


class App(Frame):
    def __init__(self, city_list, master=None):
        self.city_list = city_list
        Frame.__init__(self, master, bg='white')
        self.pack(expand=YES, fill=BOTH)
        self.master.title('天气预报—中国天气网')
        self.master.bg = 'white'
        self.province = StringVar()
        self.city = StringVar()
        self.weather_text = []
        self.fm1()
        self.fm2()
        self.fm3()
        self.fm4()

    def show_city(self):

        self.city.set('')

        self.weather_text.clear()
        self.city_weather.delete(0, END)
        for each in self.weather_text:
            self.city_weather.insert(END, each)

        self.province.set(self.choice_province.get(ACTIVE))
        self.choice_city.delete(0, END)
        for each in self.city_list[self.province.get()].keys():
            self.choice_city.insert(END, each)

    def show_weather(self):

        self.city.set(self.choice_city.get(ACTIVE))

        self.city_weather.delete(0, END)
        self.weather_text.clear()
        self.weather_text = get_weather(self.city_list[self.province.get()][self.city.get()])
        for each in self.weather_text:
            self.city_weather.insert(END, each)

    def fm1(self):
        fma = Frame(self)
        fma.pack(side='left', expand='no', fill='both', padx=5, pady=5)

        label_title = Label(fma, text='选择省份', fg="white", bg='blue')
        label_title.pack(side='top', fill='x', padx=5, pady=5)

        choice_button = Button(fma, text='确定', command=self.show_city)
        choice_button.pack(side='bottom', fill='x', padx=5, pady=5)

        scrollbar = Scrollbar(fma)
        scrollbar.pack(side='right', fill='y')

        self.choice_province = Listbox(fma, yscrollcommand=scrollbar.set)
        self.choice_province.pack(side='left', fill='y')

        for i, each in enumerate(self.city_list.keys()):
            self.choice_province.insert(END, each)
        scrollbar.config(command=self.choice_province.yview)

    def fm2(self):
        fmb = Frame(self)
        fmb.pack(side='left', expand='no', fill='both', padx=5, pady=5)

        label_title = Label(fmb, text='选择城市', fg="white", bg='blue')
        label_title.pack(side='top', fill='x', padx=5, pady=5)

        label_province = Label(fmb, textvariable=self.province).pack(side='top', fill='x')

        choice_button = Button(fmb, text='确定', command=self.show_weather)
        choice_button.pack(side='bottom', fill='x', padx=5, pady=5)

        scrollbar = Scrollbar(fmb)
        scrollbar.pack(side='right', fill='y')

        self.choice_city = Listbox(fmb, yscrollcommand=scrollbar.set)
        self.choice_city.pack(side='left', fill='y')

        if self.province.get():
            for each in self.city_list[self.province.get()].keys():
                self.choice_city.insert(END, each)
        scrollbar.config(command=self.choice_city.yview)

    def fm3(self):
        fma = Frame(self)
        fma.pack(side='left', expand='no', fill='both', padx=5, pady=5)

        label_title = Label(fma, text='天气预报（7日内）', fg="white", bg='blue')
        label_title.pack(side='top', fill='x', padx=5, pady=5)

        label_province = Label(fma, textvariable=self.province).pack(side='top')
        label_city = Label(fma, textvariable=self.city).pack(side='top')

        choice_button = Button(fma, text='退出系统', command=self.quit)
        choice_button.pack(side='bottom', fill='x', padx=5, pady=5)

        scrollbar = Scrollbar(fma)
        scrollbar.pack(side='right', fill='y')

        self.city_weather = Listbox(fma, yscrollcommand=scrollbar.set)
        self.city_weather.pack(side='left', expand='yes', fill='y')

        if self.province.get() and self.city.get():
            self.weather_text = get_weather(self.city_list[self.province.get()][self.city.get()])
        else:
            self.weather_text.clear()
        for each in self.weather_text:
            self.city_weather.insert(END, each)
        scrollbar.config(command=self.city_weather.yview)

    def fm4(self):

        def send_email():
            ret = mail(sender_mail.get(), sender_key.get(),
                       mail_title.get(), recipients_mail.get(),
                       self.weather_text, self.province.get(), self.city.get())
            if ret:
                var_result.set('发送成功！')
            else:
                var_result.set('发送失败！')

        fma = Frame(self)
        fma.pack(side='left', expand='no', fill='both', padx=5, pady=5)

        label_title = Label(fma, text='天气情况邮件发送', fg="white", bg='blue')
        label_title.pack(side='top', fill='x', padx=5, pady=5)

        label_sender = Label(fma, text='寄件人邮箱：\n（仅限网易163邮箱）')\
            .pack(side='top', fill='x')
        sender_mail = StringVar()
        sender = Entry(fma, textvariable=sender_mail)
        sender.pack(side='top', fill='x')

        label_sender_key = Label(fma, text='邮箱密码：')\
            .pack(side='top', fill='x')
        sender_key = StringVar()
        sender_pass = Entry(fma, textvariable=sender_key, show='*')
        sender_pass.pack(side='top', fill='x')

        label_mail_title = Label(fma, text='邮件主题：') \
            .pack(side='top', fill='x')
        mail_title = StringVar()
        input_mail_title = Entry(fma, textvariable=mail_title)
        input_mail_title.pack(side='top', fill='x')

        label_recipients = Label(fma, text='收件人邮箱：')\
            .pack(side='top', fill='x')
        recipients_mail = StringVar()
        recipients = Entry(fma, textvariable=recipients_mail)
        recipients.pack(side='top', fill='x')

        var_result = StringVar()
        label_result = Label(fma, textvariable=var_result, fg="white", bg='blue') \
            .pack(side='top', fill='x')

        choice_button = Button(fma, text='发送', command=send_email)
        choice_button.pack(side='bottom', fill='x', padx=5, pady=5)


def weather_main():
    city_list = get_mongodbmessage()
    app = App(city_list)
    app.mainloop()


if __name__ == '__main__':
    try:
        weather_main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        input()
