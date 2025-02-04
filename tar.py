from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expectedCondition

import re
import time
import argparse


from dataB.pysql import update_lista,connect,checkDados

#Pavadinimas - Title
#Institucijos suteiktas nr. - Authority issued no.
#Priėmimo data - Date of Admission
#Įsigaliojimo data - Entry into force


global browser
global BASE_URL
global links
global nomes_lista
global datas
global wait_time

#https://levelup.gitconnected.com/the-easy-guide-to-python-command-line-arguments-96b4607baea1

parser = argparse.ArgumentParser(description=' Lithuania scsrapper of approved Citizenship List - ')
parser.add_argument("--headless", action="store_const", const=True,help="Headless mode - will run in background")
parser.add_argument("-wt", action="store_const", default='10', help="Wait time")
parser.add_argument("-cs", action="store_const", default='BRAZILIJA', help="Citizenship to search for") #BRAZILIAN

#parser.add_argument("--name", required=True, type=str, help="Your name")

args = parser.parse_args()
hdless = args.headless
wait_time = args.wt
s_term = args.cs
print(s_term)


nomes_lista = []; datas = []; links = [];

BASE_URL = "https://www.e-tar.lt"

if hdless == True: 
    headless = Options()
    headless.add_argument("--headless")
    headless.headless = True
    browser = webdriver.Edge(options=headless)
else:    
    browser = webdriver.Edge()

def tarDefault():
    global WT
    browser.get("https://www.e-tar.lt/acc/index.html")
    # assert "TAR" in browser.title
    #Find the search box - Localiza a caixa de pesquisa
    elem = browser.find_element(By.ID,"page-index:j_id_v:page-index-search")
    #Search query - texto da pesquisa
    # elem.send_keys("pilietybę Brazilijoje" + Keys.RETURN)
    elem.send_keys("Dėl Lietuvos Respublikos pilietybės atūrimko" + Keys.RETURN)

    # selenium sleep driverName + time or it waits untill  expected condition is met
    WebDriverWait(browser, wait_time).until(expectedCondition.presence_of_element_located((By. XPATH, "//div[@class='table-content-inner']")))

    #printa NR + data no terminal da pagina mais recente  ex.Lnk + 1V-860 + data YYYY-MM-DD
    # link | Issued No. | Date

    # WebDriverWait(browser, 20).until(expectedCondition.presence_of_element_located((By. XPATH, "//div[@class = 'table-row']")))

    for a in browser.find_elements(By.XPATH,"//div[@class = 'table-row']"):
        datas.append( re.search(r'[\d][\d][\d][\d][-][\d][\d][-][\d][\d]',a.text).group(0) )

    # print(datas)

    #search for links os the most recent page | Localiza links da pagina mais recente
    link = browser.find_elements(By.XPATH,"//a[@href]")
    for lnk in link:
        links.append( re.findall("[^=]+[0-9]+[a-z0-9]*",lnk.get_attribute('href') ) )

    # print(links)
    print("")

    raw_data = datas,links
    return raw_data



#Get all brazilians names from the list | coleta os nomes de brasileiros da lista
def getNomes(links,citizenship):
        global BASE_URL
        for url in links:
            browser.get( BASE_URL + "/rs/legalact/" + url[0] )

            text=[];listaBR=[];nomes_tmp=[]
           
            for elem in browser.find_elements(By.CLASS_NAME,"MsoNormal"):
                text.append( elem.text )
            i = 0
            while i < len(text):
                if re.search(citizenship,text[i]):
                    listaBR.append( text[i].split(',') )
                    time.sleep(1)
                i += 1
            i=0

            while i < len(listaBR):
               nomes_tmp.append( listaBR[i][0] )
               
#               print( nomes_tmp )
               i += 1

            nomes_lista.append(nomes_tmp)

#       print("Nomes Lista ")
#       print (*nomes_lista[0],sep='\n')
#       print("")

        return nomes_lista



default_result = tarDefault()
links = default_result[1]
datas = default_result[0]

citizenship = s_term
nomes_lista = getNomes(links,citizenship)
nomes = nomes_lista



j=i=0
# while i < len(datas):
while i < 3:
    print( f"{datas[i]},{BASE_URL}/rs/legalact/{str(links[i][0])},{nomes}" )
    j=0
    while j < len(nomes[i]):
        print( nomes[i][j] )
        j+=1
    i += 1
    print("")

# print(f"{len(datas)}")
# print(f"{len(links)}")
# print(f"{len(nomes)}")

    
prev_result = checkDados()
print(prev_result)

