from src import session
from song_parser_lib import song_from_text
from bs4 import BeautifulSoup


def from_url(url: str) -> str:
    url = 'https://' + url

    resp = session.get(url)
    resp.raise_for_status()
    src = resp.text

    (artist, title, content) = parse(src)
    yaml = song_from_text(content, artist, title)
    return yaml


def parse(src: str) -> (str, str, str):
    soup = BeautifulSoup(src, 'html.parser')
    
    content_el = soup.find('p', class_ = 'chords')
    content = content_el.text.replace('—', '-')

    
    title_text = soup.title.text
    
    title_end = title_text.find(':')
    if title_end == -1:
        title = 'title'
    else:
        title = title_text[:title_end].strip()

    artist_start = title_text.find('•')
    if artist_start == -1:
        artist = 'artist'
    else:
        artist = title_text[artist_start + 1:].strip()


    return (artist, title, content)