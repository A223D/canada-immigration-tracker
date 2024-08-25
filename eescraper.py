import os
from dotenv import load_dotenv, dotenv_values
from bs4 import BeautifulSoup, element
from datetime import datetime
from twilio.rest import Client
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
if debug: print("TextTest evaluated as", textTest)

soup = ""
if not textTest:
    # live
    if debug: print("This is a live call")
    # link = "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations.html"
    link = "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions/express-entry-rounds.html"
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    # WebDriverWait(driver, 10)
    sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    driver.quit()

else:
    #test
    if debug: print("Using given text file")
    f = open("./prettyEE.txt", "r", encoding="utf-8")
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()

latestDrawElement = soup.find_all("tr")[1]
latestDrawDate = latestDrawElement.find_all("td")[1].get_text().strip()
if debug: print("latest Draw Date from the site:", latestDrawDate)

#checking against current date
currentSystemDate = datetime.now().strftime("%B %e, %Y")
if debug: print("current system date:", currentSystemDate)

#think about how to alert
if currentSystemDate == latestDrawDate:
    messageBody="🚨🚨EE Draw Alert🚨🚨\n"
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    messageBody+="=>"
    messageBody+= latestDrawElement.find_all("td")[2].get_text().strip()
    messageBody+= "/Minimum Score: "
    messageBody+= latestDrawElement.find_all("td")[4].get_text().strip()
    
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
        if not alreadySent(messageBody, currentSystemDate, "EE"):
            #create the file to record the messageBody
            if debug: print("Sending messages to all")
            f = open(os.path.join("./", currentSystemDate + "-" + "EE" + ".txt"))
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