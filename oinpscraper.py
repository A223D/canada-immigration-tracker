import requests
import os
from dotenv import load_dotenv, dotenv_values
from bs4 import BeautifulSoup, element
from datetime import datetime
from twilio.rest import Client
from time import sleep

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
latestDrawElement = soup.find_all("h3")[0]
latestDrawDate = latestDrawElement.get_text().strip()
if debug: print("latest Draw Date from the site:", latestDrawDate)

#checking against current date
currentSystemDate = datetime.now().strftime("%B %e, %Y")
if debug: print("current system date:", currentSystemDate)

#think about how to alert
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

    if textTest:
        message = client.messages.create(
            body=messageBody,
            from_=os.getenv("FROM_NUMBER"),
            to=os.getenv("KUSHAGRA_NUMBER"),
        )
        if debug:
            print("Log for sending to", "KUSHAGRA_NUMBER")
            print(message.body)
    else:
        #check if this is already sent or not
        if not alreadySent(messageBody, currentSystemDate, "OINP"):
            #create the file to record the messageBody
            f = open(os.path.join("./", currentSystemDate + "-" + "OINP" + ".txt"))
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
    print("There is no current draw")