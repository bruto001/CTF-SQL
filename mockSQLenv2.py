import numpy as np

import const

class mockSQLenv(object):
	def __init__(self,verbose=True):

		# Get the action space
		self.A = np.array(const.actions)

		# Random integers to setup the server
		r = np.random.randint(3)
		f = np.random.randint(5)
		self.flag_cols = f

		# The random setup contains the correct escape sequences and the correct SQL injection
		self.setup = [0+r*17, 1+r*17,(12+f)+r*17]

		# Get the set of actions that are syntactically correct
		self.syntaxmin = 0+r*17
		self.syntaxmax = 17+r*17

		self.termination = False
		self.verbose = verbose
		if(self.verbose): print('Game setup with a random query')


	def step(self,action_number=None,action_string=None):
		# step() expects a correct action number or a correct action string. No checks in place

		# If given a string find out the action number
		if (action_number==None):
			print("action_number)",action_number)
			action_number = np.where(self.A==action_string)[0][0]
		if(self.verbose): print('I received action {0}: {1}'.format(action_number, self.A[action_number]))

		# Process action
		if (action_number==self.setup[0]):
			if(self.verbose): print('Correct exploratory action for the escape. I return 1')
			return 1,-1,self.termination,'Server response is 1'
		elif (action_number==self.setup[1]):
			if(self.verbose): print('Correct exploratory action for the escape. I return 2')
			return 2,-1,self.termination,'Server response is 2'
		elif (action_number==self.setup[2]):
			if(self.verbose): print('Flag captured. I return 3')
			self.termination = True
			return 3,10,self.termination,'Server response is 3'
		elif (action_number >= self.syntaxmin and action_number < self.syntaxmax):
			if(action_number == self.flag_cols*2 + self.setup[1] + 1 or action_number == self.flag_cols*2 + self.setup[1] + 2):
				if(self.verbose): print('Query with correct number of rows')
				return 4,-1, self.termination, "Server response is 4"

			if(self.verbose): print('Query has the correct escape, but contains the wrong number of rows. I return 0')
			return 0,-1,self.termination,'Server response is 0'
		else:
			if(self.verbose): print('Query is syntactically wrong. I return -1')
			return -1,-1,self.termination,'Server response is -1'


	def reset(self):
		self.termination = False
		if(self.verbose): print('Game reset (but not reinitialized with a new random query!)')
		return None,0,self.termination,'Game reset'

	def reveal_solution(self):
		print('Correct escapes are: \n [{0}]: {1} \n [{2}]: {3}'.format(self.setup[0],self.A[self.setup[0]],self.setup[1],self.A[self.setup[1]]))
		print('Correct SQL injection is: \n [{0}]: {1}'.format(self.setup[2],self.A[self.setup[2]]))