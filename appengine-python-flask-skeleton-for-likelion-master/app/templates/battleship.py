def random_guess(record):
    x = random.randint(0, 9)
    y = random.randint(0, 9)

    while record.get_board()[x][y] < 0:
        x = random.randint(0, 9)
        y = random.randint(0, 9)

    return (x, y)

def guess_next(record):
    last = record.get_last_log()
    if "guess" in last:
        x = last["guess"]["x"]
        y = last["guess"]["y"]
        return (x + 1, y)
    else:
        return random_guess(record)

def validate_guess(record, position):
    x = position[0]
    y = position[1]

    if x > 9 or x < 0 or y > 9 or y < 0:
        return random_guess(record)
    elif record.get_board()[x][y] < 0:
        return random_guess(record)
    else:
        return position

def guess(record):
    last = record.get_last_log()
    shot = (0, 0)
    if "result" in last and last["result"] == constant.RESULT_HIT:
        shot = guess_next(record)
    else:
        shot = random_guess(record)

    return validate_guess(record, shot)