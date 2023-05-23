
try:
    import time
    from datetime import datetime, timedelta
    import requests
    import urllib.request
    import os
    import ctypes
    import json
    import datetime
    import sys
    ctypes.windll.kernel32.SetConsoleTitleW("Superbiz Uploader - By Adaks")
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
    
my_os=sys.platform
mac=False
windows=False

if my_os=="darwin":
    mac=True
else:
    windows=True

path = os.getcwd()
folder_path = path
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
email = str(config.get("superbiz","email"))
password = str(config.get("superbiz","password"))
groupid = str(config.get("roblox","groupid"))

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
        print(f"{Fore.RED}[ERROR] Your superbiz credentials are invalid.")
        time.sleep(5)
    return s

session = login(email,password)

headers = {
    'authorization': f"Bearer {res2}",
    'user-agent': 'Superbiz Uploader (https://github.com/Adaaks/Superbiz-Uploader)'
    }
lol = session.get("https://portal-api.bloxbiz.com/dev/account/details", headers=headers)
lol = lol.json()
bloxbizid = lol['data']['bloxbiz_id']
apikey = lol['data']['api_key']
first_name = lol['data']['first_name']

print(f"{Fore.GREEN}Welcome, {first_name} - you have successfully logged in to superbiz.")
print(f"{Fore.MAGENTA}Please wait whilst I'm loading your games.")
print("\n")

getgameid = session.get("https://portal-api.bloxbiz.com/games/list?with_live_status=false",headers=headers)
getgameid = getgameid.json()
count = 0
##################
gameid = 0
countads = 0
advertname = ""

path = os.getcwd()
folder_path = path

for images in test:
    if images.endswith(".txt"):
        os.remove(os.path.join(folder_path, images))

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

if actualmax == 0:
    print(f"{Fore.RED}You have no games connected to superbiz.")
    input()
else:
    print(f"{Fore.CYAN}Please select a game, reply with a number choice.")
for i in range(actualmax):
    gamename = getgameid['data'][actualcurrent]['game_name']
    print(f"{Fore.YELLOW}[{current}] {gamename}")
    current +=1
    actualcurrent +=1

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
            print(f"{Fore.RED}Please choose between games: 1-{actualmax}")
            print("\n")
            inputs2()
    
    except:
        print(f"{Fore.RED}Invalid input - enter numbers only.")
        print("\n")
        inputs2()
        
inputs2()

headers["x-game-id"] = "% s" % gameid
headers["x-bloxbiz-id"] = "% s" % bloxbizid

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
        
getads = f"https://portal-api.bloxbiz.com/dev_campaign_manager/list?game_id={gameid}&bloxbiz_id={bloxbizid}"
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
                print(f"{Fore.RED}Invalid roblox cookie, please check setup.ini\n- Ensure you include the full cookie\n- Ensure the cookie is not in speech marks\n- Ensure it's still valid")
                input()
        except NameError:
            print(NameError)
            return False
        return veri
    
    def upload(self):
        global assetid, bloxbizid, gameid, guid, countuploaded
        path = os.getcwd()
        folder_path = path

        if windows == True:
            
            with open(f"{path}\\{guid}.png", 'rb') as f:
                files = {'file': ('lol.png', f, 'image/png')} 

                if int(groupid) > 100:
                    data = {
                        '__RequestVerificationToken': self.getToken(),
                        'assetTypeId': '13', 
                        'isOggUploadEnabled': 'True',
                        'isTgaUploadEnabled': 'True',
                        
                        'onVerificationPage': "False",
                        "captchaEnabled": "True",
                        'name': "Superbiz",
                        'groupId': groupid
                    }
                else:
                    data = {
                        '__RequestVerificationToken': self.getToken(),
                        'assetTypeId': '13', 
                        'isOggUploadEnabled': 'True',
                        'isTgaUploadEnabled': 'True',
                        
                        'onVerificationPage': "False",
                        "captchaEnabled": "True",
                        'name': "Superbiz"
                    }
                    
                response = self.goose.post('https://www.roblox.com/build/upload', files=files, data=data)
                responseurl = response.url
                new = responseurl.split("=")

                if int(groupid) > 100:
                    assetid = new[3]
                else:
                    assetid = new[2]

            if response.status_code == 200:
                print(f"{Fore.GREEN}- Successfully uploaded a decal to roblox")

            else:
                print(f"{Fore.RED}- Failed to upload a decal to roblox")
        elif mac == True:
            with open(f"{path}//{guid}.png", 'rb') as f:
                files = {'file': ('lol.png', f, 'image/png')} 

                if int(groupid) > 100:
                    data = {
                        '__RequestVerificationToken': self.getToken(),
                        'assetTypeId': '13', 
                        'isOggUploadEnabled': 'True',
                        'isTgaUploadEnabled': 'True',
                        
                        'onVerificationPage': "False",
                        "captchaEnabled": "True",
                        'name': "Superbiz",
                        'groupId': groupid
                    }
                else:
                    data = {
                        '__RequestVerificationToken': self.getToken(),
                        'assetTypeId': '13', 
                        'isOggUploadEnabled': 'True',
                        'isTgaUploadEnabled': 'True',
                        
                        'onVerificationPage': "False",
                        "captchaEnabled": "True",
                        'name': "Superbiz"
                    }
                    
                response = self.goose.post('https://www.roblox.com/build/upload', files=files, data=data)
                responseurl = response.url
                new = responseurl.split("=")

                if int(groupid) > 100:
                    assetid = new[3]
                else:
                    assetid = new[2]

            if response.status_code == 200:
                print(f"{Fore.GREEN}- Successfully uploaded a decal to roblox")

            else:
                print(f"{Fore.RED}- Failed to upload a decal to roblox")
            
            
        
        
        finalone = f"https://portal-api.bloxbiz.com/ad/update_dev_ad_asset/{guid}"
        
        if gif == True and static == False:
            payload={
              "game_id": gameid,
              "bloxbiz_id": bloxbizid,
              "dev_creative_asset_url": f"https://www.roblox.com/catalog/{assetid}/Superbiz",
              "sheet_index": ad_idx
              }
            
        elif static == True and gif == False:
            payload={
                "game_id": gameid,
                "bloxbiz_id": bloxbizid,
                "dev_creative_asset_url": f"https://www.roblox.com/catalog/{assetid}/Superbiz"
                }
            
        headers = {
            
            'authorization': f"Bearer {res2}",
            'user-agent': 'Superbiz Uploader (https://github.com/Adaaks/Superbiz-Uploader)',
            'x-game-id': str(gameid),
            'x-bloxbiz-id': str(bloxbizid)
            }
        
        finalone1 = session.post(finalone,headers=headers,json=payload)
        
        if finalone1.status_code == 200:
            countuploaded +=1
            print(f"{Fore.YELLOW}[{countuploaded}/{countads}]{Fore.GREEN} Successfully submitted a decal to superbiz ({advertname})")
            path = os.getcwd()
            folder_path = path

            test = os.listdir(folder_path)

            for images in test:
                if images.endswith(".mp3"):
                    os.remove(os.path.join(folder_path, images))
            for images in test:
                if images.endswith(".png"):
                    os.remove(os.path.join(folder_path, images))
        else:
            print(f"{Fore.YELLOW}[{countuploaded}/{countads}]{Fore.RED} Failed to submit a decal to superbiz ({advertname})")
            
        print("\n")

class AudioClass():
    def __init__(self, cookie):

        try:
            self.goose = requests.Session()
            self.goose.cookies.update({
                '.ROBLOSECURITY': cookie
            })
            self.goose.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
                
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
        path=path
        if windows == True:
            
            with open(f"{path}\\{filename}.mp3", 'rb') as f:
                files = {'file': ('lol.mp3', f, 'audio/wav')}
                if int(groupid) > 100:
                    data = {
                        '__RequestVerificationToken': self.getToken(),
                        'assetTypeId': '3',
                        'isOggUploadEnabled': 'True',
                        'isTgaUploadEnabled': 'True',

                        'onVerificationPage': "False",
                        "captchaEnabled": "True",
                        'name': f"{filename}",
                        'groupId': groupid
                    }

                else:

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
                
                if int(groupid) > 100:
                    assetid = new[3]
                else:
                    assetid = new[2]

            if response.status_code == 200:
            
                print(f"{Fore.GREEN}- Successfully uploaded a audio to roblox")
            else:
                print(f"{Fore.RED}- Failed to upload a audio to roblox")
        elif mac == True:

            with open(f"{path}//{filename}.mp3", 'rb') as f:
                files = {'file': ('lol.mp3', f, 'audio/wav')}
                if int(groupid) > 100:
                    data = {
                        '__RequestVerificationToken': self.getToken(),
                        'assetTypeId': '3',
                        'isOggUploadEnabled': 'True',
                        'isTgaUploadEnabled': 'True',

                        'onVerificationPage': "False",
                        "captchaEnabled": "True",
                        'name': f"{filename}",
                        'groupId': groupid
                    }

                else:

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
                
                if int(groupid) > 100:
                    assetid = new[3]
                else:
                    assetid = new[2]

            if response.status_code == 200:
            
                print(f"{Fore.GREEN}- Successfully uploaded a audio to roblox")
            else:
                print(f"{Fore.RED}- Failed to upload a audio to roblox")
            
            


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
        if grantperms.status_code == 200:
            print(f"{Fore.GREEN}- Successfully granted audio permissions to roblox")
        else:
            print(f"{Fore.RED}- Failed to grant audio permissions to roblox")
           
        
        finalone3 = f"https://portal-api.bloxbiz.com/ad/update_dev_ad_asset/{guid}"

        data69 = {
            "bloxbiz_id": bloxbizid,
            "dev_creative_asset_url": f"https://www.roblox.com/catalog/{assetid}/",
            "game_id": gameid,
            "sheet_index": "audio"
        }

        headers = {

            'authorization': f"Bearer {res2}",
            'user-agent': 'Bloxbiz Uploader (https://github.com/Adaaks/Superbiz-Uploader)',
            'x-game-id': str(gameid),
            'x-bloxbiz-id': str(bloxbizid)
        }

        finalone3 = session.post(finalone3, headers=headers, json=data69)

        if finalone3.status_code == 200:
            countuploaded +=1
            print(f"{Fore.YELLOW}[{countuploaded}/{countads}]{Fore.GREEN} Successfully submitted a audio to superbiz ({advertname})")

            path = os.getcwd()
            folder_path = path
                
            test = os.listdir(folder_path)

            for images in test:
                if images.endswith(".mp3"):
                    os.remove(os.path.join(folder_path, images))
            for images in test:
                if images.endswith(".png"):
                    os.remove(os.path.join(folder_path, images))
        else:
            print(f"{Fore.YELLOW}[{countuploaded}/{countads}]{Fore.RED} Failed to submit a audio to superbiz ({advertname})")
           
            
        print("\n")
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
                try:
                    if ad["ad_url"] is None:
                        continue
                except:
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
### Estimation of time to upload the ads
estimatedsecs = countads * 4.5

x = datetime.datetime.now() + timedelta(seconds=estimatedsecs)
x = str(x).split(" ")
x = x[1]
x = str(x).split(".")
x = x[0]
x = x.split(":")
newx = f"{x[0]}:{x[1]}"

estimatedsecs = round(estimatedsecs)
estimatedminutes = estimatedsecs / 60
estimatedminutes = round(estimatedminutes)

if estimatedminutes == 1:
    print(f"{Fore.MAGENTA}Estimation: {estimatedminutes} minute ({newx})\n")
elif estimatedsecs == 0:
    pass
elif estimatedsecs <=59:
    estimatedminutes = estimatedsecs
    print(f"{Fore.MAGENTA}Estimation: {estimatedminutes} seconds ({newx})\n")

elif estimatedminutes > 1:
    print(f"{Fore.MAGENTA}Estimation: {estimatedminutes} minutes ({newx})\n")

robloxx = {
    '.ROBLOSECURITY': cookie
}

try:
    ageaccount = requests.get('https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie})
    ageaccount2=ageaccount.json()
    ageaccount3 = ageaccount2['UserAbove13']

    if ageaccount.status_code == 200:
        if ageaccount3 == False:
            print(f"{Fore.RED}Error - you have must use a roblox account which is 13+\n- This is because under 13 accounts get ratelimited from uploading roblox decals/audio")
            input()
except:
    pass


class DataScraper():
    def scrape(self, data):
        global assetid, headers, guid, gif, static, ad_idx, filename,advertname, lol2, windows,mac
        urls = []
        for campain in data["data"]:
            advertname = campain.get('campaign_name')
            advertname = advertname.split( )
            advertname = advertname[0]
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
                            if windows == True:
                                urllib.request.urlretrieve(ad["creative_audio_s3"], f"{path}\\{filename}.mp3")
                            elif mac == True:
                                urllib.request.urlretrieve(ad["creative_audio_s3"], f"{path}//{filename}.mp3")
                            
                            static = False
                            gif = False

                            Audio = AudioClass(cookie)
                            Audio.upload()
                            
                try:
                    if ad["ad_url"] is None:
                        continue
                except:
                    continue
                for ad_idx, ad_url in enumerate(ad["ad_url"],0):
                    if type(ad_url) == str:
                        if ad.get("dev_ad_url") is None:
                            if ad["creative_asset_s3"] not in urls:
                                
                                urls.append(ad["creative_asset_s3"])
                                guid = ad["GUID"]
                                path = os.getcwd()

                                if windows == True:
                                    urllib.request.urlretrieve(ad["creative_asset_s3"], f"{path}\\{guid}.png")
                                elif mac == True:
                                    urllib.request.urlretrieve(ad["creative_asset_s3"], f"{path}//{guid}.png")

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

                                if windows == True:
                                    urllib.request.urlretrieve(ad_url["creative_asset_s3"], f"{path}\\{guid}.png")
                                elif mac == True:
                                    urllib.request.urlretrieve(ad_url["creative_asset_s3"], f"{path}//{guid}.png")

                                gif = True
                                static = False
                                Decal = DecalClass(cookie)
                                Decal.upload()
                                     
        return urls

scraper = DataScraper()
urls = scraper.scrape(trs) 

if countads == 0:
    print(f"{Fore.RED}All adverts are already uploaded.")
elif countuploaded >= countads:
    print(f"{Fore.GREEN}Successfully uploaded all adverts to your superbiz account.")
else:
    print(f"{Fore.RED}Completed - there may have been issues with uploading all adverts to superbiz\n- Try re-running the program\n- Check your ad control to make sure everything has been uploaded")

try:
    for images in test:
        if images.endswith(".mp3"):
            os.remove(os.path.join(folder_path, images))
    for images in test:
        if images.endswith(".png"):
            os.remove(os.path.join(folder_path, images))
except:
    pass
input()                
