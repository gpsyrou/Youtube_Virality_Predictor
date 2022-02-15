

def is_title_full_capital(video_title: str, threshold: float = 0.7) -> bool:
    """ Identifies if a given video title consist only by capital letters.
    The function compares if number of capital letters >= a give threshold
    as defined by the @threshold parameter.
    """
    is_full_capital = False

    only_letters_title = [l for l in video_title if l.isalpha()]
    capital_letters = [l for l in only_letters_title if l.isupper()]

    if (len(capital_letters) / len(list(only_letters_title))) >= threshold:
        is_full_capital = True

    return is_full_capital
