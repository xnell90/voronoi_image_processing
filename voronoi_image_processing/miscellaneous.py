def forms_boundary(p1, p2, alternate = False):
	if not alternate: return p1 != p2

	r1, g1, b1 = p1[0], p1[1], p1[2]
	r2, g2, b2 = p2[0], p2[1], p2[2]

	is_p1_gray = (r1 == g1 and g1 == b1)
	is_p2_gray = (r2 == g2 and g2 == b2)

	return (is_p1_gray and not is_p2_gray) or (not is_p1_gray and is_p2_gray)
