#!/usr/bin/python

"""
--- Day 23: Coprocessor Conflagration ---

You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality seems very similar, but some of the instructions are different:

    set X Y sets register X to the value of Y.
    sub X Y decreases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

    Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?

--- Part Two ---

Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1 when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very efficient implementation. You'll need to optimize the program if it has any hope of completing before Santa needs that printer working.

The coprocessor's ultimate goal is to determine the final value left in register h once the program completes. Technically, if it had that... it wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what value would be left in register h?

"""

regs = {} # register bank
mul_count = 0 # counter
ip = 0

def init(): # zero all registers a-z
	global regs
	for reg in range(97,106): #a-h
		regs[chr(reg)] = 0
		
# set X Y sets register X to the value of Y.
def set(x, y):
	if y in regs:
		regs[x] = regs[y]
	else:
		regs[x] = int(y)
		
# mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
def mul(x, y):
	global mul_count
	mul_count += 1
	if y in regs:
		regs[x] *= regs[y]
	else:
		regs[x] *= int(y)
		
# add X Y decreases register X by the value of Y.
def sub(x, y):
	if y in regs:
		regs[x] -= regs[y]
	else:
		regs[x] -= int(y)

# jnz X Y jumps with an offset of the value of Y, but only if the value of X is not equal to zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
def jnz(x, y):
	global ip
	if x in regs:
		if regs[x] != 0:
			if y in regs:
				ip += (regs[y]-1)
			else:
				ip += (int(y)-1)
	elif x != 0:
		if y in regs:
			ip += (regs[y]-1)
		else:
			ip += (int(y)-1)		
		
if __name__ == "__main__":
	
	# Part 1 Solution

	op = {"set" : set, "sub" : sub, "mul" : mul, "jnz" : jnz }
	
	program = []
	
	with open("day23_input", "r") as infile:
		for line in infile.readlines():
			program.append(line.strip().split(" "))
			
	init()
	while ip < len(program) and ip > -1:
		op[program[ip][0]](program[ip][1],program[ip][2])
		ip += 1
	print mul_count
