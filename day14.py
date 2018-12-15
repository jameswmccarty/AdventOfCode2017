#!/usr/bin/python

"""
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit and watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system resources that are needed elsewhere, and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128 bits which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row. For example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#   
....#.#.   
#.#.##.#   
.##.#...   
##..#..#   
.#...#..   
##.#.##.-->
|      |   
V      V   

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

Your puzzle input is jzgqcdpd.

--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own isolated regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4   
....5.6.   
7.8.55.9   
.88.5...   
88..5..8   
.8...8..   
88.8.88.-->
|      |   
V      V   

Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are present.

How many regions are present given your key string?

"""

grid = []

class Block:

	def __init__(self, x, y):
		self.visited = False
		self.x = x
		self.y = y
	
	def explore(self, seen):
		if self.visited == True:
			return seen
		seen.add(self)
		self.visited = True
		if self.x > 0:
			if grid[self.y][self.x - 1] != None and not grid[self.y][self.x - 1].visited:
				seen = seen.union(grid[self.y][self.x - 1].explore(seen))
		if self.x < len(grid[self.y])-1:
			if grid[self.y][self.x + 1] != None and not grid[self.y][self.x + 1].visited:
				seen = seen.union(grid[self.y][self.x + 1].explore(seen))
		if self.y > 0:
			if grid[self.y-1][self.x] != None and not grid[self.y-1][self.x].visited:
				seen = seen.union(grid[self.y-1][self.x].explore(seen))
		if self.y < len(grid)-1:
			if grid[self.y+1][self.x] != None and not grid[self.y+1][self.x].visited:
				seen = seen.union(grid[self.y+1][self.x].explore(seen))
		return seen		

hex_bits = { 	'0' : 0,
				'1' : 1,
				'2' : 1,
				'3' : 2,
				'4' : 1,
				'5' : 2,
				'6' : 2,
				'7' : 3,
				'8' : 1,
				'9' : 2,
				'a' : 2,
				'b' : 3,
				'c' : 2,
				'd' : 3,
				'e' : 3,
				'f' : 4}

hex_val = { 	'0' : 0,
				'1' : 1,
				'2' : 2,
				'3' : 3,
				'4' : 4,
				'5' : 5,
				'6' : 6,
				'7' : 7,
				'8' : 8,
				'9' : 9,
				'a' : 10,
				'b' : 11,
				'c' : 12,
				'd' : 13,
				'e' : 14,
				'f' : 15}
				
def knot_hash(val):
	list = []
	for i in range(256):
		list.append(i)
	pos = 0
	skip = 0	
	lengths = []
	input = val
	suffix = [17, 31, 73, 47, 23]
	for char in input:
		lengths.append(ord(char))
	for val in suffix:
		lengths.append(val)	
	for round in range(64):
		for length in lengths:
			sublist = []
			for i in range(length):
				sublist.append(list[(pos+i)%len(list)])
			sublist.reverse()
			for i in range(length):
				list[(pos+i)%len(list)] = sublist[i]		
			pos += length + skip
			pos %= len(list)
			skip += 1
	hash = ''
	for i in range(16):
		char = 0
		for z in range(16):
			char ^= list[i*16 + z]
		hash += '%02x' % char	
	return hash
	
def hash_gen(val):
	tot = 0
	for i in range(128):
		tot += hash_sum(val + "-" + str(i))
	return tot
	
def hash_sum(val):
	return sum(hex_bits[x] for x in knot_hash(val))
	
def print_grid():
	for row in grid:
		line = ''
		for item in row:
			if item != None:
				line += "#"
			else:
				line += "."
		print line

def populate_grid(val):
	for i in range(128):
		row = [None] * 128
		hash = knot_hash(val + "-" + str(i))
		for j in range(len(hash)):
			for k in range(3,-1,-1):
				if (1<<k) & hex_val[hash[j]] != 0:
					row[j*4 + (3-k)] = Block(j*4 + (3-k),i)
		grid.append(row)

if __name__ == "__main__":

	# Part 1 Solution
	print hash_gen("jzgqcdpd")
	#print hash_gen("flqrgnkx")
	
	# Part 2 Solution
	blocks = []
	populate_grid("jzgqcdpd")
	#print_grid()
	for i in range(128):
		for j in range(128):
			if grid[j][i] != None and not grid[j][i].visited:
				blocks.append(grid[j][i].explore(set()))
	print len(blocks)
