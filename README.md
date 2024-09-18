# Sudoku Game

## Overview

This is a Python-based Sudoku game that is implemented entirely on TKinter (not pygame) that allows users to solve puzzles, generate new Sudoku boards, and even check the validity of their solutions. The game is interactive, with a graphical user interface (GUI) for ease of use, making it accessible to both beginners and Sudoku enthusiasts.

## Background

The program employs an algorithm that mimics the penciling strategy used to solve Sudoku puzzles in real life, allowing it to solve any Sudoku board. While this approach is quite effective, it wasn't my original idea.

Initially, I tried solving Sudoku using a basic backtracking strategy with simple while loops. After testing it on various input boards, I quickly realized that my algorithm was inefficient, with some basic puzzles taking minutes, or even hours, to solve.

I decided to revisit the algorithm, still sticking with the backtracking approach but this time utilizing recursion. Although it was faster than my original attempt, some boards still took several minutes to solve.

After more research, I stumbled upon an advanced algorithm called Dancing Links, developed by Professor Donald Knuth. This algorithm can solve any Sudoku board with lightning speed, while also detecting unsolvable boards and identifying multiple solutions when present. A Sudoku solver using this powerful algorithm can be found on this [website](https://anysudokusolver.com/), and its main logic file is available [here](https://anysudokusolver.com/js/script.js).

However, implementing the Dancing Links algorithm on my own proved to be quite challenging. I spent many hours trying to grasp its concepts by reading Professor Knuth’s book The Art of Computer Programming (Fascicle 5: Mathematical Preliminaries Redux; Introduction to Backtracking; Dancing Links), but due to time constraints, I couldn't fully comprehend it.

Eventually, I discovered a more accessible algorithm, which I mentioned at the start, from a LeetCode user named "Ov8CfeJ3Su." Their algorithm is much easier to understand and implement. You can find it [here](https://leetcode.com/problems/sudoku-solver/solutions/5757508/recursive-backtracking-beats-99/). The core logic of my program is based on their work, while the rest of the implementation was done by me.

I have also attached a folder called **_OG codes_** which contains my original python file that has my 2 initial algorithms that I mentioned above.

## Intuition

The main idea is to emulate the manual sudoku solving algorithm of keeping track of candidate numbers for each cell, penciling in cells with only one candidate, and then updating the candidates for cells in the same row, column, and block. If we get to a point where we can no longer eliminate candidates with this approach, we guess a value for a single cell and repeat the process, backtracking if we make a wrong guess.

## Features
- **Interactive GUI**: Play Sudoku using an intuitive graphical interface.
- **Sudoku Board Generation**: Generate new Sudoku boards with varying difficulty levels.
- **Solution Checker**: Check if the current board configuration is valid and adheres to Sudoku rules.

## Installation
Download **_playSudoku.pyw_** and **_sudoku_penciling.py_**

## How to run
Double click on **_playSudoku.pyw_** and play

## How to Play
Open the game, and you’ll be presented with a new Sudoku board.
Select a cell by clicking on it, and input a number (1-9).
Use the options to generate new puzzles, check your current solution

## Controls
Click on a cell: Select the cell you want to edit.
Number keys (1-9): Input a number in the selected cell.

## Requirements
Python 3+

## Future Improvements
- Showing hints when a player is stuck
- Timer for tracking how long it takes to solve a puzzle.
- A leaderboard for tracking top scores.
- Show in real-time how the algorithm changes each cell using backtracking when solving
- Note: To edit the code, just download the 2 files **_main.py_** and **_sudoku_penciling.py_**

## License
This project is licensed under the MIT License - see the LICENSE file for details.
