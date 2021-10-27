from selenium import webdriver                          
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm.autonotebook import tqdm

import re
import pandas as pd

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver_Create = lambda: webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe' , options = op)

base = "https://www.yelp.de/"
df = pd.DataFrame(columns = ['Name','href','Name_reviewer' , 'Ort_reviewer' , 'Friends_count' , 'Reviews_count', 'Pictures_count' , 'Date'  , 'Comment' , 'Names_pictures' ,'Hilfreich' , 'Lustig', 'Cool'])

def get_pages(page_, driver_ , rest_review):
    global df,pbar
    
    driver_.get(page_[1])
    driver_.implicitly_wait(20)
    
    if (rest_review == -1):
        rest_review = driver_.find_element(By.XPATH , '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[2]/div[2]/span')
        rest_review = dig(rest_review.text)
        
    rest_review -= 10
    rating = WebDriverWait(driver_, 60).until(EC.presence_of_element_located((By.XPATH , '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[2]/div[1]/span/div')))
    rating = float(rating.get_attribute("aria-label")[:2])
    reviews = driver_.find_elements(By.CLASS_NAME,"review__373c0__3MsBX.border-color--default__373c0__1WKlL")
    for i in reviews:
        break
        #name , ort , friends , reviews , pictures ,date  , comment , name_photos ,Hilfreich , lustig, Cool
        liste = i.text.split('\n')
        
        try:
            pictures_count = dig(liste[6])
        except:
            pictures_count = 0
        
        review ={'Name':page_[0],
            'href':page_[1],
            'Name_reviewer':liste[0],
            'Ort_reviewer':liste[1],
            'Friends_count':liste[2],
            'Reviews_count':liste[3],
            'Pictures_count':pictures_count,
            'Date':liste[5],
            'Hilfreich': dig(liste[-3]),
            'Lustig': dig(liste[-2]),
            'Cool': dig(liste[-1]) }
        
        if pictures_count <= 4 :
            review['Names_pictures']= ' '.join(liste[-3-pictures_count:-3])
            review['Comment']= ' '.join(liste[7:-3-pictures_count])
        else:
            review['Names_pictures']= ''
            review['Comment']= ' '.join(liste[7:-4])
             
        df = df.append([review], ignore_index=True)
    
    if rest_review > 0 :
        driver3 = driver_Create()
        get_pages(page_, driver3 , rest_review)
    else: 
        print(page_[0]," finish...")
        pbar.update(1)
    

def get_restaurants():
    classes = driver.find_elements(By.CLASS_NAME, 'css-1f2a2s6')[2:]
    for i in classes:
        page = [i.get_attribute("name") , i.get_attribute("href")]
        driver2 = driver_Create()
        get_pages(page, driver2 ,-1)
    
def dig (word):
    a = re.findall(r'\d+', word)
    a = int(a[-1]) if len(a) != 0 else 0
    return a

#get total number of pages
base_driver = driver_Create()
base_driver.get("https://www.yelp.de/search?find_desc=&find_loc=Kiel%2C+Schleswig-Holstein&ns=1")
base_driver.implicitly_wait(10)
total_pages = base_driver.find_element(By.XPATH , '//*[@id="main-content"]/div/ul/li[14]/div/div[2]/span')
total_pages = dig(total_pages.text)

pbar = tqdm(total=total_pages * 10)

for i in range (0,total_pages,10):
    driver = driver_Create()
    driver.get(base + "search?cflt=restaurants&find_loc=Kiel%2C%20Schleswig-Holstein&start=" + str(i))
    driver.implicitly_wait(10)
    get_restaurants()
    pbar.close