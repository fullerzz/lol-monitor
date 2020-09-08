# League of Legends - Match History Monitor

This python program was developed for use between me and two of my friends who play the game League of Legends.
The program makes use of the Riot Games API along with the Twilio API for sending SMS messages.

## How It Works

* Hosted on a Raspberry Pi 3.
* Runs as a Cron Job every 60 seconds.
* Player data is stored in a json file not included in this repository. This file contains data such as account ids, phone numbers, and the id of the last known match for each player.
* Program will make a request to retrieve the match history of each player and then compares the most recent match id to the one stored in the file.
* If they are different, the player data file is updated and a message is sent to me and my two friends containing details about the match.

## Example of SMS Sent by Bot
![example_lol_sms_bot_text](https://user-images.githubusercontent.com/26610175/92522600-dd373e00-f1d3-11ea-93d2-39f5edda5a62.jpg)
