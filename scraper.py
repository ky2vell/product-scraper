import requests
import shutil
from bs4 import BeautifulSoup
import csv
import time

# Array of SKU's
SKUS = ["000300", "000301", "000303"]

# Base url with request headers
BASE_URL = '[url]'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

# Create CSV
csv_file = open('csv_name.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['sku', 'description', 'type'])

for SKU in SKUS:
    try:
        r = requests.get(BASE_URL + SKU, headers=headers)
        src = r.content
        soup = BeautifulSoup(src, 'lxml')

        desc = soup.find('h1', class_='product_name').text
        ins_type = soup.find(text="Type:").findNext('span').text

        print(f'{desc} STATUS: {r.status_code}')

        csv_writer.writerow([SKU, desc, ins_type])

        # Image download
        img_url = soup.find('a', class_='fancybox').attrs['href']
        r = requests.get(f'https:{img_url}', stream=True)
        if r.status_code == 200:
            with open(f'prod_images/{SKU}.jpg', 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        # Just list SKU in CSV if 404
        csv_writer.writerow([SKU])

    # wait 5 seconds
    time.sleep(5)

csv_file.close()
