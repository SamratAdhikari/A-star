from node import Node, COLORS
import math
from queue import PriorityQueue
import pygame

# game constants
WIDTH = 800
HEIGHT = 800
ROWS = 50


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A*')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))



# heuristic function -> uses Manhattan distance : straight L line
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2

	return abs(x1-x2) + abs(y1-y2)


def construct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, source, dest):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, source))
	came_from = {}
	
	g_score = {node: float('inf') for row in grid for node in row}
	g_score[source] = 0
	f_score = {node: float('inf') for row in grid for node in row}
	f_score[source] = h(source.get_pos(), dest.get_pos())

	open_set_hash = {source}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] #get only the node from the set
		open_set_hash.remove(current)

		if current == dest:
			construct_path(came_from, dest, draw)
			dest.make_dest()
			source.make_source()
			return True

		for neighbour in current.neighbours:
			temp_g_score = g_score[current] + 1
			if temp_g_score < g_score[neighbour]:
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), dest.get_pos())

				if neighbour not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbour], count, neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()

		draw()
		if current != source:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = [] # list of lists
	gap = width // rows

	for i in range(rows):
		grid.append([])

		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows

	for i in range(rows):
		pygame.draw.line(win, COLORS['GREY'], (0, i*gap), (width, i*gap))

	for j in range(rows):
		pygame.draw.line(win, COLORS['GREY'], (j*gap, 0), (j*gap, width))


def draw(win, grid, rows, width):
	win.fill(COLORS['WHITE'])

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	grid = make_grid(ROWS, width)
	source = None
	dest = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					grid = make_grid(ROWS, width)
					source = None
					dest = None

				elif event.key == pygame.K_SPACE and source and dest:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, source, dest)


			if pygame.mouse.get_pressed()[0]: # left btn
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				try:
					node = grid[row][col]
				except:
					pass

				if not source and node != dest:
					source = node
					source.make_source()

				elif not dest and node != source:
					dest = node
					dest.make_dest()

				elif node != source and node != dest and source and dest:
					node.make_barrier()


			elif pygame.mouse.get_pressed()[2]: # right bth
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				try:
					node = grid[row][col]
					node.reset()
				except:
					pass

				if node == source:
					source = None
				elif node == dest:
					dest = None

	pygame.quit()


if __name__ == '__main__':
	main(WIN, WIDTH)