from PIL import Image
from tqdm import tqdm
import random
import math

class Cell:
	def __init__(self, center_point):
		self.center_point    = center_point
		self.neighbor_points = []
		self.cell_color 	 = (0, 0, 0)

	def update_cell_color(self, color):
		old_r = self.cell_color[0]
		old_g = self.cell_color[1]
		old_b = self.cell_color[2]

		num_neighbors = len(self.neighbor_points)

		new_r = (old_r * (num_neighbors - 1) + color[0]) / num_neighbors
		new_g = (old_g * (num_neighbors - 1) + color[1]) / num_neighbors
		new_b = (old_b * (num_neighbors - 1) + color[2]) / num_neighbors

		self.cell_color = (
			round(new_r),
			round(new_g),
			round(new_b)
		)

def generate_filter(num_cells, image_name, distance = "euclidean", add_boundary = False):
	old_img = Image.open(image_name)
	img_x = old_img.size[0]
	img_y = old_img.size[1]
	new_img = Image.new("RGB", (img_x, img_y))

	if distance == 'manhattan':
		metric = lambda x, a, y, b: math.fabs(x - a) + math.fabs(y - b)
	elif distance == 'max_norm':
		metric = lambda x, a, y, b: max(math.fabs(x - a), math.fabs(y - b))
	else:
		metric = lambda x, a, y, b: math.hypot(x - a, y - b)

	cells = []

	for _ in tqdm(range(num_cells), desc = "1)"):
		cpx = random.randrange(img_x)
		cpy = random.randrange(img_y)
		cp  = (cpx, cpy)
		cells.append(Cell(cp))

	ctr_pts   = [ cell.center_point for cell in cells ]
	all_pts_x = [ (x, y) for x in range(img_x) for y in range(img_y) ]

	for pt in tqdm(all_pts_x, desc = "2)"):
		x, y  = pt[0], pt[1]
		ctr_x = ctr_pts[0][0]
		ctr_y = ctr_pts[0][1]

		min_d = metric(x, ctr_x, y, ctr_y)
		min_j = 0

		for i in range(1, num_cells):
			ctr_x = ctr_pts[i][0]
			ctr_y = ctr_pts[i][1]
			d = metric(x, ctr_x, y, ctr_y)

			if d < min_d:
				min_d = d
				min_j = i

		cells[min_j].neighbor_points.append(pt)
		cells[min_j].update_cell_color(old_img.getpixel(pt))

	for cell in tqdm(cells, desc = "3)"):
		color = cell.cell_color

		for neighbor_point in cell.neighbor_points:
			new_img.putpixel(neighbor_point, color)


	if add_boundary:

		for pt1, pt2 in tqdm(zip(all_pts_x, all_pts_x[1:]), total = len(all_pts_x[1:]), desc = "4)"):
			if new_img.getpixel(pt1) != new_img.getpixel(pt2):
				new_img.putpixel(pt1, (0 , 0, 0))

		all_pts_y = [ (x, y) for y in range(img_y) for x in range(img_x) ]

		for pt1, pt2 in tqdm(zip(all_pts_y, all_pts_y[1:]), total = len(all_pts_y[1:]), desc = "5)"):
			if new_img.getpixel(pt1) != new_img.getpixel(pt2):
				new_img.putpixel(pt1, (0 , 0, 0))

	new_img_name = input("Enter new image name: ")
	new_img.save(new_img_name + ".jpg")
	new_img.show()
