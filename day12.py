#!/usr/bin/python

"""
--- Day 12: Digital Plumber ---

Walking along the memory banks of the stream, you find a small village that is experiencing a little confusion: some programs can't communicate with each other.

Programs in this village communicate using a fixed system of pipes. Messages are passed between programs using these pipes, but most programs aren't connected to each other directly. Instead, programs pass messages between each other until the message reaches the intended recipient.

For some reason, though, some of these messages aren't ever reaching their intended recipient, and the programs suspect that some pipes are missing. They would like you to investigate.

You walk through the village and record the ID of each program and the IDs with which it can communicate directly (your puzzle input). Each program has one or more programs with which it can communicate, and these pipes are bidirectional; if 8 says it can communicate with 11, then 11 will say it can communicate with 8.

You need to figure out how many programs are in the group that contains program ID 0.

For example, suppose you go door-to-door like a travelling salesman and record the following list:

0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5

In this example, the following programs are in the group that contains program ID 0:

    Program 0 by definition.
    Program 2, directly connected to program 0.
    Program 3 via program 2.
    Program 4 via program 2.
    Program 5 via programs 6, then 4, then 2.
    Program 6 via programs 4, then 2.

Therefore, a total of 6 programs are in this group; all but program 1, which has a pipe that connects it to itself.

How many programs are in the group that contains program ID 0?

--- Part Two ---

There are more programs than just the ones in the group containing program ID 0. The rest of them have no way of reaching that group, and still might have no way of reaching each other.

A group is a collection of programs that can all communicate via pipes either directly or indirectly. The programs you identified just a moment ago are all part of the same group. Now, they would like you to determine the total number of groups.

In the example above, there were 2 groups: one consisting of programs 0,2,3,4,5,6, and the other consisting solely of program 1.

How many groups are there in total?

"""

class Program:

	def __init__(self, name):
		self.name = name
		self.connected = []
	
	def connect(self, prog):
		self.connected.append(prog)
		
	def reachable(self, goal, visited):
		if self.name == goal:
			return True
		if self in visited:
			return False
		visited.add(self)
		for child in self.connected:
			if child.reachable(goal, visited):
				return True
		return False

	def group_members(self,seen):
		if self in seen:
			return None
		seen.add(self)
		for child in self.connected:
			ret = child.group_members(seen)
			if ret != None:
				seen = seen.union(ret)
		return seen

if __name__ == "__main__":

	# Part 1 Solution
	
	nodes = {}
	
	with open("day12_input", "r") as infile:
		for line in infile.readlines():
			id, paths = line.split("<->")
			p_node = Program(id.strip())
			nodes[id.strip()] = p_node
			
	with open("day12_input", "r") as infile:
		for line in infile.readlines():
			id, paths = line.split("<->")
			id = id.strip()
			for pipe in paths.strip().split(","):
				nodes[id].connect(nodes[pipe.strip()])
	
	connected = 0
	for prog in nodes.values():
		if prog.reachable("0", set()):
			connected += 1
	print connected
	
	# Part 2 Solution
	
	num_groups = 0
	while len(nodes) != 0:
		prog = nodes.values()[0]
		to_rmv = prog.group_members(set())
		num_groups += 1
		while len(to_rmv) != 0:
			nodes.pop(to_rmv.pop().name)
	print num_groups

	
