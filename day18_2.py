#!/usr/bin/python

"""

--- Day 18: Duet ---

You discover a tablet containing some strange assembly code labeled simply "Duet". Rather than bother the sound card with it, you decide to run the code yourself. Unfortunately, you don't see any documentation, so you're left to figure out what the instructions mean on your own.

It seems like the assembly is meant to operate on a set of registers that are each named with a single letter and that can each hold a single integer. You suppose each register should start with a value of 0.

There aren't that many instructions, so it shouldn't be hard to figure out what they do. Here's what you determine:

    snd X plays a sound with a frequency equal to the value of X.
    set X Y sets register X to the value of Y.
    add X Y increases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
    rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
    jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

Many of the instructions can take either a register (a single letter) or a number. The value of a register is the integer it contains; the value of a number is that number.

After each jump instruction, the program continues with the instruction to which the jump jumped. After any other instruction, the program continues with the next instruction. Continuing (or jumping) off either end of the program terminates it.

For example:

set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2

    The first four instructions set a to 1, add 2 to it, square it, and then set it to itself modulo 5, resulting in a value of 4.
    Then, a sound with frequency 4 (the value of a) is played.
    After that, a is set to 0, causing the subsequent rcv and jgz instructions to both be skipped (rcv because a is 0, and jgz because a is not greater than 0).
    Finally, a is set to 1, causing the next jgz instruction to activate, jumping back two instructions to another jump, which jumps again to the rcv, which ultimately triggers the recover operation.

At the time the recover operation is executed, the frequency of the last sound played is 4.

What is the value of the recovered frequency (the value of the most recently played sound) the first time a rcv instruction is executed with a non-zero value?

--- Part Two ---

As you congratulate yourself for a job well done, you notice that the documentation has been on the back of the tablet this entire time. While you actually got most of the instructions correct, there are a few key differences. This assembly code isn't about sound at all - it's meant to be run twice at the same time.

Each running copy of the program has its own set of registers and follows the code independently - in fact, the programs don't even necessarily run at the same speed. To coordinate, they use the send (snd) and receive (rcv) instructions:

    snd X sends the value of X to the other program. These values wait in a queue until that program is ready to receive them. Each program has its own message queue, so a program can never receive a message it sent.
    rcv X receives the next value and stores it in register X. If no values are in the queue, the program waits for a value to be sent to it. Programs do not continue to the next instruction until they have received a value. Values are received in the order they are sent.

Each program also has its own program ID (one 0 and the other 1); the register p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1, 2, 0; program 1 sends 1, 2, 1. Then, each program receives a value (both 1) and stores it in a, receives another value (both 2) and stores it in b, and then each receives the program ID of the other program (program 0 receives 1; program 1 receives 0) and stores it in c. Each program now sees a different value in its own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for either of them, and they reach a deadlock. When this happens, both programs terminate.

It should be noted that it would be equally valid for the programs to run at different speeds; for example, program 0 might have sent all three values and then stopped at the first rcv before program 1 executed even its first instruction.

Once both of your programs have terminated (regardless of what caused them to do so), how many times did program 1 send a value?

"""

regs1 = {} # register bank
regs2 = {} # register bank

def init(): # zero all registers a-z, set program id in reg p
	global regs1
	global regs2
	for reg in range(97,123): #a-z
		regs1[chr(reg)] = 0
		regs2[chr(reg)] = 0
	regs2['p'] = 1
	regs1['sent'] = 0 # sent message counters
	regs2['sent'] = 0
	regs1['id'] = 0
	regs2['id'] = 1
	regs1['ip'] = 0 # instruction pointer
	regs2['ip'] = 0
	regs1['msg'] = [] # message queue
	regs2['msg'] = []
	regs1['lock'] = False # deadlocked
	regs2['lock'] = False
	regs1['run'] = True # ip in bounds
	regs2['run'] = True
		
# snd X pass a message to other copy of program
def snd(reg, jnk, regs):
	global regs1
	global regs2
	if regs['id'] == 0:
		if reg in regs:
			regs2['msg'].append(regs[reg])
		else:
			regs2['msg'].append(int(reg))
	else:
		if reg in regs:
			regs1['msg'].append(regs[reg])
		else:
			regs1['msg'].append(int(reg))
	regs['sent'] += 1

# set X Y sets register X to the value of Y.
def set(x, y, regs):
	if y in regs:
		regs[x] = regs[y]
	else:
		regs[x] = int(y)

# add X Y increases register X by the value of Y.
def add(x, y, regs):
	if y in regs:
		regs[x] += regs[y]
	else:
		regs[x] += int(y)
	
# mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
def mul(x, y, regs):
	if y in regs:
		regs[x] *= regs[y]
	else:
		regs[x] *= int(y)
	
# mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
def mod(x, y, regs):
	if y in regs:
		regs[x] %= regs[y]
	else:
		regs[x] %= int(y)

# rcv X get input from other program
def rcv(x, jnk, regs):
	global regs1
	global regs2
	if len(regs['msg']) > 0:
		regs[x] = regs['msg'].pop(0)
		regs['lock'] = False
	else:
		regs['lock'] = True
		
		if regs1['lock'] and regs2['lock']:
			print "Program Terminated."
			regs1['run'] = False
			regs2['run'] = False
		
		else:
			regs['ip'] -= 1 # 'spin wait' this inst
			print "Spin waiting on program", regs['id']
				
# jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
def jgz(x, y, regs):
	if x in regs:
		if regs[x] > 0:
			if y in regs:
				regs['ip'] += (regs[y]-1)
			else:
				regs['ip'] += (int(y)-1)
	elif x > 0:
		if y in regs:
			regs['ip'] += (regs[y]-1)
		else:
			regs['ip'] += (int(y)-1)


if __name__ == "__main__":

	# Part 2 Solution

	op = {"snd" : snd, "set" : set, "add" : add, "mul" : mul, "mod" : mod, "rcv" : rcv, "jgz" : jgz }
	
	program1 = []
	program2 = []
	
	with open("day18_input", "r") as infile:
		for line in infile.readlines():
			program1.append(line.strip().split(" "))
			program2.append(line.strip().split(" "))
			
	init()
	while regs1['run'] or regs2['run']:
		if regs1['ip'] < len(program1) and regs1['ip'] > -1:
			if len(program1[regs1['ip']]) < 3: # some opcodes only have one argument
				program1[regs1['ip']].append(None) # avoid index OOB
			op[program1[regs1['ip']][0]](program1[regs1['ip']][1],program1[regs1['ip']][2], regs1)
			regs1['ip'] += 1
		else:
			regs1['run'] = False
		if regs2['ip'] < len(program2) and regs2['ip'] > -1:
			if len(program2[regs2['ip']]) < 3: # some opcodes only have one argument
				program2[regs2['ip']].append(None) # avoid index OOB
			op[program2[regs2['ip']][0]](program2[regs2['ip']][1],program2[regs2['ip']][2], regs2)
			regs2['ip'] += 1
		else:
			regs2['run'] = False
			
	print "Program 0 sent", regs1['sent']
	print "Program 1 sent", regs2['sent']
