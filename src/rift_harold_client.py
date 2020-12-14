import os
import requests

import discord

class RiftHaroldClient(discord.Client):
  """Implements event handlers from discord.Client.
  """
  def __init__(self, riot_api_key):
    discord.Client.__init__(self)
    self.riot_api_key = riot_api_key

  def get_summoner_info(self, summoner_name):
    url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name'
    request =  '{}/{}?api_key={}'.format(url, summoner_name, self.riot_api_key)
    response = requests.get(request)

    return response.json()

  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

  async def on_message(self, message):
    # Skip the message if it came from RiftHarold
    if message.author == self.user:
      return

    if message.content.startswith('!summoner'):
      requested_summoner_name = message.content.split()[1]
      summoner_info = self.get_summoner_info(requested_summoner_name)
      response = 'Summoner Name: {}\nSummoner Level: {}\n'.format(summoner_info['name'], summoner_info['summonerLevel'])
      await message.channel.send(response)
    elif message.content.startswith('!'):
      await message.channel.send("Supported commands: !summoner")