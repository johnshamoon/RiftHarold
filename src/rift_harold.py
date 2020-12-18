import json, re, requests

class RiftHarold:
  """Rift Harold's interface to talk to Riot APIs.
  """
  _base_url = 'https://na1.api.riotgames.com/lol/'

  def  __init__(self, riot_api_key):
    self.riot_api_key = riot_api_key

    # Set up information for SS calc. based on runes
    # TODO: maybe add region detection future
    with open('../data/current/data/en_US/runesReforged.json') as f:
      rune_data = f.read()

    # Initial data format is a list of dicts; load Runes into more useful format
    rune_list = json.loads(rune_data)

    self.runes = {}
    # rune_tree refers to the 6 different rune paths overall
    for rune_tree in rune_list:
      # rune_row refers to each row of choices in a tree
      for rune_row in rune_tree['slots']:
        # rune_row contains list of choice dicts
        for rune_choice in rune_row['runes']:
          self.runes[rune_choice['id']] = { 'name' : rune_choice['key'],
                                       'desc' : rune_choice['longDesc']}


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
    url = self._base_url + 'spectator/v4/active-games/by-summoner/' + encryptedSummonerId
    request =  '{}?api_key={}'.format(url, self.riot_api_key)
    response = requests.get(request)

    if response.status_code == 200:
      returnString = 'has '
      # TODO: parse response with more than one person in game and match perks to player
      current_runes = re.findall('(?<=perkIds":\[).*?(?=\],")', response.text)
      # NOTE: current_runes will likely be a list of 10 elements outside of testing : ^ )
      if current_runes:
        # NOTE: obvi this wont work for more than one person
        current_runes = current_runes[0].split(',')
        for rune in current_runes:
          # FIXME: keyerror on 5008??? is the adaptive and armor stuff but thats not in our dict. hm
          if rune == '5008':
            break
          returnString += self.runes[int(rune)]['name'] + ' '

      return returnString
    else:
      return 'Cannot get live data at this time. Response code:%s' % response.status_code


  def start_tracking(self, summoner_name):
    summonerData = self.get_summoner_info(summoner_name, True)
    return self.get_live_data(summonerData['id'])

