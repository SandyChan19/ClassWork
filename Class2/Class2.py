from bs4 import BeautifulSoup
import time
import requests
import math
import random
import json
import pymongo


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
csrf_token = ''

conn = pymongo.MongoClient(host = '127.0.0.1', port = 27017)
db = conn['DataBase1']
newsdata = db['NewData']

def getData(id):

    postId = ''
    title = ''
    location = ''
    price = ''
    houseKind = ''
    houseType = ''
    mobile = ''
    phone = ''
    area  = ''
    section  = ''
    deposit = ''
    ping = ''
    floor = ''
    houseOwner = ''
    lessor = ''
    lessorRole = ''        
    lessorGender = ''
    lessorLastname = '' 
    renterGender = '' 
    posttime = '' 

    headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-HK,zh-CN;q=0.9,zh;q=0.8',            
            'User-Agent': user_agent,
            #'Cookie': 'webp=1; Domain=.591.com.tw; Path=/',
            'X-CSRF-TOKEN': csrf_token,
            'device': 'pc',
            'deviceid': 'k7mm7be8pnd9023ng49qb29j87',
            'Referer': 'https://rent.591.com.tw/'
            }    

    review_url = 'https://api.591.com.tw/tw/v1/house/rent/detail?id=' + str(id) + '&isOnline=1'
    res = requests.get(review_url, headers = headers) 
    room_data_json = json.loads(res.text)

    row_status = room_data_json['status']

    if row_status != 0 :
        room_data = room_data_json['data']

        postId = id
        title = room_data['favData']['title']
        address = room_data['favData']['address']
        price = room_data['favData']['price']
        houseKind = room_data['favData']['kindTxt']
        ping = room_data['favData']['area']
        posttime = room_data['favData']['posttime']
        mobile = room_data['linkInfo']['mobile']
        phone = room_data['linkInfo']['phone']
        area  = str(room_data['breadcrumb'][0]['name'])[0:2]           
        section  = room_data['breadcrumb'][1]['name']
        deposit = room_data['deposit']        
        floor = room_data['info'][2]['value']
        houseOwner = room_data['linkInfo']['imName']
        lessor = room_data['linkInfo']['name']

        infoDatas = room_data['infoData']['data']

        for attrs in infoDatas:
            if attrs['key'] == 'shape':
                houseType = attrs['value']
                break

        role  = room_data['linkInfo']['role']
        if role == 1:
            lessorRole = '屋主'
        elif role == 2:
            lessorRole = '代理人'
        elif role == 3:
            lessorRole = '仲介'

        if str(room_data['linkInfo']['imName']) != '':
            if str(room_data['linkInfo']['imName']).__contains__('先生'):
                lessorGender = '男' 
            else:
                lessorGender = '女'
            lessorLastname = str(room_data['linkInfo']['imName'])[0] 

        renterGender = '不拘'
        if str(room_data['service']['rule']).__contains__('限女生'):
            renterGender = '女'
        if str(room_data['service']['rule']).__contains__('限男生'):
            renterGender = '男'    

        newsdata.insert_one({'postId' : postId, 'address' : address, 'title' : title, 'location' : location, 'price' : price
        , 'houseKind' : houseKind, 'houseType' : houseType, 'mobile' : mobile, 'phone' : phone, 'area' : area, 'section' : section
        , 'deposit' : deposit, 'ping' : ping, 'floor' : floor, 'houseOwner' : houseOwner, 'lessor' : lessor, 'posttime' : posttime
        , 'lessorRole' : lessorRole, 'lessorGender' : lessorGender, 'lessorLastname' : lessorLastname, 'renterGender' : renterGender})
    
def main():   

    for regionid in [1, 3]:
        geturl = 'https://rent.591.com.tw/?kind=0&region=' + str(regionid)
        
        res = requests.get(geturl, headers = { 'user-agent': user_agent,
                                                'Referer': 'https://rent.591.com.tw/' })
        bs = BeautifulSoup(res.text, 'html.parser') 

        meta_token = bs.find('meta',  {'name':'csrf-token'})
        csrf_token = meta_token['content'] 

        session_token = res.headers['set-cookie']
        str_start = session_token.find('591_new_session')
        str_end = len(session_token)
        session = session_token[str_start : str_end]

        #Get total rows
        total_rows = int(bs.find('span', {'class':'R'}).text.split(' ')[-2])

        headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-HK,zh-CN;q=0.9,zh;q=0.8',            
                'User-Agent': user_agent,
                'Referer': 'https://rent.591.com.tw/?kind=0&region=' + str(regionid),
                'Cookie': 'urlJumpIp={}; {};'.format(6 , session),
                'X-CSRF-TOKEN': csrf_token
                }           
        
        pageRow = int(0)        

        while pageRow > total_rows:
            review_url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=' + str(regionid) + '&firstRow=' + str(pageRow) + '&totalRows=' + str(total_rows).strip()
            respage = requests.get(review_url, headers = headers)
            print('res.current_url = ' ,respage.url)

            room_url_list = []
            room_json = json.loads(respage.text)
            room_list = room_json['data']['data']

            for roomid in room_list:
                print('roomid = ', roomid['post_id'])
                getData(roomid['post_id'])
                time.sleep(random.randint(1,10))

            pageRow = pageRow + 30 
            time.sleep(random.randint(1,10))



if __name__ == '__main__':
    main()
    print('\nfinish!')
