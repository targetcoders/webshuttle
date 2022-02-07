from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebCrawler:
    def __init__(self, start_url, options=None):
        if start_url == '':
            start_url = 'http://google.com'
        if not start_url.startswith('http://') | start_url.startswith('https://'):
            start_url = 'http://' + start_url
        self.service = Service(ChromeDriverManager().install())
        if options is None:
            self.driver = webdriver.Chrome(service=self.service)
            self.driver.maximize_window()
        else:
            self.driver = webdriver.Chrome(service=self.service, options=options)
        self.driver.implicitly_wait(3)
        self.driver.get(start_url)

    def execute_js(self, script):
        return self.driver.execute_script(script)

    def scroll_to(self, x, y):
        self.driver.execute_script("window.scrollBy({0}, {1});".format(x, y))

    def get_target_element(self):
        return self.driver.find_elements_by_class_name("ws-target-element")[0]

    def get_scroll_y(self):
        return self.execute_js("return window.scrollY;")

    def get_scroll_x(self):
        return self.execute_js("return window.scrollX;")

    def get_element_pos_x(self):
        return self.execute_js(
            '''
            let targetElement = document.getElementById('ws-tooltip');
            return targetElement.getBoundingClientRect().left-3;
            ''')

    def get_element_pos_y(self):
        return self.execute_js(
            '''
            let targetElement = document.getElementById('ws-tooltip');
            return targetElement.getBoundingClientRect().top-3;
            ''')

    def close_driver(self):
        self.driver.close()
