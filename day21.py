#!/usr/bin/python

"""
--- Day 21: Fractal Art ---

You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.). The program always begins with this pattern:

.#.
..#
###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

Then, the program repeats the following process:

    If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into a 3x3 square by following the corresponding enhancement rule.
    Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square into a 4x4 square by following the corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules. The artist explains that sometimes, one must rotate or flip the input pattern to find a match. (Never rotate or flip the output pattern, though.) Each pattern is written concisely: rows are listed as single units, ordered top-down, and separated by slashes. For example, the following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following patterns match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square; the square matches the second rule, which produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and rotation to line up with the rule. The output for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

--- Part Two ---

How many pixels stay on after 18 iterations?

"""

grid = [] # main map
t_grid = [] # swap space

# mirror input
def flip(pattern):
	out = []
	for row in pattern:
		row.reverse()
		out.append(row)
	return out
	
# rotate a matrix 
def rotate(pattern):
	out = []
	for i in range(len(pattern)):
		out.append([None] * len(pattern[0]))
	for i,row in enumerate(pattern):
		for j, c in enumerate(row):
			out[j][i] = c
	return out
	
def str_to_grid(string):
	return [ list(x) for x in string.split("/") ]
	
def grid_to_str(grid):
	out = ''
	for i,row in enumerate(grid):
		out += ''.join(row)
		if i < len(grid)-1:
			out += "/"
	return out
	
# return a sub-section at location x,y with size w*w
def grid_sample(x, y, w):
	out = []
	for i in range(w):
		out.append(grid[y+i][x:x+w])
	return out

def gen_rules(inpt, outpt):
	transforms = set()
	transforms.add(inpt)
	inpt = str_to_grid(inpt)
	transforms.add(grid_to_str(flip(inpt)))
	for i in range(3):
		inpt = rotate(inpt)
		transforms.add(grid_to_str(inpt))
		transforms.add(grid_to_str(flip(inpt)))
	inpt = flip(inpt)
	transforms.add(grid_to_str(inpt))
	return (transforms, outpt)
	
# number of "#" in the grid
def count_on():
	count = 0
	for row in grid:
		count += row.count("#")
	return count
		
def print_grid():
	for row in grid:
		print ''.join(row)


# wipe the temporary grid, enlarge for next gen
def t_grid_init(w):
	global t_grid
	t_grid = []
	next_len = len(grid) / w 
	for i in range(next_len * (w+1)):
		t_grid.append( [ None ] * next_len * (w+1) )
		
def t_grid_pop(x,y,w,subgrid):
	for j,row in enumerate(subgrid):
		for k,char in enumerate(row):
			t_grid[y*(w+1)+j][x*(w+1)+k] = char
		
if __name__ == "__main__":

	rules = []

	with open("day21_input", "r") as infile:
		for line in infile.readlines():
			inpt, outpt = line.split(" => ")
			rules.append(gen_rules(inpt.strip(), outpt.strip()))
	
	# Default Pattern
	grid = []
	grid.append(list('.#.'))
	grid.append(list('..#'))
	grid.append(list('###'))
	
	# Part 1 and 2 Solution

	max_gens = 18
	
	for _ in range(max_gens):
		if len(grid) % 2 == 0: # 2x2 squares
			w = 2
		elif len(grid) % 3 == 0: # 3x3 squares
			w = 3
		else:
			print "Unexpected grid size."
			exit()
		t_grid_init(w) # fill in next generation
		for i in range(0,len(grid),w):
			for j in range(0,len(grid),w):
				samp = grid_to_str(grid_sample(i,j,w))
				o = None
				for rule in rules:
					if samp in rule[0]:
						o = rule[1]
				if o == None:
					print "Unable to match for input: ", samp
					print rules
					exit()
				else:
					t_grid_pop(i/w,j/w,w,str_to_grid(o))
		grid = t_grid[:] # copy buffer
		if _ == 4: # Part 1
			print count_on()
	print count_on()
				
		
