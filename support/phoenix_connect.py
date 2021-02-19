import urllib.request
import requests
from bs4 import BeautifulSoup


def get_update(url):
    """
    Attempt to reach the pheonixminer webserver. Returns a dict with some useful info. If HTML code is not 200,
    returns an error message.
    """
    # Get HTML data
    resp = requests.get(url)

    # Prepare our final returned object (dict)
    summary = {'html_code': resp.status_code,
               'status_text': '',
               'full_text': '',
               'hash rate': '',
               'time': '',
               'uptime': ''}

    # Check for HTTP code, error out if necessary
    # TODO: Handle discrete cases
    if summary['html_code'] == 200:
        # Convert to lines of text
        clean_text = BeautifulSoup(resp.text, "html.parser").text
        resp.text_lines = clean_text.splitlines()

        # Remove lines that are empty or have only whitespace
        empties = ('', ' ', '\t', '\n', '&nbsp;')
        resp.text_lines = [line for line in resp.text_lines if line not in empties]

        # Extract insights
        # TODO: Replace these with some more elegant regex
        summary['hash rate'] = resp.text_lines[-1][-11:]
        timestamp = [line for line in resp.text_lines if line[0] == "*"][-1]
        # Looks like ['***', '63:20', '***', '2/19', '10:16', '**************************************']
        summary['uptime'] = timestamp.split()[1]
        summary['time'] = timestamp.split()[4]

    else:
        print(f"Warning: Got status code {summary['html_code']}")

    return summary


def status_line(url):
    activity = {'error': 0,
              'text': ''}
    summary = get_update(url)
    if summary['html_code'] == 200:
        activity['text'] = f"{summary['hash rate']} at {summary['time']}"
    else:
        activity['error'] = 1
        activity['text'] = f"Error: Code {summary['html_code']}"

    return activity
