#! /usr/bin/env python

import click
from pprint import pprint
import re
import requests
import sys
import time

try:
    from api_token import API_TOKEN
except ImportError:
    print('Please store API_TOKEN in api_token.py')
    sys.exit(1)

MESSAGE_ENDPOINT = 'https://slack.com/api/search.messages'
USER_ENDPOINT = 'https://slack.com/api/users.info'
CHANNEL_ENDPOINT = 'https://slack.com/api/channels.info'


def lookup_username(userid):
    '''Looks up username from Slack API based on userid

    Expects:
        userid: a valid userid of form <@XXX>

    Returns:
        string of username in form @YYYYY
    '''
    userid = re.sub('[<@|>]', '', userid)
    payload = {'token': API_TOKEN, 'user': userid}
    results = requests.get(USER_ENDPOINT, params=payload).json()
    if results['ok']:
        return '@' + results['user']['name']
    return 'Unknown User'


def lookup_channel(channelid):
    '''Looks up channel name from Slack API based on channelid

    Expects:
        channelid: a valid userid of form <#XXX>

    Returns:
        string of username in form #YYYYY
    '''
    channelid = re.sub('[<#|>]', '', channelid)
    payload = {'token': API_TOKEN, 'channel': channelid}
    results = requests.get(CHANNEL_ENDPOINT, params=payload).json()
    if results['ok']:
        return '#' + results['channel']['name']
    return 'Unknown Channel'


def filter_by_date(messages, start, end):
    try:
        start = time.mktime(time.strptime(start, '%m-%d-%Y'))
        end = time.mktime(time.strptime(end, '%m-%d-%Y'))
    except:
        raise ValueError('Invalid date')
    return [m for m in messages if end > float(m['ts']) > start]


def format_text(text):
    '''Replaces all userids and channelids with plaintext names

    Expects:
        A string with 0 or more userids and channelids

    Returns:
        The same text with those ids replaced
    '''
    text = re.sub('<@\w*>', lambda x: lookup_username(x.group()), text)
    text = re.sub('<#\w*>', lambda x: lookup_channel(x.group()), text)
    return text


@click.command()
@click.option('--emoji', help=('Text name of the emoji to search, without '
              'surrounding :s'))
@click.option('--outfile', help=('Outputfile to write results to.'))
@click.option('--startdate', help=('Date to begin search. Must be in '
              'MM-DD-YYYY format.'), default='01-01-1999')
@click.option('--enddate', help=('Date to end search. Must be in '
              'MM-DD-YYYY format.'), default='12-12-2222')
def get_messages(emoji, outfile, startdate, enddate):
    if not emoji:
        raise ValueError('Please supply an emoji name to search by')
    print('Querying Slack api')
    matches = []
    paging = {'page': 0, 'pages': 99999}
    while paging['page'] < paging['pages']:
        payload = {'token': API_TOKEN,
                   'query': 'has::' + emoji + ':',
                   'page': paging['page'] + 1}
        response = requests.get('https://slack.com/api/search.messages',
                                params=payload).json()
        if not response['ok']:
            raise Exception('Query Failed!')
        matches += response['messages']['matches']
        paging = response['messages']['paging']
        print('Fetched results page {} of {}'.format(paging['page'],
                                                     paging['pages']))
    print('Filtering by date')
    matches = filter_by_date(matches, startdate, enddate)
    print('Formatting results')
    results = [{'ts': time.ctime(float(m['ts'])),
                'username': m['username'],
                'permalink': m['permalink'],
                'text': format_text(m['text'])}
               for m in matches]
    if outfile:
        print('Writing results to file')
        with open(outfile, 'w') as f:
            pprint(results, stream=f)
    else:
        pprint(results)

if __name__ == '__main__':
    get_messages()
