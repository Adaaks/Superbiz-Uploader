import requests
import urllib.request
import os
import json
import configparser
from bs4 import BeautifulSoup
import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
        print("Error, incorrect email or password - please check Setup.ini.")
        input()
    return s


session = login(email,password)

headers = {
    'authorization': f"Bearer {res2}",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
lol = session.get("https://portal-api.bloxbiz.com/dev/account/details", headers=headers)
lol = lol.json()
bloxbizid = lol['data']['bloxbiz_id']
apikey = lol['data']['api_key']
first_name = lol['data']['first_name']

print(f"Welcome, {first_name} - you have successfully logged in.")
print("\n")

getgameid = session.get("https://portal-api.bloxbiz.com/dev/games/list?with_live_status=true",headers=headers)
getgameid = getgameid.json()

count = 0
def gameid3():
    global gameid, count, ask2
    while True:
        
        try:
            ask2 = getgameid['data'][count]["game_name"]
            gameid = getgameid['data'][count]["game_id"]
        except:
            print("Oops! Seems you like you don't have more games - lets go back.")
            count = 0
            gameid3()
            
        asking = str(input(f"Would you like to select (yes/no)?\n- {ask2}: "))

        if asking.upper() == "NO":
            count+=1
            print("\n")
            gameid3()

        elif asking.upper() == "YES":
            print("Great, I will begin to upload your ads.")
            print("\n")
            break
        
        else:
            print("Error! Please answer with either yes or no.")
            print("\n")
            gameid3()
        
gameid3()

getads = f"https://portal-api.bloxbiz.com/dev/dev_campaign_manager/list?game_id={gameid}&bloxbiz_id={bloxbizid}"
trs = session.get(getads,headers=headers)
trs = trs.json()

    
             
assetid = ""
guid = 0

ad_idx = 0

gif = False
static = False

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
            print("Error! Invalid cookie, please check your setup.ini.")
        
    def getToken(self): 
        homeurl= 'https://www.roblox.com/build/upload' 
        #sleep(1)
        response = self.goose.get(homeurl, verify=False)
        try:
            soup = BeautifulSoup(response.text, "lxml")
            try:
                
                veri = soup.find("input", {"name" : "__RequestVerificationToken"}).attrs["value"]
            except:
                print("Your cookie is invalid, go update it.")
                input()
        except NameError:
            print(NameError)
            return False
        return veri
    def upload(self):
        global assetid, bloxbizid, gameid, guid
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
            assetid = responseurl[62:73]
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
            }

        finalone1 = session.post(finalone,headers=headers,json=payload)
        if finalone1.status_code == 200:
            print("Uploaded 1x advert to Bloxbiz")
            
        else:
            print("Issue with uploading to bloxbiz.")
                
                



class DataScraper():
    def scrape(self, data):
        global assetid, headers, guid, gif, static, ad_idx
        
        urls = []
        for campain in data["data"]:
            for ad in campain["ads"]:
                for ad_idx, ad_url in enumerate(ad["ad_url"],0):
                    if type(ad_url) == str:
                        if ad.get("dev_ad_url") is None:
                            if ad["creative_asset_s3"] not in urls:
                                urls.append(ad["creative_asset_s3"])
                               
                                guid = ad["GUID"]
                                path = os.getcwd()
                                
                                
                                
                                
                                urllib.request.urlretrieve(ad_url["creative_asset_s3"], f"{path}\\Ads\\{guid}.png")
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
urls = scraper.scrape(trs) #scrape
print("\n")
print("Yay! All ads have been uploaded.")
input()

                          
