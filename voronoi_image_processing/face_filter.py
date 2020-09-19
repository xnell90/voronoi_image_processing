import cvlib as cv
import numpy as np
import os
import random
import time

from PIL import Image
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm
from .cell_types import *
from .miscellaneous import *

DEFAULT_FACE_FILTER_SETTINGS = {
    'num_cells': 800,
    'distance': 'euclidean',
    'add_boundary': False,
    'alternate_cell_color': False,
    'display_new_image': True
}

def generate_filtered_faces(image, settings = DEFAULT_FACE_FILTER_SETTINGS):
    distance  = settings['distance']
    num_cells = settings['num_cells']
    add_boundary = settings['add_boundary']
    alternate_cell_color = settings['alternate_cell_color']

    display_new_image = settings['display_new_image']

    old_img = Image.open(image)
    new_img = old_img.copy()
    faces, confidences = cv.detect_face(np.array(new_img))

    for ind, face in enumerate(faces):
        (x_i, y_i) = min(face[0], old_img.size[0]), min(face[1], old_img.size[1])
        (x_f, y_f) = min(face[2], old_img.size[0]), min(face[3], old_img.size[1])

        cells   = get_cells(num_cells, (x_i, x_f), (y_i, y_f), alternate_cell_color)
        ctr_pts = np.array([list(cell.center_point) for cell in cells])
        facial_pts_x = [
            (x, y)
            for x in range(x_i, x_f)
            for y in range(y_i, y_f)
        ]

        params = {'n_neighbors': 1, 'algorithm': 'auto', 'metric': distance}
        nn_model = NearestNeighbors(**params)
        nn_model.fit(ctr_pts)

        start_time = time.time()

        np_facial_pts_x = np.array([list(pt) for pt in facial_pts_x])
        _, indices = nn_model.kneighbors(np_facial_pts_x)
        indices = [int(index) for index in indices]

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        face_num = str(ind + 1)
        tqdm_params = {
            'desc': "1) Assigning Points To A Cell For Face %s" % face_num,
            'total': len(indices)
        }
        for pt, min_i in tqdm(zip(facial_pts_x, indices), **tqdm_params):
            cells[min_i].neighbor_points.append(pt)
            cells[min_i].update_cell_color(old_img.getpixel(pt))

        if alternate_cell_color:
            loading_message = (
                "2) Creating A New Filtered Image For Face %s" % face_num
            )
            for cell in tqdm(cells, desc = loading_message):
                points = cell.neighbor_points
                colors = cell.cell_colors

                for neighbor_point, color in zip(points, colors):
                    new_img.putpixel(neighbor_point, color)
        else:
            loading_message = (
                "2) Creating A New Filtered Image For Face %s" % face_num
            )
            for cell in tqdm(cells, desc = loading_message):
                color = cell.cell_color

                for neighbor_point in cell.neighbor_points:
                    new_img.putpixel(neighbor_point, color)

        if add_boundary:

            row_pair_pixels = zip(facial_pts_x, facial_pts_x[1:])
            row_params = {
                'total': len(facial_pts_x[1:]),
                'desc': "3) Drawing Boundaries (Part 1) For Face %s" % face_num
            }

            for pt1, pt2 in tqdm(row_pair_pixels, **row_params):
                rgb_pt1 = new_img.getpixel(pt1)
                rgb_pt2 = new_img.getpixel(pt2)

                if forms_boundary(rgb_pt1, rgb_pt2, alternate_cell_color):
                    new_img.putpixel(pt1, (0, 0, 0))

            facial_pts_y = [
                (x, y)
                for y in range(y_i, y_f)
                for x in range(x_i, x_f)
            ]

            col_pair_pixels = zip(facial_pts_y, facial_pts_y[1:])
            col_params = {
                'total': len(facial_pts_y[1:]),
                'desc': "3) Drawing Boundaries (Part 2) For Face %s" % face_num
            }

            for pt1, pt2 in tqdm(col_pair_pixels, **col_params):
                rgb_pt1 = new_img.getpixel(pt1)
                rgb_pt2 = new_img.getpixel(pt2)

                if forms_boundary(rgb_pt1, rgb_pt2, alternate_cell_color):
                    new_img.putpixel(pt1, (0, 0, 0))

        print("0) Prior to Step 1, Ran Nearest Neighbor Algorithm For %s secs on Face %s " % (duration, face_num))

    file = image.split(".")
    file_name, file_type = file[0], file[1]
    new_img.save(file_name + "_filtered." + file_type)

    if display_new_image: new_img.show()

def generate_filtered_faces_directory(image_directory, settings = DEFAULT_FACE_FILTER_SETTINGS):
    image_list = os.listdir(image_directory)
    num_images = len(image_list)

    for i, image in enumerate(image_list):
        print("Processing %s, %d / %d" % (image, i + 1, num_images))
        generate_filtered_faces(image_directory + image, settings)
