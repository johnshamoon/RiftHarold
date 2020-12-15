import requests

class RiftHarold:
  """Rift Harold's interface to talk to Riot APIs.
  """
  def  __init__(self, riot_api_key):
    self.riot_api_key = riot_api_key

  def get_summoner_info(self, summoner_name):
    if not summoner_name:
      return "No summoner name provided."
    url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name'
    request =  '{}/{}?api_key={}'.format(url, summoner_name, self.riot_api_key)
    response = requests.get(request)
    if response.status_code == 404:
      return 'Summoner {} not found'.format(summoner_name)

    response = response.json()
    info = 'Summoner Name: {}\nSummoner Level: {}\n'.format(response['name'], response['summonerLevel'])

    return info

