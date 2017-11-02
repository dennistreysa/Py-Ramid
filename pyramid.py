import copy

""" Py-Ramid

	Python script for solving Number Pyramid Puzzles.

	Author: dennistreysa (dennistreysa (at) gmail.com)
	License: GNU General Public License v3.0
"""

class PyRamid(object):

	def __init__(self, maxSolutions=10, globalMaxValue=10000):
		""" Constructor

			Keyword arguments:
			maxSolutions -- Number of solutions the script shall search at maximum.
			globalMaxValue -- In some caches it's not possible to find a maximum value for a brick. This value is used in these cases.
		"""
		self._maxSolutions = maxSolutions
		self._globalMaxValue = globalMaxValue

	def _AssertValidPyramid(self, pyramid):
		""" Asserts that a given pyramid is valid

			Keyword arguments:
			pyramid -- The pyramid to be checked
		"""
		assert isinstance(pyramid, (list, tuple)), "Pyramid has to be list/tuple!"
		for layerId, layer in enumerate(pyramid):
			assert isinstance(layer, (list, tuple)), "Layer has to be list/tuple!"
			assert len(layer) >= (layerId + 1), "Need at least n bricks in layer n! (See layer #%d)" % (layerId + 1)
			for brick in layer:
				assert (brick is None) or isinstance(brick, (int, float)), "Brick has to be None, or numeric value!"

	def _IsSolved(self, pyramid):
		""" Checks if a given pyramid is solved

			Keyword arguments:
			pyramid -- The pyramid to be checked
		"""
		for layer in range(len(pyramid) - 1):
			for brick in range(layer + 1):
				
				brickValue = pyramid[layer][brick]				
				leftChild = pyramid[layer + 1][brick]
				rightChild = pyramid[layer + 1][brick + 1]

				if (brickValue is None) or (leftChild is None) or (rightChild is None):
					return False
				
				if brickValue != (leftChild + rightChild):
					return False
		return True

	def _IsSolveable(self, pyramid):
		""" Checks if a given pyramid is solveable by the data already given

			Keyword arguments:
			pyramid -- The pyramid to be checked
		"""
		for layer in range(len(pyramid) - 1):
			for brick in range(layer + 1):
				brickValue = pyramid[layer][brick]
				if brickValue is not None:
					# left child
					leftChild = pyramid[layer + 1][brick]
					if leftChild is not None and leftChild > brickValue:
						return False

					# right child
					rightChild = pyramid[layer + 1][brick + 1]
					if rightChild is not None and rightChild > brickValue:
						return False
		return True

	def _GetMaxValue(self, pyramid, layer, brick):
		""" Tries to find the maximum possible value for a specific brick
		
			Keyword arguments:
			pyramid -- The pyramid
			layer/brick -- The location of the brick to get the max value for
		"""
		
		# if brick already has a value, this is the maximum
		if pyramid[layer][brick] is not None:
			return pyramid[layer][brick]

		# recursively search for parent value
		left = self._GetMaxValue(pyramid, layer - 1, brick - 1) if (layer > 0 and brick > 0) else self._globalMaxValue
		right = self._GetMaxValue(pyramid, layer - 1, brick) if (layer > 0 and brick < layer) else self._globalMaxValue

		return min([left, right])

	def _SolveGuess(self, pyramid, brick):
		""" Tries to find a solution for a given pyramid and brick by guessing values
		
			Keyword arguments:
			pyramid -- The pyramid
			brick -- Index of the brick (always bottom layer!)
		"""

		if len(self._solutions) >= self._maxSolutions:
			return

		lastLayer = len(pyramid) - 1
		brickValue = pyramid[lastLayer][brick]
		startValue = brickValue if brickValue is not None else 0
		endValue = brickValue + 1 if brickValue is not None else self._GetMaxValue(pyramid, lastLayer, brick)

		for currentValue in range(startValue, endValue):
			pyramid[lastLayer][brick] = currentValue

			# is the pyramid solveable with these values
			if self._IsSolveable(pyramid):
				# try to repair
				repairedPyramid = self._SolveRepair(copy.deepcopy(pyramid))
				if not self._IsSolved(repairedPyramid):
					if (brick + 1) < len(pyramid):
						self._SolveGuess(repairedPyramid, brick + 1)
				else:
					if len(self._solutions) < self._maxSolutions:
						self._solutions.append(repairedPyramid)

	def _SolveRepair(self, pyramid):
		""" Tries to find a solution for a given pyramid by repairing it
		
			Keyword arguments:
			pyramid -- The pyramid
		"""
		
		repairedSomething = True

		while repairedSomething:
			repairedSomething = False
			for layer in range(len(pyramid) - 1):
				for brick in range(len(pyramid[layer])):
					top = pyramid[layer][brick]
					left = pyramid[layer + 1][brick]
					right = pyramid[layer + 1][brick + 1]
					# bottom-right is missing
					if top is not None and left is not None and right is None:
						if (top - left) >= 0:
							pyramid[layer + 1][brick + 1] = top - left
							repairedSomething = True
					# bottom-left is missing
					elif top is not None and left is None and right is not None:
						if (top - right) >= 0:
							pyramid[layer + 1][brick] = top - right
							repairedSomething = True
					# top is missing
					elif top is None and right is not None and left is not None:
						pyramid[layer][brick] = left + right
						repairedSomething = True

		return pyramid

	def Solve(self, pyramid):
		""" Tries to the solution(s) for a given pyramid
		
			Keyword arguments:
			pyramid -- The pyramid
		"""

		self._AssertValidPyramid(pyramid)
		
		self._solutions = []

		pyramid = self._SolveRepair(pyramid)
		if not self._IsSolved(pyramid):
			self._SolveGuess(pyramid, 0)
		else:
			self._solutions.append(pyramid)

		return self._solutions

	def BeautyprintPyramid(self, pyramid):
		""" Prints a given pyramid to resemble the shape of a pyramid (kinda)
		
			Keyword arguments:
			pyramid -- The pyramid
		"""

		layers = [", ".join([str(value) for value in layer]) for layer in pyramid]
		maxCharsInlayer = max([len(layer) for layer in layers])
		
		for layer in layers:
			layerWidth = len(layer)
			spaceWidth = (maxCharsInlayer - layerWidth) // 2
			print("%s%s%s" % (" "*spaceWidth, layer, " "*spaceWidth ))
