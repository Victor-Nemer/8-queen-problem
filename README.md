# ♕ 8 Queens Problem

A Python desktop app that solves the classic **8 Queens problem** and lets you play it yourself.

## Features
- **Solution explorer:** browse all **92 distinct solutions**, generated at startup with a recursive backtracking algorithm.
- **Timed mini-game:** place the 8 queens yourself in **90 seconds**. Invalid moves flash red, and you can click a queen to remove it.
- Dark-themed GUI built with Tkinter.

## How it works
The solver places one queen per row. After each placement it marks the squares that queen attacks (column and both diagonals), recurses to the next row, and undoes the marks when backtracking. Every time it reaches row 8, it saves the board as a solution.

## Run it
Requires Python 3 (Tkinter is included with the standard installation).

```bash
git clone https://github.com/Victor-Nemer/8-queen-problem.git
cd 8-queen-problem
python reina.py
```

## Tech
Python · Tkinter · Backtracking

## Author
[Victor Nemer](https://github.com/Victor-Nemer)
