import os

from dotenv import load_dotenv

from rift_harold_client import RiftHaroldClient

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
RIOT_TOKEN = os.getenv('RIOT_TOKEN')

def main():
  client = RiftHaroldClient(RIOT_TOKEN)
  client.run(DISCORD_TOKEN)

if __name__ == '__main__':
  main()