from sys import argv
from song_parser_lib import song_from_text

from . import akkords_pro


def main():
    if len(argv) == 1:
        print("You need to use an url as first argument!")
        return 1

    url: str = argv[1]
    if url.startswith('https://'):
        url = url[len('https://'):]
    elif url.startswith('http://'):
        url = url[len('http://'):]

    if url.startswith('akkords.pro'):
        text = akkords_pro.from_url(url)
    else:
        print("Unknown url!")
        return 1

    yaml = song_from_text(
        text,
        artist = 'example',
        title = 'something',
    )
    print(yaml, flush = True)


if __name__ == '__main__':
    main()
