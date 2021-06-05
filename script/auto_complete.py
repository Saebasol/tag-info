import json
import logging
import re
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

formatter = logging.Formatter("%(asctime)s - (%(name)s) - [%(levelname)s]: %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

fh = logging.FileHandler("auto_complete.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)


logger.addHandler(fh)
logger.addHandler(ch)

logger.info("Starting")

driver = webdriver.Chrome("./chromedriver.exe")

crawled_dict = {}

with open("result-korean-character.json", "r", encoding="UTF-8") as f:
    charactors_json = json.loads(f.read())
    logger.info("Complete reading file")

try:
    for charactor_key in charactors_json.keys():
        logger.info("%s", charactor_key)
        driver.get(f"https://www.google.com/search?q={charactor_key}")
        logger.info("Get url: %s", f"https://www.google.com/search?q={charactor_key}")
        try:
            main_element: WebElement = driver.find_element_by_class_name("main")
            logger.info("found main element")
        except NoSuchElementException:
            logger.warning("Detect capcha sleep 60 sec")
            sleep(60)
            logger.info("retry")
            driver.get(f"https://www.google.com/search?q={charactor_key}")
            logger.info(
                "Get url: %s", f"https://www.google.com/search?q={charactor_key}"
            )
            main_element: WebElement = driver.find_element_by_class_name("main")
        else:
            try:
                charactor_element: WebElement = main_element.find_element_by_xpath(
                    '//*[@data-attrid="title"]'
                )
                logger.info("found charactor element")
            except NoSuchElementException:
                logger.info("Can't found korean_name: %s", charactor_key)
                continue
            else:
                regex_pattern = r"(.+)?(?(1) \(.+\)|.+)"

                parsed = re.match(regex_pattern, charactor_element.text)
                if regex_groups := parsed.groups()[0]:
                    korean_name = regex_groups
                    logger.info("found in group 1")
                else:
                    korean_name = parsed.group()
                    logger.info("found in match 1")
                logger.info("found korean_name: %s", korean_name)
                crawled_dict[charactor_key] = korean_name
except Exception:
    with open("crawled.json", "w") as f:
        f.write(json.dumps(crawled_dict))
