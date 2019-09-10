from bs4 import BeautifulSoup
import requests
import random

def getProxies():
    proxiesUrl = 'https://free-proxy-list.net/'
    request = requests.get(proxiesUrl).text
    soup = BeautifulSoup(request,'html.parser')
    proxyList = set()
    proxiesTable = soup.find(id='proxylisttable')
    # save proxies in list
    for proxyRow in proxiesTable.tbody.find_all('tr'):
        proxyList.add(str(proxyRow.find_all('td')[0].string) + ':' + str(proxyRow.find_all('td')[1].string))
    return proxyList

def getWorkingProxy():
    proxyList = getProxies()
    for proxy in proxyList:
        try:
            response = requests.get('https://httpbin.org/ip', proxies={"http": proxy, "https": proxy}, timeout=3)
            return proxy
        except: pass


def getLinksToCars(carManufacturer, pages):  # working on used cars
    proxy = getWorkingProxy()
    counter = 1
    cars = set()
    while(counter <= pages):
        link = 'https://www.autotrader.ie/search/result/cars/car-type/used/make/{}/page/{}/sort/latest'.format(
            carManufacturer, counter)
        try:
            r = requests.get(
                link, proxies={"http": proxy, "https": proxy}, timeout=3)
            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.find_all(class_='advert')
            for item in items:
                cars.add(
                    item.find('a', class_='advert-img-link').get('href'))
                #linkOfCar = item.find('a',class_='offer-title__link').get('href')
            counter += 1
        except:
            print('getting new proxy')
            proxy = getWorkingProxy()
    return cars


def getDetails(carLink, proxy):
    infoAboutCar = {}
    try:
        #r = requests.get(linkToCar)
        r = requests.get(carLink, proxies={
                         "http": proxy, "https": proxy}, timeout=3)
        soup = BeautifulSoup(r.text, 'html.parser')
        top = soup.find('div', class_="offer-content__gallery")
        #print(top.find('div',class_='photo-item').img.get('data-src'))
        #photo = soup.find('div', class_='photo-item')
        #photo = (photo.img.get('src'))
        photo = (top.find('div', class_='photo-item').img.get('src'))
        if photo == None:
            photo = (
                top.find('div', class_='tp-bgimg defaultimg').div.get('src'))
        #print(photo)
        infoAboutCar['photo'] = photo
        tab = soup.find(class_='fact-sheet')
        #columns = tab.find_all(class_='offer-params__list')
        #for item in columns:
        labelList = tab.find_all('dt', class_='head')
        valueList = tab.find_all('dd', class_='info')
        index = 0
        for label in labelList:
            x = label.string
            infoAboutCar[x] = valueList[index]
            index += 1


    except:
        print('getting new proxy')
        proxy = getWorkingProxy()

    return infoAboutCar


def findCars(carManufacturer, pages):
    links = getLinksToCars(carManufacturer, pages)
    proxy = getWorkingProxy()
    newCars = []
    i = 0  # how many cars will be added
    for link in links:
        if i == 15:
            break
        try:
            infoAboutCar = getDetails(link, proxy)
            #link,model,brand,year,type_car,engine
            actualCar = {
                "link": str(link),
                "make": infoAboutCar['Make'],
                "model": infoAboutCar['Model'],
                "price": infoAboutCar['Price'],
                "engine": infoAboutCar['Engine'],
                "body": infoAboutCar['Body Type'],
                "gearbox": infoAboutCar['Transmission'],
                "year": infoAboutCar['Year'],
                "color": infoAboutCar['Colour'],
                "milage": infoAboutCar['Mileage'],
                "owners": infoAboutCar['Owners'],
                "doors": infoAboutCar['Doors'],
                "location": infoAboutCar['Location'],
                "nct": infoAboutCar['NCT Expiry']

            }
            newCars.append(actualCar)
            print(
                'Car added: ', infoAboutCar['Make'], ' ', infoAboutCar['Model'])
            i += 1
        except:
            print('getting new proxy')
            proxy = getWorkingProxy()
    return newCars



#with open('https://www.autotrader.ie/browse-used-cars/mercedes-benz/180/used-2014-141-mercedes-benz-180-e-220-dublin-fpa-201906199167719') as html_file:
#    soup = BeautifulSoup(html_file, 'lxml')

#r = requests.get(
#    "https://www.autotrader.ie/browse-used-cars/mercedes-benz/180/used-2014-141-mercedes-benz-180-e-220-dublin-fpa-201906199167719")
#soup = BeautifulSoup(r.content)

#soup.prettify()

#target = soup#.find('dl', class_='fact-sheet')

#for a_tag in soup.find_all('a', class_='listing-name', href=True):
#    print ('href: ', a_tag['href'])

