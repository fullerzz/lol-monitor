import requests
import json
import random
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('logger')

class Summoner:
    def __init__(self, name, players_dict, api_key, twilio, champ_dict):
        self.name = name
        self.players_dict = players_dict
        self.account_id = players_dict[name]['accountId']
        self.api_key = api_key
        self.twilio = twilio
        self.champ_dict = champ_dict

    def get_last_match_id(self):
        logger.info('Get match list for ' + self.name)
        url = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + self.account_id + '?api_key=' + str(self.api_key)
        r = requests.get(url)
        r_json = r.json()
        last_match = r_json['matches'][0]['gameId']
        logger.info('Returning gameId of last match')
        return last_match

    def check_for_new_match(self):
        logger.info('Entered check_for_new_match()')
        logger.info('Calling get_last_match_id')
        last_match_id = self.get_last_match_id()

        file_match_id = self.players_dict[self.name]['lastMatch']
        if last_match_id != file_match_id:
            logger.info('New match found')
            self.players_dict[self.name]['lastMatch'] = last_match_id
            self.update_player_data()
            self.get_match_info(last_match_id)
        else:
            logger.info('No new match found')
            print('No new match found for ' + self.name)
            return False

    def get_match_info(self, match_id):
        logger.info('Getting match info for ' + str(match_id))
        url = 'https://na1.api.riotgames.com/lol/match/v4/matches/' + str(match_id) + '?api_key=' + self.api_key
        r = requests.get(url)
        r_json = r.json()
        participants = r_json['participants']
        players = r_json['participantIdentities']

        participant_id = None

        logger.info('Finding participantId for ' + self.name)
        for player in players:
            if player['player']['accountId'] == self.account_id:
                participant_id = player['participantId']
        
        kills = None
        deaths = None
        assists = None
        cs = None
        result = None
        team_id = None
        champion_id = None

        logger.info('Collecting player stats')
        for participant in participants:
            if participant['participantId'] == participant_id:
                kills = participant['stats']['kills']
                deaths = participant['stats']['deaths']
                assists = participant['stats']['assists']
                cs = participant['stats']['totalMinionsKilled']
                team_id = participant['teamId']
                champion_id = participant['championId']

        champion = self.champ_dict[str(champion_id)]

        teams = r_json['teams']
        logger.info('Determining result of match')
        for team in teams:
            if team['teamId'] == team_id:
                result = team['win']

        if result == 'Fail':
            logger.info('Match was a defeat')
            result = 'Defeat'
        else:
            logger.info('Match was a victory')
            result = 'Victory'

        game_info = {'kills' : kills, 'deaths' : deaths, 'assists' : assists, 'cs' : cs, 'result' : result, 'champion': champion}
        self.send_text(game_info)

    def send_text(self, game_info):
        logger.info('Entering send_text()')
        client = self.twilio

        messages_l = ['You\'ll get them next time!', 'Practice makes perfect!', 'Unlucky!']
        messages_w = ['Nice job!', 'Wow that\'s amazing!', 'What a performance!', 'Teach me your ways!.']

        person = self.name
        random.seed()

        msg = None
        if game_info['result'] != 'Victory':
            index = random.randint(0,2)
            msg = messages_l[index] + ' ' + person + ' just lost a game by going ' + str(game_info['kills']) + '/' + str(game_info['deaths']) + '/' + str(game_info['assists']) + ' as ' + game_info['champion'] + '.'
        else:
            index = random.randint(0,3)
            msg = messages_w[index] + ' ' + person + ' just won a game by going ' + str(game_info['kills']) + '/' + str(game_info['deaths']) + '/' + str(game_info['assists']) + ' as ' + game_info['champion'] + '.'
        
        logger.info('Message built: ' + msg)
        sender_num = self.players_dict['Sender']['phoneNum']

        # Sending text to Brandon
        logger.info('Sending text to Brandon: ' + self.players_dict['Brandon']['phoneNum'])
        message_b = client.messages.create(body=msg, from_=sender_num, to=self.players_dict['Brandon']['phoneNum'])
        logger.info('Message response: ' + message_b.sid)

        # Sending text to Zach
        logger.info('Sending text to Zach: ' + self.players_dict['Zach']['phoneNum'])
        message_z = client.messages.create(body=msg, from_=sender_num, to=self.players_dict['Zach']['phoneNum'])
        logger.info('Message response: ' + message_z.sid)

        # Sending text to Jarrod
        logger.info('Sending text to Jarrod: ' + self.players_dict['Jarrod']['phoneNum'])
        message_j = client.messages.create(body=msg, from_=sender_num, to=self.players_dict['Jarrod']['phoneNum'])
        logger.info('Message response: ' + message_j.sid)

    def update_player_data(self):
        logger.info('Updating last_match.json')
        with open('Resources/player_data.json', 'w') as outfile:
            json.dump(self.players_dict, outfile)
