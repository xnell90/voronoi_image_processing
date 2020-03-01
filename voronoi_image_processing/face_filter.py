import cvlib as cv
import matplotlib.pyplot as plt
import math
import numpy as np
import random

from PIL import Image
from tqdm import tqdm
from voronoi_image_processing.cell_types import *

def generate_face_filter(image_name, num_cells = 800, distance = "euclidean", alternate = False):
    old_img = Image.open(image_name)
    new_img = old_img.copy()
    faces, confidences = cv.detect_face(np.array(new_img))

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

    for ind, face in enumerate(faces):
        (x_i, y_i) = face[0], face[1]
        (x_f, y_f) = face[2], face[3]

        for i in tqdm(range(num_cells), desc = "1) Face " + str(ind + 1)):
            cpx = random.randrange(x_i, x_f)
            cpy = random.randrange(y_i, y_f)
            cp  = (cpx, cpy)

            if alternate:
                new_cell = ColorCell(cp, is_gray = (i % 2 == 0))
                cells.append(new_cell)
            else:
                cells.append(StandardCell(cp))

        ctr_pts = [ cell.center_point for cell in cells ]
        facial_pts = [
            (x, y)
            for x in range(x_i, x_f)
            for y in range(y_i, y_f)
        ]

        for pt in tqdm(facial_pts, desc = "2) Face " + str(ind + 1)):
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
            for cell in tqdm(cells, desc = "3) Face " + str(ind + 1)):
                points = cell.neighbor_points
                colors = cell.cell_colors

                for neighbor_point, color in zip(points, colors):
                    new_img.putpixel(neighbor_point, color)
        else:
            for cell in tqdm(cells, desc = "3) Face " + str(ind + 1)):
                color = cell.cell_color

                for neighbor_point in cell.neighbor_points:
                    new_img.putpixel(neighbor_point, color)

        cells = []

    new_img_name = input("Enter new image name: ")
    new_img.save(new_img_name + ".jpg")
    new_img.show()
