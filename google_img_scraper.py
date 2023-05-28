from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import urllib
from datetime import datetime
import main
import xlsxwriter

chrome_options = webdriver.ChromeOptions() # creates instance of ChromeOptions class
chrome_options.add_argument('--headless') # runs Chrome in headless mode
chrome_options.add_argument('--no-sandbox') # disable sandbox mode in Chrome
chrome_options.add_argument('--disable-dev-shm-usage') # disables '/dev/shm/ for shared resources
driver = webdriver.Chrome('chromedriver', options=chrome_options) # defines path to ChromeDriver executable

def google_image_scrape(name_item):
    workbook = xlsxwriter.Workbook("image_data_google.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write("A1", "Title")
    worksheet.write("B1", "URL")
    worksheet.write("C1", "Time")
    worksheet.write("D1", "Source")

    row = 1

    search_url = "https://www.google.com/search?q={topic}&tbm=isch&tbs=sur%3Afc&hl=en&ved=0CAIQpwVqFwoTCKCa1c6s4-oCFQAAAAAdAAAAABAC&biw=1251&bih=568"
    driver.get(search_url.format(topic=name_item)) # replaces topic in the search_url to the desired topic

    # Wait for images to load
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//img[contains(@class,'Q4LuWd')]")))
    except TimeoutException:
        print("Timed out waiting for images to load")

    img_results = driver.find_elements(By.XPATH, "//img[contains(@class,'Q4LuWd')]") # returns a list of image elements found on webpage

    src = []
    for img in img_results:
        img_src = img.get_attribute('src')
        img_name = img.get_attribute('alt')
        if img_src:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            image_data_elem = main.ImageData(img_name, img_src, formatted_time, "Google")
            worksheet.write(row, 0, image_data_elem.img_title)
            worksheet.write(row, 1, image_data_elem.source)
            worksheet.write(row, 2, image_data_elem.time_scraped)
            worksheet.write(row, 3, image_data_elem.source)
            row += 1

            src.append(img_src)

    for num in range(len(src)):
        img_filename = "./img/{topic}/image{i}_google.jpg"
        img_filename.format(topic=name_item, i=num)
        urllib.request.urlretrieve(str(src[num]), img_filename)

