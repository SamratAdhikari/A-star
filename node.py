import pygame

# color constants
COLORS = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "YELLOW": (255, 255, 0),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "PURPLE": (128, 0, 128),
    "ORANGE": (255, 165, 0),
    "GREY": (128, 128, 128),
    "BLUE": (0, 0, 255)
}

# Node to determine the position of the cells
class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row*width
		self.y = col*width
		self.color = COLORS['WHITE']
		self.neighbours = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == COLORS['RED']

	def is_open(self):
		return self.color == COLORS['BLUE']

	def is_barrier(self):
		return self.color == COLORS['BLACK']

	def is_source(self):
		return self.color == COLORS['ORANGE']

	def is_dest(self):
		return self.color == COLORS['PURPLE']

	def reset(self):
		self.color = COLORS['WHITE']

	def make_closed(self):
		self.color = COLORS['RED']

	def make_open(self):
		self.color = COLORS['BLUE']

	def make_barrier(self):
		self.color = COLORS['BLACK']

	def make_source(self):
		self.color = COLORS['ORANGE']

	def make_dest(self):
		self.color = COLORS['PURPLE']

	def make_path(self):
		self.color = COLORS['GREEN']

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbours(self, grid):
		self.neighbours = []

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #up
			self.neighbours.append(grid[self.row - 1][self.col])

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #down
			self.neighbours.append(grid[self.row + 1][self.col])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #left
			self.neighbours.append(grid[self.row][self.col - 1])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #right
			self.neighbours.append(grid[self.row][self.col + 1])



	# less than: always define that 'other' spot is greater than 'self' spot
	def __lt__(self, other): 
		return False


