from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv


movies_page = 'https://www.kinopoisk.ru/mykp/movies/'
movies_watched_page = 'https://www.kinopoisk.ru/mykp/movies/list/type'
sorted_page = 'perpage'

# ==== XPATHS
login_buton_path = '//*[@type="button" and contains(@class, "loginButton")]'
login_input_field_path = '//input[@name="login"]'
submit_button_path = '//button[@type="submit"]'
password_input_field_path = '//input[@name="passwd"]'
skip_phone_path = '//*[@data-t="phone_actual_skip"]'
account_button_path = '//*[@href="/mykp/movies/" and @aria-label="presentation"]'

sort_button_path = '(//select[@class="navigator_per_page"])[1]'
sort_200_path = '(//option[@value="200"])[1]'
movie_name_path = './/*[@class="info"]/span[1]'
my_rate_path = './/div[@title and contains(@class, "show_vote")]'
movies_path = './/*[@id="itemList"]/li'
next_page_button_path = '(//div[contains(@class, "navigator")]/ul[@class="list"])[1]/li[@class="arr"]/a[text()="»"]'

browser = webdriver.Chrome()
browser.get(movies_page)


def main():
    browser.get(movies_page)
    current_url = browser.current_url
    try:
        print(browser.find_element(
            By.XPATH, movies_path).size() != 0)
    except:
        print('okay')
    while (movies_watched_page and sorted_page) not in current_url:
        current_url = browser.current_url
        time.sleep(3)

    with open('movies_list.csv', 'w', encoding="utf-8", newline='') as file:
        next_page = 1
        writer = csv.writer(file)
        try:
            next_page_button_element = browser.find_element(
                By.XPATH, next_page_button_path)
        except:
            next_page = 1
        while next_page == 1:
            movies_list_element = browser.find_elements(By.XPATH, movies_path)
            for movie_element in movies_list_element:
                my_rate = movie_element.find_element(
                    By.XPATH, my_rate_path).text
                info_str = movie_element.find_element(
                    By.XPATH, movie_name_path).text.rsplit(" (", 1)
                name = info_str[0].encode("utf-8")
                if len(info_str) > 1:
                    year = info_str[1].rsplit(')')[0]
                else:
                    continue
                writer.writerow([name.decode(), year, my_rate])
            try:
                next_page_button_element = browser.find_element(
                    By.XPATH, next_page_button_path)
                next_page_button_element.click()
                time.sleep(8)
            except:
                next_page = 0


main()
