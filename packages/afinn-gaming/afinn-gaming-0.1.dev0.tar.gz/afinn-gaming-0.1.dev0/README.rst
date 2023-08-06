afinn
=====

AFINN sentiment analysis in Python: Wordlist-based approach for sentiment analysis.

Examples
--------

    >>> from afinn import Afinn
    >>> afinn = Afinn()
    >>> afinn.score('This is utterly excellent!')
    3.0

For Gaming:
    >>> from afinn import Afinn
    >>> afinn = Afinn(language='gaming')
    >>> afinn.score('This is utterly excellent!')
    3.0

With emoticons:

    >>> afinn = Afinn(emoticons=True)
    >>> afinn.score('I saw that yesterday :)')
    2.0
