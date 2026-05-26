import argparse

from src.parsers import akkords_pro, amdm_ru
from song_parser_lib import can_save, save


parser = argparse.ArgumentParser(description = "Cli tool for scraping songs.")
parser.add_argument('url', help = "Song's url")
parser.add_argument('-s', '--save', action = 'store_true', help = "Save song in library")


def main():
    args = parser.parse_args()
    if args.save and not can_save():
        print("Cannot save songs on android!")
        return 1

    url: str = args.url
    if url.startswith('https://'):
        url = url[len('https://'):]
    elif url.startswith('http://'):
        url = url[len('http://'):]


    if url.startswith('akkords.pro'):
        yaml = akkords_pro.from_url(url)
    elif url.startswith('amdm.ru'):
        yaml = amdm_ru.from_url(url)
    else:
        print("Unknown url!")
        return 1


    if args.save:
        save(yaml)
    else:
    	print(yaml, flush = True)


if __name__ == '__main__':
    main()
