from typing import List
import requests


from models import Session, Task, SearchResult

""" First I've tried to parse site via selenium, but it's too long. 
I have found another option to do this """


class Sender:
    def __init__(self, words_list: List, task_id: int):
        self.task_id = task_id
        self.list = words_list
        self.url = 'https://allo.ua/ua/catalogsearch/ajax/suggest/?currentTheme=main&currentLocale=uk_UA'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        self.session = Session()

    def grab_tips(self, key_word):
        req_session = requests.session()
        response = req_session.post(self.url, headers=self.headers, data={'q': key_word})
        response = response.json()
        try:
            result = response['query']

            result = [str(w) for w in result]
        except AttributeError:
            result = None
        return result

    def process_list(self):

        for word in self.list:
            try:
                result = self.grab_tips(word)
                task = self.session.query(Task).get(self.task_id)
                if result:
                    result = ''.join(res + ',' for res in result)
                    result = result[0:len(result) - 1]
                else:
                    result = ''
                task.last_word = word
                res = SearchResult(task_id=task.id, word=word, result=result)
                self.session.add(res)
                self.session.commit()
                print(f'[+] Search completed for <{word}>')
                if result:
                    for w in result.split(','):
                        print(f'\t+ {w}')
                else:
                    print('\t ! Not results found')
            except Exception:
                print(f'[!] An exception occured. Skiping <{word}>')

        self.session.close()

# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options
# import time
# import urllib.parse
# import logging

# class Graber:
#
#     def __init__(self, words_list: List):
#         self.list = words_list
#         self.gecko_path = '/usr/local/bin/geckodriver'
#         self.site_url = 'https://allo.ua/'
#
#         options = Options()
#         options.headless = True
#
#         self.options = options
#         self.driver = Firefox(options=options,
#                               executable_path=self.gecko_path)
#         self.driver.get(self.site_url)
#
#     def grab_tips(self, key_word):
#         input_form = self.driver.find_element_by_css_selector('input#search.input-text')
#         input_form.send_keys(key_word)
#         time.sleep(2)
#         box = self.driver.find_element_by_xpath('//ul[@id="search-suggest-query"]')
#         tips = box.find_elements_by_css_selector('li.search-suggest-word a')
#         tips = [urllib.parse.unquote(tip.get_attribute('href')) for tip in tips]
#         tips = [tip.split('/?q=')[-1] for tip in tips]
#
#         input_form.clear()
#
#         # Need to click somewhere to close suggestion box
#         div = self.driver.find_element_by_css_selector('div.main-menu-header')
#         div.click()
#
#         return tips
#
#     def process_list(self):
#         try:
#             for word in self.list:
#                 result = self.grab_tips(word)
#                 task = session.query(Task).order_by(Task.id.desc()).first()
#
#                 result = ''.join(res + ',' for res in result)
#                 result = result[0:len(result) - 1]
#
#                 task.last_word = word
#                 res = SearchResult(task_id=task.id, word=word, result=result)
#                 session.add(res)
#                 session.commit()
#                 session.commit()
#                 logging.info(f'[+] Search completed for <{word}>')
#                 for w in result:
#                     logging.info(f'\t+ {w}')
#             self.driver.close()
#         except Exception as e:
#             print(e)
#             self.driver.close()
