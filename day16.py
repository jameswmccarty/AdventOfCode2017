#!/usr/bin/python

"""
--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

    Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
    Exchange, written xA/B, makes the programs at positions A and B swap places.
    Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do the following dance:

    s1, a spin of size 1: eabcd.
    x3/4, swapping the last two programs: eabdc.
    pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs standing after their dance?

--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including the first dance, a total of one billion (1000000000) times.

In the example above, their second dance would begin with the order baedc, and use the same dance moves:

    s1, a spin of size 1: cbaed.
    x3/4, swapping the last two programs: cbade.
    pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?

"""

def spin(string, idx):
	out = string[:len(string)-idx]
	out = string[-idx:] + out
	return out

def exch(string, i, j):
	char1 = string[i]
	char2 = string[j]
	out = list(string)
	out[i] = char2
	out[j] = char1
	return ''.join(out)
	
def ptnr(string, p1, p2):
	idx1 = string.index(p1)
	idx2 = string.index(p2)
	out = list(string)
	out[idx1] = p2
	out[idx2] = p1
	return ''.join(out)
	

if __name__ == "__main__":

	# Part 1 Solution

	line = "abcdefghijklmnop"
	moves = []
	
	with open("day16_input", "r") as infile:
		moves = infile.read().strip().split(",")
		
	for move in moves:
		if move[0] == "s":
			line = spin(line, int(move.replace("s",'')))
		elif move[0] == "x":
			t = move.replace("x",'')
			a, b = t.split("/")
			line = exch(line, int(a), int(b))
		elif move[0] == "p":
			t = move[1:]
			a, b = t.split("/")
			line = ptnr(line, a.strip(), b.strip())
	
	print line
	
	# Part 2 Solution
	
	line = "cknmidebghlajpfo"
	seen = []
	seen.append(line)
	
	target = 1000000000
	delta = 0
	
	for i in xrange(1000):	
		for move in moves:
			if move[0] == "s":
				line = spin(line, int(move.replace("s",'')))
			elif move[0] == "x":
				t = move.replace("x",'')
				a, b = t.split("/")
				line = exch(line, int(a), int(b))
			elif move[0] == "p":
				t = move[1:]
				a, b = t.split("/")
				line = ptnr(line, a.strip(), b.strip())
		if line in seen:
			delta = i - seen.index(line) + 1
			seen.append(line)
			break
		else:
			seen.append(line)
	
	print seen[(target % 60)-1]
	
	
	
	
	
			
