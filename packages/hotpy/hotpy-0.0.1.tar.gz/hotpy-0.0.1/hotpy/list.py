def remove_duplicates(lista):
    """
    Remove duplicados de uma lista
    :param lista:
    :return:
    """
    return list(set(lista))


def flat(l):
    """
    Aplaina uma lista de lista
        ex: [[1,2,3],[4,5,6],[7,8,9]] = [1,2,3,4,5,6,7,8,9]
    :param l: lista de lista
    :return: lista
    """
    return [item for sublist in l for item in sublist]
