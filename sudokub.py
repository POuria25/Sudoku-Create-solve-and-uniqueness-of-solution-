#!/usr/bin/python3

import itertools
from math import sqrt
import sys
import subprocess
import random
import time

SIZE = [4,9,16,25]
# reads a sudoku from file
# columns are separated by |, lines by newlines
# Example of a 4x4 sudoku:
# |1| | | |
# | | | |3|
# | | |2| |
# | |2| | |
# spaces and empty lines are ignored
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

# print sudoku on stdout
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

# get number of constraints for sudoku
def sudoku_constraints_number(sudoku):

    N = len(sudoku)

    if N not in SIZE:
        exit("Invalid Size : only 4,9,16 and 25 are allowed")
    else:
        n = int(sqrt(N))
    count = ((N**3) + (N**4) + (N**3) + (N**4)) // 2
    return count

def sudoku_generic_constraints(myfile, N):

    def output(s):
        myfile.write(s)

    def newlit(i,j,k,N):

        if any(N == i for i in SIZE[:2]):
            output(str(i)+str(j)+str(k)+ " ")
        else:
            output(str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+" ")

    def nNewlit(i,j,k,N):

        if any(N == i for i in SIZE[:2]):
            output("-"+str(i)+str(j)+str(k)+ " ")
        else:
            output("-"+str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+" ")

    def newcl():
        output("0\n")
    def newcomment(s):
    #  output("c %s\n"%s)
        output("")

    if N not in SIZE:
        exit("Invalid Size : only 4,9,16 and 25 are allowed")
    else:
        n = int(sqrt(N))

    # At least one numeral in every case
    for i in range(1,N+1):
        for j in range(1,N+1):
            for k in range(1,N+1):
                newlit(i,j,k,N)
            newcl()

    # All columns have numbers 1 to N
    for i, j, k in itertools.product(range(1,N+1), repeat=3):
                newlit(i,k,j,N)
    newcl()

    # All numbers appear at least once in every case row, column,case
    for i, j, k in itertools.product(range(1,N+1), repeat=3):
                for l in range(k+1,N+1):
                    nNewlit(i+1,j+1,k+1,N)
                    nNewlit(i+1,j+1,l+1,N)
                    newcl()

                    nNewlit(i,k,j,N)
                    nNewlit(i,l,j,N)
                    newcl()

                    nNewlit(k,i,j,N)
                    nNewlit(l,i,j,N)
                    newcl()

    # All rows have numbers 1 to N
    for i, j, k in itertools.product(range(1,N+1), repeat=3):
        newlit(k,i,j,N)
    newcl()

    # All the square have all numbers
    for i in range(1,N+1):
        for j, k, l, m in itertools.product(range(n), repeat=4):
            newlit((j*n) + l + 1, (k*n) + m + 1, i,N)
        newcl()

    # All the square have a most one time the number
    for i in range(1,N+1):
        for j, k, l in itertools.product(range(n), repeat=3):
                    for m in range (1,n+1):
                        for o in range(m+1,n+1):
                            nNewlit((j*n) + l + 1, (k*n) + m , i,N)
                            nNewlit((j*n) + l + 1, (k*n) + o , i,N)
                            newcl()

    # Adding clauses to ensure the uniqueness of values in the Sudoku grid
    for i in range(1,N+1):
        for j, k in itertools.product(range(n), repeat=2):
            for l in range (1,n+1):
                for m in range (n):
                    for o in range(l+1,n+1):
                        for p in range(n):
                            nNewlit((j*n) + l , (k*n) + m + 1 ,i ,N)
                            nNewlit((j*n) + o , (k*n) + p + 1 ,i ,N)
                            newcl()


def sudoku_specific_constraints(myfile, sudoku):

    N = len(sudoku)

    def output(s):
        myfile.write(s)

    def newlit(i,j,k):

        if any(N == i for i in SIZE[:2]):
            output(str(i)+str(j)+str(k)+ " ")
        else:
            output(str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+" ")

    def newcl():
        output("0\n")

    for i in range(N):
        for j in range(N):
            if sudoku[i][j] > 0:
                newlit(i + 1, j + 1, sudoku[i][j])
                newcl()


def sudoku_other_solution_constraint(myfile, check,sudoku, sudoku_cell):

    N = len(sudoku)

    def output(s):
        myfile.write(s)

    def notnewlit(i,j,k):
        if any(N == i for i in SIZE[:2]):
            output("-"+str(i)+str(j)+str(k)+ " ")
        else:
            output("-"+str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+ " ")
    def newcl():
        output("0\n")

    for i in range(N):
        for j in range(N):
            if sudoku_cell[i][j] == 0 and (sudoku[i][j] != N or check):
                notnewlit(i+1, j+1, sudoku[i][j])
                newcl()
                break

def sudoku_solve(filename):
    B = [16, 81, 256, 625]
    command = "java -jar org.sat4j.core.jar "+filename
    process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            if any(N == i for i in B):
                N = int(sqrt(N))
            else:
                exit("strange output from SAT solver:" + line + "\n")
            sudoku = [ [0 for i in range(N)] for j in range(N)]
            if any(N == j for j in SIZE[:2]):
                for number in units:
                    sudoku[number // 100 - 1][( number // 10 )% 10 - 1] = number % 10
            elif any(N == i for i in SIZE[2:4]):
                for number in units:
                    tmp = number // 10000 - 1
                    row = (number // 100) % 100 - 1
                    column = number % 100
                    sudoku[tmp][row] = column
            else :
                exit("strange output from SAT solver:" + line + "\n")
            return sudoku
        exit("strange output from SAT solver:" + line + "\n")
        return []

#Initializes an empty Sudoku grid and a list of numbers for a given size.
def initialize_sudoku_cell(N):

    sudoku_cell = [[0] * N for i in range(1,N+1)]
    nb = list(range(1, N))

    return sudoku_cell, nb

import random


def isSafe(matrix, row, colmn, number):
    # Check if there is the same nb in the similar row return false
    for k in range(len(matrix)):
        if matrix[row][k] == number:
            return False

    # Check if there is the same nb in the similar column return false
    for l in range(len(matrix)):
        if matrix[l][colmn] == number:
            return False

    # Check if there is the same nb in the particular N*N sudoku return false
    startRow = row - row % int(sqrt(len(matrix)))
    startCol = colmn - colmn % int(sqrt(len(matrix)))
    for i in range(int(sqrt(len(matrix)))):
        for j in range(int(sqrt(len(matrix)))):
            if matrix[i + startRow][j + startCol] == number:
                return False
    return True


#Fills random cells in the Sudoku grid with numbers from the list 'nb'.
def fill_sudoku_cell(sudoku_cell, nb):

    for i in range(len(nb)):
        row = random.randint(0, int(len(nb)-1))
        column = random.randint(0, int(len(nb)-1))
        if sudoku_cell[row][column] == 0 and isSafe(sudoku_cell, row, column, nb[i]):
            sudoku_cell[row][column] = nb[i]

#Generates a CNF (Conjunctive Normal Form) file for the SAT solver.
def sudoku_generate_file(N, sudoku_cell, filename):

    with open(filename, 'w') as opf:
        opf.write("p cnf "+str(N)+str(N)+str(N)+" "+str(sudoku_constraints_number(sudoku_cell))+"\n")
        sudoku_generic_constraints(opf, N)
        sudoku_specific_constraints(opf, sudoku_cell)

#Fills random cells in the Sudoku grid with numbers from the solved Sudoku.
def fill_random_cells(check, sudoku_cell, sudoku, N):
    for i in range((N * N) // 2):
        row = random.randint(0, N - 1)
        column = random.randint(0, N - 1)
        if sudoku_cell[row][column] == 0 and (check or sudoku[row][column] != N): #check indicates whether to check for unique solutions.
            sudoku_cell[row][column] = sudoku[row][column]


#Generates a Sudoku puzzle with the specified size.
def sudoku_generate(check,size):

    if size not in SIZE:
        exit("Invalid Size : only 4,9,16 and 25 are allowed")
    else:
        n = int(sqrt(size))

    sudoku_cell, nb = initialize_sudoku_cell(size)
    fill_sudoku_cell(sudoku_cell, nb)
    sudoku_generate_file(size, sudoku_cell, "generate.cnf")

    while True:
        sudoku = sudoku_solve("generate.cnf") #solve the current puzzle.
        opf = open("generate.cnf", 'a')
        sudoku_other_solution_constraint(opf, check, sudoku, sudoku_cell) #Modifying the CNF file and adding constraints for a different solutions
        opf.close()
        sudoku2 = sudoku_solve("generate.cnf") #Checks if there is a second solution if not break if yes reinitializes the Sudoku grid
        if sudoku2 == []:
            break

    fill_random_cells(check, sudoku_cell, sudoku, size)

    return sudoku_cell

from enum import Enum
class Mode(Enum):
    SOLVE = 1
    UNIQUE = 2
    CREATE = 3
    CREATEMIN = 4

OPTIONS = {}
start_time = time.time()
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
    myfile = open("sudoku.cnf", 'w')
    myfile.write("p cnf "+str(N)+str(N)+str(N)+" "+str(sudoku_constraints_number(sudoku))+"\n")
    sudoku_generic_constraints(myfile, N)
    sudoku_specific_constraints(myfile, sudoku)
    myfile.close()
    sys.stdout.write("sudoku\n")
    sudoku_print(sys.stdout, sudoku)
    sudoku = sudoku_solve("sudoku.cnf")
    sys.stdout.write("\nsolution\n")
    sudoku_print(sys.stdout, sudoku)
    if sudoku != [] and mode == Mode.UNIQUE:
        sudoku_cell = sudoku_read(filename)
        myfile = open("sudoku.cnf", 'a')
        sudoku_other_solution_constraint(myfile, True,sudoku, sudoku_cell)
        myfile.close()
        sudoku = sudoku_solve("sudoku.cnf")
        if sudoku == []:
            sys.stdout.write("\nsolution is unique\n")
        else:
            sys.stdout.write("\nother solution\n")
            sudoku_print(sys.stdout, sudoku)
elif mode == Mode.CREATE:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(False, size)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
elif mode == Mode.CREATEMIN:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(False, size)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
elapsed_time = time.time() - start_time
print("--- {:.4f} seconds ---".format(elapsed_time))
