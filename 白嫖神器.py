#C:\Users\zty22\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.8
#-*- coding: utf-8 -*-
# =============================================================================
import os
import requests
from tqdm import tqdm

# 定义相关参数
url = 'https://music.sonimei.cn' # 下载接口
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
           'Accept':'application/json, text/javascript, */*; q=0.01',
           'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Accept-Encoding':'gzip, deflate, br',
           'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With':'XMLHttpRequest',
           'Content-Length':'53',
           'Connection':'keep-alive'} # 请求头
data = {'input':'',
        'filter':'name',
        'type':'qq',
        'page':1} # 请求参数
savePath = './musics' # 音乐保存目录

# 检查存储路径是否存在
if not os.path.exists(savePath):
    os.mkdir(savePath)

# 欢迎界面
welcome = '''

|______|______|________|
                |______________|

         '''
os.system('cls')
os.system('mode con cols=85 lines=25')
print(welcome)
# 循环开始
while True:
    choice = input('>>>请输入歌名（或歌手）：')
    if choice == 'quit':
        print('欢迎再次使用~')
        break
    data['input'] = choice
    res = requests.post(url,headers=headers,data=data)
    d_json = res.json() # 搜索结果
    musics = d_json['data']
    if d_json['code'] != 200:
        print('搜索结果为空，请重新输入')
        continue
    else:
        print('*'*45)
        print('{0:{3}<4}{1:{3}<10}{2:{3}^10}{3}'.format('序号','歌名','作者',chr(12288)))
        print('*'*45)
        N = 1 # 序号
        for m in musics:
            print('{0:{3}<4}{1:{3}<10}{2:{3}^10}{3}'.format(N,m['title'],m['author'],chr(12288)))
            N += 1
        print('*'*45)
        choice = input('>>>请选择需要下载的歌曲：')
        n = int(choice)
        name = musics[n-1]['title'] # 歌名
        url_download = musics[n-1]['url'] # 下载地址
        bar = tqdm(range(1),ncols=60) # 进度条
        for b in bar:
            res = requests.get(url_download)
            with open('%s/%s.m4a'%(savePath,name),'wb') as f:
                f.write(res.content)
            bar.set_description('下载中')
        
