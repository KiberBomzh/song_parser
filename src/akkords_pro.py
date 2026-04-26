import requests


st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

def clean_tags(text: str) -> str:
    while text.find('<') != -1 and text.find('>') != -1:
        start = text.find('<')
        end = text.find('>')

        text = text[:start] + text[end + 1:]

    return text


def from_url(url: str) -> str:
    url = 'https://' + url

    resp = requests.get(url, headers)
    resp.raise_for_status()
    content = resp.text

    start = content.find('<p class="chords">')
    end = content[start:].find('</p>') + start
    text = content[start:end]

    text = clean_tags(text).strip()
    return text
