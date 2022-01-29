from re import I
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
from itertools import zip_longest
import gspread
from oauth2client.service_account import ServiceAccountCredentials


labels = ["التسلسل", "عنوان الرواية", "رابط مقال الرواية", "المؤلف", "رابط مقال المؤلف", "البلد", "رابط مقال البلد"]
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("workenv/webscrap_task/myCreds.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("novelsSheet").sheet1

def scrap():
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9")
        
        myTable = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div[5]/div[1]/table"))
        )
        
        titles = myTable.find_elements_by_xpath("/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr/td[2]/a")
        titlesText = [title.text for title in titles]
        titlesLinks = [title.get_attribute("href") for title in titles]
        authers = myTable.find_elements_by_xpath("/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr/td[3]/a")
        authersText = [auther.text for auther in authers]
        authersLinks = [auther.get_attribute("href") for auther in authers]
        countries = myTable.find_elements_by_xpath("/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr/td[4]/a")
        countriesText = [country.text for country in countries]
        countriesLinks = [country.get_attribute("href") for country in countries]
            
    except Exception as e:
        print(str(e))
        driver.quit()
        
    finally:
        driver.quit()
        return [titlesText, titlesLinks, authersText, authersLinks, countriesText, countriesLinks]
  
def save_to_csv(file_name, file_list):
    exported = zip_longest(*file_list)
    with open("workenv/webscrap_task/" + file_name + ".csv", "w") as myFile:
        wr = csv.writer(myFile)
        wr.writerow(labels)
        wr.writerows(exported)
        
def gSheetDataInsertion(labels, data):
    for i in range(len(data)):
        data[i].insert(0, labels[i])
    sheet.insert_cols([*data])




# ******* run *******
[titlesText, titlesLinks, authersText, authersLinks, countriesText, countriesLinks] = [*scrap()]
ordersText = [i for i in range(1, len(titlesText)+1)]
scrap_result = [ordersText, titlesText, titlesLinks, authersText, authersLinks, countriesText, countriesLinks]
save_to_csv("novels", scrap_result)
gSheetDataInsertion(labels, scrap_result)
