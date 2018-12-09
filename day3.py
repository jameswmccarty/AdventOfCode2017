#!/usr/bin/python

"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the location of the only access port for this memory system) by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

    Data from square 1 is carried 0 steps, since it's at the access port.
    Data from square 12 is carried 3 steps, such as: down, left, left.
    Data from square 23 is carried only 2 steps: up twice.
    Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?

Your puzzle input is 325489.

--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.
    Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
    Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
    Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
    Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?

Your puzzle input is still 325489.

"""

if __name__ == "__main__":
    # Part 1 Solution
	data = 325489
	
	# We have a spiral shape on a grid
	# Odd Squares (9, 25, 49, ...) are on lower right-hand corners
	# An Odd Squares distance from center is N - 1 for N^2 (i.e. 9 is 2, 25 is 4, etc)
	
	# Find the first odd square larger than our input
	ring = 1
	while ring*ring < data:
		ring += 2
	
	# Our input is on the perimeter of the NxN square
	# Find out how far we need to walk around the perimeter
	remainder = (ring*ring) - data
	# sides are symmetrical, so trim off multiples of N
	remainder %= (ring-1)
	
	side = [0] * ring
	corner_distance = ring - 1  #An Odd Squares distance from center is N - 1
	side[0] = corner_distance
	# One fewer step distance as we approach centerline from the corner
	for i in range(1,ring/2 + 1):
		side[i] = side[i-1] - 1
	for i in range(ring/2 + 1,ring):
		side[i] = side[i-1] + 1
	print side[remainder]

	# Part 2 Solution
	
	grid_size = 200 # big enough 2D grid
	
	grid = [[0] * grid_size for i in range(grid_size)]
	
	grid[grid_size/2][grid_size/2] = 1 # start from center
	x = (grid_size / 2) 
	y = (grid_size / 2) 
	
	dirs = ['E', 'N', 'W', 'S']
	dir_idx = 0
	side_max = 1
	step = 0
	toggle = 0
	start = True
	
	while True:
		# sum the grid point
		if not start:
			grid[y][x] = grid[y-1][x+1] + grid[y-1][x] + grid[y-1][x-1] + grid[y+1][x+1] + grid[y+1][x] + grid[y+1][x-1] + grid[y][x-1] + grid[y][x+1]
		else:
			start = False
		
		if grid[y][x] > data:
			print grid[y][x]
			break
		
		if step == side_max:
			if toggle == 1:
				toggle = 0
				side_max += 1
			else:
				toggle = 1
			step = 0
			dir_idx += 1
			dir_idx %= 4			
		
		if dirs[dir_idx]   == 'N':
			y -= 1
		elif dirs[dir_idx] == 'W':
			x -= 1
		elif dirs[dir_idx] == 'E':
			x += 1
		elif dirs[dir_idx] == 'S':
			y += 1
		
		step += 1

	
	
	
	
		
	
	
	
