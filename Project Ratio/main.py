"""
#
# A bot to download info product content behind a WordPress login page
# Every website is a little different so might need to be optimized for your specific use
#
# Created by David a.k.a. @Davincible_
# david.brouwer.99@gmail.com -- https://github.com/Davincible
#
"""

import requests
from requests.cookies import cookiejar_from_dict
from os.path import exists, join
import json
import pickle
import bs4 as bs
import logging
from datetime import datetime
import os
import re
import time

if not os.path.exists('logs'):
    os.mkdir('logs')

# configure the logger
Logger = logging.getLogger("RatioLogger")
Logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs/ratio-logger-{}.log'.format(datetime.now().isoformat('_')[:-7].replace(':', '.')).replace(' ', '_'))
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
Logger.addHandler(fh)
Logger.addHandler(ch)


class RatioBot:
    """ main class """
    def __init__(self, creds_file):
        self.creds_file = creds_file
        self.sesh = requests.session()
        self.login_url = None
        self.domain = None
        self.base_url = None
        self.credentials = None
        self.landing_page_url = None
        self.domain_data = {}
        self.domain_data_file = None
        self.cookie_storage = None
        self.landing_page = None

        self.setup()

    def __del__(self):
        if self.sesh:
            self.sesh.close()

    def setup(self):
        """ setup the browser session"""
        self.sesh.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"})
        self.load_credentials()
        self.load_domain_data()
        self.load_cookies()

    def extract_content(self):
        """ method to be called by user to extract the content links """
        try:
            self.extract_menu_items()
        except:
            self.load_cookies(force_login=True)
            self.extract_menu_items()
        self.extract_links()

    def download(self, BaseFolder="F:\\RatioBot\\TheSystem"):
        """ method to be called by user to download the collected content """
        time.sleep(.5)
        weird_chars = "â€¬¢ƒÂ¢"  # for some reason this shit appears in some files, these should be ignored
        if not exists(BaseFolder):
            choice = input("The specified folder ('{}') does not exist, attempt to create it? Y/N".format(BaseFolder))
            if choice.lower() in ["y", "yes"]:
                os.mkdir(BaseFolder)
            elif choice.lower() in ["n", "no"]:
                Logger.info("exiting")
            else:
                Logger.info("'{}' not known".format(choice))

        Logger.info("DOWNLOADING   : staring download process")
        # parent iterator used to iterate over the main menu items
        main_counter = 0
        for menu_item in self.domain_data['menu_items']:
            file_path = join(BaseFolder, "{0:0=2d} - {1}".format(main_counter, menu_item))
            if not exists(file_path):
                os.mkdir(file_path)
            referer = self.domain_data['menu_items'][menu_item]['item_url']

            # iterate over the collected content links
            mark_for_removal = []
            for article in self.domain_data['menu_items'][menu_item]['content']:
                # check for those weird-ass characters
                for ch in weird_chars:
                    if ch in article['video_title']:
                        mark_for_removal.append(article)
                        continue

                # download the content
                if not article.get('downloaded', None):
                    if article['video_url'] or article['content_url']:
                        url = self.download_data(article, file_path, referer)
                        if not url == "Not_A_Video" and not url == 1:
                            article["direct_url"] = url
                        if url != 1:
                            article['downloaded'] = True
                        else:
                            article['downloaded'] = False
                        self.save_domain_data(silent=True)
                    else:
                        Logger.info("SKIPPING DOWNLOAD   : no url found for item '{}'".format(article['video_title']))
                else:
                    Logger.info("SKIPPING DOWNLOAD   : item already downloaded: '{}'".format(article['video_title']))

            # remove the bugged files (with those strange chars in their title)
            for to_be_removed in mark_for_removal:
                try:
                    self.domain_data['menu_items'][menu_item]['content'].remove(to_be_removed)
                except ValueError:
                    pass

            # child iterator used to iterate over the sub-menu items
            sub_counter = 0
            for sub_menu_item in self.domain_data['menu_items'][menu_item]['sub_menu_items']:
                child_path = join(file_path, "{0:0=2d} - {1}".format(sub_counter, sub_menu_item))
                if not exists(child_path):
                    os.mkdir(child_path)
                referer = self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item]['item_url']

                # iterate over the collected content links
                mark_for_removal = []
                for article in self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item]['content']:
                    # check for those weird-ass characters
                    for ch in weird_chars:
                        if ch in article['video_title']:
                            mark_for_removal.append(article)
                            continue

                    # download the content
                    if not article.get('downloaded', None):
                        if article['video_url'] or article['content_url']:
                            url = self.download_data(article, child_path, referer)
                            if not url == "Not_A_Video" and not url == 1:
                                article["direct_url"] = url
                            if url != 1:
                                article['downloaded'] = True
                            else:
                                article['downloaded'] = False
                            self.save_domain_data(silent=True)
                        else:
                            Logger.info(
                                "SKIPPING DOWNLOAD   : no url found for item '{}'".format(article['video_title']))
                    else:
                        Logger.info("SKIPPING DOWNLOAD   : item already downloaded: '{}'".format(article['video_title']))

                # remove the bugged files (with those strange chars in their title)
                for to_be_removed in mark_for_removal:
                    try:
                        self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item]['content'].remove(to_be_removed)
                    except:
                        pass
                sub_counter += 1
            main_counter += 1

        self.save_domain_data()

    def download_data(self, article, file_path, referer):
        """ internal parent method which orchestrates the download process of a link """
        video_title = article['video_title']
        video_url = article['video_url']
        content_url = article['content_url']

        try:
            if video_url:
                real_url = self.get_real_video_url(video_url, referer)
                return_code = self.download_content(file_path, real_url, video_title, type_="video")
                if return_code == 0:
                    return real_url
                else:
                    return 1
            elif content_url:
                return_code = self.download_content(file_path, content_url, video_title, type_="other")
                if return_code == 0:
                    return "Not_A_Video"
                else:
                    print("retuning 1")
                    return 1
        except Exception as e:
            Logger.warning("ERROR   : downloading content: '{}' '{}'".format(article['video_title'], article['video_url']))
            raise e

    def get_real_video_url(self, url, referer):
        """ internal method used to extract token link for Vimeo videos """
        headers = self.sesh.headers.copy()
        headers['Referer'] = referer
        root_page = self.sesh.get(url, headers=headers)
        soup = bs.BeautifulSoup(root_page.text, 'lxml')

        # find json string in html page with video information
        regex = r'var r={[^;]*'
        compiled = re.compile(regex)
        for script in soup.findAll('script'):
            regex_results = compiled.findall(script.text)
            if regex_results:
                break

        # extract the video link from the json dict
        json_data = regex_results[0].strip('var r=').strip(';')
        video_data = json.loads(json_data)
        useful_data = video_data['request']['files']['progressive']
        video_sizes = [x['width'] for x in useful_data]
        video_sizes.sort()
        use_size = None
        index = len(video_sizes) - 1
        while not use_size:
            if video_sizes[index] <= 1920:
                use_size = video_sizes[index]
            index -= 1

        element = list(filter(lambda x: str(x['width']) == str(use_size), useful_data))[0]
        video_url = element['url']

        return video_url

    def download_content(self, filepath, url, video_tile, type_):
        """ internal method which actually downloads the content to disk"""
        # check if the provided url is actually a url
        if not ('http' in url or 'www' in url):
            Logger.warning("WARNING   : provided an invalid url, unable to download: '{}'".format(url))
            return 1
        elif 'mailto' in url:  # filter out mailing links and continue without error
            return 0
        elif "â€¬¢" in video_tile:  # filter out titles with weird characters and continue without error
            print("whathefuck is this even", video_tile)
            return 0

        # compose file name
        has_valid_file_name = False
        version_counter = 0
        for ch in '<>:"\|?*':  # remove illegal characters in the windows file namespace
            video_tile = video_tile.replace(ch, '')

        while not has_valid_file_name:
            if not version_counter:
                if type_ == "video":
                    f_name = "{}.mp4".format(video_tile)
                elif type_ == "other":
                    f_name = url.split('/')[-1]
                else:
                    Logger.error("ERROR   : invalid type: '{}' in method download_content".format(type_))
                    return 1
            else:
                if type_ == "video":
                    f_name = "{} - {}.mp4".format(video_tile, version_counter)
                elif type_ == "other":
                    file_ = url.split('/')[-1]
                    f_name = "{} - {}.{}".format(file_.split('.')[0], version_counter, file_.split('.')[1])
                else:
                    Logger.error("ERROR   : invalid type: '{}' in method download_content".format(type_))
                    return 1

            file_name = join(filepath, f_name)
            if not exists(file_name):
                has_valid_file_name = True
            else:
                version_counter += 1

        Logger.info("DOWNLOADING   : downloading file '{}'".format(f_name))
        buffer_size = 8096
        attempts = 0
        file_size = 0
        download = True

        # download the file to disk
        while download:
            try:
                content_requets = self.sesh.get(url, stream=True)

                with open(file_name, 'wb') as data_file:
                    data_file.truncate()
                    for chunk in content_requets.iter_content(buffer_size):
                        data_file.write(chunk)
                        file_size += len(chunk)
                        if int(file_size % 10000) == 0:
                            print("*", end='', flush=True)

                download = False
                print()
                time.sleep(.5)
                Logger.info("DOWNLOAD SUCCESSFUL   : successfully downloaded file '{}' size: {}MB".format(f_name,
                                                                                                          file_size / 1000000))
            except Exception as e:
                attempts += 1
                Logger.warning("WARNING   : error while trying to download url '{}'. Attempt failed with error '{}'".format(url, e))
                if attempts > 10:
                    Logger.info("STOPPING   :  stopping download, error was fatal")
                    download = False
                else:
                    Logger.info("RETRYING   : retrying download")
                    time.sleep(5)
        return 0

    def extract_menu_items(self):
        """ internal method to extract the links from menu items """
        if not self.domain_data.get('menu_items', None):
            self.domain_data['menu_items'] = {}
        if not self.landing_page:
            self.landing_page = self.sesh.get(self.landing_page_url)

        # iterate over menu items
        Logger.info("EXTRACTING   : extracting menu")

        soup = bs.BeautifulSoup(self.landing_page.text, 'lxml')
        nav_element = soup.find('nav', class_="desktop")
        menu_list = nav_element.find('ul', id='menu-top')
        for main_menu_item in menu_list.find_all('li'):
            if "sub-menu" not in main_menu_item.parent['class']:
                print("*", end='', flush=True)

                # extract menu item data
                item_title = main_menu_item.find('span').text
                item_url = main_menu_item.find('a')['href']
                if 'http' not in item_url:
                    item_url = self.base_url + item_url

                if not self.domain_data['menu_items'].get(item_title, None):
                    self.domain_data['menu_items'][item_title] = {}

                sub_menu_items = self.domain_data['menu_items'][item_title].get('sub_menu_items', {})
                for sub_menu_item in main_menu_item.find_all('li'):
                    print("*", end='', flush=True)
                    sub_menu_item_title = sub_menu_item.find('span').text
                    sub_menu_item_url = sub_menu_item.find('a')['href']

                    if not sub_menu_items.get(sub_menu_item_title, None):
                        sub_menu_items[sub_menu_item_title] = {}

                    sub_menu_items[sub_menu_item_title].update({'item_url': sub_menu_item_url})
                self.domain_data['menu_items'][item_title].update({'item_url': item_url, 'sub_menu_items': sub_menu_items})

        print()
        time.sleep(.5)  # sleep statement to let the logger properly print everything out before moving on
        self.save_domain_data()
        Logger.info("EXTRACTED   : extracted all menu items")

    def extract_links(self):
        """ internal method to extract links from content page """
        Logger.info("EXTRACTING   : extracting links")
        time.sleep(.5)
        self.domain_data['added_items'] = None
        self.domain_data['updated_items'] = None

        if not self.domain_data.get('updated_items', None):
            self.domain_data['updated_items'] = {}
        old_article_counter = 0

        # iterate over content pages (aka menu entries)
        for menu_item in self.domain_data['menu_items']:
            print("*", end='', flush=True)
            # get the main menu item pages and scan for content
            if not self.domain_data['menu_items'][menu_item].get('content', None):
                self.domain_data['menu_items'][menu_item]['content'] = []

            # iterate over content items
            page = self.sesh.get(self.domain_data['menu_items'][menu_item]['item_url'])
            soup = bs.BeautifulSoup(page.text, 'lxml')
            for article in soup.find_all('article'):
                # find all the content on the page
                article_data = self.get_article_data(article)

                # process the content if it is not already known
                if not list(filter(lambda x: x['video_title'] == article_data['video_title']
                                                and x['video_url'] == article_data['video_url']
                                                and x['content_url'] == article_data['content_url'], self.domain_data['menu_items'][menu_item]['content'])):
                    dubs = list(filter(lambda x: x['video_title'] == article_data['video_title'], self.domain_data['menu_items'][menu_item]['content']))

                    # if the title of the article is already known, the content changed
                    if dubs:
                        self.domain_data['menu_items'][menu_item]['content'].remove(dubs[0])

                        if not self.domain_data['updated_items'].get(menu_item, None):
                            self.domain_data['updated_items'][menu_item] = {'content': {}}
                        self.domain_data['updated_items'][menu_item]['content'].update({article_data['video_title']: {"old": dubs[0], "new": article_data}})
                    # else just add it
                    else:
                        print("added first")
                        if not self.domain_data.get('added_items', None):
                            self.domain_data['added_items'] = {}
                        if not self.domain_data['added_items'].get(menu_item, None):
                            self.domain_data['added_items'][menu_item] = {'content': {}}
                        self.domain_data['added_items'][menu_item]['content'].update({article_data['video_title']: article_data})

                    # add it to the list
                    self.domain_data['menu_items'][menu_item]['content'].append(article_data)
                else:
                    old_article_counter += 1

            # do the same thing for sub-menu entries
            for sub_menu_item in self.domain_data['menu_items'][menu_item]['sub_menu_items']:
                print("*", end='', flush=True)
                # get the sub menu item pages and scan for content
                if not self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item].get('content', None):
                    self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item]['content'] = []

                page = self.sesh.get(self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item]['item_url'])
                soup = bs.BeautifulSoup(page.text, 'lxml')
                for article in soup.find_all('article'):
                    article_data = self.get_article_data(article)

                    if not list(filter(lambda x: x['video_title'] == article_data['video_title']
                                                    and x['video_url'] == article_data['video_url']
                                                    and x['content_url'] == article_data['content_url'], self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item]['content'])):
                        dubs = list(filter(lambda x: x['video_title'] == article_data['video_title'], self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item]['content']))

                        # if the title of the article is already known, the content changed
                        if dubs:
                            self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item].remove(dubs[0])

                            if not self.domain_data['updated_items'].get(menu_item, None):
                                self.domain_data['updated_items'][menu_item] = {'content': {}}
                            if not self.domain_data['updated_items'][menu_item].get('sub_menu_items', None):
                                self.domain_data['updated_items'][menu_item]['sub_menu_items'] = {}
                            if not self.domain_data['updated_items'][menu_item]['sub_menu_items'].get(sub_menu_item, None):
                                self.domain_data['updated_items'][menu_item]['sub_menu_items'][sub_menu_item] = {}
                            self.domain_data['updated_items'][menu_item]['sub_menu_items'][sub_menu_item].update({article_data['video_title']: {"old": dubs[0], "new": article_data}})
                        # else just add it
                        else:
                            if not self.domain_data.get('added_items', None):
                                self.domain_data['added_items'] = {}
                            if not self.domain_data['added_items'].get(menu_item, None):
                                self.domain_data['added_items'][menu_item] = {'content': {}}
                            if not self.domain_data['added_items'][menu_item].get('sub_menu_items', None):
                                self.domain_data['added_items'][menu_item]['sub_menu_items'] = {}
                            if not self.domain_data['added_items'][menu_item]['sub_menu_items'].get(sub_menu_item, None):
                                self.domain_data['added_items'][menu_item]['sub_menu_items'][sub_menu_item] = {}
                            self.domain_data['added_items'][menu_item]['sub_menu_items'][sub_menu_item].update({article_data['video_title']: article_data})

                        # add it to the list
                        self.domain_data['menu_items'][menu_item]['sub_menu_items'][sub_menu_item]['content'].append(article_data)
                    else:
                        old_article_counter += 1

        print()
        time.sleep(.5)
        self.log_changes(old_article_counter)
        self.save_domain_data()

    def log_changes(self, old=None):
        """ give all the changes that have been made back to the user """
        additions = self.domain_data['added_items']
        changes = self.domain_data['updated_items']
        if additions:
            Logger.info("CHANGES   : the following additions have been made: {}".format(json.dumps(additions, indent=4)))
        else:
            Logger.info("CHANGES   : no additions have been made")
        if changes:
            Logger.info("CHANGES   : the following changes have been made: {}".format(json.dumps(changes, indent=4)))
        else:
            Logger.info("CHANGES   : no changes have been made")
        if old:
            Logger.info("CHANGES   : items left unchanged: {}".format(old))

        # save the changes that have been made in a history file
        # open history file
        history_file = "history_{}.json".format(self.domain.split('.')[0])
        if exists(history_file):
            with open(history_file, 'r') as file:
                history_data = json.load(file)
        else:
            history_data = {}

        # add current session to the history
        history_data[datetime.now().isoformat()[:-7]] = {'added_items': self.domain_data['added_items'], 'updated_items': self.domain_data['updated_items'], "unchanged_items": old}

        # save history data back to file
        with open(history_file, 'w') as file:
            file.truncate()
            json.dump(history_data, file)

    @staticmethod
    def get_article_data(article):
        """ method to extract the content data from an article item """
        # get the title
        video_title = article.find('header').get_text().strip()
        video_url, content_url = None, None

        # get the url if any
        content_element = article.find('div', class_="entry-content")
        if content_element.find('iframe'):
            video_url = content_element.find('iframe')['src']
        elif content_element.find('a'):
            content_url = content_element.find('a')['href']

        return {"video_url": video_url, "content_url": content_url, "video_title": video_title}

    def load_cookies(self, force_login=False):
        """ load the cookie """
        loaded_cookies = False

        # load cookie if cookie file exists
        if exists(self.cookie_storage):
            try:
                with open(self.cookie_storage, 'rb') as cookies_file:
                    # load cookies from file
                    try:
                        cookies = pickle.load(cookies_file)
                    except Exception as e:
                        cookies = None
                        Logger.warning("FAILED TO LOAD   : failed to load from cookie storage with error {}".format(e))
                    if cookies:
                        #  loading cookies into session
                        jar = requests.cookies.RequestsCookieJar()
                        jar._cookies = cookies
                        self.sesh.cookies = jar
                        Logger.info("LOADED   : Re-using old cookies")
                        loaded_cookies = True

            except Exception as e:
                Logger.error("ERROR   : failed to load cookies from storage file '{}' with error '{}'".format(self.cookie_storage, e))

        # perform a login if no cookie was found or re-login forced (due to an expired cookie)
        if not loaded_cookies or not self.landing_page_url or force_login:
            if not self.landing_page_url:
                Logger.info("Landing page url not found, doing a re-login")
            elif not loaded_cookies:
                Logger.info("Failed to find or use old cookies")
            elif force_login:
                Logger.info("Forice re-login, cookies probably expired")
            self.sesh.cookies = requests.cookies.RequestsCookieJar()
            self.login()

        #  put cookies in the header
        cookies_ = ''
        cookie_list = self.sesh.cookies.get_dict()
        for cookie in cookie_list.keys():
            cookies_ += " {}={};".format(cookie, cookie_list[cookie])
        self.sesh.headers['Cookie'] = cookies_.strip()

    def save_cookies(self):
        """ save cookie back to disk """
        with open(self.cookie_storage, 'wb') as cookies_file:
            cookies_file.truncate()
            pickle.dump(self.sesh.cookies._cookies, cookies_file)
            Logger.info("SAVED   : saved cookies to file {}".format(self.cookie_storage))

    def save_domain_data(self, silent=False):
        """ save domain data back to disk """
        with open(self.domain_data_file, 'w') as file:
            file.truncate()
            json.dump(self.domain_data, file, indent=4)
            if not silent:
                Logger.info("SAVED   : saved domain data to '{}'".format(self.domain_data_file))
            time.sleep(.5)

    def load_domain_data(self):
        """ load domain data from disk """
        if exists(self.domain_data_file):
            with open(self.domain_data_file, 'r') as file:
                self.domain_data = json.load(file, encoding='utf-8')
                self.landing_page_url = self.domain_data.get('landing_page_url', None)
                Logger.info("LOADED   : loaded domain data from file '{}'".format(self.domain_data_file))
                time.sleep(.5)

    def login(self):
        """ perform a login """
        Logger.info("Logging in again on url: '{}'".format(self.login_url))
        self.landing_page = self.sesh.post(self.login_url, data=self.credentials)
        self.landing_page_url = self.landing_page.url
        self.domain_data['landing_page_url'] = self.landing_page_url
        self.save_cookies()
        self.save_domain_data()

    def load_credentials(self):
        """ load login credentials from disk """
        with open(self.creds_file, 'r') as file:
            self.login_url = file.readline().strip()
            parser = requests.utils.urlparse(self.login_url)
            self.domain = parser.hostname
            self.base_url = "{}://{}".format(parser.scheme, parser.hostname)
            self.domain_data_file = "data_{}.json".format(self.domain.split('.')[0])
            self.credentials = {"log": file.readline().strip(), "pwd": file.readline().strip()}
            self.cookie_storage = "CookieStorage-{}".format(self.domain.split('.')[0])
        Logger.info("LOADED   : loaded credentials from {}".format(self.creds_file))


if __name__ == '__main__':
    bot = RatioBot('1XD.txt')
    bot.extract_content()
    bot.download()
