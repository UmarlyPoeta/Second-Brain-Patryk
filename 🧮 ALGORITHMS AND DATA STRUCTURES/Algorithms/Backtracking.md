# Backtracking

> Systematic method for solving problems by exploring all possible solutions and abandoning ("backtracking") partial solutions that cannot lead to a valid solution.

## 📖 Definition

Backtracking is a general algorithmic approach that considers searching every possible combination to solve computational problems. It builds candidates to the solution incrementally and abandons candidates ("backtracks") when they cannot possibly lead to a valid solution.

## ⚡ Time & Space Complexity

- **Time Complexity**: Often O(b^d) where b = branching factor, d = depth
- **Space Complexity**: O(d) for recursion stack
- **Worst Case**: Explores all possible combinations
- **Best Case**: Early pruning reduces search space significantly

## 🔑 Key Components

1. **Choice**: What decisions can be made at each step?
2. **Constraint**: What are the rules/limitations?
3. **Goal**: What constitutes a complete solution?
4. **Pruning**: When can we abandon a partial solution?

## 🐍 Python Implementation Examples

```python
# Classic Example 1: N-Queens Problem
def solve_n_queens(n):
    """Solve N-Queens problem using backtracking"""
    def is_safe(board, row, col):
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        
        # Check diagonals
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def backtrack(board, row):
        if row == n:
            solutions.append(board[:])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                # Backtrack (implicit - board[row] gets overwritten)
    
    solutions = []
    backtrack([-1] * n, 0)
    return solutions

def print_queens_solution(solution):
    """Print N-Queens solution as board"""
    n = len(solution)
    for row in range(n):
        line = ""
        for col in range(n):
            line += "Q " if solution[row] == col else ". "
        print(line)
    print()

# Classic Example 2: Sudoku Solver
def solve_sudoku(board):
    """Solve 9x9 Sudoku using backtracking"""
    def is_valid(board, row, col, num):
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def backtrack():
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if backtrack():
                                return True
                            board[row][col] = 0  # Backtrack
                    return False
        return True
    
    return backtrack()

# Example 3: Generate Permutations
def generate_permutations(nums):
    """Generate all permutations using backtracking"""
    def backtrack(current_perm):
        if len(current_perm) == len(nums):
            result.append(current_perm[:])
            return
        
        for num in nums:
            if num not in current_perm:
                current_perm.append(num)
                backtrack(current_perm)
                current_perm.pop()  # Backtrack
    
    result = []
    backtrack([])
    return result

# Example 4: Subset Sum
def subset_sum(nums, target):
    """Find if there's a subset with given sum"""
    def backtrack(index, current_sum, current_subset):
        if current_sum == target:
            solutions.append(current_subset[:])
            return True
        
        if index >= len(nums) or current_sum > target:
            return False
        
        # Include current number
        current_subset.append(nums[index])
        if backtrack(index + 1, current_sum + nums[index], current_subset):
            return True
        current_subset.pop()  # Backtrack
        
        # Skip current number
        return backtrack(index + 1, current_sum, current_subset)
    
    solutions = []
    backtrack(0, 0, [])
    return solutions

# Example 5: Word Break
def word_break_all(s, word_dict):
    """Find all possible word breaks"""
    def backtrack(start, current_sentence):
        if start == len(s):
            result.append(current_sentence[:])
            return
        
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_dict:
                current_sentence.append(word)
                backtrack(end, current_sentence)
                current_sentence.pop()  # Backtrack
    
    result = []
    backtrack(0, [])
    return [' '.join(sentence) for sentence in result]

# Example usage
if __name__ == "__main__":
    # N-Queens
    print("4-Queens solutions:")
    queens_solutions = solve_n_queens(4)
    for i, solution in enumerate(queens_solutions):
        print(f"Solution {i + 1}:")
        print_queens_solution(solution)
    
    # Permutations
    perms = generate_permutations([1, 2, 3])
    print("Permutations of [1,2,3]:", perms)
    
    # Subset sum
    subsets = subset_sum([2, 3, 6, 7], 7)
    print("Subsets that sum to 7:", subsets)
    
    # Word break
    sentences = word_break_all("catsanddog", {"cat", "cats", "and", "sand", "dog"})
    print("Word break sentences:", sentences)
```

## 🎯 Backtracking Applications

### 1. Constraint Satisfaction Problems
- **N-Queens**: Place queens on chessboard
- **Sudoku**: Fill grid with constraints
- **Graph Coloring**: Color vertices with constraints

### 2. Optimization Problems
- **Traveling Salesman**: Find shortest route
- **Knapsack**: Select items optimally
- **Job Scheduling**: Optimize task allocation

### 3. Combinatorial Generation
- **Permutations**: All arrangements
- **Combinations**: All selections
- **Power Set**: All subsets

### 4. Puzzle Solving
- **Maze Navigation**: Find path through maze
- **Crossword Puzzles**: Fill grid with words
- **Logic Puzzles**: Solve constraint-based puzzles

## 💡 Backtracking Template

```python
def backtrack(state):
    if is_complete(state):
        process_solution(state)
        return
    
    for choice in get_choices(state):
        if is_valid(state, choice):
            make_choice(state, choice)
            backtrack(state)
            undo_choice(state, choice)  # Backtrack
```

## 🔧 Optimization Techniques

1. **Pruning**: Early termination of invalid branches
2. **Constraint Propagation**: Reduce search space using constraints
3. **Heuristics**: Order choices by likelihood of success
4. **Memoization**: Cache results of expensive validity checks

## 🎯 When to Use Backtracking

✅ **Use Backtracking when:**
- Need to find all solutions
- Problem has constraints that can be checked incrementally
- Solution can be built incrementally
- Early pruning is possible

❌ **Avoid when:**
- Only need one solution and greedy/DP works
- Search space is too large without pruning
- Problem doesn't have incremental constraints

## 🔗 Related Topics

- [[Depth-First Search]] - Similar exploration strategy
- [[Dynamic Programming]] - Alternative for optimization problems
- [[Greedy Algorithms]] - Faster but may not find optimal
- [[Constraint Satisfaction]] - Formal framework for backtracking

---

*See also: [[Depth-First Search]], [[Dynamic Programming]], [[algorithms_and_ds]]*