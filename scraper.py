import requests
from bs4 import BeautifulSoup
from datetime import datetime

debug = True

# live
# link = "https://www.ontario.ca/page/2024-ontario-immigrant-nominee-program-updates"
# res = requests.get(link).text

#test
f = open("./prettyOINP.txt", "r", encoding="utf-8")
res = f.read()
f.close()


soup = BeautifulSoup(res, 'html.parser')

latestDrawDate = soup.find_all("h3")[0].get_text().strip()
if debug: print("latest Draw Date from the site:", latestDrawDate)

#checking against current date
currentSystemDate = datetime.now().strftime("%B %e, %Y")
if debug: print("current system date:", currentSystemDate)

#think about how to alert
if currentSystemDate == latestDrawDate:
    print("A draw happened today")


# print(soup.prettify())