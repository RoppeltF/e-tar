from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expectedCondition


import re
import time
import argparse


#from dataB.pysql import insertFila,getFila,connect

#Pavadinimas - Title
#Institucijos suteiktas nr. - Authority issued no.
#Priėmimo data - Date of Admission
#Įsigaliojimo data - Entry into force


global browser
global BASE_URL
global links
global nomes_lista
global datas
global WT

#https://levelup.gitconnected.com/the-easy-guide-to-python-command-line-arguments-96b4607baea1

parser = argparse.ArgumentParser(description='Robo de coleta de novos lituanos')
parser.add_argument("--headless", action="store_const", const=True,help="Headless mode - não abrira o navegador e rodara em 2ndo plano")
parser.add_argument("-wt", action="store_const", const='10', help="Wait time")
#parser.add_argument("--name", required=True, type=str, help="Your name")

args = parser.parse_args()
#a = args.a
hdless = args.headless
WT = args.wt


nomes_lista = []; datas = []; links = [];

BASE_URL = "https://www.e-tar.lt"

if hdless == True: 
    headless = Options()
    headless.add_argument("--headless")
    headless.headless = True
    browser = webdriver.Firefox(options=headless)
else:    
    browser = webdriver.Firefox()

def tarDefault():
    global WT
    browser.get("https://www.e-tar.lt/acc/index.html")
    assert "TAR" in browser.title
    #Find the search box - Localiza a caixa de pesquisa
    elem = browser.find_element_by_name("page-index:j_id_v:page-index-search")

    #Search query - texto da pesquisa
    elem.send_keys("pilietybę Brazilijoje" + Keys.RETURN)

    # selenium sleep driverName + time or it waits untill  expected condition is met - Tempo de espera do Selenium Nome do driver+tempo ou espera a condicao ser atendida
    WebDriverWait(browser, 10).until(expectedCondition.presence_of_element_located((By. XPATH, "//div[@class='table-content-inner']")))

    #printa NR + data no terminal da pagina mais recente  ex.Lnk + 1V-860 + data YYYY-MM-DD
    # link | Issued No. | Date

    WebDriverWait(browser, 10).until(expectedCondition.presence_of_element_located((By. XPATH, "//div[@class = 'table-row']")))

    for a in browser.find_elements_by_xpath("//div[@class = 'table-row']"):
        datas.append( re.search(r'[\d][\d][\d][\d][-][\d][\d][-][\d][\d]',a.text).group(0) )

#    print(datas)

    #search for links os the most recent page | Localiza links da pagina mais recente

    link = browser.find_elements_by_xpath("//a[@href]")
    for lnk in link:
        links.append( re.findall("[^=]+[0-9]+[a-z0-9]*",lnk.get_attribute('href') ) )

#    print(links)
    print("")

    #Find All links (* element(S) - element get only the first occurrence)
    #browser.find_element_by_xpath('.//a').click()

    raw_data = datas,links
    return raw_data



#Get all brazilians names from the list | coleta os nomes de brasileiros da lista
def getNomes(links,data):
        global BASE_URL
        for url in links[0:3]:
#        browser.get(BASE_URL + "/rs/legalact/" + str(links[0][0]))
            browser.get( BASE_URL + "/rs/legalact/" + url[0] )

            text=[];listaBR=[];nomes_tmp=[]
           
            for elem in browser.find_elements(By.CLASS_NAME,"MsoNormal"):
                text.append( elem.text )
            i = 0
            while i < len(text):
                if re.search(r'Brazil',text[i]):
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


def insertDados(nomes,link,datas):
#def insertDados():
    link = []
    nomes = []

    #check last data on db
    lastDataDB = []
    lastDataDB = checkDados()

    print(lastDataDB)
    nomes = getNomes()

#    compare link with the lats link on DB | compara link com ultimo link no BD

#    for x in datas:
#        if str( lastDataDB ) > str( x ):
#            continue
#        else:
#            link.append( datas.index( x ) )


    #insert New info | faz o insert das info. novas
    sql = "INSERT INTO listas (nomes, link, data ) VALUES (%s, %s, %s)"

    x=0
    while x < len( linkX ):
        val.append( "("+nomes, url, datas [ x ] +")" )
        i+=1
    print("")
    print(val)

    dBase.executemany(sql, val)
    mydb.commit()
    print(dBase.rowcount, "was inserted.")
    dBaseClose()
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
nomes = nomes_lista


print("Links")
print(links)
print(len(links))
print("")
print("Datas")
print(datas)
print(len(datas))
print("")
print("Nomes")
print(nomes)
print(len(nomes))
print("")

x=0 

DLN = {}

while( x < len(nomes) ):
    DLN.setdefault(datas[x], []).append( [ {links[x][0]:nomes[x]} ] )
    x+=1 
    
#while( x < len(nomes) ):
#    print(datas[x])
#    print(links[x][0])
#    print(len(nomes))
#    print(x)
#    print("")
#    x+=1
#print(nomes)

#data, url = DLN.items()[0]             

print("Dict datas - link : nomes")
print(DLN)
asd = DLN[datas[0]]
print("")
print("The 1st key of dictionary is : " + str(asd ) )
#print("The 1st value of dictionary is : " + str( DLN[datas[0][0] ) ) 


#print("Data da(s) ultima(s) lista(s) " + datas[0] + "total de BR's:  " + str(len(nomes)) )

#print("")
#print("Nome(s)")

#for x in nomes:
#    print(x)


#print("")
#print("Links")
#print(BASE_URL + "/rs/legalact/" + str(links[0][0]))



#prev_result = checkDados()



















