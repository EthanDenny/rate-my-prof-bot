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
    try:
        with urlopen(URL_PREFIX + query) as response:
            html_doc = response.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            script_text = soup.body.script.text
            json_index = script_text.find('window.__RELAY_STORE__ = ')
            script_text = script_text[json_index + 25:]
            script_text = script_text[:script_text.index('\n')-1]
            j = json.loads(script_text)

            firstName = get_recursively(j, 'firstName')[0]
            lastName = get_recursively(j, 'lastName')[0]
            avgRating = get_recursively(j, 'avgRating')[0]
            wouldTakeAgainPercent = round(get_recursively(j, 'wouldTakeAgainPercent')[0], 2)
            avgDifficulty = get_recursively(j, 'avgDifficulty')[0]

            return True, firstName, lastName, avgRating, wouldTakeAgainPercent, avgDifficulty
    except Exception:
        print(traceback.format_exc())
        return False, None, None, None, None, None
