import requests
import os
from dotenv import load_dotenv, dotenv_values
from bs4 import BeautifulSoup, element
from datetime import datetime
from twilio.rest import Client
from time import sleep
import json

def alreadySent(messageBody, dateString, typeString):
    if not os.path.isfile(os.path.join("./", dateString + "-" + typeString + ".txt")):
        return False
    else:
        f = open(os.path.join("./", dateString + "-" + typeString + ".txt"), "r")
        compareTo = f.read()
        f.close()
        if compareTo == messageBody:
            return True
        else:
            return False

debug = True

# load_dotenv()

textTest = True
if os.getenv("TEXT_TEST") == "false" or os.getenv("TEXT_TEST") == None or len(os.getenv("TEXT_TEST").strip()) == 0:
    textTest = False

sendTo = "Kushagra"
if os.getenv("SEND_TO") == "All" or os.getenv("SEND_TO") == None or len(os.getenv("SEND_TO").strip()) == 0:
    sendTo = "All"

recipients = ["KUSHAGRA_NUMBER", "MAHAK_NUMBER", "CHIRAG_SETHI_NUMBER"]

if debug: print("I got", os.getenv("TEXT_TEST"), "as text test")
if debug: print("I got type of text test as ", type(os.getenv("TEXT_TEST")))

if not textTest:
    # live
    link = "https://www.ontario.ca/page/2024-ontario-immigrant-nominee-program-updates"
    res = requests.get(link).text
else:
    #test
    f = open("./prettyOINP.txt", "r", encoding="utf-8")
    res = f.read()
    f.close()


soup = BeautifulSoup(res, 'html.parser')
try:
    latestDrawElement = soup.find_all("h3")[0]
    latestDrawDate = latestDrawElement.get_text().strip()
except:
    print("An error occurred reading the date")
    print("Here is the latest Draw element")
    print(latestDrawElement)
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="❌Some error occurred with OINP scraper. Check github logs❌",
        from_=os.getenv("FROM_NUMBER"),
        to=os.getenv("KUSHAGRA_NUMBER"),
    )
    exit(0)
if debug: print("latest Draw Date from the site:", latestDrawDate)

#checking against current date
res = requests.get("http://worldtimeapi.org/api/timezone/America/Toronto")
jsonData = json.loads(res.text)
dateData = datetime.fromisoformat(jsonData['datetime'])
currentSystemDate = dateData.strftime("%B %e, %Y").replace("  ", " ")
if debug: print("current system date Full:", dateData)
if debug: print("current system date:", currentSystemDate)
if debug: print("latest Draw Date:", latestDrawDate)

#think about how to alert
try:
    if currentSystemDate == latestDrawDate:
        messageBody="🚨🚨OINP Draw Alert🚨🚨\n"
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
        while messageBody[-1] == "\n":
            messageBody = messageBody[:-1]
        if debug: print(messageBody)

        if sendTo == "Kushagra":
            if debug: print("Sending only to Kushagra")
            message = client.messages.create(
                body=messageBody,
                from_=os.getenv("FROM_NUMBER"),
                to=os.getenv("KUSHAGRA_NUMBER"),
            )
            if debug:
                print("Log for sending to", "KUSHAGRA_NUMBER")
                print(message.body)
        elif sendTo == "All":
            #check if this is already sent or not
            if not alreadySent(messageBody, currentSystemDate, "OINP"):
                #create the file to record the messageBody
                if debug: print("Sending messages to all")
                f = open(os.path.join("./", currentSystemDate + "-" + "OINP" + ".txt"), "w")
                f.write(messageBody)
                f.close()
                githubOutputObjectFile = open(os.environ["GITHUB_OUTPUT"], 'a')
                githubOutputObjectFile.write("newPush=true\n")
                githubOutputObjectFile.close()
                #now sending announcements
                for person in recipients:
                    personNumber = os.getenv(person)
                    if not (len(personNumber.strip()) == 0 or personNumber == None):
                        message = client.messages.create(
                            body=messageBody,
                            from_=os.getenv("FROM_NUMBER"),
                            to=personNumber,
                        )
                        if debug:
                            print("Log for sending to", person)
                            print(message.body)
                        sleep(1)
            else:
                if debug: print("This is a repeat scrape")
    else:
        print("Date didn't match")
        print("There is no current draw")
except BaseException as e:
    print("An exception occurred")
    print(e)
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="❌Some error occurred with OINP scraper. Check github logs❌",
        from_=os.getenv("FROM_NUMBER"),
        to=os.getenv("KUSHAGRA_NUMBER"),
    )
except:
    print("Some other error occurred")
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="❌Some error occurred with OINP scraper. Check github logs❌",
        from_=os.getenv("FROM_NUMBER"),
        to=os.getenv("KUSHAGRA_NUMBER"),
    )
