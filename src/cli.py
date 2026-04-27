from sys import argv

from src.parsers import akkords_pro, amdm_ru


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
        yaml = akkords_pro.from_url(url)
    elif url.startswith('amdm.ru'):
        yaml = amdm_ru.from_url(url)
    else:
        print("Unknown url!")
        return 1

    print(yaml, flush = True)


if __name__ == '__main__':
    main()
