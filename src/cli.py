from song_parser_lib import song_from_text_for_editing


def main():
    yaml = song_from_text_for_editing(text_example)
    print(yaml)


if __name__ == '__main__':
    main()

text_example: str = '''
{metadata:}
{song_title}: Как на войне
{song_artist}: Агата Кристи
{song_key}: Am
{song_capo}: 
{song_autoscroll_speed}: 1950
{:metadata}


{block:}
{title}: Вступление
{note}: х8
{chords_line}: Am G C E 
{:block}


{block:}
{title}: Куплет
{C}| Am        G        C         E     Am
{R}|
{T}|Ляг, отдохни, и послушай, что я скажу:

{C}|      G         C      E   Am
{R}|
{T}|Я терпел, но сегодня я ухожу.

{C}|      G        C       E     Am  
{R}|
{T}|Я сказал: успокойся и рот закрой.

{C}|        G         C      E       Am  
{R}|
{T}|Вот и всё, до свидания, чёрт с тобой.
{:block}


{block:}
{title}: Припев
{C}|        G             C           E            Am
{R}|
{T}|Я на тебе, как на войне, а на войне, как на тебе.

{C}|        G            C             E           Am 
{R}|
{T}|Но я устал, окончен бой, беру портвейн, иду домой.

{C}|         G           C           E          Am
{R}|
{T}|Окончен бой, зачах огонь и не осталось ничего.

{C}|        G             C        E      Am
{R}|
{T}|А мы живем а нам с тобою повезло на зло.
{:block}


{block:}
{title}: Проигрыш
{note}: х2
{chords_line}: Am G C E 
{:block}


{block:}
{title}: Куплет 2
{C}| Am        G         C        E  Am 
{R}|
{T}|Боль, это боль, как её ты не назови.

{C}|       G              C          E     Am 
{R}|
{T}|Это страх, там где страх, места нет любви.

{C}|      G        C       E      Am 
{R}|
{T}|Я сказал: успокойся и рот закрой.

{C}|        G         C      E        Am 
{R}|
{T}|Вот и всё, до свидания, чёрт с тобой.
{:block}


{block:}
{title}: Припев
{C}|        G             C           E            Am
{R}|
{T}|Я на тебе, как на войне, а на войне, как на тебе.

{C}|        G            C             E           Am 
{R}|
{T}|Но я устал, окончен бой, беру портвейн, иду домой.

{C}|         G           C           E          Am
{R}|
{T}|Окончен бой, зачах огонь и не осталось ничего.

{C}|        G             C        E      Am
{R}|
{T}|А мы живем а нам с тобою повезло на зло.
{:block}


{block:}
{title}: Проигрыш
{note}: х2
{chords_line}: Am G C E 
{:block}
'''
