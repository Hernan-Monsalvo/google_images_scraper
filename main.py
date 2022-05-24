import sys, os, io, time, base64, urllib3

from PIL import Image
from urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver

urllib3.disable_warnings(InsecureRequestWarning)

def download_google_staticimages(searchword):

    dirs = 'pictures'
    if not os.path.exists(dirs):
        os.mkdir(dirs)

    searchurl = 'https://www.google.com/search?q=' + searchword + '&source=lnms&tbm=isch'
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')

    chromedriver = '/usr/lib/chromium-browser/chromedriver'
    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(800, 600)
    browser.get(searchurl)
    time.sleep(2)

    result_img = browser.find_element_by_class_name("rg_i")

    print("result img: ",result_img.get_attribute("src"))

    url = result_img.get_attribute("src")

    try:
        imageStr = url.split(",")[1]

        image = base64.b64decode(str(imageStr))

        imagePath = (f"./pictures/{searchword}.jpeg")
        img = Image.open(io.BytesIO(image))
        img.save(imagePath, 'jpeg')

    except Exception as e:
        print('Failed to write rawdata.')
        print(e)
        return 0

    browser.close()
    return 1

# Main block
def main():
    t0 = time.time()
    search_words = ["batata", "remolacha", "zanahoria", "papa"]
    for word in search_words:
        download_google_staticimages(word)
        time.sleep(1)
    t1 = time.time()

    print(t1 - t0)

if __name__ == '__main__':
    main()