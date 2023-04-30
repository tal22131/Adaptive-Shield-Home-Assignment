import requests
from bs4 import BeautifulSoup

def fanc():
    # getting the html content of https://en.wikipedia.org/wiki/List_of_animal_names
    url = 'https://en.wikipedia.org/wiki/List_of_animal_names'
    response = requests.get(url)
    html_content = response.content

    # check that the site has been reached
    if response.status_code != 200:
        print("Error! Status code is not 200.")
        return 1

    # parse html content with beautifulSoup.
    # Making sure im takeing the data of the second table on the page.
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find_all('table', {'class': 'wikitable'})[1]

    # Extract the th elements in the first row.
    header_row = table.find_all('tr')[0]
    headers = [th.text.strip() for th in header_row.find_all('th')]
    # print(headers) # used for testing, to find the index of "Animal" & "Collateral adjective"

    # Instead of using magic numbers and taking risk that the page will change in the future,
    # This section of the code will find the index location of the headers we are looking into.
    target_headers = ['Animal', 'Collateral adjective']
    animalLoc = headers.index(target_headers[0]) # equals to 0
    collateralAdjectiveLoc = headers.index(target_headers[1]) # equals to 5
    
    # Using dict to store the data:
    data = {}
    # for loop going on all of the cells:
    for row in table.find_all('tr')[1:]:  # "[1:]" to exclude the header row.
        cells = row.find_all('td') # devide each row.
        if len(cells) == 0: continue # If the cell is empty; skips it, To avoid cells that contains the first letter of the animals
        animal = cells[animalLoc].text.strip()
        
        # To avoid the cell data crumping together, I'm replacing "<br/>" with ", "
        cellContent = str(cells[collateralAdjectiveLoc])
        cellContent = cellContent.replace('<br/>', ', ')
        textContent = BeautifulSoup(cellContent, 'html.parser').get_text().strip()

        # adding the adjectives to data dict
        adjectives = [adj.strip() for adj in textContent.strip().split(',')]
        data[animal] = adjectives

    for animal, adjectives in data.items():
        print(f'{animal}: {", ".join(adjectives)}')

if __name__ == "__main__":
    fanc()