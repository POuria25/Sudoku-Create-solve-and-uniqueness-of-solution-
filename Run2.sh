#!/bin/bash

# Run the command to generate 16 random Sudoku puzzles and save the result to TXT.txt
#!/bin/bash

for ((i=1; i<=32; i++)); do
  echo "Iteration: $i"
    # Run the command to generate 16 random Sudoku puzzles and save the result to TXT.txt
    python3 sudokub.py -c 25 > "TXT_$i.txt"

    # Run the command to solve the Sudoku puzzles from TXT.txt
    python3 sudokub.py -u "TXT_$i.txt"
done
