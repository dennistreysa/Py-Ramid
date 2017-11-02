# Py-Ramid
Python script for solving Number Pyramid Puzzles

## Example

The following puzzle...

![The Puzzle](https://github.com/dennistreysa/Py-Ramid/raw/master/images/puzzle.png)

...can be solved by the script below (see *exmaple.py*):

```python
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

```

Output:

```
Found 1 Solution(s)

Solution #1:
      169      
     92, 77     
   52, 40, 37   
 29, 23, 17, 20 
11, 18, 5, 12, 8
```

As you can see, usage is quite simple, just convert the pyramid to a left-aligned array and you're ready to to.

### Notes

If the pyramid has no unique solution, or the solution can not be found by simply 'repairing' the pyramid, the script tries to bruteforce a solution. If you want to limit the solution, pass the **maxSolutions** parameter to the constructor. If you want to change the maximum value for bruteforcing, pass the **globalMaxValue** to the constructor.
