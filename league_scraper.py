#!/home/ubuntu/Code/lol_match_sms_bot/lol-sms-env/bin/python3
from summoner import Summoner
from twilio.rest import Client
import requests as req
import urllib.request
import time
import json
import logging
from logging.handlers import RotatingFileHandler
import sys

def load_champ_dict():
    with open('Resources/champion_ids.json', 'r') as file:
        champion_dict = json.load(file)
        return champion_dict

def load_player_data():
    with open('Resources/player_data.json', 'r') as file:
        players_dict = json.load(file)
        return players_dict


logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler('./logs/sms_bot_summoner.log', maxBytes=20000, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

account_sid = None
auth_token = None
riot_key = None
champion_dict = load_champ_dict()

# Gets Twilo Account ID
sid_file = open('Credentials/account_sid.txt', 'r')
if sid_file.mode == 'r':
    logger.debug('Reading sid from account_sid.txt')
    account_sid = sid_file.read()
    sid_file.close()

# Gets Twilio Auhtorization Token
auth_file = open('Credentials/auth_token.txt', 'r')
if auth_file.mode == 'r':
    logger.debug('Reading token from auth_token.txt')
    auth_token = auth_file.read()
    auth_file.close()

# Creates Twilio Client
logger.info('Creating new Twilio client')
client = Client(account_sid, auth_token)
logger.info('Twilio client created successfully')

# Gets Riot API Key
riot_file = open('Credentials/riot_key.txt', 'r')
if riot_file.mode == 'r':
    logger.debug('Reading riot api key from riot_key.txt')
    riot_key = riot_file.read()
    riot_file.close()

# Loads player data from json file
players_dict = load_player_data()

# Checks Zach's matches for new games
logger.info('Creating Summoner object for Zach')
zach = Summoner('Zach', players_dict, riot_key, client, champion_dict)
zach.check_for_new_match()

# Checks Jarrod's matches for new games
logger.info('Creating Summoner object for Jarrod')
jarrod = Summoner('Jarrod', players_dict, riot_key, client, champion_dict)
jarrod.check_for_new_match()

# Checks Brandon's matches for new games
logger.info('Creating Summoner object for Brandon')
brandon = Summoner('Brandon', players_dict, riot_key, client, champion_dict)
brandon.check_for_new_match()

sys.exit()
