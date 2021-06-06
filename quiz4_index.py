""" გამარჯობა. ეს არის ბაჩი მოსულიშვილის პროექტი ვებ-გვერდის პარსინგის შესახებ. ლექტორი: ლიკა სვანაძე.
აღნიშნულ ფაილში შეგხვდებათ კომენტარები, რომელიც აღწერს ამა თუ იმ ხაზის მუშაობას, თუმცა ვეცდები მოკლედ
ავხსნა ამ პროგრამის მუშაობის პრინციპი.

პროგრამის საავტორო უფლებები დაცულია!

Hello. This is web parsing project from Bachi Mosulishvili. Lecturer: Lika Svanadze.
In this file you will see comments, that describe how each line works, however, I will try to introduce
working principle of this program.

All rights reserved! """


'''პროგრამა დაფუძნებულია ვებ-გვერდზე ebg.ge, რაც ebay.com-ის ქართული ანალოგია.
პროგრამის გაშვებისთანავე პროგრამა მომხმარებელს სთხოვს შეიყვანოს საძიებო სიტყვა ან სიტყვები, რის შემდეგაც იწყება კოდის
მუშაობა და ამ ფრაზის საშუალებით ინფორმაციის მოძიება. უშუალოდ კოდის ნაწილს რომ შევეხოთ, პროგრამა თითოეულ განცხადებაზე
იღებს ზოგად ინფორმაციას და ასევე ხსნის განცხადებას და ამ გვერდიდანაც იღებს მონაცემებს, რაც ფუნქციებად მაქვს აღწერილი
კოდის დასაწყისში. დანარჩენს კომენტარების სახით გაეცნობით. 

Program is based on web-page ebg.ge, which is Georgian analogue of ebay.com.
After running the program, it will prompt user to type keyword or keywords after which code starts working and
searching using mentioned keyword(s). Let's talk about code directly. Program will get general information about
each advertisement and also opens the ad to get more detailed info about it, which I have defined as functions.
You will get to know about code using comments later.'''

import csv
import requests
from bs4 import BeautifulSoup as BS
from lxml import etree
from random import randint
from time import sleep



'''ქვემოთ აღწერილ ფუნქციებში გამოვიყენე დამატებით მოდული lxml რათა უფრო მარტივად, xpath-ის საშუალებით მეპოვა ესა თუ
ის ელემენტი. რა თქმა უნდა, გამოვიყენე ყველა პროგრამისტის განუყრელი მეგობარი - StackOverflow

I have used additional module lxml in the functions down below just to find each element more easily, using xpath.
Of course, I used StackOverflow, which is best friend of each programmer.'''


def Left(url):  # აღვწერე ფუნქცია უშუალოდ განცხადების გვერდიდან ნივთების დარჩენილი რაოდენობის წამოსაღებად.
                # Defined function to get the amount of items left from the ad page.
    sleep(randint(1, 5))
    c = requests.get(url).text
    s = BS(c, 'html.parser')
    dom = etree.HTML(str(s))
    left = dom.xpath(
        "//*[@id=\"product-in\"]/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/form[1]/div/div[1]/p[1]/span/span[2]")[
        0].text.strip()
    return left


def Delivery_date(url):  # აღვწერე ფუნქცია უშუალოდ განცხადების გვერდიდან ნივთების სავარაუდო მიტანის თარიღის წამოსაღებად.
                         # Defined function to get the estimated delivery date from the ad page.
    try:
        sleep(randint(1, 5))
        c = requests.get(url).text
        s = BS(c, 'html.parser')
        dom = etree.HTML(str(s))
        delivery_date = dom.xpath(
            '//*[@id="product-in"]/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/form[1]/div/div[4]/section[3]/div['
            '1]/p[2]')[
            0].text.split(' ')[2]
        return delivery_date
    except:
        pass


def Location(url):  # აღვწერე ფუნქცია უშუალოდ განცხადების გვერდიდან ნივთების ლოკაციის წამოსაღებად.
                    # Defined function to get the location from the ad page.
    sleep(randint(1, 5))
    c = requests.get(url).text
    s = BS(c, 'html.parser')
    dom = etree.HTML(str(s))
    location = dom.xpath(
        '//*[@id="product-in"]/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/form[1]/div/div[4]/section[3]/div['
        '3]/p[2]')[
        0].text
    return location


# მომხმარებელს შეჰყავს საძიებო სიტყვა და გარდავქმნი მასში ' '-ს '+'-ად, რათა შემდეგ URL-ში ჩავსვა.
# User types keyword(s) and I replace ' ' with '+' to put it in URL.
searchValue = input('What are you searching?\n').replace(' ', '+')

# ვიყენებ try ... except-ს იმ შემთხვევის თავიდან ასაცილებლად, თუკი ძიების შედეგში 5-ზე ნაკლები გვერდის რაოდენობაა.
# I use try ... except to avoid page numbers more than 5 in search results.
try:
    file = open('products.csv', 'w')
    file_obj = csv.writer(file)
    file_obj.writerow(['Title', 'Price', 'Amount left', 'Delivery date', 'Location'])
    for page in range(1, 6):  # Paging
        url = f'https://ebg.ge/catalog?s={searchValue}&p={page}'
        content = requests.get(url).text
        s = BS(content, 'html.parser')
            # ვუახლოვდები კონკრეტულ სექციას, რათა უფრო მივუახლოვდე ჩემთვის საჭირო ელემენტებს.
            # Getting closer to section just to get even closer to wanted elements.
        section1 = s.find('div', class_='col-sm-7 col-md-9')
        section2 = section1.find('div', class_='row')
        allItems = section2.find_all('div', class_='col-sm-6 col-md-3 item_ebay')

            # თითოეულ ელემენტში (item) ვიღებ მონაცემებს და ვბეჭდავ.
            # I am getting data from each element (item) and print.
        for item in allItems:
            title = item.find('p').text.strip()
            price = item.find('div', class_='product_prime_price').text.replace(' i', 'GEL').strip()
            url = item.find('a', class_='ce-fav-ic-full').get('href').strip()
            left = Left(url)
            delivery_date = Delivery_date(url)
            location = Location(url)
            print(f'TITLE:\n'
                  f'{title}\n\n'
                  f'PRICE:\n'
                  f'{price}\n\n'
                  f'LEFT:\n'
                  f'{left} items\n\n'
                  f'DELIVERY DATE:\n'
                  f'{delivery_date}\n\n'
                  f'LOCATION:\n'
                  f'{location}\n\n\n')
                # ვამატებ მონაცემებს CSV ფაილში
                # Adding data to CSV file
            file_obj.writerow([title, price, left, delivery_date, location])
            sleep(randint(1, 5))
        sleep(randint(1, 5))
    file.close()
except:
    pass
