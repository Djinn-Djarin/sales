
from bs4 import BeautifulSoup

def parse_html(asin, soup):
    # soup = BeautifulSoup(response, "html.parser")
    # print(response.content)
    def suppressed():
        data_asin_div = soup.find(attrs={'data-asin': True})
        if data_asin_div and data_asin_div.get('data-asin') == asin:
            return 'Live'
        return 'Suppressed'
    x = suppressed()
    if x == 'Live':
        def get_title():
            title_element = soup.find("span", attrs={"id": "productTitle"})
            return title_element.get_text(strip=True) if title_element else None
        
        def browse_node():
            browse_node_element = soup.find("div", id="wayfinding-breadcrumbs_feature_div")
            if browse_node_element:
                ul_node = browse_node_element.find('ul', class_="a-unordered-list a-horizontal a-size-small")
                if ul_node:
                    li_nodes = ul_node.find_all('li')
                    breadcrumb = "".join([li.get_text(strip=True) for li in li_nodes])
                    return breadcrumb
            return None

        def images():
            try:
                # Try the first class configuration
                ul_element = soup.find("ul", class_="a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro gridAltImageViewLayoutIn1x7")
                if not ul_element:
                    # If the first class is not found, try the second configuration
                    ul_element = soup.find('ul', class_='a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-extra-large regularAltImageViewLayout')
                
                # If ul_element is found, proceed to find the images
                if ul_element:
                    images = ul_element.find_all('img')
                    jpg_images = [img['src'] for img in images if img['src'].endswith('.jpg')]
                    return len(jpg_images)
                else:
                    # Return 0 if no ul_element is found
                    return 0
            except Exception as e:
                # Print the exception for debugging purposes
                print(f"An error occurred: {e}")
                return 0


        def main_image():
                try:
                
                    ul_element = soup.find("ul", class_="a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro gridAltImageViewLayoutIn1x7")
                    if not ul_element:
                    
                        ul_element = soup.find('ul', class_='a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-extra-large regularAltImageViewLayout')
                    
            
                    if ul_element:
                        images = ul_element.find_all('img')
                        jpg_images = [img['src'] for img in images if img['src'].endswith('.jpg')]
                        if jpg_images:
                            main_image_url = jpg_images[0].replace("SS100", "SS1000")
                            return main_image_url
                    return None
                except Exception as e:
                    print(f"An error occurred")
                return None
    

        def videos():
            video_thumbnail_li = soup.find('li', class_='videoThumbnail')
            if video_thumbnail_li:
                img_tag = video_thumbnail_li.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    return 'Available'
                else:
                    return "Not Available"

        def bullet_points():
            element = soup.find("div", id="feature-bullets")
            if element:
                bullet = element.find('ul', class_="a-unordered-list a-vertical a-spacing-mini")
                if bullet:
                    bullet_li = bullet.find_all('li')
                    bps = [img for img in bullet_li]
                    return len(bps)

        def bsr():
            table = soup.find('table', {'id': 'productDetails_detailBullets_sections1'})
            if table:
                th_elements = table.find_all('th')

                best_sellers_td = None
                for th in th_elements:
                    if th.get_text(strip=True) == 'Best Sellers Rank':
                        best_sellers_td = th.find_next('td')
                        break

                if best_sellers_td:
                    spans = best_sellers_td.find_all('span')
                    best_sellers_ranks = [span.get_text(strip=True) for span in spans]
                    ranks_text = ' '.join(best_sellers_ranks)
                    split_ranks = ranks_text.split('#')

                    if len(split_ranks) > 3:
                        return split_ranks[1:4]
                    elif len(split_ranks) > 1:
                        return split_ranks[1:] + ["Not Available"] * (3 - len(split_ranks[1:]))
                else:
                    return ["Not Available", "Not Available", "Not Available"]
            else:
                return ["Not Available", "Not Available", "Not Available"]

        bsr1, bsr2, bsr3 = bsr()

        def get_price():
            price_element = soup.find("span", attrs={'class': 'a-price-whole'})
            return price_element.get_text(strip=True) if price_element else None

        def rating():
            rating_span = soup.find('span', id='acrCustomerReviewText')
            if rating_span:
                return rating_span.text
            return "Not Available"
        
        def reviews():
            rating_element = soup.find("span", id="acrPopover")
            if rating_element:
                rating = rating_element.get('title')
                if rating:
                    return rating.split()[0]
            return "Not Available"

        def get_availability():
            availability_element = soup.find("div", attrs={"id": "availability"})
            return availability_element.get_text(strip=True) if availability_element else None

        def description():
            A_plus_element = soup.find("div", id="productDescription")
            return "Available" if A_plus_element else "Not available"

        def A_plus():
            x = description()
            if x:
                return "Available"
            else:
                return 'Not Available'
        
        def deal():
            deal_badge = soup.find('span', class_='dealBadgeTextColor')
            if deal_badge and 'Limited time deal' in deal_badge.get_text():
                return 'Available'
            else:
                return 'NA'

        def storefront_link():
            store_link_tag = soup.find('a', id='bylineInfo')
            if store_link_tag:
                link = f"http://amazon.in{store_link_tag['href']}"
                return link
            else:
                return ''
        
        def mrp():
            mrp_tag = soup.find('span', class_='a-price a-text-price')
            if mrp_tag:
                mrp_value_tag = mrp_tag.find('span', class_='a-offscreen')
                if mrp_value_tag:
                    return mrp_value_tag.get_text()
            return ''
        
        def buybox():
            buybox = soup.find('div', id='desktop_qualifiedBuyBox')
            if buybox:
                return 'Available'
            else:
                return 'NA'
        
        def brand():
            brand_snapshot_div = soup.find('div', id='brandSnapshot_feature_div')
            if brand_snapshot_div:
                brand_span = brand_snapshot_div.find('span', class_='a-size-medium a-text-bold')
                if brand_span:
                    return brand_span.text.strip()
            return None

        def generic_name():
            table = soup.find('table', id='productDetails_detailBullets_sections1')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    header = row.find('th', class_='a-color-secondary a-size-base prodDetSectionEntry')
                    if header and header.text.strip() == 'Generic Name':
                        value = row.find('td', class_='a-size-base prodDetAttrValue')
                        if value:
                            return value.text.strip()
            return None

        def sold_by():
            outer_div = soup.find('div', class_='tabular-buybox-text', attrs={'tabular-attribute-name': 'Sold by'})
            if outer_div:
                span_element = outer_div.find('span', class_='a-size-small tabular-buybox-text-message')
                a_element = span_element.find('a')
                seller_name = a_element.text.strip()
                return seller_name

        def varations():
            color_element = soup.find(id="variation_color_name")            
            size_element = soup.find(id="variation_size_name")
            pattern_element = soup.find(id="variation_pattern_name")
            style_element = soup.find(id="variation_style_name")

            if color_element or size_element or pattern_element or style_element:
                return "Available"
            else:
                return 'NA'
    
        return {
            'ASIN': asin,
            'Status': suppressed(),
            'Browse Node': browse_node(),
            'title': get_title(),
            'All Images': images(),
            'Main Image': main_image(),
            'video': videos(),
            'Reviews': reviews(),
            'Rating': rating(),
            'Varations':varations(),
            'Deal': deal(),
            'Sold By': sold_by(),
            'Bullet Points': bullet_points(),
            'BSR-1': bsr1,
            'BSR-2': bsr2,
            'BSR-3': bsr3,
            'description': description(),
            'Price': get_price(),
            'MRP': mrp(),
            'Buybox': buybox(),
            'A+': A_plus(),
            'Storefront Link': storefront_link(),
            'Brand Name': brand(),
            'Generic Name': generic_name(),
            'availability': get_availability(),
        }

    else:
        x = suppressed_asin(asin)
        return x
    

def suppressed_asin(asin):
    
    return {
        'ASIN': asin,
        'Status': 'Suppressed',
        'Browse Node': None,
        'title': None,
        'All Images': None,
        'Main Image': None,
        'video': None,
        'Reviews': None,
        'Rating': None,
        'Varations':None,
        'Deal': None,
        'Sold By': None,
        'Bullet Points': None,
        'BSR-1': None,
        'BSR-2': None,
        'BSR-3': None,
        'description': None,
        'Price': None,
        'MRP': None,
        'Buybox': None,
        'A+': None,
        'Storefront Link': None,
        'Brand Name': None,
        'Generic Name': None,
        'availability': None,
    }

# ******************************************************************************************************************

def audit_main(file):
    import openpyxl
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import pandas as pd
    import csv
    import random
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from queue import Queue
    from bs4 import BeautifulSoup
    from amazoncaptcha import AmazonCaptcha
    import re
    import os

    if not os.path.isfile(file):
        raise FileNotFoundError(f"The file {file} does not exist.")

    if not file.endswith(('.xlsx', '.xlsm', '.xltx', '.xltm')):
        raise ValueError(f"Invalid file format: {file}. Please provide a valid Excel file with .xlsx, .xlsm, .xltx, or .xltm extension.")

    import openpyxl

    def get_user_agents():
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        ]
        return random.choice(user_agents)

    def setup_driver():
        chrome_driver_path = r'C:\Users\OMG\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe'
        chrome_binary_path = r'C:\Users\OMG\Downloads\chrome-win64\chrome-win64\chrome.exe'

        chrome_options = Options()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument(f'user-agent={get_user_agents()}')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def is_captcha_present(driver):
        try:
            driver.find_element(By.XPATH, "//h4[contains(text(), 'Enter the characters you see below')]")
            return True
        except:
            return False

    def solve_captcha(driver):
        try:
            captcha_image = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='a-row a-text-center']//img"))
            )
            captcha_src = captcha_image.get_attribute('src')
            print(f"Captcha source URL: {captcha_src}")
            captcha = AmazonCaptcha.fromlink(captcha_src)
            solution = captcha.solve()
            print(f"Captcha solution: {solution}")
            captcha_input = driver.find_element(By.ID, 'captchacharacters')
            captcha_input.send_keys(solution)
            submit_button = driver.find_element(By.CLASS_NAME, "a-button-text")
            submit_button.click()
            return True
        except Exception as e:
            print(f"Failed to solve captcha: {e}")
            return False

    def scrape_asin(asin, driver):
        try:
            url = f'https://www.amazon.in/dp/{asin}'
            
            driver.get(url)

            if is_captcha_present(driver):
                if not solve_captcha(driver):
                    print(f"Failed to solve captcha for ASIN {asin}")
                    return None

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'productTitle'))
            )

            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'lxml')
            product_data = parse_html(asin, soup)

            if product_data:
                return product_data

        except Exception as e:
            # print(f"Failed to retrieve data for ASIN {asin}")

            return suppressed_asin(asin)

    def process_asin(asin, driver):
        product_data = scrape_asin(asin, driver)
        if product_data:
            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow(product_data)
                print(product_data)

    def worker(browser_pool, asins_queue):
        while not asins_queue.empty():
            asin = asins_queue.get()
            driver = browser_pool.get()
            try:
                process_asin(asin, driver)
            finally:
                browser_pool.put(driver)
            asins_queue.task_done()

    

    wb = openpyxl.load_workbook(file)
    sheet = wb.active

    # Extract the ASINs from the first column, skipping the header row
    asins = []
    for row in sheet.iter_rows(min_row=2, max_col=1, values_only=True):
        if row[0]:  # Ensure the cell is not empty
            asins.append(row[0])

    filename = 'audit.csv'
    fieldnames = ['ASIN', 'Status', 'Browse Node', 'title', 'All Images', 'Main Image', 'video', 'Reviews', 'Rating', 'Varations','Deal', 'Sold By', 'Bullet Points', 'BSR-1', 'BSR-2', 'BSR-3', 'description', 'Price', 'MRP', 'Buybox', 'A+', 'Storefront Link', 'Brand Name', 'Generic Name', 'availability']

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()

    # Create a pool of browser instances
    browser_pool = Queue(maxsize=2)  # Adjust the pool size as needed
    for _ in range(browser_pool.maxsize):
        browser_pool.put(setup_driver())

    # Create a queue for ASINs
    asins_queue = Queue()
    for asin in asins:
        asins_queue.put(asin)

    # Use ThreadPoolExecutor to process ASINs with the browser pool
    max_workers = 2  # Adjust the number of workers as needed


    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, browser_pool, asins_queue) for _ in range(max_workers)]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f'Generated an exception')

    # Close all browser instances
    while not browser_pool.empty():
        driver = browser_pool.get()
        driver.quit()

    return future.result()

# import os

# # Assuming your .xlsx file is in the same directory as this script
# file_path = os.path.join(os.path.dirname(__file__), 'audit1.xlsx')
# audit_main(file_path)