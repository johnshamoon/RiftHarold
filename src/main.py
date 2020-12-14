import os

from dotenv import load_dotenv

from rift_harold_client import RiftHaroldClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def main():
  client = RiftHaroldClient()
  client.run(TOKEN)

if __name__ == '__main__':
  main()