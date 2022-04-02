

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
        seconds = int(m_divider[0].split('S')[0])
    
        if target_format=='seconds':
            return (60 * minutes) + seconds
        elif target_format=='minutes':
            return minutes + (seconds/60)
        elif target_format=='hours':
            return ((minutes + (seconds/60)) / 60)
    else:
        raise ValueError('The input string is not in ISO_8601 format..!')
