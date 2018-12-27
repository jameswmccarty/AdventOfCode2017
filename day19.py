#!/usr/bin/python

"""

--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take, starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only turn left or right when there's no other option. In addition, someone has left letters on the line; these also don't change its direction, but it can use them to keep track of where it's been. For example:

     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 

Given this diagram, the packet needs to take the following path:

    Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to the first +.
    Travel right, up, and right, passing through B in the process.
    Continue down (collecting C), right, and up (collecting D).
    Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it would see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line wrapping.)

--- Part Two ---

The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |          
     |  +--+    
     A  |  C    
 F---|--|-E---+ 
     |  |  |  D 
     +B-+  +--+ 

...the packet would go:

    6 steps down (including the first line at the top of the diagram).
    3 steps right.
    4 steps up.
    3 steps right.
    4 steps down.
    3 steps right.
    2 steps up.
    13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?

"""

map = []
letters = [chr(i) for i in range(65,91)] # Upper ASCII
path = []

class Packet:

	# Directions
	"""
		0 - Up
		1 - Down
		2 - Left
		3 - Right
	"""

	def __init__(self, x, y):
		self.x = x 
		self.y = y 
		self.dir = 1 # Down by default on both Example and Problem Input
		self.steps = 0
		
	def move(self):
	
		# Go to next spot on the map
		if self.dir == 0:
			self.y -= 1
		elif self.dir == 1:
			self.y += 1
		elif self.dir == 2:
			self.x -= 1
		elif self.dir == 3:
			self.x += 1
	
		# if we moved out of bounds, terminate movement
		if self.y < 0 or self.y > len(map):
			return False
		if self.x < 0 or self.x > len(map[self.y]):
			return False
	
		# see what character is on the map
		mapchar = map[self.y][self.x]
		
		if mapchar == " ": # ran off the track
			return False
	
		if mapchar in letters: # passing a Letter
			path.append(mapchar)
		#elif mapchar == "|" or mapchar == "-":
			# continue same direction
		elif mapchar == "+": # turn
			if self.dir == 0 or self.dir == 1: # if moving up or down
				# check left and right for more track, or a letter.  
				if self.x > 0 and map[self.y][self.x-1] in letters or map[self.y][self.x-1] == "-":
					self.dir = 2
				elif self.x < len(map[self.y]) and map[self.y][self.x+1] in letters or map[self.y][self.x+1] == "-":
					self.dir = 3
			else: # were moving left to right or right to left
				# check above or below for more track, or a letter
				if self.y > 0 and map[self.y-1][self.x] in letters or map[self.y-1][self.x] == "|":
					self.dir = 0
				elif self.y < len(map) and map[self.y+1][self.x] in letters or map[self.y+1][self.x] == "|":
					self.dir = 1

		# Completed movement
		self.steps += 1
		return True
		

if __name__ == "__main__":

	# Part 1 Solution
	
	pkt = None

	with open("day19_input", "r") as infile:
		for line in infile.readlines():
			map.append(list(line))
	
	# Get initial cart position
	
	for i in range(len(map[0])):
		if map[0][i] == "|":
			pkt = Packet(i,0)
			break
	
	while pkt.move():
		continue
	print ''.join(path)
	print pkt.steps+1 # include final step
	
			

			
	
