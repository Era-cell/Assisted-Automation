import os
import Testing.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Job(webdriver.Chrome):
    def __init__(self, driver_path=r"E:\AssistedAutomation", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        opts = webdriver.ChromeOptions()
        opts.add_argument("--start-maximized")
        opts.add_experimental_option("detach", True)
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Job, self).__init__(options=opts)
        self.implicitly_wait(40)
        self.wait = WebDriverWait(self, 20)
        self._emptys = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def chooseType(self, type):
        o = self.find_element(
            By.XPATH,
            const.job_categories
        )
        o.click()
        self.find_element(
            By.XPATH,
            const.c1engineering
        ).click()

    def clickemptyspace(self):
        self.wait.until(EC.presence_of_element_located((
                By.XPATH,
                "/html/body/div[11]/div[1]"
        ))).click()

    def recentGraduated(self, status='No'):
        self.find_element(
            By.XPATH,
            const.graduated
        ).click()
        no, yes = self.find_element(
            By.ID,
            "mat-select-6-panel"
        ).find_elements(By.TAG_NAME, 'mat-option')
        if status == 'Yes':
            yes.click()
        else:
            no.click()

    def applyfilter(self, location='india', city='bangalore'):
        # set location
        # 1.set country
        self.find_element(
            By.XPATH,
            const.lpath
        ).click()
        parent = self.find_element(
            By.ID,
            "mat-select-0-panel"
        )
        region_list = parent.find_elements(
            By.TAG_NAME,
            "mat-option"
        )
        # list[0].click()
        for i in region_list:
            if location in i.find_element(
                    By.TAG_NAME,
                    'span'
            ).text.lower():
                i.click()
                break

        self.clickemptyspace()

        # 2.set city-------------
        self.find_element(
            By.XPATH,
            const.cpath
        ).click()
        parent = self.find_element(
            By.ID,
            "mat-select-2-panel"
        )
        for i in parent.find_elements(By.TAG_NAME, 'mat-option'):
            if city in i.find_element(
                    By.TAG_NAME,
                    'span'
            ).text.lower():
                i.click()
                break
        self.clickemptyspace()
        self.recentGraduated()
        self.clickemptyspace()

    def getJobList(self):

        jobelements = self.find_element(
            By.CLASS_NAME,
            "job-results-container"
        ).find_element(By.TAG_NAME, "search-job-cards").find_element(By.TAG_NAME, "mat-accordion").find_elements(By.TAG_NAME,"mat-expansion-panel")
        joblist=[]
        for i in range(len(jobelements)):
            joblist.append(
                self.find_element(By.XPATH,
                f"/html/body/div[2]/search-app/search-base-search-holder/search-results/div/div/div[2]/search-job-cards/mat-accordion/mat-expansion-panel[{i+1}]/mat-expansion-panel-header/span[1]/mat-panel-title/p[1]/a/span").text
            )
        return joblist
