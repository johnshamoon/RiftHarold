import json, re, requests

class RiftHarold:
  """Rift Harold's interface to talk to Riot APIs.
  """
  _base_url = 'https://na1.api.riotgames.com/lol/'

  def  __init__(self, riot_api_key):
    self.game = {}
    self.champs = {}
    self.runes = {}
    self.summoner_spells = {}

    self.riot_api_key = riot_api_key

    # TODO: maybe add region detection future


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
    info = 'Summoner Name: {}\nSummoner Level: {}\n'.format(response['name'], response['summonerLevel'])

    return info


  def get_live_data(self, encryptedSummonerId):
    url = self._base_url + 'spectator/v4/active-games/by-summoner/' + encryptedSummonerId
    request =  '{}?api_key={}'.format(url, self.riot_api_key)
    response = requests.get(request)

    if response.status_code == 200:
      response_text = json.loads(response.text)
      for player in response_text['participants']:
        # remove the bottom 3 "perks" that are not actually runes
        perks = player['perks']['perkIds'][:-3]

        self.game[player['championId']] = { 'team' : player['teamId'],
                                            'summoner_spell_1' : player['spell1Id'],
                                            'summoner_spell_2' : player['spell2Id'],
                                            'runes' : perks}
      return 'Started tracking game'
    else:
      return 'Cannot get live data at this time. Response code:%s' % response.status_code


  def setup_champs(self):
    with open('../data/current/data/en_US/championsFull.json') as f:
      data = f.read()

    champ_dict = json.loads(data)
    champ_dict = champ_dict['data']
    for champ in champ_dict:
      # Grab spells, description, cooldowns; want to index by champ key
      self.champs[champ['key']] = { 'name' : champ['name'],
                                    # NOTE: may want to do, per spell: id, name, cooldown, cost, description
                                    'spells' : champ['spells'],
                                    'passive' : champ['passive']}


  def setup_runes(self):
    # Set up information for SS calc. based on runes
    with open('../data/current/data/en_US/runesReforged.json') as f:
      rune_data = f.read()

    # Initial data format is a list of dicts; load Runes into more useful format
    rune_list = json.loads(rune_data)

    # rune_tree refers to the 6 different rune paths overall
    for rune_tree in rune_list:
      # rune_row refers to each row of choices in a tree
      for rune_row in rune_tree['slots']:
        # rune_row contains list of choice dicts
        for rune_choice in rune_row['runes']:
          self.runes[rune_choice['id']] = { 'name' : rune_choice['key'],
                                            'desc' : rune_choice['longDesc']}


  def setup_summs(self):
    # Get summoner spell info
    with open('../data/current/data/en_US/summoner.json') as f:
      summoner_spell_data = f.read()

    ss_list = json.loads(summoner_spell_data)

    for spell in ss_list:
      # NOTE: There's also the key 'cooldown' but it has a list and i cant tell
      # the difference between the two of them
      self.summoner_spells[spell['key']] = spell['cooldownBurn']


  def start_tracking(self, summoner_name):
    self.setup_champs()
    self.setup_runes()
    self.setup_summs()

    summonerData = self.get_summoner_info(summoner_name, True)
    return self.get_live_data(summonerData['id'])

