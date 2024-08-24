import requests
import os
from dotenv import load_dotenv, dotenv_values
from bs4 import BeautifulSoup, element
from datetime import datetime
from twilio.rest import Client
debug = True
# load_dotenv()

numbers = [os.getenv("KUSHAGRA_NUMBER")]

if debug: print("I got", os.getenv("TEXT_TEST"), "as text test")

if os.getenv("TEXT_TEST") == False:
    # live
    link = "https://www.ontario.ca/page/2024-ontario-immigrant-nominee-program-updates"
    res = requests.get(link).text
else:
    #test
    f = open("./prettyOINP.txt", "r", encoding="utf-8")
    res = f.read()
    f.close()


soup = BeautifulSoup(res, 'html.parser')
latestDrawElement = soup.find_all("h3")[0]
latestDrawDate = latestDrawElement.get_text().strip()
if debug: print("latest Draw Date from the site:", latestDrawDate)

#checking against current date
currentSystemDate = datetime.now().strftime("%B %e, %Y")
if debug: print("current system date:", currentSystemDate)

#think about how to alert
if currentSystemDate == latestDrawDate:
    messageBody="An OINP Draw occurred.\n"
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    catListElement = latestDrawElement.find_next("ul")
    for child in catListElement.children:
        if type(child) != element.Tag:
            continue
        if debug: print(child.find("a").contents[0].strip())
        messageBody+="=> "
        messageBody+= child.find("a").contents[0].strip()
        messageBody+="\n"
    
    #remove trailing "\n" if any
    messageBody = messageBody[:-1]
    if debug: print(messageBody)

    for number in numbers:
        message = client.messages.create(
            body=messageBody,
            from_=os.getenv("FROM_NUMBER"),
            to=number,
        )
        if debug:
            print("Log for sending to", number)
            print(message.body)
else:
    print("There is no current draw")