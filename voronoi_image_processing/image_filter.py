import numpy as np
import random

from PIL import Image
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm
from voronoi_image_processing.cell_types import *
from voronoi_image_processing.miscellaneous import *

def generate_image_filter(image_name, num_cells = 3000, distance = "euclidean", add_boundary = False, alternate = False):
	old_img = Image.open(image_name)
	new_img = Image.new("RGB", old_img.size)
	img_x = old_img.size[0]
	img_y = old_img.size[1]

	cells   = get_cells(num_cells, img_x, img_y, alternate)
	ctr_pts = np.array([list(cell.center_point) for cell in cells])
	all_pts_x = [(x, y) for x in range(img_x) for y in range(img_y)]

	nn_model = NearestNeighbors(n_neighbors = 1, algorithm = 'auto', metric = distance)
	nn_model.fit(ctr_pts)

	for pt in tqdm(all_pts_x, desc = "1)"):
		distance, index = nn_model.kneighbors(np.array([list(pt)]))
		min_j = int(index)
		cells[min_j].neighbor_points.append(pt)
		cells[min_j].update_cell_color(old_img.getpixel(pt))

	if alternate:

		for cell in tqdm(cells, desc = "2)"):
			points = cell.neighbor_points
			colors = cell.cell_colors

			for neighbor_point, color in zip(points, colors):
				new_img.putpixel(neighbor_point, color)
	else:

		for cell in tqdm(cells, desc = "2)"):
			color = cell.cell_color

			for neighbor_point in cell.neighbor_points:
				new_img.putpixel(neighbor_point, color)

	if add_boundary:

		row_pair_pixels = zip(all_pts_x, all_pts_x[1:])
		row_params = {'total': len(all_pts_x[1:]), 'desc': "3)"}

		for pt1, pt2 in tqdm(row_pair_pixels, **row_params):
			rgb_pt1 = new_img.getpixel(pt1)
			rgb_pt2 = new_img.getpixel(pt2)

			if forms_boundary(rgb_pt1, rgb_pt2, alternate = alternate):
				new_img.putpixel(pt1, (0, 0, 0))

		all_pts_y = [(x, y) for y in range(img_y) for x in range(img_x)]

		col_pair_pixels = zip(all_pts_y, all_pts_y[1:])
		col_params = {'total': len(all_pts_y[1:]), 'desc': "4)"}

		for pt1, pt2 in tqdm(col_pair_pixels, **col_params):
			rgb_pt1 = new_img.getpixel(pt1)
			rgb_pt2 = new_img.getpixel(pt2)

			if forms_boundary(rgb_pt1, rgb_pt2, alternate = alternate):
				new_img.putpixel(pt1, (0, 0, 0))

	new_img_name = input("Enter new image name: ")
	new_img.save(new_img_name + ".jpg")
	new_img.show()
