#!/usr/bin/python3
import itertools
import sys
import subprocess
import time
import random
import math
import copy

"""
    @Author : KATOUZIAN Pouria ID: S-192865
    @Date : 18/07/2024
    @Description :  
        This program is a sudoku solver that uses the SAT solver to solve the sudoku.
        The program can solve any sudoku of size 4, 9, 16 and 25.
        The program can also generate a sudoku of size 4, 9, 16 and 25.
        The program can also check the uniqueness of the solution of a sudoku of size 4, 9, 16 and 25.
"""



# Supported sizes
SIZE = [4, 9, 16, 25]

"""
    Read a sudoku from a file.
    
    Args:
        filename (str): The name of the file.
    Returns:
        sudoku (list): The sudoku puzzle.
"""
def sudoku_read(filename):
    myfile = open(filename, 'r')
    sudoku = []
    N = 0
    for line in myfile:
        line = line.replace(" ", "")
        if line == "":
            continue
        line = line.split("|")
        if line[0] != '':
            exit("illegal input: every line should start with |\n")
        line = line[1:]
        if line.pop() != '\n':
            exit("illegal input\n")
        if N == 0:
            N = len(line)
            if N != 4 and N != 9 and N != 16 and N != 25:
                exit("illegal input: only size 4, 9, 16 and 25 are supported\n")
        elif N != len(line):
            exit("illegal input: number of columns not invariant\n")
        line = [int(x) if x != '' and int(x) >= 0 and int(x) <= N else 0 for x in line]
        sudoku += [line]
    return sudoku



"""
    Print a sudoku to a file.
    
    Args:
        myfile (file): The file.
        sudoku (list): The sudoku puzzle.
    Returns:
        None
"""
def sudoku_print(myfile, sudoku):
    if sudoku == []:
        myfile.write("impossible sudoku\n")
    N = len(sudoku)
    for line in sudoku:
        myfile.write("|")
        for number in line:
            if N > 9 and number < 10:
                myfile.write(" ")
            myfile.write(" " if number == 0 else str(number))
            myfile.write("|")
        myfile.write("\n")



"""
    Generate lit values for a Sudoku puzzle.
    
    Args:
        N (int): The size of the Sudoku puzzle.
        dataLength (int): The length of the data.
    Returns:
        litValues (list): The lit values for the Sudoku puzzle.
"""
def generate_lit_values(N, dataLength):
    litValues = []
    for i in range(1, N+1):
        lit_i = []
        for j in range(1, N+1):
            lit_j = []
            for k in range(1, N+1):
                lit_j.append(f"{str(i).zfill(dataLength)}{str(j).zfill(dataLength)}{str(k).zfill(dataLength)} ")
            lit_i.append(lit_j)
        litValues.append(lit_i)
    return litValues




"""
    Generate not lit values for a Sudoku puzzle.
    
    Args:
        N (int): The size of the Sudoku puzzle.
        dataLength (int): The length of the data.
    Returns:
        notLitValues (list): The not lit values for the Sudoku puzzle.
"""
def generate_not_lit_values(N, dataLength):
    notLitValues = []
    for i in range(1, N+1):
        notlit_i = []
        for j in range(1, N+1):
            notlit_j = []
            for k in range(1, N+1):
                notlit_j.append(f"-{str(i).zfill(dataLength)}{str(j).zfill(dataLength)}{str(k).zfill(dataLength)} ")
            notlit_i.append(notlit_j)
        notLitValues.append(notlit_i)
    return notLitValues



"""
    Get the size of the Sudoku puzzle.
    
    Args:
        N (int): The size of the Sudoku puzzle.
    Returns:
        n (int): The size of the Sudoku puzzle.
"""
def get_size(N):
    if N not in SIZE:
        exit("Invalid Size: only 4, 9, 16, and 25 are allowed")
    else:
        n = int(math.sqrt(N))
        
    return n



"""
    Generate cell constraints for a Sudoku puzzle.
    
    Args:
        N (int): The size of the Sudoku puzzle.
        populate_cell_literals (function): A function that populates the cell literals.
        newcl (function): A function that adds a new clause to the constraint.
        notNewLit (function): A function that adds a negated literal to the constraint.
    Returns:
        None
"""
def generate_cell_constraints(N, populate_cell_literals, newcl, notNewLit):
    for i, j in itertools.product(range(1, N+1), range(1, N+1)):
        populate_cell_literals(i, j)
        newcl()
        for value, otherValue in itertools.combinations(range(1, N+1), 2):
            notNewLit(i, j, value)
            notNewLit(i, j, otherValue)
            newcl()



"""
    Generate line constraints for a Sudoku puzzle.
    
    Args:
        N (int): The size of the Sudoku puzzle.
        newlit (function): A function that adds a new literal to the constraint.
        newcl (function): A function that adds a new clause to the constraint.
        notNewLit (function): A function that adds a negated literal to the constraint.
    Returns:
        None
"""
def generate_line_constraints(N, newlit, newcl, notNewLit):
    
    for line, value in itertools.product(range(1, N+1), range(1, N+1)):
        for column in range(1, N+1):
            newlit(line, column, value)
        newcl()
        for column in range(1, N+1):
            for otherColumn in range(column+1, N+1):
                for value in range(1, N+1):
                    notNewLit(line, column, value)
                    notNewLit(line, otherColumn, value)
                    newcl()



"""
    Generate column constraints for a Sudoku puzzle.
    
    Args:
        N (int): The size of the Sudoku puzzle.
        newlit (function): A function that adds a new literal to the constraint.
        newcl (function): A function that adds a new clause to the constraint.
        notNewLit (function): A function that adds a negated literal to the constraint.
    Returns:
        None
"""
def generate_column_constraints(N, newlit, newcl, notNewLit):
    for column, value in itertools.product(range(1, N + 1), repeat=2):
        for line in range(1, N + 1):
            newlit(line, column, value)
        newcl()
        
    for column in range(1, N + 1):
        for cellLine, otherCellLine in itertools.combinations(range(1, N + 1), 2):
            for value in range(1, N + 1):
                notNewLit(cellLine, column, value)
                notNewLit(otherCellLine, column, value)
                newcl()



"""
    Generate block constraints for a Sudoku puzzle.

    Args:
        N (int): The size of the Sudoku puzzle.
        newlit (function): A function that adds a new literal to the constraint.
        newcl (function): A function that adds a new clause to the constraint.
        notNewLit (function): A function that adds a negated literal to the constraint.

    Returns:
        None
"""
def generate_block_constraints(N, newlit, newcl, notNewLit):
    n = int(math.sqrt(N))
    
    for i, j in itertools.product(range(n), repeat=2):
        for value in range(1, N + 1):
            for line, column in itertools.product(range(1, n + 1), repeat=2):
                newlit(line + i * n, column + j * n, value)
            newcl()
        
        for firstline, firstColumn in itertools.product(range(1, n + 1), repeat=2):
            for secondColumn in range(firstColumn + 1, n + 1):
                for value in range(1, N + 1):
                    notNewLit(firstline + i * n, firstColumn + j * n, value)
                    notNewLit(firstline + i * n, secondColumn + j * n, value)
                    newcl()
            
            for secondline in range(firstline + 1, n + 1):
                for secondColumn in range(1, n + 1):
                    for value in range(1, N + 1):
                        notNewLit(firstline + i * n, firstColumn + j * n, value)
                        notNewLit(secondline + i * n, secondColumn + j * n, value)
                        newcl()


"""
    Generate generic constraints for a Sudoku puzzle.
    
    Args:
        N (int): The size of the Sudoku puzzle.
    Returns:
        constraints (str): The constraints for the Sudoku puzzle.
        count (int): The number of constraints.
"""
def sudoku_generic_constraints(N):
    dataLength = len(str(N))
    constraints = []
    count = 0

    # Output function
    def output(s):
        constraints.append(s)

    litValues = generate_lit_values(N, dataLength)
    notLitValues = generate_not_lit_values(N, dataLength)

    # Populate cell literals
    def populate_cell_literals(i, j):
        constraints.extend(litValues[i-1][j-1])

    def newlit(i,j,k):
        output(litValues[i-1][j-1][k-1])

    def notNewLit(i,j,k):
        output(notLitValues[i-1][j-1][k-1])

    def newcl():
        nonlocal count
        output("0\n")
        count += 1
    
    # Generate cell constraints
    generate_cell_constraints(N, populate_cell_literals, newcl, notNewLit)

    # Generate line constraints
    generate_line_constraints(N, newlit, newcl, notNewLit)
    
    # Generate column constraints
    generate_column_constraints(N, newlit, newcl, notNewLit)

    # Generate block constraints
    generate_block_constraints(N, newlit, newcl, notNewLit)
    
    return ''.join(constraints), count



"""
    Generate specific constraints for a Sudoku puzzle.
    
    Args:
        sudoku (list): The Sudoku puzzle.
    Returns:
        constraints (str): The constraints for the Sudoku puzzle.
        count (int): The number of constraints.
"""
def sudoku_specific_constraints(sudoku):

    N = len(sudoku)
    constraints = []
    dataLength = len(str(N))
    count = 0

    def output(s):
        constraints.append(s)

    def newlit(i,j,k):
        output(f"{str(i).zfill(dataLength)}{str(j).zfill(dataLength)}{str(k).zfill(dataLength)} ")

    def newcl():
        nonlocal count
        output("0\n")
        count += 1

    for i in range(N):
        for j in range(N):
            if sudoku[i][j] > 0:
                newlit(i + 1, j + 1, sudoku[i][j])
                newcl()

    return ''.join(constraints), count



"""
    Generate other solution constraints for a Sudoku puzzle.
    
    Args:
        solved_sudoku (list): The solved Sudoku puzzle.
        unsolved_sudoku (list): The unsolved Sudoku puzzle.
    Returns:
        constraints (str): The constraints for the Sudoku puzzle.
        count (int): The number of constraints.
"""
def sudoku_other_solution_constraint(solved_sudoku, unsolved_sudoku):

    N = len(unsolved_sudoku)
    constraints = []
    dataLength = len(str(N))

    def output(s):
        constraints.append(s)

    def notNewLit(i,j,k):
        output(f"{str(-i).zfill(dataLength)}{str(j).zfill(dataLength)}{str(k).zfill(dataLength)} ")

    def newcl():
        output("0\n")

    for i in range(1, N+1):
        for j in range(1, N+1):
            if unsolved_sudoku[i-1][j-1] == 0:
                notNewLit(i, j, solved_sudoku[i-1][j-1])
    newcl()
    return ''.join(constraints), 1

def sudoku_solve(filename):
    command = "java -jar org.sat4j.core.jar sudoku.cnf"
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    for line in out.split(b'\n'):
        line = line.decode("utf-8")
        if line == "" or line[0] == 'c':
            continue
        if line[0] == 's':
            if line != 's SATISFIABLE':
                return []
            continue
        if line[0] == 'v':
            line = line[2:]
            units = line.split()
            if units.pop() != '0':
                exit("strange output from SAT solver:" + line + "\n")
            units = [int(x) for x in units if int(x) >= 0]
            N = len(units)
            if N == 16:
                N = 4
            elif N == 81:
                N = 9
            elif N == 256:
                N = 16
            elif N == 625:
                N = 25
            else:
                exit("strange output from SAT solver:" + line + "\n")
            sudoku = [ [0 for i in range(N)] for j in range(N)]
            data_len = len(str(N))
            i_pos = 100 ** data_len
            j_pos = 10 ** data_len
            value_size =  10 ** data_len
            for number in units:
                sudoku[(number // i_pos) - 1][((number // j_pos) % j_pos) - 1] = number % value_size
            return sudoku
        exit("strange output from SAT solver:" + line + "\n")
        return []

# returns a sudoku grid of size N
def sudoku_generate(size, minimal=False):
    def sudoku_generate_is_valid(sudoku, i, j, value):
        N = len(sudoku)
        square_size = int(math.sqrt(N))

        for k in range(N):
            if sudoku[i][k] == value or sudoku[k][j] == value:
                return False

        top_left_line, top_left_column = (i // square_size) * square_size, (j // square_size) * square_size

        for line in range(top_left_line, top_left_line + square_size):
            for column in range(top_left_column, top_left_column + square_size):
                if sudoku[line][column] == value:
                    return False
        return True

    def sudoku_generate_solve_sudoku(sudoku):
        N = len(sudoku)
        for i in range(N):
            for j in range(N):
                if sudoku[i][j] == 0:
                    possible_values = list(range(1, N + 1))
                    random.shuffle(possible_values)
                    for value in possible_values:
                        if sudoku_generate_is_valid(sudoku, i, j, value):
                            sudoku[i][j] = value
                            if sudoku_generate_solve_sudoku(sudoku):
                                return True
                            sudoku[i][j] = 0
                    return False
        return True

    n = math.isqrt(size)
    if(n*n != size):
        exit("Unable to create a sudoku grid of size :", size)
    solved_sudoku = [[0 for value in range(size)] for line in range(size)]
    if(not sudoku_generate_solve_sudoku(solved_sudoku)):
        exit("Unable to generate a solved grid for this size")
    sudoku_grid = copy.deepcopy(solved_sudoku)
    generic_constraints_string, constraintsCount1 = sudoku_generic_constraints(size)

    if minimal :
        for i in range(0, size):
            for j in range(0, size):
                if sudoku_grid[i][j] == size:
                    sudoku_grid[i][j] = 0

    positions = [(i, j) for i in range(0, size) for j in range(0, size)]
    random.shuffle(positions)
    nbToRemove = n
    
    while len(positions) != 0:
        removed = {}
        for i in range(0, nbToRemove):
            position = positions.pop()
            removed[position] = sudoku_grid[position[0]][position[1]]
        for position, _ in removed.items():
            sudoku_grid[position[0]][position[1]] = 0

        specific_constraints_string, constraintsCount2 = sudoku_specific_constraints(sudoku_grid)
        other_solution_constraints, constraintsCount3 = sudoku_other_solution_constraint(solved_sudoku, sudoku_grid)

        myfile = open("sudoku.cnf", 'w')
        myfile.write("p cnf "+str(size)+str(size)+str(size)+" "+str(constraintsCount1+constraintsCount2+constraintsCount3)+"\n")
        myfile.write(generic_constraints_string)
        myfile.write(specific_constraints_string)
        myfile.write(other_solution_constraints)
        myfile.close()

        other_solution = sudoku_solve("sudoku.cnf")
        if other_solution != []:
            for position, value in removed.items():
                sudoku_grid[position[0]][position[1]] = value

    return sudoku_grid

from enum import Enum
class Mode(Enum):
    SOLVE = 1
    UNIQUE = 2
    CREATE = 3
    CREATEMIN = 4

start_time = time.time()
OPTIONS = {}
OPTIONS["-s"] = Mode.SOLVE
OPTIONS["-u"] = Mode.UNIQUE
OPTIONS["-c"] = Mode.CREATE
OPTIONS["-cm"] = Mode.CREATEMIN

if len(sys.argv) != 3 or not sys.argv[1] in OPTIONS :
    sys.stdout.write("./sudokub.py <operation> <argument>\n")
    sys.stdout.write("     where <operation> can be -s, -u, -c, -cm\n")
    sys.stdout.write("  ./sudokub.py -s <input>.txt: solves the Sudoku in input, whatever its size\n")
    sys.stdout.write("  ./sudokub.py -u <input>.txt: check the uniqueness of solution for Sudoku in input, whatever its size\n")
    sys.stdout.write("  ./sudokub.py -c <size>: creates a Sudoku of appropriate <size>\n")
    sys.stdout.write("  ./sudokub.py -cm <size>: creates a Sudoku of appropriate <size> using only <size>-1 numbers\n")
    sys.stdout.write("    <size> is either 4, 9, 16, or 25\n")
    exit("Bad arguments\n")

mode = OPTIONS[sys.argv[1]]

if mode == Mode.SOLVE or mode == Mode.UNIQUE:
    filename = str(sys.argv[2])
    sudoku = sudoku_read(filename)
    N = len(sudoku)

    generic_constraints_string, constraintsCount1 = sudoku_generic_constraints(N)
    specific_constraints_string, constraintsCount2 = sudoku_specific_constraints(sudoku)

    myfile = open("sudoku.cnf", 'w')
    myfile.write("p cnf "+str(N)+str(N)+str(N)+" "+str(constraintsCount1+constraintsCount2)+"\n")
    myfile.write(generic_constraints_string)
    myfile.write(specific_constraints_string)
    myfile.close()

    sys.stdout.write("sudoku\n")
    sudoku_print(sys.stdout, sudoku)
    sudoku = sudoku_solve("sudoku.cnf")
    sys.stdout.write("\nsolution\n")
    sudoku_print(sys.stdout, sudoku)

    if sudoku != [] and mode == Mode.UNIQUE:
        unsolved_sudoku = sudoku_read(filename)
        other_solution_constraints, constraintsCount3 = sudoku_other_solution_constraint(sudoku, unsolved_sudoku)

        myfile = open("sudoku.cnf", 'w')
        myfile.write("p cnf "+str(N)+str(N)+str(N)+" "+str(constraintsCount1+constraintsCount2+constraintsCount3)+"\n")
        myfile.write(generic_constraints_string)
        myfile.write(specific_constraints_string)
        myfile.write(other_solution_constraints)
        myfile.close()

        sudoku = sudoku_solve("sudoku.cnf")
        if sudoku == []:
            sys.stdout.write("\nsolution is unique\n")
        else:
            sys.stdout.write("\nother solution\n")
            sudoku_print(sys.stdout, sudoku)

elif mode == Mode.CREATE:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(size)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)

elif mode == Mode.CREATEMIN:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(size, True)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
print("---"+ str(time.time()-start_time) +"seconds ---")
