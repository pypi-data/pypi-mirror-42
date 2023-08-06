"""merge dictionaries."""
#http://stackoverflow.com/a/12735459


def merge(dict_1, dict_2, priority='left'):
    """merge the dictionaries, with priority."""
    dict_1_copy = dict_1.copy()
    dict_2_copy = dict_2.copy()
    if priority == 'left':
        return dict(dict_2_copy, **dict_1_copy)
    if priority == 'right':
        return dict(dict_1_copy, **dict_2_copy)
    if priority == 'append':
        for key in dict_2_copy:
            if not key in dict_1_copy:
                dict_1_copy[key] = dict_2_copy[key]
            else:
                if not isinstance(dict_1_copy[key], list):
                    dict_1_copy[key] = [dict_1_copy[key]]
                if not isinstance(dict_2_copy[key], list):
                    dict_2_copy[key] = [dict_2_copy[key]]
                dict_1_copy[key].extend(dict_2_copy[key])
        return dict_1_copy
    raise ValueError("priority needs to be left, right or append")


def unify(seq, unlist_single=True):
    """unify."""
    if not isinstance(seq, list):
        return seq

    res = []
    for i in seq:
        if not i in res:
            res.append(i)
    if unlist_single and len(res) == 1:
        return res[0]
    return res
