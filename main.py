from collections.abc import Iterable
import requests
import argparse
import steamid

parser = argparse.ArgumentParser(description="Look up and compare Steam users' libraries")
parser.add_argument('--api-key', type=str, dest='apikey', required=True, help='Your Steam API key; see https://steamcommunity.com/dev/apikey')
parser.add_argument('steamid', type=str, nargs='+', help='A Steam ID to add to the comparison list. Accepts any format (vanity URL, Steam ID, SteamID64, etc)')
args = parser.parse_args()

apikey = args.apikey

def steam_request(endpoint: str, params: dict[str, str]) -> any:
	"""Generic method to perform a request to Steam's public API.

	Parameters
	----------
	endpoint : str
		The endpoint to hit
	params : dict[str, str]
		The query parameters to pass to requests
	
	Returns
	-------
	any
		The JSON-decoded body of the returned response

	Raises
	------
	requests.RequestException
		If any failures occurred while making the request
	"""
	r = requests.get(
		f'https://api.steampowered.com/{endpoint}/',
		{
			**params,
			**{
				'key': apikey,
				'format': 'json'
			}
		}
	)
	r.raise_for_status()

	body = r.json()
	return body

def get_games_for_steamid(steamid: str) -> set[tuple[int, str]]:
	"""Gets the games owned by a Steam user

	Parameters
	----------
	steamid : str
		The user's 64-bit Steam ID
	
	Returns
	-------
	set[tuple[int, str]]
		The set of games this user owns, in tuples of appid and game name
	"""
	body = steam_request('IPlayerService/GetOwnedGames/v0001', params={
		'include_appinfo': True, 'steamid': steamid
	})
	return set((game['appid'], game['name']) for game in body['response']['games'])

def convert_to_steamid64(possible_steamid: str) -> str:
	"""Attempts to convert a Steam ID or vanity URL into a 64-bit Steam ID

	First, this attempts to parse the Steam ID into any known format, and convert that into a
	64-bit Steam ID. Failing that, this will issue a request to Steam in order to resolve the
	string as a vanity URL.

	Parameters
	----------
	possible_steamid : str
		The string to convert. Can be a Steam ID or a vanity URL.
	
	Returns
	-------
	str
		The 64-bit Steam ID of the found user
	"""
	try:
		sid = steamid.SteamID(possible_steamid)
		return sid.toString()
	except ValueError:
		return steam_request('ISteamUser/ResolveVanityURL/v1', params={
			'vanityurl': possible_steamid
		})['response']['steamid']

def get_names_from_steamids(steamids: Iterable[str]) -> dict[str, str]:
	"""Gets the display names of all provided users

	Parameters
	----------
	steamids : Iterable[str]
		The 64-bit Steam IDs to fetch the names of
	
	Returns
	-------
	dict[str, str]
		A list of names of users, keyed by their Steam IDs
	"""
	players = steam_request('ISteamUser/GetPlayerSummaries/v2', params={
		'steamids': ','.join(steamids)
	})['response']['players']
	return { player['steamid']: player['personaname'] for player in players }

def print_games(games: set[tuple[int, str]]):
	"""Helper function to print a list of games"""
	for game in sorted(games, key=lambda g: g[1]):
		print(f' - {game[1]}')
	print()

steamids = [convert_to_steamid64(sid) for sid in args.steamids]
steamid_names = get_names_from_steamids(steamids)
steamid_games = { steamid: get_games_for_steamid(steamid) for steamid in steamids }
common_games = set.intersection(*steamid_games.values())

for steamid in steamids:
	header = f"{steamid_names[steamid]}'s games"
	print(header)
	print('-' * len(header))
	print_games(steamid_games[steamid])

if len(steamids) > 1:
	print('Games in common')
	print('---------------')
	print_games(common_games)
