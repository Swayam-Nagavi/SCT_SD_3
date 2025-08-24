import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.cell_size = 50
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        size = self.cell_size * 9
        self.canvas = tk.Canvas(root, width=size+2, height=size+2, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.draw_grid()
        self.create_entries()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Solve", width=10, command=self.solve).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Clear", width=10, command=self.clear).grid(row=0, column=1, padx=10)

    def draw_grid(self):
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            x = i * self.cell_size + 0.5
            self.canvas.create_line(x, 0.5, x, self.cell_size*9+0.5, width=width, fill="black")
            y = i * self.cell_size + 0.5
            self.canvas.create_line(0.5, y, self.cell_size*9+0.5, y, width=width, fill="black")

    def create_entries(self):
        for row in range(9):
            for col in range(9):
                vcmd = (self.root.register(self.validate_entry), "%P", row, col)
                entry = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center",
                                 bd=0, highlightthickness=0,
                                 validate="key", validatecommand=vcmd)
                self.entries[row][col] = entry
                self.canvas.create_window(col*self.cell_size + self.cell_size/2 + 0.5,
                                          row*self.cell_size + self.cell_size/2 + 0.5,
                                          window=entry, width=self.cell_size-5, height=self.cell_size-5)

    def validate_entry(self, new_value, row, col):
        row, col = int(row), int(col)
        if new_value == "":
            return True
        if len(new_value) == 1 and new_value.isdigit() and 1 <= int(new_value) <= 9:
            num = int(new_value)
            grid = self.get_grid()
            grid[row][col] = 0  # pretend this cell empty before checking
            return self.is_valid(grid, row, col, num)
        return False

    def get_grid(self):
        grid = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.entries[r][c].get().strip()
                row.append(int(val) if val else 0)
            grid.append(row)
        return grid

    def set_grid(self, grid):
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)
                if grid[r][c] != 0:
                    self.entries[r][c].insert(0, str(grid[r][c]))

    def clear(self):
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)

    def solve(self):
        grid = self.get_grid()
        if self.solve_sudoku(grid):
            self.set_grid(grid)
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists")

    def solve_sudoku(self, grid):
        empty = self.find_empty(grid)
        if not empty:
            return True
        r, c = empty
        for num in range(1, 10):
            if self.is_valid(grid, r, c, num):
                grid[r][c] = num
                if self.solve_sudoku(grid):
                    return True
                grid[r][c] = 0
        return False

    def find_empty(self, grid):
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return r, c
        return None

    def is_valid(self, grid, row, col, num):
        if num in grid[row]:
            return False
        if num in [grid[r][col] for r in range(9)]:
            return False
        sr, sc = 3*(row//3), 3*(col//3)
        for r in range(sr, sr+3):
            for c in range(sc, sc+3):
                if grid[r][c] == num:
                    return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
