

# Create your views here.
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Create your views here.
#####################################################################
###define 首頁

def home(request):
    
    #####################################################################
    ###requests網站(氣象局)
    xx = requests.get("https://www.cwb.gov.tw/V7/forecast/f_index.htm?_=1574823538428",
                      headers={ 
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                    'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3'
                    
                    },
        )
                      
    xx.encoding = "utf-8"
    ssoup = BeautifulSoup(xx.text, 'html.parser')


    #####################################################################
    ###爬溫度並丟入widths_list裡
    temp_list = []
    temps = ssoup.find_all("td",{"width":"50%"})
    for t in temps:
        temp_list.append(t.text)
        
    #####################################################################
    ###爬地區並丟入area_list裡
    area_list = []
    area = ssoup.find_all("td",{"width":"60%"})
    for a in area:
        area_list.append(a.text)               
    
    alll = zip(area_list,temp_list)


    
    #####################################################################
    ###request 最近熱門料理    
    
    hotlist=[]
    xxx = requests.get("https://icook.tw/recipes/popular",
                      headers={ 
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                    'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3'
                    
                    },
        )
                      
    xxx.encoding = "utf-8"
    sssoup = BeautifulSoup(xxx.text, 'html.parser')
    
    pp = sssoup.find_all('div', class_='browse-recipe-preview')

    ###把每一個熱門料理的名字丟入list
    for p in pp:    
        
    ###把食譜的名稱抓出來並丟到cuisine_name_list裡面
        hot_name = p.find('span', class_='browse-recipe-name').text
    
        hotlist.append(hot_name[11:-1])  ###因為後來發現前面有好多空格
        
    
    
    return render(request, 'home.html',locals())


def bot(request):
    
    if request.method == "GET":
        question = ""
        response = ""
        
        return render(request, "bot.html",locals())
    else:
        question = request.POST["question"]

        authenticator = IAMAuthenticator('BDVepx7tCExuwYMxWdSyJhn8ahL3ZN-1AXMQkyXRyghp')
        service = AssistantV2(
            version='2019-11-28',
            authenticator=authenticator
        )
        
        ###找出session_id
        service.set_service_url('https://gateway.watsonplatform.net/assistant/api')
        
        session_response = service.create_session(
            assistant_id='a7d3a456-718f-4326-8c86-8200f06a9305'
        ).get_result()
        
        s_id = session_response["session_id"]
        
        
        x = service.message(assistant_id='a7d3a456-718f-4326-8c86-8200f06a9305',
                            session_id=s_id,
                            input={
                                    'message_type': 'text',
                                    'text': question
                                    }
        ).get_result()
        
        y = x["output"]["generic"]
        r = y[0]["text"]
        if r == "我不明白您的意思" :
            
            x1= requests.get(
                'https://icook.tw/recipes/search?q=&ingredients='+question,
                headers={ 
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3'                    
                        },
            )
            x1.encoding = 'utf-8'
        
        
        
            soup = BeautifulSoup(x1.text, 'html.parser')
            
            ###先設定用來存放name, herf, cooker, discription, ingredients 的list
            cuisine_pic_list = []
            cuisine_name_list = []
            cuisine_herf_list = []    
            cuisine_cooker_list = []
            cuisine_discription_list = []
            cuisine_ingredient_list = []
            
            ##################################################################
            ###因為只有pic和別人不同層所以獨立find
            pics = soup.find_all("div",{"class":"browse-recipe-cover"})
            
            for p in pics:
                coll = p.find("img",alt = True)
                img = coll.attrs["data-src"]
                cuisine_pic_list.append(img)
            
            
                
            ###把食譜的連結抓出來並丟到cuisine_herf_list裡面
            herf = soup.find_all("a",{"class":"browse-recipe-touch-link"})
            
            for h in herf:
                cuisine_herf = h['href']
                cuisine_herf_list.append("https://icook.tw"+cuisine_herf)
            
            
            ##################################################################
            ###因為title/discription/ingredients 都在這層
            preview = soup.find_all('div', class_='browse-recipe-preview')
            
            ###把每一個料理的對應資料丟入list
            for p in preview:    
                
            ###把食譜的名稱抓出來並丟到cuisine_name_list裡面
                cuisine_name = p.find('span', class_='browse-recipe-name').text
            
                cuisine_name_list.append(cuisine_name)
            
            ###把食譜的作者抓出來並丟到cuisine_cooker_list裡面
                cuisine_cooker = p.find('span', class_='result-username-by').text
                
                cuisine_cooker_list.append(cuisine_cooker)
                
            ###把食譜的步驟抓出來丟到cuisine_discription_list裡面，因為有的文章是沒有描述的所以需自行幫他設製成null
            
                cuisine_discription = p.find('p', class_='browse-recipe-content-description')
                if (cuisine_discription != None) :
            
                    cuisine_discription_list.append(cuisine_discription.text)
                else:
            
                    cuisine_discription_list.append("無描述")
                    
            
                ###把食譜的原材抓出來丟到cuisine_ingredient_list裡面\
                cuisine_ingredient = p.find('p', class_='browse-recipe-content-ingredient').text
            
                cuisine_ingredient_list.append(cuisine_ingredient)
                
            
            if len(cuisine_name_list)>5:
                cuisine_pic_list = cuisine_pic_list[0:5]
                cuisine_name_list = cuisine_name_list[0:5]
                cuisine_herf_list = cuisine_herf_list[0:5]
                cuisine_cooker_list = cuisine_cooker_list[0:5]
                cuisine_discription_list = cuisine_discription_list[0:5]
                cuisine_ingredient_list = cuisine_ingredient_list[0:5]
                
                
            all = zip(cuisine_pic_list,cuisine_name_list,cuisine_herf_list, cuisine_cooker_list,cuisine_discription_list,cuisine_ingredient_list)
            
            response = all
            return render(request, "bott.html",locals())
            
        else:
            response = r
            return render(request, "bot.html",locals())