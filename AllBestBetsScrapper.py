from selenium import webdriver
import zipfile
import os
from SecretWinsWebsite.ArbsReader import arbs


PROXY_HOST = '91.149.167.93'  # rotating proxy or host
PROXY_PORT = 45785  # port
PROXY_USER = 'Selminerone8'  # username
PROXY_PASS = 'O9h3BkX'  # password

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = r'C:\Windows'
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => false
               })
             """
    })
    return driver


search_filter = {"0": "433829", "1": "433919", "2": "433922", "3": "433924",
                 "4": "433927",
                 "5": "433929",
                 "6": "433930",
                 "7": "433931"}


def scope():
    all_best_bets = get_chromedriver()
    all_best_bets.get("https://www.allbestbets.com/")
    return all_best_bets


def ABBAPI(all_best_bets, filter):
    t = str(all_best_bets.find_element_by_class_name('standalone-calculator').get_attribute('href'))
    token = t.split("access_token=")[1].split("&is_live")[0]
    while token == "":
        t = str(all_best_bets.find_element_by_class_name('standalone-calculator').get_attribute('href'))
        token = t.split("access_token=")[1].split("&is_live")[0]
    print(token)
    local_response = all_best_bets.execute_script("""
        var a = fetch("https://rest-api-pr.allbestbets.com/api/v1/arbs/pro_search?access_token=""" + token + """&locale=en", {
      "headers": {
        "accept": "*/*",
        "accept-language": "ru,en;q=0.9,az;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
      },
      "referrer": "https://www.allbestbets.com/",
      "referrerPolicy": "strict-origin-when-cross-origin",
      "body": "auto_update=true&notification_sound=false&notification_popup=false&show_event_arbs=true&grouped=true&per_page=20&sort_by=percent&event_id=&koef_format=decimal&q=&event_arb_types%5B%5D=1&event_arb_types%5B%5D=2&event_arb_types%5B%5D=3&event_arb_types%5B%5D=4&event_arb_types%5B%5D=5&event_arb_types%5B%5D=6&event_arb_types%5B%5D=7&event_arb_types%5B%5D=8&event_arb_types%5B%5D=9&bk_ids%5B%5D=1&bk_ids%5B%5D=2&bk_ids%5B%5D=3&bk_ids%5B%5D=4&bk_ids%5B%5D=5&bk_ids%5B%5D=6&bk_ids%5B%5D=7&bk_ids%5B%5D=8&bk_ids%5B%5D=9&bk_ids%5B%5D=10&bk_ids%5B%5D=11&bk_ids%5B%5D=12&bk_ids%5B%5D=13&bk_ids%5B%5D=14&bk_ids%5B%5D=15&bk_ids%5B%5D=16&bk_ids%5B%5D=17&bk_ids%5B%5D=18&bk_ids%5B%5D=19&bk_ids%5B%5D=20&bk_ids%5B%5D=21&bk_ids%5B%5D=22&bk_ids%5B%5D=23&bk_ids%5B%5D=24&bk_ids%5B%5D=25&bk_ids%5B%5D=26&bk_ids%5B%5D=27&bk_ids%5B%5D=28&bk_ids%5B%5D=29&bk_ids%5B%5D=30&bk_ids%5B%5D=31&bk_ids%5B%5D=32&bk_ids%5B%5D=33&bk_ids%5B%5D=34&bk_ids%5B%5D=35&bk_ids%5B%5D=36&bk_ids%5B%5D=37&bk_ids%5B%5D=38&bk_ids%5B%5D=39&bk_ids%5B%5D=40&bk_ids%5B%5D=41&bk_ids%5B%5D=42&bk_ids%5B%5D=43&bk_ids%5B%5D=44&bk_ids%5B%5D=45&bk_ids%5B%5D=46&bk_ids%5B%5D=47&bk_ids%5B%5D=48&bk_ids%5B%5D=49&bk_ids%5B%5D=50&bk_ids%5B%5D=51&bk_ids%5B%5D=52&bk_ids%5B%5D=53&bk_ids%5B%5D=54&bk_ids%5B%5D=55&bk_ids%5B%5D=56&bk_ids%5B%5D=57&bk_ids%5B%5D=58&bk_ids%5B%5D=59&bk_ids%5B%5D=60&bk_ids%5B%5D=61&bk_ids%5B%5D=62&bk_ids%5B%5D=63&bk_ids%5B%5D=64&bk_ids%5B%5D=65&bk_ids%5B%5D=66&bk_ids%5B%5D=67&bk_ids%5B%5D=68&bk_ids%5B%5D=69&bk_ids%5B%5D=70&bk_ids%5B%5D=71&bk_ids%5B%5D=72&bk_ids%5B%5D=73&bk_ids%5B%5D=74&bk_ids%5B%5D=75&bk_ids%5B%5D=76&bk_ids%5B%5D=77&bk_ids%5B%5D=78&bk_ids%5B%5D=79&bk_ids%5B%5D=80&bk_ids%5B%5D=81&bk_ids%5B%5D=82&bk_ids%5B%5D=83&bk_ids%5B%5D=84&bk_ids%5B%5D=85&bk_ids%5B%5D=86&bk_ids%5B%5D=87&bk_ids%5B%5D=88&bk_ids%5B%5D=89&bk_ids%5B%5D=90&bk_ids%5B%5D=91&bk_ids%5B%5D=92&bk_ids%5B%5D=93&bk_ids%5B%5D=94&bk_ids%5B%5D=95&bk_ids%5B%5D=96&bk_ids%5B%5D=97&bk_ids%5B%5D=98&bk_ids%5B%5D=99&bk_ids%5B%5D=100&bk_ids%5B%5D=101&bk_ids%5B%5D=102&bk_ids%5B%5D=103&bk_ids%5B%5D=104&bk_ids%5B%5D=105&bk_ids%5B%5D=106&bk_ids%5B%5D=107&bk_ids%5B%5D=108&bk_ids%5B%5D=109&bk_ids%5B%5D=110&bk_ids%5B%5D=111&bk_ids%5B%5D=112&bk_ids%5B%5D=113&bk_ids%5B%5D=114&bk_ids%5B%5D=115&bk_ids%5B%5D=116&bk_ids%5B%5D=117&bk_ids%5B%5D=118&bk_ids%5B%5D=119&bk_ids%5B%5D=120&bk_ids%5B%5D=121&bk_ids%5B%5D=122&bk_ids%5B%5D=123&bk_ids%5B%5D=124&bk_ids%5B%5D=125&bk_ids%5B%5D=126&bk_ids%5B%5D=127&bk_ids%5B%5D=128&bk_ids%5B%5D=129&bk_ids%5B%5D=130&bk_ids%5B%5D=131&bk_ids%5B%5D=132&bk_ids%5B%5D=133&bk_ids%5B%5D=134&bk_ids%5B%5D=200&bk_ids%5B%5D=201&bk_ids%5B%5D=202&bk_ids%5B%5D=203&is_live=false&search_filter%5B%5D="""+ search_filter[filter]+"""",
      "method": "POST",
      "mode": "cors",
      "credentials": "omit"
    })
            .then(response => response.json())
            return a;
            """)

    a = arbs(local_response, token)
    return a


if __name__ == "__main__":
    a = scope()
    ABBAPI(a)
