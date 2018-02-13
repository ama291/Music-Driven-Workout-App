#python3

from bs4 import BeautifulSoup as Soup
from multiprocessing.dummy import Pool
import newlinejson as nlj
import requests
import json

class Runner():
    """Gets the body parts from the exercise page of bodybuilding.com, them gets the exercises from those body part urls
    """

    session = requests.session()
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                        'https': 'socks5://127.0.0.1:9050'}

    def __init__(self):
        self.s = Scraper()

    def run(self, filename):
        body_parts = self.get_body_parts()
        exercises = [exercise for sublist in list(map(self.get_exercises, body_parts)) for exercise in sublist]
        res = list(map(self.get_exercise, exercises))
        self.save_to_file(filename, res)

    def get_body_parts(self):
        res = []
        sitemap = 'https://www.bodybuilding.com/exercises'
        soup = Soup(self.session.get(sitemap).content, 'lxml')
        body_list = soup.find('div', {'class':'exercise-list'})
        return ['https://www.bodybuilding.com' + x['href'] for x in body_list.find_all('a')]

    def get_exercises(self, body_part):
        urls = []
        i = 1
        while True:
            body_part_page = body_part + '/' + str(i)
            soup = Soup(self.session.get(body_part_page).content, 'lxml')
            exercise_wrappers = soup.find_all('h3', {'class': 'ExHeading ExResult-resultsHeading'})
            if exercise_wrappers == []:
                return urls
            urls += ['https://www.bodybuilding.com' + x.a['href'] for x in exercise_wrappers]
            i += 1

    def get_exercise(self, exercise):
        failures = 0
        for i in range(10):
            try:
                soup = Soup(self.session.get(exercise).content, 'lxml')
                return self.s.process(soup)
            except:
                continue
        return

    def save_to_file(self, filename, results):
        writer = nlj.open(filename, 'w')
        for item in results:
            writer.write(item)
        writer.close()

class Scraper():
    """Given an exercise page html, will parse the page and return the needed info"""

    def process(self, soup):
        """Given an exercise soup, parse the soup.
        """
        return {
            'exercise_name': self.get_name(soup),
            'type': self.get_type(soup),
            'main_muscle_worked': self.get_main_muscle_worked(soup),
            'equipment': self.get_equipment(soup),
            'level': self.get_level(soup),
            'associated_images': self.get_image_urls(soup),
            'guide': self.get_guide(soup)
        }

    def get_name(self, soup):
        try:
            return soup.find('meta', {'property': "og:title"})['content'].split('|')[0].strip()
        except:
            return None

    def get_type(self, soup):
        try:
            location = soup.find('ul', {'class': "bb-list--plain"})
            type_li = list(filter(lambda x: 'Type' in x.get_text(), location.find_all('li')))[0]
            return type_li.a.get_text().strip()
        except:
            return None

    def get_main_muscle_worked(self, soup):
        try:
            location = soup.find('ul', {'class': "bb-list--plain"})
            type_li = list(filter(lambda x: 'Main Muscle Worked' in x.get_text(), location.find_all('li')))[0]
            return type_li.a.get_text().strip()
        except:
            return None

    def get_equipment(self, soup):
        try:
            location = soup.find('ul', {'class': "bb-list--plain"})
            type_li = list(filter(lambda x: 'Equipment' in x.get_text(), location.find_all('li')))[0]
            return type_li.a.get_text().strip()
        except:
            return None

    def get_level(self, soup):
        try:
            location = soup.find('ul', {'class': "bb-list--plain"})
            type_li = list(filter(lambda x: 'Level' in x.get_text(), location.find_all('li')))[0]
            return type_li.get_text().split(':')[1].strip()
        except:
            return None

    def get_image_urls(self, soup):
        try:
            return [img['src'] for img in soup.find_all('img', {'class': 'ExImg ExDetail-img js-ex-enlarge'})]
        except:
            return None

    def get_guide(self, soup):
        try:
            guide = soup.find('ol', {'class': 'ExDetail-descriptionSteps'})
            return [x.get_text() for x in guide.find_all('li')]
        except:
            return None


r = Runner()
r.run('exercises.json')
