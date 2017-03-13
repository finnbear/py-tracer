
import sys
import math
import time
import numpy
import pygame
import random
import datetime

max_fps = 10
surface_width = 500
surface_height = 500
display_caption = "Py-Ray"

camera_position = (0, 0, 3)
camera_orientation = (0, 0, -1)
camera_fov = math.pi / 3;

max_spf = float(1) / max_fps
pygame.init()
surface = pygame.display.set_mode((surface_width, surface_height))
pygame.display.set_caption(display_caption)

def lerp(value, leftMin, leftMax, rightMin, rightMax):
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin
	valueScaled = float(value - leftMin) / float(leftSpan)

	return rightMin + (valueScaled * rightSpan)

def distance(point1, point2):
	point1_X, point1_Y, point1_Z = point1
	point2_X, point2_Y, point2_Z = point2

	square_X = math.pow(point1_X - point2_X, 2)
	square_Y = math.pow(point1_Y - point2_Y, 2)
	square_Z = math.pow(point1_Z - point2_Z, 2)
	
	return math.sqrt(square_X + square_Y + square_Z)

def magnitude(vector):
	vector_x, vector_y, vector_z = vector
	return math.sqrt(math.pow(vector_x, 2) + math.pow(vector_y, 2) + math.pow(vector_z, 2))

def normalize(vector):
	magVector = magnitude(vector)
	vector_x, vector_y, vector_z = vector
	return (vector_x / magVector, vector_y / magVector, vector_z / magVector)

def dot(vector1, vector2):
	vector1_X, vector1_Y, vector1_Z = vector1
	vector2_X, vector2_Y, vector2_Z = vector2
	
	product_X = vector1_X * vector2_X
	product_Y = vector1_Y * vector2_Y
	product_Z = vector1_Z * vector2_Z
	
	return product_X + product_Y + product_Z

def angle(vector1, vector2):
	vector1_X, vector1_Y, vector1_Z = vector1
	vector2_X, vector2_Y, vector2_Z = vector2
	
	dot_Vector1Vector2 = dot(vector1, vector2)
	mag_Vector1Vector2 = magnitude(vector1) * magnitude(vector2)
	return math.acos(dot_Vector1Vector2 / mag_Vector1Vector2)

def distanceVecPoint(A, B, P):
	A_x, A_y, A_z = A
	B_x, B_y, B_z = B
	P_x, P_y, P_z = P

	sum_AP = (A_x + P_x, A_y + P_y, A_z + P_z)
	dist_AP = distance(A, P)
	angle_BP = angle(B, sum_AP)
	return dist_AP * math.sin(angle_BP)

#print(distanceVecPoint((0,1,0), (0,1,0), (1, 1, 0)))
#print(angle((0,4,8), (0, 3,1)) * 180 / math.pi)

def trace(x, y):
	I = (0, 0, 0) # Illumination

	# Camera math
	camera_px, camera_py, camera_pz = camera_position
	camera_ox, camera_oy, camera_oz = camera_orientation
	camera_fov_x = math.atan(camera_fov)
	camera_fov_y = math.atan(camera_fov)
	
	# Ray vector math
	V_x = lerp(x, 0, surface_width, -camera_fov_x, camera_fov_x)
	V_y = lerp(y, 0, surface_height, -camera_fov_y, camera_fov_y)
	V_z = camera_oz
	V = (V_x, V_y, V_z)
	V = normalize(V)
	
	d1 = distanceVecPoint(camera_position, V, (1, 2, 2))	
	
	if d1 < 0.6:
		I = (100, int(1 / (1 + math.exp(d1 * 2)) * 500), 0)
	
	d2 = distanceVecPoint(camera_position, V, (-0.8, -0.8, 0))	
	
	if d2 < 0.5:
		I = (int(1 / (1 + math.exp(d2 * 2)) * 500), 100, 255)
	return I

running = True

while (running):
	t0 = datetime.datetime.now()
	
	pixels = numpy.zeros((surface_width, surface_height))

	for y in xrange(surface_height):
		for x in xrange(surface_width):
			r, g, b = trace(x, y)
			pixels[x,y] = (r << 16 | g << 8 | b)
	pygame.surfarray.blit_array(surface, pixels)
	
	t1 = datetime.datetime.now()
	
	tDelta = (t1 - t0).total_seconds()
	
	if (max_spf > tDelta):
		time.sleep(max_spf - tDelta)

	pygame.display.flip()

	pygame.image.save(surface, "frame.png")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
pygame.quit()
sys.exit()
