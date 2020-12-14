import os

import discord

class RiftHaroldClient(discord.Client):
  """Implements event handlers from discord.Client.
  """
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

  async def on_message(self, message):
    # Skip the message if it came from RiftHarold
    if message.author == self.user:
      return
    
    if message.content.startswith('!hello'):
      await message.channel.send('hello')