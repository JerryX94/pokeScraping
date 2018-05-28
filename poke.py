from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import random
import sys
import time

def scrapeData(dataBase, bsObj):
    newdata = []
    #编号
    no = bsObj.find("td", {"colspan":"2"}).find("a", {"href":\
"/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"}).\
get_text()
    no = re.sub(re.compile("#+"), " ", no)
    no = re.sub(re.compile(" +"), "", no)
    newdata.append(no)
    #名称
    newdata.append(bsObj.find("h1", {"id":"firstHeading"}).get_text())
    newdata[1] = re.sub(re.compile(" +"), "_", newdata[1][:\
len(newdata[1]) - 10])
    print("Scraping Pokemon No.", newdata[0], " \t", newdata[1])
    #属性
    attribute = bsObj.find("div", {"id":"mw-content-text"}).\
find("a", {"title":"Type"}).parent.parent.find("table").findAll("a", \
limit = 2)
    if (attribute[0].get_text() == attribute[1].get_text()):
        newdata.append(attribute[0].get_text())
        newdata.append("Unknown")
    else:
        newdata.append(attribute[0].get_text())
        newdata.append(attribute[1].get_text())
    #特性
    ability = bsObj.find("div", {"id":"mw-content-text"}).find("a", \
{"title":"Ability"}).parent.parent.find("table").findAll("td")
    normalAbility = ability[0].findAll("a", limit = 2)
    for i in range(len(normalAbility)):
        normalAbility[i] = re.sub(" +", "_", normalAbility[i].\
get_text())
    if (len(normalAbility) > 1):
        newdata.append(normalAbility[0])
        newdata.append(normalAbility[1])
    else:
        newdata.append(normalAbility[0])
        newdata.append("Unknown")
    hiddenAbility = re.sub(" +", "_", ability[3].find("a").\
get_text())
    if ("style" not in ability[3].attrs):
        newdata.append(hiddenAbility)
    elif (ability[3].attrs["style"] != "display: none"):
        newdata.append(hiddenAbility)
    else:
        newdata.append("Unknown")
    #捕获率
    catchRate = bsObj.find("div", {"id":"mw-content-text"}).\
find("a", {"title":"Catch rate"}).parent.parent.find("table").\
find("td").get_text()
    catchRate = re.sub(re.compile("\(.+\)"), " ", catchRate)
    catchRate = re.sub("\n+", " ", catchRate)
    catchRate = re.sub(" +", "", catchRate)
    newdata.append(catchRate)
    #蛋组
    eggGroup = bsObj.find("div", {"id":"mw-content-text"}).\
find("a", {"title":"Egg Group"}).parent.parent.find("table").\
findAll("a", limit = 2)
    eggGroup[0] = re.sub(re.compile("\(.+\)"), "", eggGroup[0].\
get_text())
    eggGroup[0] = re.sub("\n+", "", eggGroup[0])
    eggGroup[0] = re.sub(" ", "_", eggGroup[0])
    newdata.append(eggGroup[0])
    if (len(eggGroup) > 1):
        eggGroup[1] = re.sub(re.compile("\(.+\)"), "", eggGroup[1].\
get_text())
        eggGroup[1] = re.sub("\n+", "", eggGroup[1])
        eggGroup[1] = re.sub(" ", "_", eggGroup[1])
        newdata.append(eggGroup[1])
    else:
        newdata.append("Unknown")
    #最小孵化步数
    eggCycle = bsObj.find("div", {"id":"mw-content-text"}).\
find("a", {"title":"Egg cycle"}).parent.parent.\
find("table").find("td").get_text()
    eggCycle = re.sub("-.+", " ", eggCycle)
    eggCycle = re.sub("(\xa0)+", " ", eggCycle)
    eggCycle = re.sub("\n+", " ", eggCycle)
    eggCycle = re.sub(" +", "", eggCycle)
    newdata.append(eggCycle)
    #身高(m)
    height = bsObj.find("div", {"id":"mw-content-text"}).find("a", \
{"href":"/wiki/List_of_Pok%C3%A9mon_by_height"}).parent.parent.\
find("table").find("tr").get_text()
    height = re.sub(".*(\"|\″)", " ", height)
    height = re.sub("m", " ", height)
    height = re.sub("\n+", " ", height)
    height = re.sub(" +", "", height)
    newdata.append(height)
    #体重(kg)
    weight = bsObj.find("div", {"id":"mw-content-text"}).find("a", \
{"href":"/wiki/List_of_Pok%C3%A9mon_by_weight"}).parent.parent.\
find("table").find("tr").get_text()
    weight = re.sub(".*lbs.", " ", weight)
    weight = re.sub("kg", " ", weight)
    weight = re.sub("\n+", " ", weight)
    weight = re.sub(" +", "", weight)
    newdata.append(weight)
    #选定六围表单
    statTable = bsObj.find("span", {"id":re.compile("(Base_\
stats)|(Stats)")}).parent
    while (statTable.name != "table"):
        statTable = statTable.next_sibling
    #HP
    hp = statTable.\
find("a", {"href":"/wiki/Statistic#Hit_Points"}).parent.next_sibling.\
next_sibling.get_text()
    hp = re.sub("\n+", " ", hp)
    hp = re.sub(" +", "", hp)
    newdata.append(hp)
    #物攻
    at = statTable.\
find("a", {"href":"/wiki/Statistic#Attack"}).parent.next_sibling.\
next_sibling.get_text()
    at = re.sub("\n+", " ", at)
    at = re.sub(" +", "", at)
    newdata.append(at)
    #物防
    df = statTable.\
find("a", {"href":"/wiki/Statistic#Defense"}).parent.next_sibling.\
next_sibling.get_text()
    df = re.sub("\n+", " ", df)
    df = re.sub(" +", "", df)
    newdata.append(df)
    #特攻
    sa = statTable.\
find("a", {"href":"/wiki/Statistic#Special_Attack"}).parent.\
next_sibling.next_sibling.get_text()
    sa = re.sub("\n+", " ", sa)
    sa = re.sub(" +", "", sa)
    newdata.append(sa)
    #特防
    sd = statTable.\
find("a", {"href":"/wiki/Statistic#Special_Defense"}).parent.\
next_sibling.next_sibling.get_text()
    sd = re.sub("\n+", " ", sd)
    sd = re.sub(" +", "", sd)
    newdata.append(sd)
    #速度
    sp = statTable.\
find("a", {"href":"/wiki/Statistic#Speed"}).parent.next_sibling.\
next_sibling.get_text()
    sp = re.sub("\n+", " ", sp)
    sp = re.sub(" +", "", sp)
    newdata.append(sp)
    #总和
    total = 0
    for data in newdata[len(newdata) - 6:]:
        total += int(data)
    newdata.append(total)
    
    dataBase.append(newdata)
    return

def postProcess(dataBase):
    f = open("output.dat", "w")
    title = ["No.", "Name", "Type1", "Type2", "Normal_Abili\
ty1", "Normal_Ability2", "Hidden_Ability", "Catch_Rate", "E\
gg_Group1", "Egg_Group2", "Egg_Cycle", "Height(m)", "Weight\
(kg)", "HP", "Attack", "Defense", "Spcial_Attack", "Spcial_\
Defense", "Speed", "Total"]
    for element in title:
        f.write(element)
        compBlank = 20 - len(element)
        for i in range(compBlank):
            f.write(" ")
    f.write("\n")
    for data in dataBase:
        for element in data:
            f.write(str(element))
            compBlank = 20 - len(str(element))
            for i in range(compBlank):
                f.write(" ")
        f.write("\n")
    
    f.close()
    return

session = requests.Session()
header = {\
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Saf\
ari/537.36", \
"Accept":"text/html,application/xhtml+xml,application/xml;q\
=0.9,image/webp,image/apng,*/*;q=0.8", \
"Accept-Encoding":"gzip, deflate", \
"Accept-Language":"zh-CN,zh;q=0.9", \
"Upgrade-Insecure-Requests":"1"}
nextUrl = "https://bulbapedia.bulbagarden.net/wiki/Bulbasau\
r_(Pok%C3%A9mon)"
nPoke = 807
counter = 0
dataBase = []
print("Scraping Start!")

while (counter < nPoke):
    try:
        counter += 1
        url = nextUrl
        req = session.get(url, headers = header)
        bsObj = BeautifulSoup(req.text, "html.parser")
        scrapeData(dataBase, bsObj)
        nextUrl = bsObj.find("div", {"id":"mw-content-text"}).\
find("table").\
findAll("a", {"href":re.compile(".+(\(Pok%C3%A9mon\))$")})[3]
        nextUrl = "https://bulbapedia.bulbagarden.net" + nextUrl.\
attrs["href"]
        time.sleep(random.randint(1001, 2000) / 1000.)
    except:
        print("Scraping Pokemon No." + dataBase[len(dataBase) \
- 1][0] + " Error!")
        print(sys.exc_info())

postProcess(dataBase)
print("Scraping Accomplish!")