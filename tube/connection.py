
import pandas as pd
import urllib
import time
import re
from dateutil.parser import isoparse
from datetime import datetime
from typing import List, Mapping
from bs4 import (BeautifulSoup,
                 element)




def url_to_bs4(target_url: str) -> BeautifulSoup:
    """
    Given a website link (URL), retrieve the corresponding website in an html
    format.
    Parameters
    ----------
    target_url : str
        URL of the webpage that will be transformed to a BeautifulSoup object.
    """
    #print('Attempting to retrieve HTML object for {0}'.format(target_url))
    request = urllib.request.urlopen(target_url)
    if request.getcode() != 200:
        raise Exception('Can not communicate with the client')        
    else:
        response = request.read()
        response_html = BeautifulSoup(response, 'html.parser')
        return response_html






test = url_to_bs4(target_url='https://youtu.be/X6DIc_iQd9I')




test.find_all('div')





