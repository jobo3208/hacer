#!/usr/bin/env python3

"""Interactive quiz on Spanish verb conjugations"""

import argparse
import bs4
import os
import random
import shelve
import shutil
import urllib.request


ALL_NUMBERS = ['singular', 'plural']
ALL_PERSONS = ['first', 'second', 'third']
ALL_TENSES  = ['present', 'preterit', 'imperfect', 'conditional', 'future']

PRONOUN_HINTS = {
    'singular': {
        'first': 'yo',
        'second': 'tú',
        'third': 'él/ella/usted',
    },
    'plural': {
        'first': 'nosotros',
        'second': 'ustedes',
        'third': 'ellos/ellas'
    }
}


def _parse_args():
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument(
        'action',
        choices=['update', 'play'],
        nargs='?',
        help="if no action is specified, update, then play"
    )
    return arg_parser.parse_args()


def _initialize_config():
    """Create a barebones config if necessary."""
    for config_file in ['numbers', 'persons', 'tenses', 'verbs']:
        if not os.path.exists(os.path.join('config', config_file)):
            print("creating {} file from default...".format(config_file))
            shutil.copy(
                os.path.join('config', config_file + '.default'),
                os.path.join('config', config_file)
            )


def _load_config():
    numbers = open(os.path.join('config', 'numbers')).read().splitlines()
    persons = open(os.path.join('config', 'persons')).read().splitlines()
    tenses = open(os.path.join('config', 'tenses')).read().splitlines()
    verbs = open(os.path.join('config', 'verbs')).read().splitlines()
    return numbers, persons, tenses, verbs


def _fetch_conjugations(verb):
    """Fetch all conjugations of verb and return as a dictionary."""
    url = 'http://www.spanishdict.com/conjugate/' + verb
    with urllib.request.urlopen(url) as f:
        soup = bs4.BeautifulSoup(f)
    all_words = [c.strip() for c in soup.table.strings if c.strip()][5:]
    assert len(all_words) == 36

    # Delete vosotros conjugations
    del all_words[24:30]

    # 2nd person plural = 3rd person plural
    all_words += all_words[24:]

    # Populate data dictionary
    all_words = iter(all_words)
    data = {}
    for number in ALL_NUMBERS:
        data[number] = {}
        for person in ALL_PERSONS:
            next(all_words)  # skip pronouns
            data[number][person] = {}
            for tense in ALL_TENSES:
                data[number][person][tense] = next(all_words)

    return data


def update():
    """Fetch conjugations for missing verbs from web."""
    _, _, _, verbs = _load_config()
    if not os.path.exists('data'):
        os.mkdir('data')
    data = shelve.open(os.path.join('data', 'conjugations'))
    for verb in verbs:
        if verb not in data:
            print("fetching conjugations for:", verb)
            data[verb] = _fetch_conjugations(verb)
    data.close()


def play():
    """Interactively quiz user on random conjugations."""
    numbers, persons, tenses, verbs = _load_config()
    data = shelve.open(os.path.join('data', 'conjugations'))
    print("(enter 'q' to quit)\n")
    while True:
        number = random.choice(numbers)
        person = random.choice(persons)
        tense = random.choice(tenses)
        verb = random.choice(verbs)

        print("{} '{}', {}".format(
            PRONOUN_HINTS[number][person], verb, tense
        ))

        answer = data[verb][number][person][tense]
        response = input("? ")
        if answer == response:
            print("correct!\n")
        elif response in 'Qq':
            break
        else:
            print("sorry, it's '{}'\n".format(answer))

    data.close()


if __name__ == '__main__':
    args = _parse_args()
    _initialize_config()
    if not args.action or args.action == 'update':
        update()
    if not args.action or args.action == 'play':
        play()
