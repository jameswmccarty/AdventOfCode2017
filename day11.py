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
	
	most = 0
	t_path = []
	for i in range(len(path)):
		t_path.append(path[i])
		t_path = distance(t_path)
		most = max(most, len(t_path))
	print most
