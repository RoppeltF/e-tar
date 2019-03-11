from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expectedCondition

import re
import time
import mysql.connector
from dataB.dbCon import mydb,dBase,dBaseClose

#Pavadinimas - Title
#Institucijos suteiktas nr. - Authority issued no.
#Priėmimo data - Date of Admission
#Įsigaliojimo data - Entry into force

global browser
global BASE_URL
global links
global nomes_lista
global datas

nomes_lista = []; datas = []; links = [];

BASE_URL = "https://www.e-tar.lt"

headless = Options()
#headless.add_argument("--headless")
headless.headless = True

#browser = webdriver.Firefox(options=headless)
browser = webdriver.Firefox()

def tarDefault():
    browser.get("https://www.e-tar.lt/acc/index.html")
    assert "TAR" in browser.title
    #Find the search box - Localiza a caixa de pesquisa
    elem = browser.find_element_by_name("page-index:j_id_v:page-index-search")

        #Search query - texto da pesquisa
    elem.send_keys("pilietybę Brazilijoje" + Keys.RETURN)

        # selenium sleep driverName + time or it waits untill  expected condition is met - Tempo de espera do Selenium Nome do driver+tempo ou espera a condicao ser atendida
    WebDriverWait(browser, 7).until(expectedCondition.presence_of_element_located((By. XPATH, "//div[@class='table-content-inner']")))

    #printa NR + data no terminal da pagina mais recente  ex.Lnk + 1V-860 + data YYYY-MM-DD
    # link | Issued No. | Date

    WebDriverWait(browser,7 ).until(expectedCondition.presence_of_element_located((By. XPATH, "//div[@class = 'table-row']")))

    for a in browser.find_elements_by_xpath("//div[@class = 'table-row']"):
        datas.append( re.search(r'[\d][\d][\d][\d[\d][-][\d][\d][-][\d][\d]',a.text).group(0) )

    #Localiza links da pagina mais recente
    for c in browser.find_elements_by_xpath('.//a'):
        links = re.findall("[^=]+[0-9]+[a-z0-9]*",c.get_attribute('href'))

    #Find All links (* element(S) - element get only the first occurrence)
    #browser.find_element_by_xpath('.//a').click()

    raw_data = datas,links

    return raw_data



#Get all brazilians names/ Family names from the list | coleta os nomes brasileiros da lista
def getNomes(links,data):

    for url in links:
        browser.get(BASE_URL + "/rs/legalact/" + url)

        texto=[];listaBR=[];nomes_tmp=[]
        for elem in browser.find_elements(By.CLASS_NAME,"MsoNormal"):
            texto.append( elem.text )
        i = 0
        while i < len(texto):
            if re.search(r'Brazil',texto[i]):
                listaBR.append( texto[i].split(',') )
                time.sleep(1)
            i += 1
        i=0

        while i < len(listaBR):
           nomes_tmp.append( listaBR[i][0] )
#           print( listaBR[i][0].split(',') )
#           print( nomes_tmp )
           i += 1
        nomes_lista.append(nomes_tmp)

    return nomes_lista


def insertDados(link,datas):
#def insertDados():
    link = []
    nomes = []

    #check last data on db
    lastDataDB = []
    lastDataDB = checkDados()

    print(lastDataDB)
    nomes = getNomes()

    #compare link with the las link on DB | compara link com ultimo link no BD
#    for x in datas:
#        if str( lastDataDB ) > str( x ):
#            continue
#        else:
#            link.append( datas.index( x ) )


    #do insert | faz o insert das info. novas
    sql = "INSERT INTO listas (nomes, link, data ) VALUES (%s, %s, %s)"

    x=0
    while x < len( linkX ):
        val.append( "("+nomes, url, datas [ x ] +")" )
        i+=1
    print("")
    print(val)

#    dBase.executemany(sql, val)
#    mydb.commit()
#    print(dBase.rowcount, "was inserted.")
#    dBaseClose()
    return 0

def checkDados():
    dBase.execute( 'SELECT link FROM listas ORDER BY id DESC LIMIT 1;' )
    myresult = dBase.fetchall()
    for x in myresult:
          print(x)
    dBaseClose()
    return myresult



default_result = tarDefault()
links = default_result[1]
datas = default_result[0]

nomes_lista = getNomes(links,datas)


print("Nomes Lista")
print (nomes_lista)

print("Links")
print (links)

print("Datas")
print (datas)


#prev_result = checkDados()

#Whats()

















































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
