

def melt(it: list) -> str:
    """String together objects using their specific __str__ method
    :param it: List of objects implementing __str__
    """

    return "".join(map(str, it))

