from src import session
from song_parser_lib import song_from_text_for_editing
from bs4 import BeautifulSoup

METADATA_START = '{metadata:}'
METADATA_END = '{:metadata}'
SONG_TITLE = '{song_title}: '
SONG_ARTIST = '{song_artist}: '

BLOCK_START = '{block:}'
BLOCK_END = '{:block}'
TITLE = '{title}: '
NOTE = '{note}: '
CHORDS_LINE = '{chords_line}: '
EMPTY_LINE = '{empty_line}'
CHORDS = '{C}|'
TEXT = '{T}|'


def from_url(url: str) -> (str, str, str):
    url = 'https://' + url
    
    resp = session.get(url)
    resp.raise_for_status()
    src = resp.text
    
    (artist, title, content) = parse(src)
    metadata = get_metadata(artist, title)
    content = metadata + format_content(content)
    yaml = song_from_text_for_editing(content)
    
    return yaml


def parse(src: str) -> (str, str, str):
    soup = BeautifulSoup(src, 'html.parser')
    artist_el = soup.find('span', attrs = { 'itemprop': 'byArtist' })
    title_el = soup.find('span', attrs = { 'itemprop': 'name' })
    
    title = title_el.text
    artist = artist_el.text
    
    content_el = soup.find('pre', attrs = { 'itemprop': 'chordsBlock' })
    content = content_el.text
    
    return (artist, title, content)


def format_content(content: str) -> str:
    content = content.replace(']:', '\n')
    content = content.replace('*/', '\n')
    
    s = '\n'
    in_block = False
    chords = ''
    for line in content.splitlines():
        if not s.endswith('\n'):
            s += '\n'

        if line.startswith('['): # title
            title = line[1:]
            if in_block:
                s += BLOCK_END + '\n'
                s += BLOCK_START + '\n'
            else:
                s += BLOCK_START + '\n'
                in_block = True

            s += TITLE + title + '\n'
        
        
        elif line.startswith('/*'): # note
            if not in_block:
                s += BLOCK_START + '\n'
                in_block = True
            
            note = line[2:]
            s += NOTE + note + '\n'
            
        
        elif not line.strip():
            if not in_block:
                s += BLOCK_START + '\n'
                in_block = True
            
            s += EMPTY_LINE + '\n'
            
            
        elif is_chords_line(line):
            if not in_block:
                s += BLOCK_START + '\n'
                in_block = True
            
            if chords != '':
                s += CHORDS_LINE + chords + '\n'
            
            chords = line
            
            
        else: # text
            if not in_block:
                s += BLOCK_START + '\n'
                in_block = True
            
            if chords != '':
                s += CHORDS + chords + '\n'
                chords = ''
            
            s += TEXT + line + '\n'
            
            
    if chords != '':
        s += CHORDS_LINE + chords + '\n'
    
    if in_block:
        s += BLOCK_END + '\n'
    
    return s


def get_metadata(artist: str, title: str) -> str:
    return f'''
{METADATA_START}
{SONG_TITLE}{title}
{SONG_ARTIST}{artist}
{METADATA_END}
'''


def is_chords_line(line: str) -> bool:
    allowed = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for word in line.split():
        word = word.strip()
        if not any(word.startswith(a) for a in allowed):
            return False
    
    return True


if __name__ == '__main__':
    with open('x.html', 'r') as f:
        src = f.read()
        
    (artist, title, content) = parse(src)
    metadata = get_metadata(artist, title)
    content = metadata + format_content(content)