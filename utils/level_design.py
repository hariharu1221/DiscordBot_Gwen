def exp_to_level(exp: int):
    if exp < 0:
        return 0
    return int(((exp/5)+(1/4))**0.5 + 0.5)
