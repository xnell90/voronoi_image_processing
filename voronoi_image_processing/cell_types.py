class StandardCell:
    
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
