import os, time
class GameOfLife:
	"""
	Internally, dead and alive cells should be '0' and '1'
	(string) respectively. The display should however follow self.chrtheme (indexes [0] for dead and [1] for alive).

	TODO: Optimize the whole thing
	TODO: character style converter for cleaning seeds etc;
	      convert 'alive' character, treat the rest as dead
	TODO: consider str().join(list) - set as string beforehand
	      or treat at storage time with [str(i) for i in list];
	      latter sounds less efficient
	"""

	fieldw, fieldh = 40, 30 # initial size of field
	iterations = 200 # default number of iterations
	field = [tuple(),list()] # [0] is current and a tuple, [1] is new and a list
	                # [0] should never be modified directly, but only be
	                # read or substituted. [1] is modified instead, and
	                # then copied over [0].
	# used by dumpcur()
	chrtheme = [' ','●'] # Character for dead [0] and alive [1] cells
	seed = ['00000000000000000000000000000000000000',
	 '00000000000000000000000001000000000000',
	 '00000000000000000000000101000000000000',
	 '00000000000001100000011000000000000110',
	 '00000000000010001000011000000000000110',
	 '01100000000100000100011000000000000000',
	 '01100000000100010110000101000000000000',
	 '00000000000100000100000001000000000000',
	 '00000000000010001000000000000000000000',
	 '00000000000001100000000000000000000000',
	 '00000000000000000000000000000000000000',
	 '00000000000000000000000000000000000000']
	# Statistics
	swtimes = [0,0] # used by self.stopwatch(),[start,end]
	lastcycles = 0 # used by self.cycles(), number of cycles in last execution

	# w and h arguments are passed to
	def __init__(self):
		# Setting up
		self.setfield(self.fieldw,self.fieldh)
		self.field[1] = self.sow(self.field[1], self.seed)
		self.update0()

		# Displaying the current seed
		self.dumpcur()
		time.sleep(1) # Drama

		self.stopwatch('start')
		self.cycle(self.iterations)
		self.stopwatch('endump')

	# Resets the field
	def setfield(self,w,h,update0=False):
		self.field = [tuple(),list()]
		# str().rjust... > ''.rjust... > 'x'*...
		self.field[1] = ['0'*w for x in range(h)]
		if (update0):
			self.update0()


	# apply seed to field
	# self.field[0] should probably be passed as the field argument
	# TODO: specify alive character in the arguments, treat others as dead
	def sow(self,field,seed):
		cx = cy = 0; # Cursor coordinates
		field = field[:]
		for y in seed: # y should be a string like '0010'
			newy = list(field[cy]) # newy stores the row to be updated; splitted so we can modify it directly TODO: Find a way to directly modify the character?
			if (cy > len(seed)-1 or cy > len(field)-1):

				break
			for x in y: # x should be either '0' or '1'
				if (cx > len(newy)-1 or cx > len(field[cy])-1):
					break
				newy[cx] = x # x is the same as seed[cy][cx]
				cx += 1
			field[cy] = ''.join(newy) #NOTE: I suppose newy contents shouldn't need to be converted to string at this point because the seed is already supposed to be a string in first place.
			cx  = 0
			cy += 1
		return field

	# Run game for cycles cycles
	def cycle(self,cycles,delay=0):
		if int(cycles > 1):
			if (delay != 0):
				for c in range(cycles):
					self.step()
					self.dumpcur()
					time.sleep(delay)
			else:
				for c in range(cycles):
					self.step()
					self.dumpcur()
			print('Ran',cycles,'cycles')
		else:
			self.dumpcur()
		self.lastcycles = cycles

	# Calculates the next field
	def step(self):
		for y in range(len(self.field[0])-1):
			newy = list(self.field[0][y]);
			for x in range(len(self.field[0][y])-1):
				newy[x] = str(self.fate(self.field[0],x,y))
			self.field[1][y] = ''.join(newy)
		self.update0()

### INTERNAL METHODS ###
	# Decides if a cell lives or die
	def fate(self,field,x,y):
		neighbors = 0

		if (y > 0):
			if (x > 0):
				neighbors += int(field[y-1][x-1])
			neighbors += int(field[y-1][x])
			if (x <= self.fieldw-2):
				neighbors += int(field[y-1][x+1])
		if (x > 0):
			neighbors += int(field[y][x-1])
		if (x <= self.fieldw-2):
			neighbors += int(field[y][x+1])

		if (y < self.fieldh-2):
			if (x > 0):
				neighbors += int(field[y+1][x-1])
			neighbors += int(field[y+1][x])
			if (x <= self.fieldw-2):
				neighbors += int(field[y+1][x+1])
		return self.rule(self.cellstate(field,x,y),neighbors)


	# The return values can be summed to decide if a cell lives or dies
	def cellstate(self,field,x,y):
		return 0 if field[y][x] == '0' else 1

	# Apply Game of Life rules
	#[1] state (0 or 1) [2] neighbors
	def rule(self,sta,nei):
		if (sta == 0):
			return 1 if nei == 3 else 0
		else:
			return 0 if nei < 2 or nei > 3 else 1

	# Replaces self.field[0] with new state
	def update0(self):
		self.field[0] = tuple(self.field[1])
		return None

	# standardizes field formats
	def clean(self,field,alive=None): pass
	# NOTE: Is there a way to do this?
	#clean = lambda self, field, alive=None: pass

### Views ###
	def dumpcur(self):
		os.system('cls'); #jumps to 75.4 fps without this

		print("\n".join(self.field[0]).replace('0',self.chrtheme[0]).replace('1',self.chrtheme[1]))#37.9 fps

	def stopwatch(self,step):
		if (step == 'start'):
			self.swtimes[0] = time.time()
			return None
		elif (step == 'endump'):
			totaltime = time.time() - self.swtimes[0]
		elif (step == 'end'):
			self.swtimes[1] = time.time()
			return None
		elif (step == 'dump'):
			print('Time elapsed in seconds (cached): '+str(self.swtimes[1] - self.swtimes[0]))
			return None
		else:
			print('stopwatch tool called incorrectly')

		print('Time elapsed in seconds: '+str(totaltime))
		print('Cycles per second:',self.lastcycles/totaltime)
		self.swtimes = [0,0]
if __name__ == "__main__": GameOfLife()
