import urllib.request
import requests
from bs4 import BeautifulSoup


def get_update(url):
    """
    Attempt to reach the pheonixminer webserver. Returns a requests-like object with an additional
    text_lines attribute
    """
    resp = requests.get(url)

    # Check for HTTP code, error out if necessary
    # TODO: Handle discrete cases
    if resp.status_code == 200:
        # Convert to lines of text
        clean_text = BeautifulSoup(resp.text, "html.parser").text
        resp.text_lines = clean_text.splitlines()

        # Remove lines that are empty or have only whitespace
        empties = ('', ' ', '\t', '\n', '&nbsp;')
        resp.text_lines = [line for line in resp.text_lines if line not in empties]
    else:
        print(f"Warning: Got status code {resp.status_code}")
    return resp


def status_line(url):
    status = {'error': 0,
              'text': ''}
    resp = get_update(url)
    if resp.status_code == 200:
        status['text'] = f'{resp.text_lines[-1][-11:]}'
    else:
        status['error'] = 1
        status['text'] = f"Error: Code {resp.status_code}"

    return status
