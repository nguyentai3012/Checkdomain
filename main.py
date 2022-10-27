import csv
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def write_to_csv(filename='data.csv', data=None):
    # data rows of csv file
    if data is None:
        data = ()
    rows = data
    # writing to csv file
    with open(filename, 'a', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the data rows
        csvwriter.writerows(rows)


# def send_request():
#     df = pd.read_csv('data.csv')
#     url = "https://api.godaddy.com/v2/domains/available?checkType=FAST"
#
#     proxies = {
#         "url_http": "http://R0R4W10YG52UESOHZ68GZF20VLQ9VD62Y03KZTKCWQGIM35C7GE0QA86QCG76CX7UBQEFHWZRZ7F171M"
#                     ":render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
#         "url_https": "https://R0R4W10YG52UESOHZ68GZF20VLQ9VD62Y03KZTKCWQGIM35C7GE0QA86QCG76CX7UBQEFHWZRZ7F171M"
#                      ":render_js=False&premium_proxy=True@proxy.scrapingbee.com:8887",
#         "url_socks5": "socks5://R0R4W10YG52UESOHZ68GZF20VLQ9VD62Y03KZTKCWQGIM35C7GE0QA86QCG76CX7UBQEFHWZRZ7F171M"
#                       ":render_js=False&premium_proxy=True@socks.scrapingbee.com:8888",
#     }
#
#     datas = df['Domain'].tolist()
#
#     try:
#         for i in range(0, len(datas), 500):
#             payload = json.dumps(datas[i:i + 500])
#             headers = {
#                 'accept': 'application/json',
#                 'Content-Type': 'application/json',
#                 'Authorization': 'sso-key gHA5VXUX3gvc_yZZTkr3iFCmpChKwdNJcT:UMoJXE8CJoQj98BjQmF72F'
#             }
#             response = requests.request("POST", url, headers=headers, proxies=proxies , data=payload, verify=False)
#             # time.sleep(0.1)
#             json_object = json.loads(response.text)
#             if 'domains' in json_object:
#                 if json_object['domains'] is not None:
#                     for j in json_object['domains']:
#                         if j['available'] is True:
#                             write_to_csv(filename='available_domain.csv', data=[j['domain'], 'Available'])
#                         else:
#                             write_to_csv(filename='unavailable_domain.csv', data=[j['domain'], 'Unavailable'])
#
#             if 'errors' in json_object:
#                 if json_object['errors'] is not None:
#                     for j in json_object['errors']:
#                         if j['code'] == "UNSUPPORTED_TLD":
#                             write_to_csv(filename='UNSUPPORTED_TLD.csv', data=[j['domain'], 'UNSUPPORTED_TLD'])
#
#             if 'code' in json_object:
#                 if json_object['code'] == 'TOO_MANY_REQUESTS':
#                     i = i - 500
#                     time.sleep(30)
#     except Exception as e:
#         print("Loi " + str(e))
# # Configure Proxy Option
# prox = Proxy()
# prox.proxy_type = ProxyType.MANUAL
#
# # Proxy IP & Port
# prox.http_proxy = "23.94.230.25:3128"
# # prox.socks_proxy = "23.94.230.25:3128"
# prox.ssl_proxy = "23.94.230.25:3128"
# # Configure capabilities
# capabilities = webdriver.DesiredCapabilities.CHROME
# prox.add_to_capabilities(capabilities)

option = Options()
option.add_argument('--window-size=1920,1280')
option.add_argument('--start-maximized')
option.add_argument('--headless')
option.add_argument('--ignore-certificate-errors')
option.add_argument('--allow-running-insecure-content')
option.add_argument("--no-sandbox")
option.add_argument('--disable-gpu')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('--ignore-certificate-errors')
# option.add_argument('--proxy-server=%s' % "https"
#                                           "://R0R4W10YG52UESOHZ68GZF20VLQ9VD62Y03KZTKCWQGIM35C7GE0QA86QCG76CX7UBQEFHWZRZ7F171M"
#                                           ":render_js=False&premium_proxy=True@proxy.scrapingbee.com:8887")

# option.add_argument('--proxy-server=%s' % "23.94.230.25:3128")

file_input = input("File directory(Only csv supported): ")
df = pd.read_csv(file_input)
datas = df['Domain'].tolist()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get("https://www.netim.com/en/domain-name/search")
# driver.maximize_window()
wait = WebDriverWait(driver, timeout=20)
driver.implicitly_wait(10)
# Close accept cookies pop up
accept_cookies = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ACM-button-accept"]')))
if accept_cookies is not None:
    accept_cookies.click()
bulk_search = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@id='recherche-multiple-trigger']")))
bulk_search.click()


def check_exists_by_xpath(xpath):
    try:
        e = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False, None
    return True, e


def check_exists_by_xpath_with_explicit_wait(xpath):
    try:
        e = wait_in_element.until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath)))
    except NoSuchElementException:
        return False, None
    return True, e


current_index = 0
for i in range(current_index, len(datas), 40):
    if (i + 40) <= len(datas):
        try:
            # Send keys to search text box
            search_box = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//textarea[@id='recherche-domaine-input_multiple']")))
            print("Send keys to search box")
            payload = datas[i:i + 40]
            for p in payload:
                search_box.send_keys(p + '\n')
            # Click btn search
            search_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="trigger-search-multiple"]')))
            search_btn.click()
            print("Clicked btn search")

            contain_result = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="resultats"]')))
            wait_in_element = WebDriverWait(contain_result, timeout=60)
            if check_exists_by_xpath(xpath='//*[@id="resultats"]//div[@class="message"]') \
                    or check_exists_by_xpath(xpath='//*[@id="resultats"]//button'):
                print('Located the result.')
                # Check if domain cannot register.
                if check_exists_by_xpath(xpath='//*[@id="resultats"]//div[@class="message"]'):
                    print("Domain can not register")
                    domain = [d.text for d in driver.find_elements(By.XPATH, '//*[@id="resultats"]/div//a')]
                    text_result = [t.text for t in
                                   driver.find_elements(By.XPATH, '//*[@id="resultats"]/div//div['
                                                                  '@class="message"]')]
                    res = zip(domain, text_result)
                    write_to_csv(filename="domain.csv", data=res)
                # Check if domain can register.
                if check_exists_by_xpath(xpath='//*[@id="resultats"]//button'):
                    print("Domain can register")
                    domain = [d.text for d in driver.find_elements(By.XPATH, '//*[@id="resultats"]//div['
                                                                             '@class="label"]')]
                    text_result = [t.text for t in
                                   driver.find_elements(By.XPATH, "//*[@id='resultats']//button[contains("
                                                                  "text(), "
                                                                  "'Register')]")]
                    res = zip(domain, text_result)
                    write_to_csv(filename="domain.csv", data=res)
                html_element = driver.find_element(By.TAG_NAME, 'html')
                for j in range(6):
                    html_element.send_keys(Keys.PAGE_UP)
                search_box = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="recherche-domaine'
                                                                                    '-input_multiple"]')))
                search_box.clear()
                print("Clear search box and scroll up.")
                print("--------------------------------")
        except Exception as e:
            print(e)
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            driver.get_screenshot_as_file('screenshot/screenshot-%s.png' % now)
            continue
        finally:
            current_index = i + 40
            with open("current_index.txt", 'a', newline='') as file:
                file.write(str(current_index))
    else:
        print("Done.")
        break
# Terminate session
driver.quit()

# if __name__ == '__main__':
# send_request()
