import math
import random

from .cell_types import *
from PIL import Image
from tqdm import tqdm

def __is_boundary(p1, p2, alternate = False):
	if not alternate:
		return p1 != p2

	r1, g1, b1 = p1[0], p1[1], p1[2]
	r2, g2, b2 = p2[0], p2[1], p2[2]

	is_p1_gray = (r1 == g1 and g1 == b1)
	is_p2_gray = (r2 == g2 and g2 == b2)

	return (is_p1_gray and not is_p2_gray) or (not is_p1_gray and is_p2_gray)

def generate_filter(num_cells, image_name, distance = "euclidean", add_boundary = False, alternate = False):
	old_img = Image.open(image_name)
	img_x = old_img.size[0]
	img_y = old_img.size[1]
	new_img = Image.new("RGB", (img_x, img_y))

	if distance == 'manhattan':
		metric = lambda x, a, y, b: math.fabs(x - a) + math.fabs(y - b)
	elif distance == 'max_norm':
		metric = lambda x, a, y, b: max(math.fabs(x - a), math.fabs(y - b))
	elif distance == 'euclidean':
		metric = lambda x, a, y, b: math.hypot(x - a, y - b)
	else:
		print("Error: distance function does not exist...")
		return

	cells = []

	for i in tqdm(range(num_cells), desc = "1)"):
		cpx = random.randrange(img_x)
		cpy = random.randrange(img_y)
		cp  = (cpx, cpy)

		if alternate:
			is_gray = (i % 2 == 0)
			new_cell = ColorCell(cp, is_gray = is_gray)
			cells.append(new_cell)
		else:
			cells.append(StandardCell(cp))

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

	if alternate:
		for cell in tqdm(cells, desc = "3)"):
			points = cell.neighbor_points
			colors = cell.cell_colors

			for neighbor_point, color in zip(points, colors):
				new_img.putpixel(neighbor_point, color)
	else:
		for cell in tqdm(cells, desc = "3)"):
			color = cell.cell_color

			for neighbor_point in cell.neighbor_points:
				new_img.putpixel(neighbor_point, color)

	if add_boundary:

		row_pair_pixels = zip(all_pts_x, all_pts_x[1:])
		row_params = {'total': len(all_pts_x[1:]), 'desc': "4)"}

		for pt1, pt2 in tqdm(row_pair_pixels, **row_params):
			rgb_pt1 = new_img.getpixel(pt1)
			rgb_pt2 = new_img.getpixel(pt2)

			if __is_boundary(rgb_pt1, rgb_pt2, alternate = alternate):
				new_img.putpixel(pt1, (0, 0, 0))


		all_pts_y = [ (x, y) for y in range(img_y) for x in range(img_x) ]

		col_pair_pixels = zip(all_pts_y, all_pts_y[1:])
		col_params = {'total': len(all_pts_y[1:]), 'desc': "5)"}

		for pt1, pt2 in tqdm(col_pair_pixels, **col_params):
			rgb_pt1 = new_img.getpixel(pt1)
			rgb_pt2 = new_img.getpixel(pt2)

			if __is_boundary(rgb_pt1, rgb_pt2, alternate = alternate):
				new_img.putpixel(pt1, (0, 0, 0))

	new_img_name = input("Enter new image name: ")
	new_img.save(new_img_name + ".jpg")
	new_img.show()
