import requests
from bs4 import BeautifulSoup
import os
import re

#*** This script is a modified verion of the final main script to download all of the animals pictures. *** 
#*** Bonus 1 ***

# getting the html content of https://en.wikipedia.org/wiki/List_of_animal_names
url = 'https://en.wikipedia.org/wiki/List_of_animal_names'
response = requests.get(url)
html_content = response.content
# check that the site has been reached
if response.status_code != 200:
    print("Error! Status code is not 200.")
    

# parse html content with beautifulSoup.
# Making sure im takeing the data of the second table on the page.
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find_all('table', {'class': 'wikitable'})[1]
# Extract the th elements in the first row.
header_row = table.find_all('tr')[0]
headers = [th.text.strip() for th in header_row.find_all('th')]

# Instead of using magic numbers and taking risk that the page will change in the future,
# This section of the code will find the index location of the headers we are looking into.
target_headers = 'Animal'
animalLoc = headers.index(target_headers) # equals to 0

# for loop going on all of the cells:
for row in table.find_all('tr')[1:]:  # "[1:]" to exclude the header row.
    cells = row.find_all('td') # devide each row.
    if len(cells) == 0: continue # If the cell is empty; skips it, To avoid cells that contains the first letter of the animals
    animalWikiUrl = "https://en.wikipedia.org" + cells[animalLoc].find('a')['href'] # getting the url for the animal page.
    animalPageResponse = requests.get(f'{animalWikiUrl}') # sending request to get the animal page site.
    animalPageContent = animalPageResponse.content
    animalPageSoup = BeautifulSoup(animalPageContent, 'html.parser')

    # Using try-except incase there is no infobox in the animal page.
    try:
        imageUrl = animalPageSoup.find('table', {'class': re.compile('infobox.*')}).find('img')['src'] # using regex to find anything with "infobox" in it.
    except AttributeError:
        findThumbinner = animalPageSoup.find('div', {'class': 'thumbinner'})
        if findThumbinner == None:
            continue
        imageUrl = animalPageSoup.find('div', {'class': 'thumbinner'}).find('img')['src'] # find "thumbinner" div in it.

    animal = cells[animalLoc].text.strip().split(" ")[0] # split by space and takes the first word to not include wiki info like: "(list) Also see Boar"

    imageUrl = "https:"+imageUrl # adds "https:" to the name of the url
    if "/" in animal: # if animal have / in the name (like ass/donkey) removes the "/"
        animal = animal.split("/")[0] + animal.split("/")[1]
    image_path = os.path.join('./tmp/', animal+".jpg")
    response = requests.get(imageUrl)
    with open(image_path, 'wb') as f:
        f.write(response.content)

