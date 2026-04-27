from src import session
from song_parser_lib import song_from_text


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
    
    with open('x.html', 'w') as f:
        f.write(content)

    start = content.find('<p class="chords">')
    end = content[start:].find('</p>') + start
    text = content[start:end]

    text = clean_tags(text).strip()
    yaml = song_from_text(text,
        artist = 'artist',
        title = 'title',
    )
    return yaml
