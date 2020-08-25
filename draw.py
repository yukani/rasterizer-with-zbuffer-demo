#
# Triangle rasterizer with z-buffer demo - 27/5/2020
#

import math				# for ceil and inf
import numpy as np		# for vector operations
from PIL import Image	# for drawing

pout_str = input("Print draw calls? (slow): [y/N]")
pout = True if pout_str.lower() == "y" else False # prints putpixel calls and z-buffer discard logs for triangle rasterizer when enabled, slows program.

width, height = 980, 800

image = Image.new('RGB', (width, height))

# Initialize z-buffer with +Infinity values.
zbuffer = [[math.inf for x in range(width)] for y in range(height)]

def drawline(p1, p2, color):
	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]

	# if two points are the same.
	if dx == 0 and dy == 0: return
	elif dx == 0:
		# if the line is vertical.

		for y in range(abs(dy) + 1):
			if dy >= 0: image.putpixel((p1[0], p1[1] + y), color)
			else: image.putpixel((p1[0], p1[1] - y), color)
	elif dy == 0:
		# if the line is horizontal.

		for x in range(abs(dx) + 1):
			if dx >= 0: image.putpixel((p1[0] + x, p1[1]), color)
			else: image.putpixel((p1[0] - x, p1[1]), color)
	else:
		if abs(dx) >= abs(dy): step = abs(dx)
		else: step = abs(dy)

		dx /= step
		dy /= step

		x, y = p1[0], p1[1]

		for i in range(step + 1):
			image.putpixel((int(x), int(y)), color)
			x += dx
			y += dy
def drawtriangle(vp1, vp2, vp3, color):
	# sort by y
	if vp1[1] > vp2[1]: vp1, vp2 = vp2, vp1
	if vp2[1] > vp3[1]: vp2, vp3 = vp3, vp2
	if vp1[1] > vp2[1]: vp1, vp2 = vp2, vp1

	if vp1[1] == vp2[1]:
		# sort by x
		if vp1[0] > vp2[0]: vp1, vp2 = vp2, vp1
		drawtoptriangle(vp1, vp2, vp3, color)

	elif vp2[1] == vp3[1]:
		# sort by x
		if vp2[0] > vp3[0]: vp2, vp3 = vp3, vp2
		drawbottomtriangle(vp1, vp2, vp3, color)
	
	else:
		alpha = (vp2[1] - vp1[1]) / (vp3[1] - vp1[1])
		vi = vp1 + (vp3 - vp1) * alpha

		if vi[0] > vp1[0]:
			# major right
			drawbottomtriangle(vp1, vp2, vi, color)
			drawtoptriangle(vp2, vi, vp3, color)
		else:
			# major left
			drawbottomtriangle(vp1, vi, vp2, color)
			drawtoptriangle(vi, vp2, vp3, color)
def drawtoptriangle(v0, v1, v2, color):
	# m = x / y; change in x for y.
	m0 = (v2[0] - v0[0]) / (v2[1] - v0[1]) # first x location
	m1 = (v2[0] - v1[0]) / (v2[1] - v1[1]) # last x location

	yStart = math.ceil(v0[1] - 0.5)
	yEnd = math.ceil(v2[1] - 0.5)

	for y in range(yStart, yEnd):
		px0 = m0 * (y + 0.5 - v0[1]) + v0[0]
		px1 = m1 * (y + 0.5 - v1[1]) + v1[0]

		xStart = math.ceil(px0 - 0.5)
		xEnd = math.ceil(px1 - 0.5)

		for x in range(xStart, xEnd):
			if zbuffer[x][y] > v2[2]:
				if pout: print("T: putpixel(%d, %d)" % (x, y))
				image.putpixel((x, y), color)
				zbuffer[x][y] = v2[2]
			elif pout: print("T: zbuffer excluded.")
def drawbottomtriangle(v0, v1, v2, color):
	# m = x / y; change in x for y.
	m0 = (v1[0] - v0[0]) / (v1[1] - v0[1])
	m1 = (v2[0] - v0[0]) / (v2[1] - v0[1])

	yStart = math.ceil(v0[1] - 0.5)
	yEnd = math.ceil(v2[1] - 0.5)

	for y in range(yStart, yEnd):
		px0 = m0 * (y + 0.5 - v0[1]) + v0[0] # first x location
		px1 = m1 * (y + 0.5 - v0[1]) + v0[0] # last x location

		xStart = math.ceil(px0 - 0.5)
		xEnd = math.ceil(px1 - 0.5)

		for x in range(xStart, xEnd):
			if zbuffer[x][y] > v2[2]:
				if pout: print("B: putpixel(%d, %d)" % (x, y))
				image.putpixel((x, y), color)
				zbuffer[x][y] = v2[2]
			elif pout: print("B: zbuffer excluded.")

# 1st & 2nd triangle's verticies
verts1 = [ np.array([400, 200, 15]), np.array([450, 600, 15]), np.array([200, 400, 15]) ]
verts2 = [ np.array([280, 350, 20]), np.array([300, 200, 20]), np.array([420, 470, 20]) ]

# draw 1st and 2nd triangles
drawtriangle(verts1[0], verts1[1], verts1[2], (255, 255, 0))
drawtriangle(verts2[0], verts2[1], verts2[2], (0, 255, 255))

# draw 1st and 2nd triangles with inverse Z order
drawtriangle(verts1[0] + np.array([300,0,5]), verts1[1] + np.array([300,0,5]), verts1[2] + np.array([300,0,5]), (255, 255, 0))

drawtriangle(verts2[0] + np.array([300,0,-5]), verts2[1] + np.array([300,0,-5]), verts2[2] + np.array([300,0,-5]), (0, 255, 255))

image.show()
