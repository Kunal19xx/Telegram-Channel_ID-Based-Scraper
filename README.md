<div align="center">

# **Telegram-Scraper**: `a Python-based open-source tool for Telegram Channel Scraping`

---

---
</div>

## Overview

Currrently some Telegram channels use special characters in channel name or sometimes keep the name hidden making scraping impossible by ususal method. This tool uses the channel ID to fetch information from the channel such as messages, posts etc.

Upon opening a Telegram channel from the browser, a URL is generated, such as https://web.telegram.org/a/#-1001234567890. In this case, the ID is -1001234567890.

This tool is a modification on this project https://github.com/estebanpdl/telegram-tracker.

**Software required**

* [Python 3.9 or above](https://www.python.org/)
* [Telegram API credentials](https://my.telegram.org/auth?to=apps)
	+ Telegram account
	+ App `api_id`
	+ App `api_hash`

**Python required libraries**

* [Telethon](https://docs.telethon.dev/en/stable/)
* [Pandas](https://pandas.pydata.org/)
* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
* [tqdm](https://tqdm.github.io/)
* [Networkx](https://networkx.org/)
* [Matplotlib](https://matplotlib.org/)
* [Louvain Community Detection](https://github.com/taynaud/python-louvain)


Installing
----------

- **Via git clone**

```
git clone https://github.com/Kunal19xx/telegram-channel-id-based-scraper
```

This will create a directory called `telegram-channel-id-based-scraper` which contains the Python scripts. Cloning allows you to easily upgrade and switch between available releases.

- **From the github download button**

Download the ZIP file from github and use your favorite zip utility to unpack the file `telegram-channel-id-based-scraper.zip` on your preferred location.

**After cloning or downloding the repository, install the libraries from `requirements.txt`.**

```
pip install -r requirements.txt
```

or

```
pip3 install -r requirements.txt
```

**Once you obtain an API ID and API hash on my.telegram.org, populate the `config/config.ini` file with the described values.**

```ini

[Telegram API credentials]
api_id = api_id
api_hash = api_hash
phone = phone
```

*Note: Your phone must be included to authenticate for the first time. Use the format +\<code>\<number> (e.g., +19876543210). Telegram API will send you a code via Telegram app that you will need to include.*

<br />

---

# Example usage

## `main.py`

This Python script will connect to Telegram's API and handle your API request.

### Options

* `--telegram-channel` Specifies Telegram Channel to download data from.
* `--telegram-channel-id` Specifies Telegram Channel ID to download data from.
* `--batch-file` File containing Telegram Channels to download data from, one channel per line.
* `--limit-download-to-channel-metadata` Will collect channels metadata only, not channel's messages. (default = False)
* `--output, -o` Specifies a folder to save collected data. If not given, script will generate a default folder called `./output/data`
* `--min-id` Specifies the offset id. This will update Telegram data with new posts.

<br />

### Structure of output data

```
├──🗂 output
|   └──🗂 data
|   	└──🗂 <channel_name>
|   		└──<channel_name>.json
|   		└──<channel_name>_messages.json
|   	└──chats.txt // TM channels, groups, or users' IDs found in data.
|   	└──collected_chats.csv // TM channels or groups found in data (e.g., forwards)
|   	└──collected_chats.xlsx // TM channels or groups found in data (e.g., forwards)
|   	└──counter.csv // TM channels, groups or users found in data (e.g., forwards)
|   	└──user_exceptions.txt // From collected_chats, these are mostly TM users' which 
|									metadata was not possible to retrieve via the API
|   	└──msgs_dataset.csv // Posts and messages from the requested channels
```

<br />

## **Examples**

<br />

### **Basic request**

```
python main.py --telegram-channel channelname
```
```
python main.py --telegram-channel-id channel_ID
```

**Expected output**

- Files of collected channels:
	- chats.txt
	- collected_chats.csv
	- user_exceptions.txt
	- counter.csv
- A new folder: *<channel_name>* containing
	- A JSON file containing channel's profile metadata
	- A JSON file containing posts from the requested channel

<br />

### **Request using a text file containing a set of channels**

```
python main.py --batch-file './path/to/channels_text_file.txt'
```

**Expected output**

- Files of collected channels:
	- chats.txt
	- collected_chats.csv
	- user_exceptions.txt
	- counter.csv
- New folders - based on the number of requested channels: *<channel_name>* containing
	- A JSON file containing channel's profile metadata
	- A JSON file containing posts from the requested channel

These examples will retrieve all posts available through the API from the requested channel. If you want to collect channel's information only, without posts, you can run:

<br />

### **Limit download to channel's metadata only**

```
python main.py --telegram-channel channelname --limit-download-to-channel-metadata
```

or, using a set of telegram channels via a text file:

```
python main.py --batch-file './path/to/channels_text_file.txt' --limit-download-to-channel-metadata
```

<br />

### **Updating channel's data**

If you want to collect new messages from one channel, you need to identify the message ID from the last post. Once you identify the id, run:

```
python main.py --telegram-channel channelname --min-id 12345
```

**Expected output**

- Files of collected channels:
	- chats.txt
	- collected_chats.csv
	- user_exceptions.txt
	- counter.csv
- A new folder: *<channel_name>* containing
	- A JSON file containing channel's profile metadata
	- A JSON file containing posts from the requested channel

<br />

### **Specify output folder**

The script allows you to specify a specific output directory to save collected data. The sxcript will create those folders in case do not exist.

```
python main.py --telegram-channel channelname --output ./path/to/chosen/directory`
```

The expected output is the same a described above but data will be save using the chosen directory.

<br />

---

## `link_scraper.py`

This Python script reads a file containing collected messages and generates a new dataset with links from the specified channel. By default, the resulting dataset is stored in the `./output/data/<channel_name>` directory.

### Options

If a specific directory was not provided in `main.py`, run:

```
python link_scraper.py --telegram-channel-id <eg. - -1001234567890> --url-domain <eg. - fkrt, myntr, amazon, teraboxapp etc.>
```

If --url-domain portion is not provided, it will get all the links in messages starting with https. This option will create a dataset: `https_DOMAIN_links.csv`, a file containing https links from the requested channel with specific domain name. One can use channel name as well. Example given below.

```
python link_scraper.py --telegram-channel-id -1001234567890 --url-domain fkrt
python link_scraper.py --telegram-channel channel_name --url-domain fkrt
```

<br />

---

## `build-datasets.py`

This Python script reads the collected files and creates a new dataset containing messages from the requested channels. By default, the created dataset will be located in the `output` folder.

If you provided a specific directory to save collected data, you need to provide the same path to use this script.

### Options

* `--data-path` Path were data is located. Will use `./output/data` if not given.

If a specific directory was not provided in `main.py`, run:

```
python build-datasets.py
```

If you provided a specific directory using the option `--output` in `main.py`, run:

```
python build-datasets.py --data-path ./path/to/chosen/directory
```

These option will create the above-mentioned dataset: `msgs_dataset.csv`, a file containing posts and messages from the requested channels.

<br />

---

## `channels-to-network.py`

This Python script builds a network graph. By default, the file will be located in the `output` folder. The script also saves a preliminary graph: `network.png` using the modules matplotlib, networkx, and python-louvain, which implements community detection. You can import the GEFX Graph File using different softwares, including Gephi.

### Options

* `--data-path` Path were data is located. Will use `./output/data` if not given.

If a specific directory was not provided in `main.py`, run:

```
python channels-to-network.py
```

If you provided a specific directory using the option `--output` in `main.py`, run:

```
python channels-to-network.py --data-path ./path/to/chosen/directory
```
