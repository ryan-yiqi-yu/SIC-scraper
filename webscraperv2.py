from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.common.keys import Keys

class Scraper:
    link = "https://www.sec.gov/edgar/searchedgar/companysearch.html"
    search_bar_id = "company"
    chromedriver_filepath = '/Users/Ryan/Desktop/chromedriver'
    sic_tag = 'a'
    txt_file_name = 'companies-sic-codes.txt'
    pop_up_xpath = "/html/body/div[8]/div/div[1]/div/a[1]"

    def __init__(self, write_txt, read_txt):
        self.list_of_companies = read_txt
        self.data_file = write_txt

    def is_pop_up(self, browser):
        try:
            browser.find_element_by_xpath(self.pop_up_xpath)
            return True
        except:
            return False

    def open_browser(self, link, id, cd_filepath):
        browser = webdriver.Chrome(cd_filepath)


        def search_term_link(search_term):
            browser.get(link)
            sleep(1.2)
            if self.is_pop_up(browser):
                close_button = browser.find_element_by_xpath(self.pop_up_xpath)
                close_button.click()
            search_bar = browser.find_element_by_id(id)
            search_bar.send_keys(search_term)
            search_bar.send_keys(Keys.ENTER)
            sleep(1.2)
            current_url = browser.current_url
            return current_url
        return search_term_link

    def find_sic_in_soup(self, url, name, file):
        soup = self.soupify(url)
        company_name = soup.find('span', {"class":"companyName"})
        print()
        print(name + ":")
        list = ["\n"]
        for bits in soup.find_all(self.sic_tag):
            if str(bits.text).isdigit() and bits.next_sibling and bits.text:
                print(company_name.text.split(' CIK', 1)[0], "SIC:", bits.text, bits.next_sibling)
                list.extend(["SIC:", str(bits.text), str(bits.next_sibling)])
        self.write_to_file(file, list)

    def open_to_write_file(self, txt_file_name):
        f = open(txt_file_name, "w")
        return f

    def write_to_file(self, file, arr):
        file.writelines(arr)

    def close_file(self, file):
        file.close()

    def soupify(self, url):
        source_code = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source_code)
        return soup

    def find_all_sic(self):
        searchable_browser = self.open_browser(self.link, self.search_bar_id, self.chromedriver_filepath)
        f = self.open_to_write_file(self.data_file)
        f2 = open(self.list_of_companies, 'r')
        companies_in_list = f2.readlines()
        for company in companies_in_list:
            self.find_sic_in_soup(searchable_browser(company), company, f)

        self.close_file(f)

bot = Scraper("1-4sic.txt", "100-400companies.txt")
bot.find_all_sic()
