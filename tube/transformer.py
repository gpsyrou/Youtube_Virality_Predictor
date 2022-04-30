"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Purpose: A collection of functions/methods used to support the metadata
retrieval process. Support the main collector.py script to perform data
transformation operations.
"""

import datetime
from typing import List
from bs4 import BeautifulSoup
import urllib.request

global chars
chars = ['"', '\'']


def transform_pt_format(pt: str, target_format: str = 'minutes') -> float:
    """ Method to transform time duration of format ISO_8601 to a numeric
    representation.

    Arguments:
    ---------
        pt:
            The duration time in ISO_8601 format
        target_format:
                The target transforation format: 'seconds', 'minutes', 'hours'
    """
    if pt[0:2] == 'PT':
        pt = pt.replace('PT', '')
        m_divider = pt.split('M')
        minutes = int(m_divider[0])
        seconds = int(m_divider[1].split('S')[0])

        if target_format == 'seconds':
            return (60 * minutes) + seconds
        elif target_format == 'minutes':
            return minutes + (seconds/60)
        elif target_format == 'hours':
            return ((minutes + (seconds/60)) / 60)
    else:
        raise ValueError('The input string is not in ISO_8601 format..!')


def get_current_datetime(as_type='str') -> str:
    time_now = datetime.datetime.now()
    if as_type == 'str':
        return str(time_now).split('.')[0]
    elif as_type == 'datetime':
        return time_now
    else:
        raise ValueError('The specified date time is not valid..!')


def remove_chars(s: str, chars: List[str] = chars) -> str:
    """ Removes the characters contained in chars from string s
    """
    for char in chars:
        if char in s:
            s = s.replace(char, '')
    return s


def url_to_bs4(url: str) -> BeautifulSoup:
    """
    Given a website link (URL), retrieve the corresponding website in an
    html format.
    Parameters
    ----------
    video_url : str
        URL of the webpage that will be transformed to a BeautifulSoup obj.
    """
    # print('Attempting to retrieve HTML object for {0}'.format(video_url))
    request = urllib.request.urlopen(url)
    if request.getcode() != 200:
        raise Exception('Can not communicate with the client')
    else:
        response = request.read()
        response_html = BeautifulSoup(response, 'html.parser')
        return response_html
