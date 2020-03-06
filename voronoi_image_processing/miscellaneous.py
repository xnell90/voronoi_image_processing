import math

def get_metric(distance):
	if distance == 'manhattan':
		metric = lambda x, a, y, b: math.fabs(x - a) + math.fabs(y - b)
	elif distance == 'max_norm':
		metric = lambda x, a, y, b: max(math.fabs(x - a), math.fabs(y - b))
	elif distance == 'euclidean':
		metric = lambda x, a, y, b: math.hypot(x - a, y - b)
	else:
		metric = False

	return metric

def forms_boundary(p1, p2, alternate = False):
	if not alternate: return p1 != p2

	r1, g1, b1 = p1[0], p1[1], p1[2]
	r2, g2, b2 = p2[0], p2[1], p2[2]

	is_p1_gray = (r1 == g1 and g1 == b1)
	is_p2_gray = (r2 == g2 and g2 == b2)

	return (is_p1_gray and not is_p2_gray) or (not is_p1_gray and is_p2_gray)
