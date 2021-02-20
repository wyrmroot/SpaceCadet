import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup


load_dotenv()
MONITOR_URL = os.getenv('SERVER_URL')


def get_update():
    """
    Attempt to reach the pheonixminer webserver. Returns a dict with some useful info. If HTML code is not 200,
    returns an error message.
    """
    # Get HTML data
    resp = requests.get(MONITOR_URL)

    # Prepare our final returned object (dict)
    # TODO: Convert numerics into int from str
    summary = {'html_code': resp.status_code,
               'status_text': '',
               'full_text': '',
               'hash rate': '',
               'time': '',
               'power': '',
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
        summary['hash rate'] = resp.text_lines[-2].split()[-2]
        summary['power'] = resp.text_lines[-7].split()[-2]
        timestamp = [line for line in resp.text_lines if line[0] == "*"][-1]
        # Looks like ['***', '63:20', '***', '2/19', '10:16', '**************************************']
        summary['uptime'] = timestamp.split()[1]
        summary['time'] = timestamp.split()[4]

    else:
        print(f"Warning: Got status code {summary['html_code']}")

    return summary


def status_line():
    activity = {'error': 0,
              'text': ''}
    summary = get_update()
    if summary['html_code'] == 200:
        activity['text'] = f"{summary['hash rate']} MH/s at {summary['time']}"
    else:
        activity['error'] = 1
        activity['text'] = f"Error: Code {summary['html_code']}"

    return activity


def get_profit():
    """
    Use a website based mining calculator to figure out daily profits
    """
    summary = get_update()
    hr = summary['hash rate']  # Hash rate (MH/s)
    p = summary['power']  # Power (W)
    fee = '1.4'  # Pool fee (%)
    pcost = '0.16'  # Power cost ($/kWh)


    url = f"https://whattomine.com/coins/151-eth-ethash?hr={hr}&p={p}&fee={fee}&cost={pcost}&hcost=0.0&commit=Calculate"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Got code {resp.status_code}, aborting")
    soup = BeautifulSoup(resp.content, "html.parser")
    eth = soup.findAll('span')[3].text.split('\n')[2]
    empties = ('', ' ', '\t', '\n', '&nbsp;')
    row = [line for line in soup.find_all("tr")[2].text.split('\n') if line not in empties]
    day_profit = row[-1]
    response = f"Current profits: **{day_profit} / day** (ETH = {eth}).\n" \
               f"Based on {hr}MH/s, {p}W at ${pcost}/kWh, fee {fee}%."
    return response





