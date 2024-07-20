#!/usr/bin/python3
import itertools
from math import sqrt
import sys
import subprocess
import random
import time


"""
    @author : KATOUZIAN Pouria ID: S-192865
    @Date : 18/07/2024
"""

# reads a sudoku from file
# columns are separated by |, lines by newlines
# Example of a 4x4 sudoku:
# |1| | | |
# | | | |3|
# | | |2| |
# | |2| | |
# spaces and empty lines are ignored


SIZE = [4, 9, 16, 25]

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
    return ( ((N**3) * 3) + ((N**4) * 3) + (N**3) + ((N**4) * 2) ) // 2

"""
# prints the generic constraints for sudoku of size N
def sudoku_generic_constraints(myfile, N):

    def output(s):
        myfile.write(s)

    def newlit(i,j,k,N):
        if N in SIZE[:2]:
            output(str(i)+str(j)+str(k)+ " ")
        else:
            output(str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+ " ")
        
    def notnewlit(i,j,k,N):
        if N in SIZE[:2]:
            output("-"+str(i)+str(j)+str(k)+ " ")
        else:
            output("-"+str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+ " ")

    def newcl():
        output("0\n")
    def newcomment(s):
    # output("c %s\n"%s)
        output("")

    if N not in SIZE:
        exit("Invalid Size : only 4,9,16 and 25 are allowed")
    else:
        n = int(sqrt(N))


    for i, j, k in itertools.product(range(1, N+1), range(1, N+1), range(1, N+1)):
        notnewlit(i, j, k, N)
    newcl()
    
    for i, j, k in itertools.product(range(1, N+1), range(1, N+1), range(1, N+1)):
        for l in range(k+1, N+1):
            notnewlit(i, j, k, N)
            notnewlit(i, j, l, N)
            newcl()
        
        
    for i, j in itertools.product(range(1, N+1), range(1, N+1)):
        for k in range(1, N+1):
            newlit(i, k, j, N)
        newcl()
    
    for i, j, k in itertools.product(range(1, N+1), range(1, N+1), range(1, N+1)):
        for l in range(k + 1, N):
            notnewlit(i, k, j, N)
            notnewlit(i, l, j, N)
            newcl()
                    
    for i, j, k in itertools.product(range(1, N+1), range(1, N+1), range(1, N+1)):
        newlit(k, i, j, N)
    newcl()
    
    #maybe this block of the loop can be optimized or caused a bug
    for i, j, k in itertools.product(range(1, N+1), range(1, N+1), range(1, N+1)):
        for l in range(k + 1, N + 1):
            notnewlit(k, i, j, N)
            notnewlit(l, i, j, N)
            newcl()
    
    for k in range(1, N + 1):
        for i, j in itertools.product(range(n), range(n)):
            for l, m in itertools.product(range(n), range(n)):
                newlit((i * n) + l + 1, (j * n) + m + 1, k, N)
            newcl()
    
    for k in range(1, N+1):
        for i, j ,l in itertools.product(range(n), range(n), range(n)):
            for m in range(1, n+1):
                for s in range(m+1, n+1):
                    notnewlit((i * n) + l + 1, (j * n) + m, k, N)
                    notnewlit((i * n) + l + 1, (j * n) + s, k, N)
                    newcl()

    for k in range(1, N+1):
        for i, j in itertools.product(range(n), range(n)):
            for l in range(1, n+1):
                for m in range(n):
                    for s in range(l+1, n+1):
                        for t in range(n):
                            notnewlit((i * n) + l, (j * n) + m + 1, k, N)
                            notnewlit((i * n) + s, (j * n) + t + 1, k, N)
                            newcl()
"""

def sudoku_generic_constraints(myfile, N):
    
    def output(s):
        myfile.write(s)

    def newlit(i, j, k, N):
        if N in SIZE[:2]:
            return f"{i}{j}{k} "
        else:
            return f"{str(i).zfill(2)}{str(j).zfill(2)}{str(k).zfill(2)} "
        
    def notnewlit(i, j, k, N):
        if N in SIZE[:2]:
            return f"-{i}{j}{k} "
        else:
            return f"-{str(i).zfill(2)}{str(j).zfill(2)}{str(k).zfill(2)} "

    def newcl():
        return "0\n"
    
    def newcomment(s):
        return ""

    if N not in SIZE:
        exit("Invalid Size : only 4,9,16 and 25 are allowed")
    else:
        n = int(sqrt(N))

    buffer = []

    for i, j, k in itertools.product(range(1, N + 1), range(1, N + 1), range(1, N + 1)):
        buffer.append(notnewlit(i, j, k, N))
    buffer.append(newcl())
    
    for i, j, k in itertools.product(range(1, N + 1), range(1, N + 1), range(1, N + 1)):
        for l in range(k + 1, N + 1):
            buffer.append(notnewlit(i, j, k, N))
            buffer.append(notnewlit(i, j, l, N))
            buffer.append(newcl())
    
    for i, j in itertools.product(range(1, N + 1), range(1, N + 1)):
        for k in range(1, N + 1):
            buffer.append(newlit(i, k, j, N))
        buffer.append(newcl())
    
    for i, j, k in itertools.product(range(1, N + 1), range(1, N + 1), range(1, N + 1)):
        for l in range(k + 1, N):
            buffer.append(notnewlit(i, k, j, N))
            buffer.append(notnewlit(i, l, j, N))
            buffer.append(newcl())
    
    for i, j, k in itertools.product(range(1, N + 1), range(1, N + 1), range(1, N + 1)):
        buffer.append(newlit(k, i, j, N))
    buffer.append(newcl())
    
    for k in range(1, N + 1):
        for i, j in itertools.product(range(n), range(n)):
            for l, m in itertools.product(range(n), range(n)):
                buffer.append(newlit((i * n) + l + 1, (j * n) + m + 1, k, N))
            buffer.append(newcl())
    
    for k in range(1, N + 1):
        for i, j, l in itertools.product(range(n), range(n), range(n)):
            for m in range(1, n + 1):
                for s in range(m + 1, n + 1):
                    buffer.append(notnewlit((i * n) + l + 1, (j * n) + m, k, N))
                    buffer.append(notnewlit((i * n) + l + 1, (j * n) + s, k, N))
                    buffer.append(newcl())
    
    for k in range(1, N + 1):
        for i, j in itertools.product(range(n), range(n)):
            for l in range(1, n + 1):
                for m in range(n):
                    for s in range(l + 1, n + 1):
                        for t in range(n):
                            buffer.append(notnewlit((i * n) + l, (j * n) + m + 1, k, N))
                            buffer.append(notnewlit((i * n) + s, (j * n) + t + 1, k, N))
                            buffer.append(newcl())
    
    output(''.join(buffer))

def sudoku_specific_constraints(myfile, sudoku):

    N = len(sudoku)

    def output(s):
        myfile.write(s)

    def newlit(i,j,k,N):
        if N == 4 or N == 9:
            output(str(i)+str(j)+str(k)+ " ")
        else:
            output(str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+ " ")

    def newcl():
        output("0\n")

    for i in range(N):
        for j in range(N):
            if sudoku[i][j] > 0:
                newlit(i + 1, j + 1, sudoku[i][j],N)
                newcl()

def sudoku_other_solution_constraint(myfile, sudoku, sudoku_control, gate):

    N = len(sudoku)

    def output(s):
        myfile.write(s)

    def newlit(i,j,k,N):
        if N == 4 or N == 9:
            output(str(i)+str(j)+str(k)+ " ")
        else:
            output(str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+ " ")
    def notnewlit(i,j,k,N):
        if N == 4 or N == 9:
            output("-"+str(i)+str(j)+str(k)+ " ")
        else:
            output("-"+str(i).zfill(2)+str(j).zfill(2)+str(k).zfill(2)+ " ")

    def newcl():
        output("0\n")

    for i in range(N):
        for j in range(N):
            if sudoku_control[i][j] == 0 and (sudoku[i][j] != N or gate ):
                notnewlit(i+1, j+1, sudoku[i][j],N)
                newcl()
                break


def sudoku_solve(filename):
    command = "java -jar org.sat4j.core.jar "+filename
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
            if N == 4 or N == 9 :
                for number in units:
                    sudoku[number // 100 - 1][( number // 10 )% 10 - 1] = number % 10
            elif N == 16 or N == 25 :
                for number in units:
                    sudoku[number // 10000 - 1][( number // 100 )% 100 - 1] = number % 100
            else :
                exit("strange output from SAT solver:" + line + "\n")
            return sudoku
        exit("strange output from SAT solver:" + line + "\n")
        return []

def sudoku_generate(size,mini):
    N = size
    if N == 4:
        n = 2
    elif N == 9:
        n = 3
    elif N == 16:
        n = 4
    elif N == 25:
        n = 5
    else:
        exit("Only supports size 4, 9, 16 and 25")
    sudoku_control = []
    number = []
    for i in range(N):
        sudoku_column = []
        if i < N-1:
            number.append(i+1)
        for j in range(N):
            sudoku_column.append(0)
        sudoku_control.append(sudoku_column)

    i = 0
    while i < len(number):
        row = random.randint(0,N-1)
        column = random.randint(0,N-1)
        if sudoku_control[row][column] == 0:
            sudoku_control[row][column] = number[i]
            i += 1
    myfile = open("generate.cnf", 'w')
    myfile.write("p cnf "+str(N)+str(N)+str(N)+" "+
                 str(sudoku_constraints_number(sudoku_control))+"\n")
    sudoku_generic_constraints(myfile, N)
    sudoku_specific_constraints(myfile, sudoku_control)
    myfile.close()
    sudoku= []
    #End of the initialisation

    while True:
        sudoku = sudoku_solve("generate.cnf")
        myfile = open("generate.cnf", 'a')
        sudoku_other_solution_constraint(myfile, sudoku, sudoku_control,mini)
        myfile.close()
        sudoku2 = sudoku_solve("generate.cnf")
        if sudoku2 == []:
            break
    i = 0
    while i < ((N*N)//2):
        row = random.randint(0,N-1)
        column = random.randint(0,N-1)
        if sudoku_control[row][column] == 0 and (sudoku[row][column] != N or mini):
            sudoku_control[row][column]= sudoku[row][column]
            i += 1

    return sudoku_control


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
    myfile = open("sudoku.cnf", 'w')
    # Notice that this may not be correct for N > 9
    myfile.write("p cnf "+str(N)+str(N)+str(N)+" "+
                 str(sudoku_constraints_number(sudoku))+"\n")
    sudoku_generic_constraints(myfile, N)
    sudoku_specific_constraints(myfile, sudoku)
    myfile.close()
    sys.stdout.write("sudoku\n")
    sudoku_print(sys.stdout, sudoku)
    sudoku = sudoku_solve("sudoku.cnf")
    sys.stdout.write("\nsolution\n")
    sudoku_print(sys.stdout, sudoku)
    if sudoku != [] and mode == Mode.UNIQUE:
        sudoku_control = sudoku_read(filename)
        myfile = open("sudoku.cnf", 'a')
        sudoku_other_solution_constraint(myfile, sudoku, sudoku_control,True)
        myfile.close()
        sudoku = sudoku_solve("sudoku.cnf")
        if sudoku == []:
            sys.stdout.write("\nsolution is unique\n")
        else:
            sys.stdout.write("\nother solution\n")
            sudoku_print(sys.stdout, sudoku)
elif mode == Mode.CREATE:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(size,True)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
elif mode == Mode.CREATEMIN:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(size,False)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
print("---"+ str(time.time()-start_time) +"seconds ---")
