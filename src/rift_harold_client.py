import discord

from rift_harold import RiftHarold

class RiftHaroldClient(discord.Client):
  """Implements event handlers from discord.Client.
  """
  def __init__(self, riot_api_key):
    discord.Client.__init__(self)
    self.rift_harold = RiftHarold(riot_api_key)

  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

  async def on_message(self, message):
    # Skip the message if it came from RiftHarold
    if message.author == self.user:
      return

    if message.content.startswith('!summoner'):
      summoner_name = message.content.split(' ', 1)
      if len(summoner_name) > 1:
        summoner_name = summoner_name[1]
      else:
        summoner_name = ''
      await message.channel.send(self.rift_harold.get_summoner_info(summoner_name))
    elif message.content.startswith('!'):
      await message.channel.send("Supported commands: !summoner")