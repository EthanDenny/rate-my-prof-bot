from bs4 import BeautifulSoup
from urllib.request import urlopen

import json
import traceback


URL_PREFIX = 'https://www.ratemyprofessors.com/search/teachers?sid=1441&query='


# Taken from https://stackoverflow.com/a/20254842
def get_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.items():

        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found


def parse_query(query):
    with urlopen(URL_PREFIX + query) as response:
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        script_text = soup.body.script.text
        json_index = script_text.index('window.__RELAY_STORE__')
        script_text = script_text[json_index:]
        script_text = script_text[script_text.index('{'):script_text.index(';')]
        j = json.loads(script_text)

        firstName = get_recursively(j, 'firstName')
        lastName = get_recursively(j, 'lastName')
        avgRating = get_recursively(j, 'avgRating')
        wouldTakeAgainPercent = get_recursively(j, 'wouldTakeAgainPercent')
        avgDifficulty = get_recursively(j, 'avgDifficulty')

        return firstName, lastName, avgRating, wouldTakeAgainPercent, avgDifficulty
