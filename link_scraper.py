import re
import sys
import json
import argparse
import pandas as pd
import logging

logging.basicConfig(filename='link_scrapper.log', encoding='utf-8', level=logging.DEBUG)



def https_link_scrapper(channel_name, id_flag=True, domain_name: str = None):
    # None domain handling
    domain_name = str(domain_name or "")
    # executed if we input channel ID instead of name
    if id_flag:
        channel_name = 'channel_' + channel_name
    input_path = f"./output/data/{channel_name}/{channel_name}_messages.json"
    output_path = f"./output/data/{channel_name}/https_{domain_name}_links.csv"

    # Open the JSON file for reading
    logging.info('Reading json file containing messages')
    with open(input_path, 'r', encoding= 'utf-8') as file:
        data = json.load(file)

    # Select messages dictionary only
    msgs = data['messages']
    links = []

    # Regular expression pattern to match URLs
    link_pattern = f'https://{domain_name}.*?\n'
    for i in msgs:
        if 'message' in i.keys():
            links += re.findall(link_pattern, i['message'])

    df = pd.DataFrame(links)
    df = df.iloc[:,0].apply(lambda x: x.strip())
    df.drop_duplicates(inplace = True)
    logging.info('Writing csv file containing messages')
    df.to_csv(output_path, header=False, index=False)
    logging.info('Writing completed')

    return None

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Arguments.')
    parser.add_argument(
        '--telegram-channel-id',
        type=str,
        required= '--telegram-channel' not in sys.argv,
        help='Specifies a Telegram Channel ID'
    )
    parser.add_argument(
        '--telegram-channel',
        type=str,
        required= '--telegram-channel-id' not in sys.argv,
        help='Specifies a Telegram Channel'
    )
    parser.add_argument(
        '--url-domain',
        type=str,
        required= False,
        help='Specifies a URL domain name'
    )
    args = vars(parser.parse_args())

    if args['telegram_channel_id']:
        https_link_scrapper(args['telegram_channel_id'], 
                            True,
                            args['url_domain']
                            )
    else :
        https_link_scrapper(args['telegram_channel'], 
                            False,
                            args['url_domain']
                            )
