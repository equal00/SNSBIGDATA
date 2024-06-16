import os
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


keyword = input('검색할 키워드를 입력하세요: ')
count = int(input('다운로드할 PDF 파일 수를 입력하세요: '))
save_folder = input('파일이 저장될 경로를 입력하세요: ')

try:
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/')
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea'))
    )
    search_box.send_keys(f'{keyword} filetype:pdf')
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)


    next_btn = driver.find_element(By.CSS_SELECTOR, 'span.RVQdVd')

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    last_scroll_position = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
    pdf_links = set()

    while len(pdf_links) < count:

        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if(href not in pdf_links):
                if href and href.endswith('.pdf'):
                    pdf_links.add(href)
                    if len(pdf_links) == count:
                        break
        
    
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)  
        current = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
        if(current == last_scroll_position):
            next_btn.click()
        last_scroll_position = current

    for i, link in enumerate(list(pdf_links)[:count]):
        try:
            response = requests.get(link)
            file_name = os.path.join(save_folder, f'pdf_{i + 1}.pdf')
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f'{i + 1}/{count} PDF 다운로드 완료: {file_name}')
        except Exception as e:
            print(f'pdf_{i + 1}파일을 받아올 수 없습니다.')

except Exception as e:
    print(f'오류 발생: {e}')

finally:
    driver.quit()
    print('크롤링 완료')
