"""
MIT License

Copyright (c) 2018-2019 truedl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests, aiohttp

Key = None

class User:
    def __init__(self, steamid=None, custom=None):
        self.key = Key
        if not steamid:
            self.steamid = self.SteamIdByCustom(custom=custom)
        else:
            self.steamid = steamid
    
    def SteamIdByCustom(self, custom=None):
        """ Get Steam ID By Steam Custom, Returned: SteamID """

        return requests.get(f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={self.key}&vanityurl={custom}').json()['response']['steamid']
    
    def Data(self):
        """ Get information about steam user, Returned: SteamUser Class """

        data = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.key}&steamids={self.steamid}').json()['response']['players'][0]
        required = ['steamid', 'communityvisibilitystate', 'profilestate', 'personaname', 'lastlogoff', 'commentpermission', 'avatar', 'avatarmedium', 'avatarfull'
                    'personastate', 'realname', 'primaryclanid', 'timecreated', 'personastateflags', 'loccountrycode', 'locstatecode']
        for x in data:
            try:
                required.remove(x)
            except:
                pass
        for x in required:
            data[x] = None
        return SteamUser(data['steamid'], data['communityvisibilitystate'], data['profilestate'], data['personaname'], data['lastlogoff'],
                         data['commentpermission'], data['avatar'], data['avatarmedium'], data['avatarfull'], data['personastate'],
                         data['realname'], data['primaryclanid'], data['timecreated'], data['personastateflags'], data['loccountrycode'],
                         data['locstatecode'])
    
    def Friends(self, friends=[]):
        """ Get user friendlist, Returned: SteamFriendList Class """

        data = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.key}&steamid={self.steamid}&relationship=friend').json()['friendslist']['friends']
        for x in data:
            friends.append(SteamFriend(x['steamid'], x['relationship'], x['friend_since']))
        return SteamFriendList(friends)
    
    def Stats(self, appid=None, stats={}, gn=None):
        """ Get user stats by appid, Returned: SteamGameStats Class """

        data = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={self.key}&steamid={self.steamid}').json()['playerstats']
        gn = data['gameName']
        for x in data['stats']:
            stats[x['name']] = x['value']
        return SteamGameStats(gn, appid, stats)
    
    def Games(self, _list=[], total=None):
        """ Get user gamelist, Returned: SteamGameList Class """

        data = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.key}&steamid={self.steamid}&format=json').json()['response']
        total = data['game_count']
        for x in data['games']:
            _list.append(x['appid'])
        return SteamGameList(total, _list)
    
    def RecentlyPlayed(self):
        """ Get user recently game(s) played, Returned: SteamRecentlyPlayed Class """

        data = requests.get(f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={self.key}&steamid={self.steamid}&format=json').json()['response']['games'][0]
        return SteamRecentlyPlayed(data['appid'], data['name'], data['playtime_2weeks'], data['playtime_forever'], data['img_icon_url'], data['img_logo_url'])

    def CheckBan(self):
        """ Get user bans information by steamid or custom, Returned: SteamBanStatus Class """

        data = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={self.key}&steamids={self.steamid}').json()['players'][0]
        return SteamBanStatus(data['CommunityBanned'], data['VACBanned'], data['NumberOfVACBans'], data['DaysSinceLastBan'], data['NumberOfGameBans'], data['EconomyBan'])

    def Level(self):
        """ Get user steam level, Returned: Level(int) """

        return int(requests.get(f'https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={self.key}&steamid={self.steamid}').json()['response']['player_level'])

class AsyncedUser:
    def __init__(self, steamid=None, custom=None):
        self.key = Key
        self.steamid = steamid
        self.custom = custom

    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()
    
    async def start(self):
        if not self.steamid:
            self.steamid = await self.SteamIdByCustom(custom=self.custom)

    async def SteamIdByCustom(self, custom=None):
        """ Get Steam ID By Steam Custom, Returned: SteamID """
        f = await self.fetch(f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={self.key}&vanityurl={custom}')
        return f['response']['steamid']

    async def Data(self):
        """ Get information about steam user by steamid or custom, Returned: SteamUser Class """

        f = await self.fetch(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.key}&steamids={self.steamid}')
        data = f['response']['players'][0]
        required = ['steamid', 'communityvisibilitystate', 'profilestate', 'personaname', 'lastlogoff', 'commentpermission', 'avatar', 'avatarmedium', 'avatarfull'
                    'personastate', 'realname', 'primaryclanid', 'timecreated', 'personastateflags', 'loccountrycode', 'locstatecode']
        for x in data:
            try:
                required.remove(x)
            except:
                pass
        for x in required:
            data[x] = None
        return SteamUser(data['steamid'], data['communityvisibilitystate'], data['profilestate'], data['personaname'], data['lastlogoff'],
                           data['commentpermission'], data['avatar'], data['avatarmedium'], data['avatarfull'], data['personastate'],
                           data['realname'], data['primaryclanid'], data['timecreated'], data['personastateflags'], data['loccountrycode'],
                           data['locstatecode'])

    async def Friends(self, friends=[]):
        """ Get user friendlist by steamid or custom, Returned: SteamFriendList Class """
        f = await self.fetch(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.key}&steamid={self.steamid}&relationship=friend')
        data = f['friendslist']['friends']
        for x in data:
            friends.append(SteamFriend(x['steamid'], x['relationship'], x['friend_since']))
        return SteamFriendList(friends)

    async def Stats(self, appid=None, stats={}, gn=None):
        """ Get user stats by appid and steamid/custom, Returned: SteamGameStats Class """

        f = await self.fetch(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={self.key}&steamid={self.steamid}')
        data = f['playerstats']
        gn = data['gameName']
        for x in data['stats']:
            stats[x['name']] = x['value']
        return SteamGameStats(gn, appid, stats)

    async def Games(self, _list=[], total=None):
        """ Get user gameslist by steamid or custom, Returned: SteamGamesList Class """

        f = await self.fetch(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.key}&steamid={self.steamid}&format=json')
        data = f['response']
        for x in data['games']:
            _list.append(x['appid'])
        return SteamGamesList(data['game_count'], _list)

    async def RecentlyPlayed(self):
        """ Get user recently game played by steamid or custom, Returned: SteamRecentlyPlayed Class """

        f = await self.fetch(f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={self.key}&steamid={self.steamid}&format=json')
        data = f['response']['games'][0]
        return SteamRecentlyPlayed(data['appid'], data['name'], data['playtime_2weeks'], data['playtime_forever'], data['img_icon_url'], data['img_logo_url'])

    async def CheckBan(self, steamid=None, custom=None):
        """ Get user ban's information by steamid or custom, Returned: SteamBanStatus Class """

        f = await self.fetch(f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={self.key}&steamids={self.steamid}')
        data = f['players'][0]
        return SteamBanStatus(data['CommunityBanned'], data['VACBanned'], data['NumberOfVACBans'], data['DaysSinceLastBan'], data['NumberOfGameBans'], data['EconomyBan'])

    async def Level(self):
        """ Get user steam level, Returned: Level(int) """

        f = await self.fetch(f'https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={self.key}&steamid={self.steamid}')
        return int(f['response']['player_level'])

class AsyncedC:
    User = AsyncedUser

asynced = AsyncedC()

class SteamBanStatus:
    def __init__(self, communityban, vacban, total_vacs, dayssincelastban, total_game_bans, economyban):
        self.communityban = communityban
        self.vacban = vacban
        self.total_vacs = total_vacs
        self.dayssincelastban = dayssincelastban
        self.total_game_bans = total_game_bans
        self.economyban = economyban

class SteamUser:
    def __init__(self, steamid, communityvisibilitystate, profilestate, personaname, lastlogoff, commentpermission, avatar, avatarmedium, avatarfull, personastate, realname, primaryclanid, timecreated, personastateflags, loccountrycode, locstatecode):
        self.steamid = steamid
        self.communityvisibilitystate = communityvisibilitystate
        self.profilestate = profilestate
        self.personaname = personaname
        self.lastlogoff = lastlogoff
        self.commentpermission = commentpermission
        self.avatar = avatar
        self.avatarmedium = avatarmedium
        self.avatarfull = avatarfull
        self.personastate = personastate
        self.realname = realname
        self.primaryclanid = primaryclanid
        self.timecreated = timecreated
        self.personastateflags = personastateflags
        self.loccountrycode = loccountrycode
        self.locstatecode = locstatecode

class SteamFriendList:
    def __init__(self, _list):
        self.list = _list

class SteamFriend:
    def __init__(self, steamid, relationship, friend_since):
        self.steamid = steamid
        self.relationship = relationship
        self.friend_since = friend_since

class SteamGameStats:
    def __init__(self, game, appid, stats):
        self.game = game
        self.appid = appid
        self.stats = stats

class SteamGameList:
    def __init__(self, tg, _list):
        self.games_count = tg
        self.list = _list

class SteamRecentlyPlayed:
    def __init__(self, appid, name, playtimetwoweeks, playtime, icon_url, logo_url):
        self.appid = appid
        self.name = name
        self.playtimetwoweeks = playtimetwoweeks
        self.playtime = playtime
        self.icon_url = f'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/{appid}/{icon_url}.jpg'
        self.logo_url = f'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/{appid}/{logo_url}.jpg'
