import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import json
from unidecode import unidecode

start_url = "https://www.boxofficemojo.com/date/2023-06-02/" #request
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
movie_urls = []
# url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
response = requests.get(start_url, headers=header) #explain beautfiful soup and etree
soup = BeautifulSoup(response.content, 'html.parser')
dom = et.HTML(str(soup))
movie_urls_list = dom.xpath('//td[@class="a-text-left mojo-field-type-release mojo-cell-wide"]/a/@href')

class CrawlMovies:
    def __init__(self, start_url, header):
        self.start_url = start_url
        self.header = header
        self.movie_urls = []
        self.movie_urls_list = []
        self.movies_info = []

    def get_dom(self, start_url):
        response = requests.get(start_url, headers=self.header)
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = et.HTML(str(soup))
        return dom
    
    def get_movie_dim(self, start_url):
        dom = self.get_dom(start_url)
        movie_urls_list = dom.xpath('//td[@class="a-text-left mojo-field-type-release mojo-cell-wide"]/a/@href')
        return movie_urls_list
    
    def get_movie_urls(self):
        movie_urls_list = self.get_movie_dim(self.start_url)
        for i in movie_urls_list:
            long_url = "https://www.boxofficemojo.com" + i
            short_url = long_url.split("?")[0]
            self.movie_urls.append(short_url)
        return self.movie_urls
    # add data to json line by line
    def write_to_json(self, new_data, filename='data_v1.json'):
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data.append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

# ham nay la lay o imdb ne oki
    def get_movie_info(self):
        movie_urls = self.get_movie_urls()
        for movie_url in movie_urls:
            dom = self.get_dom(movie_url)
            id = movie_url.split("/")[4]
            ref_id = dom.xpath('//div[@id="title-summary-refiner"]/a/@href')[0].split("/")[2]
            dom_ref_id = self.get_dom("https://www.imdb.com/title/" + ref_id)
            abstract = dom_ref_id.xpath('//span[@class="sc-6a7933c5-1 fPmRoa"]')[0].text
            name = dom_ref_id.xpath('//h1[@data-testid="hero__pageTitle"]/span/text()')[0]
            genre = [i.text for i in dom_ref_id.xpath('//div[@data-testid="genres"]/div/a/span')]
    
            self.write_to_json(new_data={'id': id,
                                    'name': name,
                                    'genre': genre,
                                    'abstract': abstract,
                                    'ref_id': ref_id}, filename='data_v1.json')

        return self.movies_info
 # ham nay la lay o box office ne okiiiiii        
    def get_movie_from_box_office(self):
        dom = self.get_dom(self.start_url)
        tr = dom.xpath('//tr')

        for i in tr[1:]:
            td = i.xpath('.//td')
            rank = td[0].text
            name = td[2].xpath('.//a')[0].text
            daily_gross = td[3].text 
            gross_change_day = td[4].text
            theaters = td[6].text
            days_release = td[9].text
            try:
                distributor = td[10].xpath('.//a')[0].text
            except:
                distributor = ""

            self.write_to_json(new_data={'rank': rank,
                                    'name': name,
                                    'daily_gross': daily_gross,
                                    'gross_change_day': gross_change_day,
                                    'theaters': theaters,
                                    'days_release': days_release,
                                    'distributor': distributor}, filename='data_v2.json')

        return self.movies_info

if __name__ == "__main__":

    crawl = CrawlMovies(start_url, header)

    #to get movie info from imdb

    with open("data_v1.json", "w") as f:
        json.dump([], f)
    crawl.get_movie_info()

    #to get movie info from box office

    # with open("data_v2.json", "w") as f:
    #     json.dump([], f)
    # crawl.get_movie_from_box_office()

