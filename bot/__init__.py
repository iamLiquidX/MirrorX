import logging
import os
import threading
import time
import random
import string
import subprocess
import pkgutil
import pathlib
import sys

import aria2p
import requests
import telegram.ext as tg
from dotenv import load_dotenv
from pyrogram import Client
from telegraph import Telegraph
from megasdkrestclient import MegaSdkRestClient, errors as mega_err

import socket
import faulthandler
faulthandler.enable()

socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

load_dotenv('config.env')

Interval = []


def getConfig(name: str):
    return os.environ[name]


LOGGER = logging.getLogger(__name__)

try:
    if bool(getConfig('_____REMOVE_THIS_LINE_____')):
        logging.error('The README.md file there to be read! Exiting now!')
        exit()
except KeyError:
    pass
CWD = os.getcwd()
ariaconfig = pkgutil.get_data("bot", "data/aria.conf").decode()
dhtfile = pkgutil.get_data("bot", "data/dht.dat")
dht6file = pkgutil.get_data("bot", "data/dht6.dat")
with open("dht.dat", "wb+") as dht:
    dht.write(dhtfile)
with open("dht6.dat", "wb+") as dht6:
    dht6.write(dhtfile)
ariaconfig = ariaconfig.replace("/currentwd", str(CWD))
try:
    max_dl = getConfig("MAX_CONCURRENT_DOWNLOADS")
except KeyError:
    max_dl = "4"
tracker_list = requests.get("https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all_aria2.txt").text
ariaconfig += f"\nmax-concurrent-downloads={max_dl}\nbt-tracker={tracker_list}"

with open("aria.conf", "w+") as ariaconf:
    ariaconf.write(ariaconfig)

ARIA_CHILD_PROC = None
try:
    ARIA_CHILD_PROC = subprocess.Popen(["aria2c", f"--conf-path={CWD}/aria.conf"])
except FileNotFoundError:
    LOGGER.error("Please install Aria2c, Exiting..")
    sys.exit(0)
except OSError:
    LOGGER.error("Aria2c Binary might have got damaged, Please Check and reinstall..")
    sys.exit(0)
time.sleep(1)

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="",
    )
)

DOWNLOAD_DIR = None
BOT_TOKEN = None

download_dict_lock = threading.Lock()
status_reply_dict_lock = threading.Lock()
# Key: update.effective_chat.id
# Value: telegram.Message
status_reply_dict = {}
# Key: update.message.message_id
# Value: An object of Status
download_dict = {}
# Stores list of users and chats the bot is authorized to use in
AUTHORIZED_CHATS = set()
if os.path.exists('authorized_chats.txt'):
    with open('authorized_chats.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            #    LOGGER.info(line.split())
            AUTHORIZED_CHATS.add(int(line.split()[0]))
try:
    achats = getConfig('AUTHORIZED_CHATS')
    achats = achats.split(" ")
    for chats in achats:
        AUTHORIZED_CHATS.add(int(chats))
except:
    pass

try:
    BOT_TOKEN = getConfig('BOT_TOKEN')
    parent_id = getConfig('GDRIVE_FOLDER_ID')
    DOWNLOAD_DIR = getConfig('DOWNLOAD_DIR')
    if not DOWNLOAD_DIR.endswith("/"):
        DOWNLOAD_DIR = DOWNLOAD_DIR + '/'
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR, 0o777)
    DOWNLOAD_STATUS_UPDATE_INTERVAL = int(getConfig('DOWNLOAD_STATUS_UPDATE_INTERVAL'))
    OWNER_ID = int(getConfig('OWNER_ID'))
    AUTO_DELETE_MESSAGE_DURATION = int(getConfig('AUTO_DELETE_MESSAGE_DURATION'))
    TELEGRAM_API = getConfig('TELEGRAM_API')
    TELEGRAM_HASH = getConfig('TELEGRAM_HASH')
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    sys.exit()
    # exit()

LOGGER.info("Generating USER_SESSION_STRING")
app = Client(':memory:', api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN)

#Generate Telegraph Token
sname = ''.join(random.SystemRandom().choices(string.ascii_letters, k=8))
LOGGER.info("Generating Telegraph Token using '" + sname + "' name")
telegraph = Telegraph()
telegraph.create_account(short_name=sname)
telegraph_token = telegraph.get_access_token()
LOGGER.info("Telegraph Token Generated: '" + telegraph_token + "'")

try:
    UPTOBOX_TOKEN = getConfig('UPTOBOX_TOKEN')
except KeyError:
    logging.warning('UPTOBOX_TOKEN not provided!')
    UPTOBOX_TOKEN = None

try:
    MEGA_KEY = getConfig('MEGA_KEY')
except KeyError:
    MEGA_KEY = None
    LOGGER.info('MEGA API KEY NOT AVAILABLE')
MEGA_CHILD_PROC = None
if MEGA_KEY is not None:
    try:
        MEGA_CHILD_PROC = subprocess.Popen(["megasdkrest", "--apikey", MEGA_KEY])
    except FileNotFoundError:
        LOGGER.error("Please install Megasdkrest Binary, Exiting..")
        sys.exit(0)
    except OSError:
        LOGGER.error("Megasdkrest Binary might have got damaged, Please Check ..")
        sys.exit(0)
    time.sleep(3)
    mega_client = MegaSdkRestClient('http://localhost:6090')
    try:
        MEGA_USERNAME = getConfig('MEGA_USERNAME')
        MEGA_PASSWORD = getConfig('MEGA_PASSWORD')
        if len(MEGA_USERNAME) > 0 and len(MEGA_PASSWORD) > 0:
            try:
                mega_client.login(MEGA_USERNAME, MEGA_PASSWORD)
            except mega_err.MegaSdkRestClientException as e:
                logging.error(e.message['message'])
                exit(0)
        else:
            LOGGER.info("Mega API KEY provided but credentials not provided. Starting mega in anonymous mode!")
            MEGA_USERNAME = None
            MEGA_PASSWORD = None
    except KeyError:
        LOGGER.info("Mega API KEY provided but credentials not provided. Starting mega in anonymous mode!")
        MEGA_USERNAME = None
        MEGA_PASSWORD = None
else:
    MEGA_USERNAME = None
    MEGA_PASSWORD = None
try:
    INDEX_URL = getConfig('INDEX_URL')
    if len(INDEX_URL) == 0:
        INDEX_URL = None
except KeyError:
    INDEX_URL = None
try:
    BUTTON_THREE_NAME = getConfig('BUTTON_THREE_NAME')
    BUTTON_THREE_URL = getConfig('BUTTON_THREE_URL')
    if len(BUTTON_THREE_NAME) == 0 or len(BUTTON_THREE_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_THREE_NAME = None
    BUTTON_THREE_URL = None
try:
    BUTTON_FOUR_NAME = getConfig('BUTTON_FOUR_NAME')
    BUTTON_FOUR_URL = getConfig('BUTTON_FOUR_URL')
    if len(BUTTON_FOUR_NAME) == 0 or len(BUTTON_FOUR_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_FOUR_NAME = None
    BUTTON_FOUR_URL = None
try:
    BUTTON_FIVE_NAME = getConfig('BUTTON_FIVE_NAME')
    BUTTON_FIVE_URL = getConfig('BUTTON_FIVE_URL')
    if len(BUTTON_FIVE_NAME) == 0 or len(BUTTON_FIVE_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_FIVE_NAME = None
    BUTTON_FIVE_URL = None
try:
    STOP_DUPLICATE_MIRROR = getConfig('STOP_DUPLICATE_MIRROR')
    if STOP_DUPLICATE_MIRROR.lower() == 'true':
        STOP_DUPLICATE_MIRROR = True
    else:
        STOP_DUPLICATE_MIRROR = False
except KeyError:
    STOP_DUPLICATE_MIRROR = False
try:
    IS_TEAM_DRIVE = getConfig('IS_TEAM_DRIVE')
    if IS_TEAM_DRIVE.lower() == 'true':
        IS_TEAM_DRIVE = True
    else:
        IS_TEAM_DRIVE = False
except KeyError:
    IS_TEAM_DRIVE = False

try:
    USE_SERVICE_ACCOUNTS = getConfig('USE_SERVICE_ACCOUNTS')
    if USE_SERVICE_ACCOUNTS.lower() == 'true':
        USE_SERVICE_ACCOUNTS = True
    else:
        USE_SERVICE_ACCOUNTS = False
except KeyError:
    USE_SERVICE_ACCOUNTS = False

try:
    BLOCK_MEGA_LINKS = getConfig('BLOCK_MEGA_LINKS')
    if BLOCK_MEGA_LINKS.lower() == 'true':
        BLOCK_MEGA_LINKS = True
    else:
        BLOCK_MEGA_LINKS = False
except KeyError:
    BLOCK_MEGA_LINKS = False

try:
    SHORTENER = getConfig('SHORTENER')
    SHORTENER_API = getConfig('SHORTENER_API')
    if len(SHORTENER) == 0 or len(SHORTENER_API) == 0:
        raise KeyError
except KeyError:
    SHORTENER = None
    SHORTENER_API = None

updater = tg.Updater(token=BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher
