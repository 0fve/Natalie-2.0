import requests, os
from bs4 import BeautifulSoup 
from time import sleep
from colorama import init, Fore
import shutil
init()


class Natalie:
    print("\n\n")
    def __init__(self, link):
        self.link = link
        self.headers = {
            "user-agent": "Mozilla/4.9 (Windows NT 10.0; Win64; x64) AppleWebKit/537.32 (KHTML, like Gecko) Chrome/90.0.4430.86 Safari/537.3",
            'dnt': '1',
        }
        self.page = requests.get(self.link, headers=self.headers)
        self.soup = BeautifulSoup(self.page.text,'html.parser')

    def get_elements(self):
        self.links = []
        try:          
            # This loop will get each element< and then extract the image link from it
            for i in range(100):
                ele = self.soup.select(f'#image-{i}')
                # {ele[0]['data-src']}
                print(f"           {i+1}.{Fore.CYAN}    {ele[0]['data-src'][0:30]}.... {Fore.RESET}") #data-src is where the link is, its a 2D list thats why we are using [0]
                # next pic
                requests.post('https://analytics.zg-api.com/click/se_prod_web/e6be386d-6e52-417b-9875-6066409db730',headers=self.headers)
                if 'img' in ele[0]['data-src']:
                    self.links.append(ele[0]['data-src'])
        except Exception as e:
            pass
        self.naming()
                
    def naming(self):
        try:
            self.estate_name = self.soup.select('#content > main > div.row.DetailsPage > article.right-two-fifths > section.main-info > h1 > a')
            sleep(2)
            self.estate_name = self.estate_name[0].text
            estate_status = self.soup.select('#content > main > div.row.DetailsPage > article.right-two-fifths > section.main-info > div > div.details_info_price > div.price > span.secondary_text')
            estate_status = estate_status[0].text
        except Exception as e:
            self.estate_name = self.soup.select('#content > main > div.row.DetailsPage > article.right-two-fifths > section.main-info > h1 > a')
            sleep(2)
            self.estate_name = self.estate_name[0].text
            
        # goto folder and name it after estate name
        try:
            os.mkdir(f'{self.estate_name} -{estate_status}')
            os.chdir(f'{self.estate_name} -{estate_status}')
        except OSError as e:
            shutil.rmtree(f'{self.estate_name} -{estate_status}')
            os.mkdir(f'{self.estate_name} -{estate_status}')
            os.chdir(f'{self.estate_name} -{estate_status}')

        self.download_pics()

    def download_pics(self):
        i = 1
        
        for link in self.links:
            with open(f'{self.estate_name} {i}.jpg ', 'wb') as f:
                pic = requests.get(link)
                f.write(pic.content)
                i += 1

        self.get_description()

    def get_description(self):
        try:
            description = self.soup.select('#content > main > div.row.DetailsPage > article.left-three-fifths > section.DetailsPage-contentBlock > div.Description > div.Description-block > p')
            with open('description.txt','w') as f:
                f.write(description[0].text)
            
            
        except Exception as e:
            print(e)
            print('could not extract description, try again.')



Natalie(input(Fore.GREEN + "\n           Link: " + Fore.RESET)).get_elements()
print('\n')
q = input(f"\n           {Fore.YELLOW}Do you wish to continue? (Y/N){Fore.RESET}: ")

if q == 'Y' or q == 'y':
    run = True
else:
    run = False
    print(f'\n               {Fore.RED}         GoodBye.')
    sleep(3)

while run:
    Natalie(input(Fore.GREEN + "\n           Link: " + Fore.RESET)).get_elements()

    q = input(f"\n           {Fore.YELLOW}Do you wish to continue? (Y/N){Fore.RESET}: ")
    if q == 'n' or q == 'N':
        run = False
        print(f'\n               {Fore.RED}         GoodBye.')
        sleep(3)
    else:
        run = True