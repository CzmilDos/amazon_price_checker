import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.message import EmailMessage
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


def check_price(Url):
    page = requests.get(Url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(name='span', class_='a-price-whole').text[:-1]

    if len(price) > 3:
        formated_price = price.split()[0] + price.split()[1]
        return formated_price
    else:
        return price


def sendMail(email, Url):
    port = 465  # SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "czmild.montana@gmail.com"
    receiver_email = email
    password = '##########'
    subject = "C'est le moment pour ton achat !"
    message = f"""
    Le prix a baissé! go pour ton achat!\n
    Voici le lien: {Url}
              """
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(message)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, em.as_string())
        print("Gooo!")
    exit()


if __name__ == '__main__':
    URL = input("Entrer le lien amazon du produit: ")
    my_price = input("\nSaisir prix d'achat souhaité: ")
    mailAddress = input("\nEntrer l'adresse email de notification: ")

    try:
        debut = True
        while(True):
            if float(check_price(URL)) <= float(my_price):
                sendMail(mailAddress, URL)
            else:
                if debut:
                    print('\nVous recevrez un mail lorsque le produit sera au prix souhaité. \nPour arrêter le programme, faites Ctrl C\n')
                print('Pas encore au bon prix...')
                time.sleep(10800)
            debut = False
    except KeyboardInterrupt:
        pass
