
try:
    import requests
    import urllib.request
    import os
    os.system('cls')
    import json
    import configparser
    from bs4 import BeautifulSoup
    import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    import colorama
    from colorama import init, Fore, Back, Style
    init()
except:
    print("[ERROR] There was an issue importing the required modules, make sure to install all modules in requirements.txt.")
    input()

path = os.getcwd()
folder_path = (fr'{path}\\Ads')
test = os.listdir(folder_path)

for images in test:
    if images.endswith(".mp3"):
        os.remove(os.path.join(folder_path, images))
for images in test:
    if images.endswith(".png"):
        os.remove(os.path.join(folder_path, images))

config = configparser.ConfigParser()
config.read_file(open(r"Setup.ini"))

cookie = str(config.get("roblox","cookie"))
email = str(config.get("bloxbiz","email"))
password = str(config.get("bloxbiz","password"))
res2 = ""
def login(mail,password):
    global res2
    s = requests.Session()
    payload = {
        "audience": "https://dev.bloxbiz.com",
        "client_id": "4CUqNqmxQH9gkoHH6JadmtGp3R3Eq5DM",
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "password": password,
        "realm": "Username-Password-Authentication",
        "scope": "openid profile email",
        "username": mail
        }
    try:  
        res = s.post("https://dev-4bkwj9o4.us.auth0.com/oauth/token",json=payload)
        s.headers.update({'authorization': json.loads(res.content)['access_token']})
        res = res.json()
        res2 = res['access_token']
    except:
        print(f"{Fore.RED}[ERROR] Your bloxbiz credentials are invalid.")
        input()
    return s

session = login(email,password)

headers = {
    'authorization': f"Bearer {res2}",
    'user-agent': 'Bloxbiz Uploader (https://github.com/Adaaks/Bloxbiz-Uploader)'
    }
lol = session.get("https://portal-api.bloxbiz.com/dev/account/details", headers=headers)
lol = lol.json()
bloxbizid = lol['data']['bloxbiz_id']
apikey = lol['data']['api_key']
first_name = lol['data']['first_name']

import json
import datetime

print(f"{Fore.GREEN}Welcome, {first_name} - you have successfully logged in to bloxbiz.")
print(f"{Fore.MAGENTA}Please wait whilst I'm loading your games.")
print("\n")

getgameid = session.get("https://portal-api.bloxbiz.com/dev/games/list?with_live_status=false",headers=headers)
getgameid = getgameid.json()
count = 0
##################
gameid = 0
countads = 0
advertname = ""
class RevenueScraper():



    def scrape(self, data):
        """Totals revenue for each month

        Keyword arguments:
        json_dict -- The python dictionary containing data from json
        Return: Dict
        """
        month_dict = {
            "January": [],
            "February": [],
            "March": [],
            "April": [],
            "May": [],
            "June": [],
            "July": [],
            "August": [],
            "September": [],
            "October": [],
            "November": [],
            "December": [],
        }
        for entry in data["data"]:
            try:
                
                data = datetime.datetime.strptime(entry["end_day"], "%Y-%m-%d")
                month = data.strftime("%B")
            except:
                continue
                
             
            try:
                month_dict[month].append(entry["report_contents"]["Amount Earned"])
            except:
                continue
        for k, v in month_dict.items():
            month_dict[k] = round(sum(v),2)
        return month_dict
count = 0


    
print(f"{Fore.CYAN}Please select a game, reply with a number choice.")

ask2 = getgameid['data']
list = []
max = 0
for data in ask2:
    max+=1
    list.append(data)

actualmax = max
max = -1
current = 1
actualcurrent = 0
for i in range(actualmax):
    gamename = getgameid['data'][actualcurrent]['game_name']
    print(f"{Fore.YELLOW}[{current}] {gamename}")
    current +=1
    actualcurrent +=1
print("\n")
def inputs2():
    global gameid
    try:

        whichone = int(input(f"{Fore.MAGENTA}Enter your choice: "))
    

        if whichone <= actualmax and whichone >= 1:
            gamename = getgameid['data'][whichone-1]['game_name']
            gameid = getgameid['data'][whichone-1]["game_id"]
            print("\n")
            print(f"{Fore.CYAN}Game: {gamename}")
        else:
            print(f"{Fore.RED}Error, please choose between games: 1-{actualmax}")
            print("\n")
            inputs2()
    
    except:
        print(f"{Fore.RED}Error, invalid input - enter numbers only.")
        print("\n")
        inputs2()
        
inputs2()

revenuedata = {
    "category": "revenue",
    "end_day": "2099-08-30",
    "game_id": gameid,
    "report_type": "daily_performance",
    "start_day": "2020-01-01"
    }

send1 = session.post("https://portal-api.bloxbiz.com/dev/reports",headers=headers,json=revenuedata)
send1 = send1.json()
scraper = RevenueScraper()
response = scraper.scrape(send1)

current = datetime.date.today()
current2 = current.strftime("%B")
_first_day = current.replace(day=1)
prev_month_lastday = _first_day - datetime.timedelta(days=1)
previous = prev_month_lastday.replace(day=1)
previous = previous.strftime("%B")


print(f"{Fore.CYAN}Current Month: $ {response[current2]}")
print(f"{Fore.CYAN}Last Month: $ {response[previous]}")
print("\n")
    








####################################################
        
getads = f"https://portal-api.bloxbiz.com/dev/dev_campaign_manager/list?game_id={gameid}&bloxbiz_id={bloxbizid}"
trs = session.get(getads,headers=headers)
trs = trs.json()
           
assetid = ""
guid = 0
ad_idx = 0
gif = False
static = False
countuploaded = 0

class DecalClass():
    def __init__(self, cookie):
        
        try:
            self.goose = requests.Session()
            self.goose.cookies.update({
                '.ROBLOSECURITY': cookie
            })
            self.goose.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134", #might as well use a User Agent
            })
        except:
            print(f"{Fore.RED}[ERROR] Invalid roblox cookie, please check setup.ini.")
            input()
            
    def getToken(self): 
        homeurl= 'https://www.roblox.com/build/upload' 
        response = self.goose.get(homeurl, verify=False)
        
        try:
            soup = BeautifulSoup(response.text, "lxml")
            try: 
                veri = soup.find("input", {"name" : "__RequestVerificationToken"}).attrs["value"]
            except:
                print(f"{Fore.RED}[ERROR] Invalid roblox cookie, please check setup.ini\n- Ensure you include the full cookie\n- Ensure the cookie is not in speech marks\n- Ensure it's still valid")
                input()
        except NameError:
            print(NameError)
            return False
        return veri
    
    def upload(self):
        global assetid, bloxbizid, gameid, guid, countuploaded
        path = os.getcwd()
        path = f"{path}\\Ads"
        
        with open(f"{path}\\{os.listdir(path)[0]}", 'rb') as f:
            files = {'file': ('lol.png', f, 'image/png')} 
            data = {
                '__RequestVerificationToken': self.getToken(),
                'assetTypeId': '13', 
                'isOggUploadEnabled': 'True',
                'isTgaUploadEnabled': 'True',
                
                'onVerificationPage': "False",
                "captchaEnabled": "True",
                'name': "Bloxbiz"
            }
            response = self.goose.post('https://www.roblox.com/build/upload', files=files, data=data)
            responseurl = response.url
            new = responseurl.split("=")
            assetid = new[2]
            
        path = os.getcwd()
        folder_path = (fr'{path}\\Ads')
        test = os.listdir(folder_path)
        
        for images in test:
            if images.endswith(".png"):
                os.remove(os.path.join(folder_path, images))
        session = login(email,password)
        finalone = f"https://portal-api.bloxbiz.com/dev/ad/update_dev_ad_asset/{guid}"
        
        if gif == True and static == False:
            payload={
              "game_id": gameid,
              "bloxbiz_id": bloxbizid,
              "dev_creative_asset_url": f"https://www.roblox.com/catalog/{assetid}/Bloxbiz",
              "sheet_index": ad_idx
              }
            
        elif static == True and gif == False:
            payload={
                "game_id": gameid,
                "bloxbiz_id": bloxbizid,
                "dev_creative_asset_url": f"https://www.roblox.com/catalog/{assetid}/Bloxbiz"
                }
            
        headers = {
            
            'authorization': f"Bearer {res2}",
            'user-agent': 'Bloxbiz Uploader (https://github.com/Adaaks/Bloxbiz-Uploader)'
            }
        
        finalone1 = session.post(finalone,headers=headers,json=payload)
        
        if finalone1.status_code == 200:
            countuploaded+=1
            print(f"{Fore.YELLOW}[{countuploaded}/{countads}]{Fore.GREEN} Successfully uploaded a decal ({advertname}).")
        else:
            print(f"{Fore.RED}[ERROR - {finalone1.status_code}] Failed to upload a decal")

class AudioClass():
    def __init__(self, cookie):

        try:
            self.goose = requests.Session()
            self.goose.cookies.update({
                '.ROBLOSECURITY': cookie
            })
            self.goose.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
                # might as well use a User Agent
            })
        except:
            print(f"{Fore.RED}[ERROR] Invalid roblox cookie, please check setup.ini.")
            input()

    def getToken(self):
        homeurl = 'https://www.roblox.com/build/upload'
        response = self.goose.get(homeurl, verify=False)

        try:
            soup = BeautifulSoup(response.text, "lxml")
            try:
                veri = soup.find("input", {"name": "__RequestVerificationToken"}).attrs["value"]
            except:
                print(
                    f"{Fore.RED}[ERROR] Invalid roblox cookie, please check setup.ini\n- Ensure you include the full cookie\n- Ensure the cookie is not in speech marks\n- Ensure it's still valid")
                input()
        except NameError:
            print(NameError)
            return False
        return veri

    def upload(self):
        global assetid, bloxbizid, gameid, guid, countuploaded
        path = os.getcwd()
        path = f"{path}\\Ads"

        with open(f"{path}\\{os.listdir(path)[0]}", 'rb') as f:
            files = {'file': ('lol.mp3', f, 'audio/wav')}
            data = {
                '__RequestVerificationToken': self.getToken(),
                'assetTypeId': '3',
                'isOggUploadEnabled': 'True',
                'isTgaUploadEnabled': 'True',

                'onVerificationPage': "False",
                "captchaEnabled": "True",
                'name': f"{filename}"
            }
            response = self.goose.post('https://www.roblox.com/build/upload', files=files, data=data)
            responseurl = response.url
            new = responseurl.split("=")
            assetid = new[2]


        path = os.getcwd()
        folder_path = (fr'{path}\\Ads')
        test = os.listdir(folder_path)

        for images in test:
            if images.endswith(".mp3"):
                os.remove(os.path.join(folder_path, images))
        for images in test:
            if images.endswith(".png"):
                os.remove(os.path.join(folder_path, images))


        session = requests.Session()
        session.cookies[".ROBLOSECURITY"] = cookie
        req = session.post(
            url="https://auth.roblox.com/"
        )
        if "X-CSRF-Token" in req.headers:
            session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
        req2 = session.post(
            url="https://auth.roblox.com/"
        )
        check = session.get('https://api.roblox.com/currency/balance')
        headers = {

            'X-CSRF-Token': f'{session.headers["X-CSRF-Token"]}',
            'Cookie': f'.ROBLOSECURITY={cookie}'

        }
        data2 = {
            "requests": [
                {
                    "action": "Use",
                    "subjectId": f"{gameid}",
                    "subjectType": "Universe",

                }
            ]
        }
        url2 = f"https://apis.roblox.com/asset-permissions-api/v1/assets/{assetid}/permissions"
        grantperms = session.patch(url2, headers=headers,json=data2)


        session = login(email, password)
        finalone3 = f"https://portal-api.bloxbiz.com/dev/ad/update_dev_ad_asset/{guid}"

        data69 = {
            "bloxbiz_id": bloxbizid,
            "dev_creative_asset_url": f"https://www.roblox.com/catalog/{assetid}/",
            "game_id": gameid,
            "sheet_index": "audio"
        }

        headers = {

            'authorization': f"Bearer {res2}",
            'user-agent': 'Bloxbiz Uploader (https://github.com/Adaaks/Bloxbiz-Uploader)'
        }

        finalone3 = session.post(finalone3, headers=headers, json=data69)


        if finalone3.status_code == 200:
            countuploaded += 1
            print(f"{Fore.YELLOW}[{countuploaded}/{countads}]{Fore.GREEN} Successfully uploaded a audio ({advertname}).")
        else:
            print(f"{Fore.RED}[ERROR - {finalone3.status_code}] Failed to upload a audio.")
filename = ""

class CountScraper():
    def scrape(self, data):
        global assetid, headers, guid, gif, static, ad_idx, filename, countads
        drls = []
        for campain in data["data"]:
            for ad in campain["ads"]:
                if ad.get("dev_creative_asset_url") is None:
                    if ad.get("creative_audio_s3") is not None:
                        if ad.get("creative_audio_s3") not in drls:
                            drls.append(ad.get("creative_audio_s3"))
                            countads+=1
                if ad["ad_url"] is None:
                    continue
                for ad_idx, ad_url in enumerate(ad["ad_url"],0):
                    if type(ad_url) == str:
                        if ad.get("dev_ad_url") is None:
                            if ad["creative_asset_s3"] not in drls:
                                
                                drls.append(ad["creative_asset_s3"])
                                countads+=1
                                
                        continue
                    if ad_url.get("dev_ad_url") is None:
                        if ad_url["creative_asset_s3"] not in drls:
                            
                                drls.append(ad_url["creative_asset_s3"])
                                countads+=1
                                     
        return drls

scrapers = CountScraper()
drls = scrapers.scrape(trs) 


class DataScraper():
    def scrape(self, data):
        global assetid, headers, guid, gif, static, ad_idx, filename,advertname
        urls = []
        for campain in data["data"]:
            advertname = campain.get('campaign_name')
            for ad in campain["ads"]:
                if ad.get("dev_creative_asset_url") is None:
                    if ad.get("creative_audio_s3") is not None:
                        if ad.get("creative_audio_s3") not in urls:
                            urls.append(ad.get("creative_audio_s3"))
                            
                            guid = ad["GUID"]
                            path = os.getcwd()
                            lol2 = ad["creative_audio_url"]
                            new = lol2.split("/")
                            filename = new[5]
                            urllib.request.urlretrieve(ad["creative_audio_s3"], f"{path}\\Ads\\{filename}.mp3")
                            static = False
                            gif = False

                            Audio = AudioClass(cookie)
                            Audio.upload()
                if ad["ad_url"] is None:
                    continue
                for ad_idx, ad_url in enumerate(ad["ad_url"],0):
                    if type(ad_url) == str:
                        if ad.get("dev_ad_url") is None:
                            if ad["creative_asset_s3"] not in urls:
                                
                                urls.append(ad["creative_asset_s3"])
                                guid = ad["GUID"]
                                path = os.getcwd()
                                urllib.request.urlretrieve(ad["creative_asset_s3"], f"{path}\\Ads\\{guid}.png")
                                static = True
                                gif = False
                                Decal = DecalClass(cookie)
                                Decal.upload()
                                
                        continue
                    if ad_url.get("dev_ad_url") is None:
                        if ad_url["creative_asset_s3"] not in urls:
                                
                                urls.append(ad_url["creative_asset_s3"])
                                guid = ad["GUID"]
                                path = os.getcwd()
                                urllib.request.urlretrieve(ad_url["creative_asset_s3"], f"{path}\\Ads\\{guid}.png")
                                gif = True
                                static = False
                                Decal = DecalClass(cookie)
                                Decal.upload()
                                     
        return urls

scraper = DataScraper()
urls = scraper.scrape(trs) 
print(f"{Fore.GREEN}Completed uploading all adverts.")
input()                
