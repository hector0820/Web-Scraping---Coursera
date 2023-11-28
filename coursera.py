import os
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

class Coursera:
    def __init__(self):
        self.webpage = 'https://www.coursera.org/'
        self.pages = None
        self.public_key = os.environ['MY_PUBLIC_KEY']
        self.email = os.environ['MAIL']
        self.data = []
        pass
    
    def MAIN(self):
        self.driver = webdriver.Firefox(options=Options())
        self.driver.get("https://www.coursera.org/")
        self.driver.maximize_window()
        time.sleep(3)
        pass

    def ENCRYPT(self):
        os.system(f"gpg --output cookies.json.gpg --encrypt --recipient {self.public_key} cookies.json")
        self.Delete_Cookies()
        pass
    
    def DECRYPT(self):
        os.system("gpg --output cookies.json --decrypt cookies.json.gpg")
        pass
    
    def Save_cookies(self): 
        cookies = self.driver.get_cookies()
        with open('cookies.json', 'w') as f: 
            json.dump(cookies, f, indent = 4)
        self.Encrypt()
        pass

    def COOKIES(self):
        try: 
            self.DECRYPT()
            with open('cookies.json', 'r') as f:
                cookies = json.load(f)

            [self.driver.add_cookie(cookie) for cookie in cookies]
            os.remove('cookies.json')
            self.driver.refresh()
        except:
            pass
    
    def ACCOMPLISHMENTS(self):
        self.driver.get("https://www.coursera.org/accomplishments")
        self.driver.set_page_load_timeout(5)
        pass
    
    def PAGINATION(self):
        botones = self.driver.find_elements(By.XPATH, '//div[@class="pagination-controls-container"]//button')
        self.pages = [int(boton.text) for boton in botones[2:-1]]
        pass
    
    def GET_PAGES(self):
        time.sleep(3)
        self.PAGINATION()
        for i in self.pages:
            self.driver.find_element(By.ID, f"pagination_number_box_{i}").click()
            self.driver.set_page_load_timeout(5)
            self.LINKEDIN_LABELS()
            self.GET_COURSES()
        pass

    def LINKEDIN_LABELS(self):
        time.sleep(3)
        temps = self.driver.find_elements(By.XPATH, "//button[@class='button-link add-to-linkedin-label']")
        [ temp.click() for temp in temps ]
        pass

    def HTML_TEMP(self, elements):
        try: 
            os.remove('temp.html')
        except:
            pass
        with open('temp.html', 'w') as h:
            for element in elements:
                h.write(element.get_attribute("innerHTML"))
        pass

    def HTML_READ(self):
        with open('temp.html', 'r') as h:
            soup = BeautifulSoup(h, 'html.parser')
        return soup
    
    def FIND_ELEMENTS(self, tag, classs):
        time.sleep(3)
        soup = self.HTML_READ()
        elements = soup.find_all(tag, {'class':f'{classs}'})

        for element in elements:
            data = [x.text for x in element.find_all('dd')] 
            self.data.append({'type':'course', 'name': data[0], 'date': data[2], 'id' : data[4], 'link' : data[5]})
        pass

    def GET_COURSES(self):
        time.sleep(3)
        cards = self.driver.find_elements(By.XPATH, "//div[@class='rc-CourseCertificateList']")

        self.HTML_TEMP(cards)
        self.FIND_ELEMENTS('div', 'linkedin-details')
        pass

    def GET_SPECIALIZATIONS(self):
        cards = self.driver.find_elements(By.XPATH, '//div[@class="rc-S12nCertificateList"]//div')

        self.HTML_TEMP(cards)
        self.FIND_ELEMENTS('div', 'linkedin-details')
        pass

    def CLEANING(self):
        for i in ['temp.html', 'cookies.json']:
            try:
                os.remove(i)
            except:
                pass
        self.driver.close()
        pass

    def SAVE_DATA(self):
        JSON_OBJECT = json.dumps(self.data, indent=4)

        with open('certificates.json', 'w') as c:
            c.write(JSON_OBJECT)
        pass

coursera = Coursera()
coursera.MAIN()
coursera.COOKIES()
coursera.ACCOMPLISHMENTS()
coursera.LINKEDIN_LABELS()
coursera.GET_SPECIALIZATIONS()
coursera.GET_PAGES()
coursera.SAVE_DATA()
coursera.CLEANING()