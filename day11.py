#!/usr/bin/python

"""
--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to determine the fewest number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).

--- Part Two ---

How many steps away is the furthest he ever got from his starting position?

"""

# use a counter instead of a list
# of steps taken to improve speed
dir_idx = { "n" : 0,
			"s" : 1,
			"ne": 2,
			"nw": 3,
			"se": 4,
			"sw": 5 }

def opposite(a):
	if a == "ne":
		return "sw"
	elif a == "n":
		return "s"
	elif a == "nw":
		return "se"
	elif a == "se":
		return "nw"
	elif a == "s":
		return "n"
	elif a == "sw":
		return "ne"
	else:
		return None
		
def condense(a, b):
	if a == "ne" and b == "s":
		return "se"
	elif b == "ne" and a == "s":
		return "se"
	elif a == "ne" and b == "nw":
		return "n"
	elif b == "ne" and a == "nw":
		return "n"
	elif a == "se" and b == "sw":
		return "s"
	elif b == "se" and a == "sw":
		return "s"
	elif a == "nw" and b == "s":
		return "sw"
	elif b == "nw" and a == "s":
		return "sw"
	elif a == "se" and b == "n":
		return "ne"
	elif b == "se" and a == "n":
		return "ne"
	elif a == "sw" and b == "n":
		return "nw"
	elif b == "sw" and a == "n":
		return "nw"
	return None

def build_count(arr, seq):
	for step in seq:
		arr[dir_idx[step]] += 1
	return arr

def distance2(counter):
	last_sum = 0
	while last_sum != sum(counter):
		# Cancel N and S
		m = min(counter[0],counter[1])
		counter[0] -= m
		counter[1] -= m
		# Cancel NE and SW
		m = min(counter[2],counter[5])
		counter[2] -= m
		counter[5] -= m
		# Cancel NW and SE
		m = min(counter[3],counter[4])
		counter[3] -= m
		counter[4] -= m
		# Compress NE and S to SE
		m = min(counter[2],counter[1])
		counter[2] -= m
		counter[1] -= m
		counter[4] += m
		# Compress NE and NW to N
		m = min(counter[2],counter[3])
		counter[2] -= m
		counter[3] -= m
		counter[0] += m
		# Compress SE and SW to S
		m = min(counter[4],counter[5])
		counter[4] -= m
		counter[5] -= m
		counter[1] += m
		# Compress NW and S to SW
		m = min(counter[3],counter[1])
		counter[3] -= m
		counter[1] -= m
		counter[5] += m
		# Compress SE and N to NE
		m = min(counter[4],counter[0])
		counter[4] -= m
		counter[0] -= m
		counter[2] += m
		# Compress SW and N to NW
		m = min(counter[5],counter[0])
		counter[5] -= m
		counter[0] -= m
		counter[3] += m
		last_sum = sum(counter)
	return counter
	
def distance(seq):
	steps = []
	path = seq
	while True:
		changed = False
		while len(path) > 0:
			cur = path[0]
			op = opposite(cur)
			if op in path[1:]:
				path.remove(op)
				path.remove(cur)
				changed = True
			else:
				steps.append(cur)
				path = path[1:]
		while len(steps) > 0:
			cur = steps[0]
			for val in steps[1:]:
				cond = condense(cur, val)
				if cond != None:
					path.append(cond)
					steps.remove(val)
					cur = ''
					changed = True
					break
			if cur != '':
				path.append(cur)
			steps = steps[1:]
		if changed == False:
			break
	return path
				
if __name__ == "__main__":

	# Part 1 Solution
	
	with open("day11_input", "r") as infile:
		path = infile.read().strip()
	#path = "se,sw,se,sw,sw"
	path = path.split(",")
	print len(distance(path))
	
	# Part 2 Solution

	with open("day11_input", "r") as infile:
		path = infile.read().strip()
	path = path.split(",")	
	dirs = [0] * 6
	most = 0
	for step in path:
		dirs = build_count(dirs, [step])
		most = max(most,sum(distance2(dirs)))
	print most
	
	"""
	!!! Too Slow !!!
	"""
	
	#most = 0
	#t_path = []
	#for i in range(len(path)):
	#	t_path.append(path[i])
	#	t_path = distance(t_path)
	#	most = max(most, len(t_path))
	#print most
