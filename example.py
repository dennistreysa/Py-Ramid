from pyramid import PyRamid

pyramidToSolve = [
	[None],
	[None, 77],
	[52, None, None],
	[None, None, 17, None],
	[None, 18, None, 12, None]
]

ps = PyRamid()

solutions = ps.Solve(pyramidToSolve)

print("Found %d Solution(s)" % (len(solutions)))

for solutionId, solution in enumerate(solutions):
	print("\nSolution #%d:" % (solutionId + 1))
	ps.BeautyprintPyramid(solution)