def exp_to_level(exp: int):
    '''누적 경험치값을 레벨로 전환시켜줍니다. 음수 경험치는 레벨 0으로 처리됩니다.'''
    if exp < 0:
        return 0
    return int(((exp/5)+(1/4))**0.5 + 0.5)


def level_to_atk(level: int):
    '''레벨 -> 공격력'''
    return int(10*(level**1/2))


def level_to_def(level: int):
    '''레벨 -> 방어력'''
    return int(10*(level**1/2))


def level_to_maxhp(level: int):
    '''레벨 -> 최대 HP'''
    return int(25*(level**1/2))


def level_to_maxmp(level: int):
    '''레벨 -> 최대 MP'''
    return int(20*(level**1/2))


def exp_to_atk(exp: int):
    return level_to_atk(exp_to_level(exp))


def exp_to_def(exp: int):
    return level_to_def(exp_to_level(exp))


def exp_to_maxhp(exp: int):
    return level_to_maxhp(exp_to_level(exp))


def exp_to_maxmp(exp: int):
    return level_to_maxmp(exp_to_level(exp))
