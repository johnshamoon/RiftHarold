import json, re, requests

class RiftHarold:
  """Rift Harold's interface to talk to Riot APIs.
  """
  _base_url = 'https://na1.api.riotgames.com/lol/'

  def  __init__(self, riot_api_key):
    self.game = {}
    self.champs = {}
    self.champ_keys = {}
    self.runes = {}
    self.summoner_spells = {}

    self.riot_api_key = riot_api_key

    self._setup_champs()
    self._setup_runes()
    self._setup_summs()


  def _setup_champs(self):
    with open('../data/current/data/en_US/championsFull.json') as f:
      champ_dict = json.load(f)['data']

    for champ in champ_dict:
      # Grab spells, description, cooldowns; want to index by champ key
      self.champs[champ['key']] = { 'name' : champ['name'],
                                    # NOTE: may want to do, per spell: id, name, cooldown, cost, description
                                    'spells' : champ['spells'],
                                    'passive' : champ['passive']}

      # meh maybe this is bad/lazy; but we want to use for user look up later
      self.champ_keys[champ['name']] = champ['key']


  def _setup_runes(self):
    # Set up information for SS calc. based on runes
    with open('../data/current/data/en_US/runesReforged.json') as f:
      # Initial data format is a list of dicts; load Runes into more useful format
      rune_list = json.load(f)

    # rune_tree refers to the 6 different rune paths overall
    for rune_tree in rune_list:
      # rune_row refers to each row of choices in a tree
      for rune_row in rune_tree['slots']:
        # rune_row contains list of choice dicts
        for rune_choice in rune_row['runes']:
          self.runes[rune_choice['id']] = { 'name' : rune_choice['key'],
                                            'desc' : rune_choice['longDesc']}


  def _setup_summs(self):
    # Get summoner spell info
    with open('../data/current/data/en_US/summoner.json') as f:
      summoner_spell_data = f.read()

    ss_list = json.loads(summoner_spell_data)

    for spell in ss_list:
      # NOTE: There's also the key 'cooldown' but it has a list and i cant tell
      # the difference between the two of them
      self.summoner_spells[spell['key']] = spell['cooldownBurn']


  def get_summoner_info(self, summoner_name):
    if not summoner_name:
      return "No summoner name provided."

    # Make request
    url = self._base_url + 'summoner/v4/summoners/by-name'
    request =  '{}/{}?api_key={}'.format(url, summoner_name, self.riot_api_key)
    response = requests.get(request)
    
    # self.check_response(response) # NOTE: unsure how to use
    if response.status_code != 200:
      return 'Summoner {} not found'.format(summoner_name)

    response = response.json()

    return response


  def get_live_data(self, encryptedSummonerId):
    teamId = None
    playerId = None
    self.enemy_teamId = None

    # GET
    url = self._base_url + 'spectator/v4/active-games/by-summoner/' + encryptedSummonerId
    request =  '{}?api_key={}'.format(url, self.riot_api_key)
    response = requests.get(request)

    # PARSE
    if response.status_code == 200:
      response = response.json
      for player in response['participants']:
        # remove the bottom 3 "perks" that are not actually runes
        perks = player['perks']['perkIds'][:-3]

        # FIXME: we have a bug here due to using champ id as a key; in blind, 2 of same champ can exist;
        # organize into 2 dicts, 1 per team and the disregard our team? lol
        self.game[player['championId']] = { 'team' : player['teamId'],
                                            'summoner_spell_1' : player['spell1Id'],
                                            'summoner_spell_2' : player['spell2Id'],
                                            'runes' : perks}

        # Discern tracked player's team so we can get enemy team id for later
        if teamId and teamId != player['teamId']:
          self.enemy_teamId = player['teamId']
        elif encryptedSummonerId == player['summonerId']:
          teamId = player['teamId']

      return 'Started tracking game'
    else:
      return 'Cannot get live data at this time. Response code:%s' % response.status_code


  def print_summoner(self, summoner_name):
    response = self.get_summoner_info(summoner_name)
    
    return 'Summoner Name: {}\nSummoner Level: {}\n'.format(response['name'], response['summonerLevel'])


  def start_tracking(self, summoner_name):
    summonerData = self.get_summoner_info(summoner_name)
    return self.get_live_data(summonerData['id'])


  def summoner_cal(self, champ_name, spell, time):
    ''' Input should be something like !zed flash (and record the time entered)
    '''
    # Assume we've told harold to track our own game and not someone on enemy team's
    # Get player based on team and champion selected
    champ_key = self.champ_keys[champ_name]

    player = self.game[champ_key]
    if lenself.game[champ_key]['team'] == self.enemy_teamId

