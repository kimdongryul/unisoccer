def random_guess(record):
	x=random.randint(0,9)
	y=random.randint(0,9)

	while record.get_board()[x][y]<0:
		x=random.randint(0,9)
		y=random.randint(0,9)
	return (x,y)



def guess_next(record):
	last=record.get_last_log()
	if "guess" in last:
		if "x" in last["guess"]:
			return 0,0
		else:
			return 0,1
		x=last["guess"]["x"]
		# y=last["guess"]["y"]

		if x<9 and (record.get_board()[x+1][y]==constant.STATUS_EMPTY):
		    return (x+1,y)
		elif x>0 and (record.get_board()[x-1][y]==constant.STATUS_EMPTY):
		  return (x-1,y)
		elif y<9 and (record.get_board()[x][y+1]==constant.STATUS_EMPTY):
		  return (x,y+1)
		elif y>0 and (record.get_board()[x][y-1]==constant.STATUS_EMPTY):
		  return (x,y-1)



	else:
		return random_guess(record)



def validate_guess(record,position):
	x=position[0]
	y=position[1]

	if x>9 or x<0 or y>9 or y<0:
		return random_guess(record)
	elif record.get_board()[x][y]<0:
		return random_guess(record)
	else:
		return position


def guess(record):
	return guess_next(record)
	last=record.get_last_log()
	shot=(0,0)
	if "result" in last and last["result"]==constant.RESULT_HIT:
		shot=guess_next(record)
	else:
		shot=random_guess(record)

	return validate_guess(record,shot)