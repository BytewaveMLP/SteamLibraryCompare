# SteamLibraryCompare

> View or compare the libraries of Steam users

Steam has a great tool for comparing the libraries of you and your friend. But what if you want to compare your library with two other friends? Or what if you want to compare the libraries of an entire group of people? This tool lets you compare the libraries of as many Steam users as you want (provided their game libraries are public).

## Installation

### Prerequisites

- Python (3.9)
- pipenv (`pip install pipenv`)
- Steam API key (get one [here](https://steamcommunity.com/dev/apikey))

### Installation

```shell
$ git clone https://github.com/BytewaveMLP/SteamLibraryCompare.git
$ cd SteamLibraryCompare
$ pipenv install
$ pipenv run main.py -h
```

## Usage

Using this tool is pretty simple. Simply provide your API key with the `--api-key` flag, and pass the Steam IDs (or vanity URLs) of the Steam users whose libraries you want to compare. SLC will output the list of games each user has, as well as a list of all games every user has in common. There's nothing more to it than that.

Example invocation:

```shell
$ pipenv run main.py --api-key YOUR_API_KEY Bytewave caramel-sweet
Bytewave's games
----------------
 - 1000 Amps
 - 112 Operator
 - 7 Days to Die
 ...

Adam's games
------------
 - 100% Orange Juice
 - 200% Mixed Juice!
 - A Story About My Uncle
 ...

Games in common
---------------
 - Alien: Isolation
 - Among Us
 - Arma 2: DayZ Mod
 ...
```

**Tip:** This output can get pretty long. It may be helpful to use output redirection to output the list to a file by appending `> games.txt` to the end of the command.

## License

Copyright (c) Eliot Partridge, 2020. Licensed under [the MIT License](/LICENSE).
