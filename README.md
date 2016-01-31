# Slack Emoji Search

A commandline utility to search across Slack for messages that were reacted to with a specific emoji.

## Installation

Ensure Python, [pip](https://pip.pypa.io/en/stable/installing/), [virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) are set up. If you've run the [laptop script](https://github.com/18F/laptop), you're all good.

Assuming you are using Python 2.7.9+ or 3.4+ the following steps should work:

    $ python -m ensurepip
    $ pip install virtualenv virtualenvwrapper

Clone the repo, set up a python virtualenvironment, and install requirements:

    $ git clone https://github.com/18F/emoji_search.git ~/emoji_search
    $ cd ~/emoji_search
    $ mkvirtualenv emoji_search
    $ pip install -r requirements.txt

### Optionally make script executable outside of virtualenv

If you always plan on running the script with the virtualenv activated, you can skip this step.

Activate virtualenv if necessary:

    $ workon emoji_search && cd ~/emoji_search

Make script executable:

    $ echo '#!'`which python`|cat - emoji_search.py > /tmp/out && mv /tmp/out emoji_search.py
    $ chmod 755 emoji_search.py

## Usage

You will need a Slack API key. You can get this from the [Slack website](https://api.slack.com/web). The script expects the token to be in a file in the same directory, which will not be checked in to Github. To create it, run the following from the ~/emoji_search directory, subbing in your token and making sure to keep the quotes:

    echo "API_TOKEN = '<MY-API-TOKEN>'" > api_token.py

If you did not make the script executable in the optional step above use `python ~/emoji_search/emoji_search.py` in place of `~/emoji_search/emoji_search.py` below:

To query for messages reacted to with the :evergreen_tree: emoji between Nov 2, 2015 and Oct 31, 2015 and write the output to a file called evergreen.txt in the current directory, run:

    ~/emoji_search/emoji_search.py --emoji evergreen_tree \
                                   --startdate 10-31-2015 \
                                   --enddate 11-02-2015 \
                                   --outfile evergreen.txt
All flags are optional except for --emoji. If no destination file is provided, results will be written to the terminal.

## Public Domain
18F's work on this project is in the worldwide [public domain](LICENSE.md).

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
