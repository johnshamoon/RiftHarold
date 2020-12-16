import requests

class RiftHarold:
  """Rift Harold's interface to talk to Riot APIs.
  """
  _base_url = 'https://na1.api.riotgames.com/lol/'

  def  __init__(self, riot_api_key):
    self.riot_api_key = riot_api_key

  def get_summoner_info(self, summoner_name, internalUse=False):
    if not summoner_name:
      return "No summoner name provided."
    url = self._base_url + 'summoner/v4/summoners/by-name'
    request =  '{}/{}?api_key={}'.format(url, summoner_name, self.riot_api_key)
    response = requests.get(request)
    if response.status_code != 200:
      return 'Summoner {} not found'.format(summoner_name)

    response = response.json()

    # I need for more than a print out; need encryptedId and maybe more
    if internalUse:
      return response
    print(response)
    info = 'Summoner Name: {}\nSummoner Level: {}\n'.format(response['name'], response['summonerLevel'])

    return info


def get_live_data(self, encryptedSummonerId):
  url = self._base_url + 'spectator/v4/active-games/by-summoner/{encryptedSummonerId}'
  request =  '{}?api_key={}'.format(url, self.riot_api_key)
  response = requests.get(request)

  if response.status == 200:
    return response
  else:
    return 'Cannot get live data at this time'


def start_tracking(self, summoner_name):
  summonerData = self.get_summoner_info(summoner_name, True)
  return self.get_live_data(summonerData['id'])

