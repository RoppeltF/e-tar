from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expectedCondition


import pickle


import re
import time


browser = webdriver.Firefox()

browser.get("https://www.e-tar.lt/acc/index.html")
assert "TAR" in browser.title

# Find the search box
elem = browser.find_element_by_name("page-index:j_id_v:page-index-search")

#query da pesquisa
elem.send_keys("pilietybę Brazilijoje" + Keys.RETURN)

# selenium sleep driverName + time or it will wait untill  expected condition is met
WebDriverWait(browser, 5).until(expectedCondition.presence_of_element_located((By. XPATH, "//div[@class='table-content-inner']")))

#printa NR + data no terminal da pagina mais recente  ex. 1V-860 + data YYYY-MM-DD

A=['']; B=['']; C=['']
for a in browser.find_elements_by_xpath("//div[@class = 'table-row']"):
#    print(re.search(r'[\d]V-[\d][\d][\d]',a.text).group(0))
#    print(re.search(r'[\d][\d][\d][\d[\d][-][\d][\d][-][\d][\d]',a.text).group(0))

    A.append( re.search(r'[\d]V-[\d][\d][\d]',a.text).group(0) )
    B.append( re.search(r'[\d][\d][\d][\d[\d][-][\d][\d][-][\d][\d]',a.text).group(0) )

#printa os links no terminal da pagina mais recente  ex. 1V-860 + data YYYY-MM-DD

for b in browser.find_elements_by_xpath('.//a'):
#    print(b.get_attribute('href'))
    C.append( b.get_attribute('href') )

#for B, A,C in zip(A, B, C):
#    print(A, " | ", B, " - ", C)

#Find All links (* elementS - element get only the first occurrence)
browser.find_element_by_xpath('.//a').click()


#WebDriverWait - espera o carregamento do browser ate  encontrar a TAG iframe
WebDriverWait(browser, 3).until(expectedCondition.presence_of_element_located((By. TAG_NAME, "iframe")))

#pegar link do iframe
for lk in browser.find_elements(By.TAG_NAME, "iframe"):
    iframe = lk.get_attribute('src')


#msg=iframe, " | ", A[1], " - ", B[1]

data = iframe,A[1],B[1]



with open("lock.lock", 'w+', encoding='utf-8') as file:
    file.write(str(data))


browser.get(iframe)  # Acessa o link

texto=['']

for elem in browser.find_elements(By.CLASS_NAME,"MsoNormal"):
    #texto.append( re.search(r'Brazil',elem.text) )
    texto.append( elem.text )

br=[] ; i=0
while i < len(texto):
    if re.search(r'Brazil',texto[i]):
        print(texto[i])
#    br.append(texto[i])
        time.sleep(2)
#    print( str(i) +" - "+ texto[i] )

    i += 1

#print(br[0])










































########### WHATS APP  ##############

#
## Replace below path with the absolute path
## to chromedriver in your computer
#
#
##options = Options()
##options.add_argument("user-data-dir=profile/")
##options.add_argument("")
#
#
##driver = webdriver.Chrome('./chromedriver')
##driver = webdriver.Chrome('/home/tux/DEV/python/whatspython/whatsappmessagepython/chromedriver', options=options)
#
#
#driver = webdriver.Firefox()
#
#driver.get("https://web.whatsapp.com/")

#load Cookies
#for cookie in pickle.load(open("whats.pkl", "rb")):
#    driver.add_cookie(cookie)


#wait = WebDriverWait(driver, 800)
#
# Replace 'Friend's Name' with the name of your friend
# or the name of a group
#target = '"Lietuva"'
#
## Replace the below string with your own message
#string = sys.argv[1]
#string = msg
#string = "teste"
#
#x_arg = '//span[contains(@title,' + target + ')]'
#group_title = wait.until(expectedCondition.presence_of_element_located((By.XPATH, x_arg)))
#group_title.click()
#
#
#message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
#
#message.send_keys(string)
#
#sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
#sendbutton.click()


#pickle.dump( browser.get_cookies(), open("whats.pkl","wb") )

#cookies = []




#
#
##Salvar cookies
## Go to the correct domain
#
## Now set the cookie. Here's one for the entire domain
## the cookie name here is 'key' and its value is 'value'
#driver.add_cookie({'name':'key', 'value':'value', 'path':'profile'})
#
## additional keys that can be passed in are:
## 'domain' -> String,
## 'secure' -> Boolean,
## 'expiry' -> Milliseconds since the Epoch it should expire.
#
## And now output all the available cookies for the current URL
#for cookie in driver.get_cookies():
#    print ( "%s -> %s" % (cookie['name'], cookie['value']) )
#
## You can delete cookies in 2 ways
## By name
##driver.delete_cookie("CookieName")
# Or all of them
#driver.delete_all_cookies()#print( browser.manage().getCookies() )






#browser.quit()
