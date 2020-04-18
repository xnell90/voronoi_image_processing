import numpy as np
import random
import time

from PIL import Image
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm
from voronoi_image_processing.cell_types import *
from voronoi_image_processing.miscellaneous import *

def generate_filtered_image(image, num_cells = 3000, distance = "euclidean", add_boundary = False, alternate_cell_color = False, display_new_image = True):
	old_img = Image.open(image)
	new_img = Image.new("RGB", old_img.size)
	img_x   = old_img.size[0]
	img_y   = old_img.size[1]

	cells = get_cells(num_cells, img_x, img_y, alternate_cell_color)
	ctr_pts = np.array([list(cell.center_point) for cell in cells])
	all_pts_x = [[x, y] for x in range(img_x) for y in range(img_y)]

	params = {'n_neighbors': 1, 'algorithm': 'auto', 'metric': distance}
	nn_model = NearestNeighbors(**params)
	nn_model.fit(ctr_pts)

	start_time = time.time()

	np_all_pts_x = np.array(all_pts_x)
	_, indices = nn_model.kneighbors(np_all_pts_x)
	indices = [int(index) for index in indices]

	end_time = time.time()
	duration = round(end_time - start_time, 2)

	tqdm_params = {
		'desc': "1) Assigning Points To A Cell ",
		'total': len(indices)
	}
	for pt, min_i in tqdm(zip(all_pts_x, indices), **tqdm_params):
		cells[min_i].neighbor_points.append(tuple(pt))
		cells[min_i].update_cell_color(old_img.getpixel(tuple(pt)))

	if alternate_cell_color:

		for cell in tqdm(cells, desc = "2) Creating A New Filtered Image "):
			points = cell.neighbor_points
			colors = cell.cell_colors

			for neighbor_point, color in zip(points, colors):
				new_img.putpixel(neighbor_point, color)
	else:

		for cell in tqdm(cells, desc = "2) Creating A New Filtered Image "):
			color = cell.cell_color

			for neighbor_point in cell.neighbor_points:
				new_img.putpixel(neighbor_point, color)

	if add_boundary:

		row_pair_pixels = zip(all_pts_x, all_pts_x[1:])
		row_params = {
			'total': len(all_pts_x[1:]),
			'desc': "3) Drawing Boundaries (Part 1) "
		}

		for pt1, pt2 in tqdm(row_pair_pixels, **row_params):
			rgb_pt1 = new_img.getpixel(tuple(pt1))
			rgb_pt2 = new_img.getpixel(tuple(pt2))

			if forms_boundary(rgb_pt1, rgb_pt2, alternate_cell_color = alternate_cell_color):
				new_img.putpixel(tuple(pt1), (0, 0, 0))

		all_pts_y = [[x, y] for y in range(img_y) for x in range(img_x)]

		col_pair_pixels = zip(all_pts_y, all_pts_y[1:])
		col_params = {
			'total': len(all_pts_y[1:]),
			'desc': "3) Drawing Boundaries (Part 2) "
		}

		for pt1, pt2 in tqdm(col_pair_pixels, **col_params):
			rgb_pt1 = new_img.getpixel(tuple(pt1))
			rgb_pt2 = new_img.getpixel(tuple(pt2))

			if forms_boundary(rgb_pt1, rgb_pt2, alternate_cell_color = alternate_cell_color):
				new_img.putpixel(tuple(pt1), (0, 0, 0))

	print("0) Prior to Step 1, Ran Nearest Neighbor Algorithm For %s secs " % duration)

	file = image.split(".")
	file_name, file_type = file[0], file[1]
	new_img.save(file_name + "_filtered." + file_type)
	
	if display_new_image: new_img.show()
