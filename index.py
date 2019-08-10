from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
from selenium import webdriver
import re 
from datetime import date


url = 'https://boutique.orange.fr/mobile/forfaits-orange'

#create new instance of the Firefox driver
driver = webdriver.Firefox(executable_path="./geckodriver")

#opening a connection
driver.get(url)
# page_html = uClient.read()
# uClient.close()

#html parsing
page_soup = soup(driver.page_source, "html.parser")

#traverse to the child container
main_body= page_soup.main.div
div_body = main_body.find('div', 'clearfix')
main_section = div_body.find('section', 'offers conteneur-center with-push' )
main_article = main_section.div

#find the main containers with the data to be scrapped 
containers = main_article.findAll('article')


#save inte .csv file 
filename = "tarifica.csv"
f = open(filename, "w")

#headers for the .csv file
headers ="date, plan_name, promo_price, promo_month, actual_price, call_unlimited, sms_unlimited \n"
f.write(headers)

#get today's date
today = date.today()
# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")

#loop to get the data from all the plans
for container in containers:

    #get the plan name 
    plan_name = container.header.strong.a.p.text

    #get the price of the plan
    price_div = container.find('div', 'bloc-price')
    promo_price1= price_div.span.span.span.text 
    promo_price2 = price_div.span.span.sup.text.replace(',','.')
    promo_price = str(promo_price1 + promo_price2)
    promo_price = promo_price.replace('€', '')

    #get the actual proce of the promo and replace the unnecessary texts
    actual_price_text = price_div.p.text
    numbers_in_text = re.findall(r'\d+', actual_price_text) 
    actual_price = str(numbers_in_text[1] + '.' + numbers_in_text[2])

    #get the promo month and strip unnecessary texts
    paragraph_month = price_div.find('p', 'engagement ng-binding')
    promo_month_text = paragraph_month.text
    promo_month = str(int(re.search(r'\d+', promo_month_text).group()))

    #find if the call is unlimited 
    call_sms_text = container.div.p.span.text

    #split the text into two arrays one with call and other with sms
    split_text = call_sms_text.split('\n',1)

    #check if the call is unlimited or not 
    call_unlimited_text = split_text[0]
    call_unlimited = str('illimités' in call_unlimited_text )

    #check if the sms is unlimited or not
    sms_unlimited_text = split_text[1]
    sms_unlimited = str('illimités' in sms_unlimited_text )

    #write on the .csv file 
    f.write(d1+ " ," + plan_name + " ,"+promo_price + " ,"+promo_month +  " ,"+actual_price + " ,"+call_unlimited + " ,"+sms_unlimited+"\n")

f.close()

