from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import smtplib
import traceback
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
import schedule
import time
import datetime


def setup(url):
    chrome_options = Options();
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    driver = webdriver.Chrome(executable_path='/mnt/c/Users/Moti Begna/Downloads/ChromeDriver/chromedriver.exe', chrome_options=chrome_options)
    URL= url
    driver.get(URL)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,"html.parser")
    driver.quit()
    return soup, URL

def toFloat(price):
    price = float(price[1:len(price)])
    return price

def send_mail(type, price, URL, subject, content, imageFilename):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('begna002@umn.edu', 'fyahlujwpzhkrfje')

    msg = EmailMessage()

    # generic email headers
    msg['Subject'] =  subject
    msg['From'] = 'begna002@umn.edu'
    msg['To'] = 'coolfire1675@gmail.com'

    # set the plain text body
    msg.set_content(content)

    # now create a Content-ID for the image
    image_cid = make_msgid(domain='xyz.com')
    # if `domain` argument isn't provided, it will
    # use your computer's name

    # set an alternative html body
    if (type != "Status"):
        msg.add_alternative("""\
        <html>
            <body>
                <p>Price is now "{cost}"<br>
                   Check the link {url}
                </p>
                <img src="cid:{image_cid}">
            </body>
        </html>
        """.format(cost=str(price), url=URL, image_cid=image_cid[1:-1]), subtype='html')
    else:
        msg.add_alternative("""\
        <html>
            <body>
                <p>Price Checker is still active.
                </p>
            </body>
        </html>
        """.format(cost=str(price), url=URL, image_cid=image_cid[1:-1]), subtype='html')


    if (imageFilename != None):
        # now open the image and attach it to the email
        with open(imageFilename, 'rb') as img:

            # know the Content-Type of the image
            maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

            # attach it
            msg.get_payload()[1].add_related(img.read(),
                                                 maintype=maintype,
                                                 subtype=subtype,
                                                 cid=image_cid)




    server.sendmail("begna002@umn.edu", "coolfire1675@gmail.com", msg.as_string())
    print("Email has been sent")
    server.quit()

def checkPriceProduct(attempt, url, prodElement, priceElement, priceBelow, imageFilename, specifier):
    try:
        grabber, URL = setup(url)
        productName = grabber.find(prodElement[0], prodElement[1]).get_text()
        price = toFloat(grabber.find(priceElement[0], priceElement[1]).get_text())
        print("Product:", productName, "Price:", price)
        print("TimeStamp:", datetime.datetime.now(), "\n")
        if (specifier != None and specifier not in productName):
            print("Wrong Product Found, continuing job...")
        else:
            if (price < priceBelow):
                subject = f'Price for {productName} fell down!'
                content = f"Price is now {price}\nCheck the link {URL}"
                send_mail("tv", price, URL, subject, content, imageFilename)
            else:
                print(f"Price is not below ${priceBelow}")
    # For whatever reason, BeautifulSoup is unable to find values on occasion,
    # thus the code is run again until it functions properly or it is tried 10 times
    except AttributeError as error:
        attempt += 1
        if (attempt!=10):
            traceback.print_exc()
            print(error)
            print("Failed attempt", attempt, "trying again...")
            checkPriceProduct(attempt, url, prodElement, priceElement, priceBelow, imageFilename, specifier)
        else:
            print("BeautifulSoup was unable to find values after 10 attempts. Shutting down...")

def tv():
    attempt = 0
    url = "https://www.google.com/search?biw=1041&bih=754&tbm=shop&ei=7wtcXZOINLC80PEPq4WpyA0&q=best+buy+insignia+32%22&oq=best+buy+insignia+32%22&gs_l=psy-ab.3..33i299k1l3.3343.6598.0.6848.12.9.0.3.3.0.239.1015.0j5j1.6.0....0...1c.1.64.psy-ab..3.9.1032...0.0.Psp65njYACo"
    prodElement=("a", "AGVhpb")
    priceElement=("span","h1Wfwb")
    priceBelow = 129.00
    imageFilename = 'tv.jpg'
    checkPriceProduct(attempt, url, prodElement, priceElement, priceBelow, imageFilename, "Fire")

def chair():
    attempt = 0
    url = "https://www.google.com/search?q=Arozzi+-+Milano+Gaming+Chair+-+Red+best+buy&source=lnms&sa=X&ved=0ahUKEwiiz7GX2pHkAhVYIDQIHckzCmoQ_AUInQIoAA&biw=1536&bih=754"
    prodElement=("span", "pymv4e")
    priceElement=("div","e10twf T4OwTb")
    priceBelow = 199.00
    imageFilename = 'chair.jpg'
    checkPriceProduct(attempt, url, prodElement, priceElement, priceBelow, imageFilename, "Milano")

def statusCheck():
    subject = f'Price Checker Status Update'
    content = f"Price Checker is still active"
    send_mail("Status", 0.0, "URL", subject, content, None)


schedule.every().hour.at(":00").do(tv)
schedule.every().day.at("15:00").do(statusCheck)

while True:
    schedule.run_pending()
    time.sleep(1)
