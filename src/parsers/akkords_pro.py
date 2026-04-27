from src import session


def clean_tags(text: str) -> str:
    while text.find('<') != -1 and text.find('>') != -1:
        start = text.find('<')
        end = text.find('>')

        text = text[:start] + text[end + 1:]

    return text


def from_url(url: str) -> str:
    url = 'https://' + url

    resp = session.get(url)
    resp.raise_for_status()
    content = resp.text

    start = content.find('<p class="chords">')
    end = content[start:].find('</p>') + start
    text = content[start:end]

    text = clean_tags(text).strip()
    return text
