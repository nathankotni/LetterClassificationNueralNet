import installLibraries
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from PIL import Image

options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome()
url = 'https://www.calligrapher.ai/'

driver.get(url)

def collectData(charac):
    path = './Images/' + charac
    if not os.path.exists(path):
        os.mkdir(path)

        driver.find_element(By.ID, "text-input").send_keys(charac)
        numImg = 1
        for _ in range(500):
            driver.find_element(By.ID, "text-input").send_keys(Keys.ENTER)
            imageTitle = charac + str(numImg) + '.png'
            time.sleep(0.1)
            screenshot = driver.find_element(By.ID, "canvas").find_element(By.TAG_NAME, "path").screenshot_as_png
            with open('./Images/' + charac + '/' + imageTitle, 'wb') as file:
                file.write(screenshot)
            numImg += 1
    driver.find_element(By.ID, "text-input").clear()


def collectDataTest(charac):
    path = './ImagesTest/' + charac
    if not os.path.exists(path):
        os.mkdir(path)

        driver.find_element(By.ID, "text-input").send_keys(charac)
        numImg = 1
        for _ in range(100):
            driver.find_element(By.ID, "text-input").send_keys(Keys.ENTER)
            imageTitle = charac + str(numImg) + '.png'
            time.sleep(0.1)
            screenshot = driver.find_element(By.ID, "canvas").find_element(By.TAG_NAME, "path").screenshot_as_png
            with open('./ImagesTest/' + charac + '/' + imageTitle, 'wb') as file:
                file.write(screenshot)
            numImg += 1
    driver.find_element(By.ID, "text-input").clear()


characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',]


for _ in range(125):
    driver.find_element(By.ID, "speed-slider").send_keys(Keys.ARROW_RIGHT)
    driver.find_element(By.ID, "bias-slider").send_keys(Keys.ARROW_RIGHT)
    driver.find_element(By.ID, "width-slider").send_keys(Keys.ARROW_RIGHT)
for charact in characters:
    collectData(charact)

for characte in characters:
    collectDataTest(characte)




