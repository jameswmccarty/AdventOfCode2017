#!/usr/bin/python

"""
--- Day 20: Particle Swarm ---

Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be able to finish them all in time to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

    Increase the X velocity by the X acceleration.
    Increase the Y velocity by the Y acceleration.
    Increase the Z velocity by the Z acceleration.
    Increase the X position by the X velocity.
    Increase the Y position by the Y velocity.
    Increase the Z position by the Z velocity.

Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity). Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current X positions (marked in parentheses), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)   

At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?

--- Part Two ---

To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if their positions ever exactly match. Because particles are updated simultaneously, more than two particles can collide at the same time and place. Once particles collide, they are removed and cannot collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)   
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)      
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------    
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)         
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?

"""

class Vect:

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	
	# Manhattan distance
	def dist(self, pos):
		return abs(self.x-pos.x)+abs(self.y-pos.y)+abs(self.z-pos.z)
		
	# Simple vector addition
	def sum(self, pos):
		self.x += pos.x
		self.y += pos.y
		self.z += pos.z
		
	def coord(self):
		return str(self.x) + "," + str(self.y) + "," + str(self.z)
		
class Particle:


	# take a line from the input file, parse and create particle
	def __init__(self, line, line_num):
		line = line.split(">, ")
		pos_line = line[0].replace("p=<", '')
		pos_line = pos_line.split(",")
		self.pos = Vect(int(pos_line[0]),int(pos_line[1]), int(pos_line[2]))
		vel_line = line[1].replace("v=<", '')
		vel_line = vel_line.split(",")
		self.vel = Vect(int(vel_line[0]),int(vel_line[1]), int(vel_line[2]))
		acc_line = line[2].replace("a=<", '')
		acc_line = acc_line.replace(">", '')
		acc_line = acc_line.split(",")
		self.acc = Vect(int(acc_line[0]),int(acc_line[1]), int(acc_line[2]))
		self.id_num = line_num
		self.collided = False
	
	# distance from the origin <0,0,0>
	def dist(self):
		return self.pos.dist(Vect(0,0,0))
		
	def tick(self):
		self.vel.sum(self.acc)
		self.pos.sum(self.vel)
		
	def collide(self, p):
		if p != self and self.pos.x == p.pos.x and self.pos.y == p.pos.y and self.pos.z == p.pos.z:
			self.collided = True
			p.collided = True		

if __name__ == "__main__":

	# Part 1 Solution

	particles = []

	with open("day20_input", "r") as infile:
		row_idx = 0
		for line in infile.readlines():
			particles.append(Particle(line, row_idx))
			row_idx += 1
	
	for i in range(1000):
		for particle in particles:
			particle.tick()
	
	particles.sort(key=lambda x : x.dist())
	
	print particles[0].id_num
	
	# Part 2 Solution

	particles = [] # Reset

	with open("day20_input", "r") as infile:
		row_idx = 0
		for line in infile.readlines():
			particles.append(Particle(line, row_idx))
			row_idx += 1
			

	
	for i in range(50):
		occupied = {}
		for particle in particles:
			particle.tick()
			if particle.pos.coord() in occupied:
				occupied[particle.pos.coord()].add(particle)
			else:
				occupied[particle.pos.coord()] = {particle}
		if len(occupied) < len(particles):
			rmv = [ occupied[x] for x in occupied if len(occupied[x]) > 1 ]
			rmv = [ x for y in rmv for x in y ]
			for item in rmv:
				particles.remove(item)
				
	print len(particles)
	
		