import numpy as np
import scipy as sp
import random
from operator import itemgetter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Penguin(object):

	def __init__(self, radius, position, alignment):
		"""
		Arguments:
			radius		:=	float representing penguin radius
			position	:=	numpy array representing penguin position (x, y, z)
			alignment	:=	numpy array representing alignment unit vector
			boundary	:=	boolean value, True if boundary penguin, False if bulk penguin
		"""

		self.radius = radius
		self.position = position
		self.alignment = alignment
		self.boundary = False

	def __str__(self):

		return "Penguin located at ({}, {})".format(self.position[0], self.position[1])

	def __repr__(self):

		return self.__str__()

	def get_distance(self, penguin2):

		return self.position - penguin2.position

	def determine_boundary_condition(self, penguin_list, a):

		critical_radius = 2.0 * a

		theta_list = []

		for i in range(len(penguin_list)):

			if (penguin_list[i] != self):

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)

				if (r_mag < critical_radius):

					theta = np.arctan2(r[1],r[0])
					theta_list.append(theta)

		theta_list.sort()

		for j in range(len(theta_list)):

			try:

				difference = theta_list[j+1] - theta_list[j]

			except IndexError:

				difference =  (np.pi - theta_list[j]) + (theta_list[0] + np.pi)

			# print(difference * 180 / np.pi)

			if (difference >= np.pi):

				self.boundary = True

				return True

			else:

				self.boundary = False

	def find_exterior_bisector(self, penguin_list, a):

		critical_radius = 1.5 * a

		r_theta_list = []

		for i in range(len(penguin_list)):

			if (penguin_list[i] != self):

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)

				if (r_mag < critical_radius):

					theta = np.arctan2(r[1],r[0])
					r_theta_list.append([r,theta])

		r_theta_list = sorted(r_theta_list, key=itemgetter(1))

		for j in range(len(r_theta_list)):

			try:

				a = j
				b = j+1
				difference = r_theta_list[b][1] - r_theta_list[a][1]

			except IndexError:

				a = 0
				b = j
				difference =  (np.pi - r_theta_list[b][1]) + (r_theta_list[a][1] + np.pi)

			if (difference >= np.pi):

				self.boundary = True

				exterior_bisector = -1.0 * (r_theta_list[a][0] + r_theta_list[b][0])

				angle1 = np.arctan2(r_theta_list[a][0][1], r_theta_list[a][0][0]) * 180 / np.pi
				angle2 = np.arctan2(r_theta_list[b][0][1], r_theta_list[b][0][0]) * 180 / np.pi

				# bisector_angle = (angle1 + angle2) / 2.0

				# exterior_bisector = np.array([np.cos(bisector_angle), np.sin(bisector_angle)])

				if (exterior_bisector[0] == 0) and (exterior_bisector[1] == 0):

					if (angle1 == 0) and (angle2 == 180):

						exterior_bisector = np.array([0.0,-1.0])

					if (angle1 == 180) and (angle2 == 0):

						exterior_bisector = np.array([0.0,1.0])

					if (angle1 == 90) and (angle2 == -90):

						exterior_bisector = np.array([-1.0,0.0])

					if (angle1 == -90) and (angle2 == 90):

						exterior_bisector = np.array([1.0,0.0])

					



				return exterior_bisector

			else:

				self.boundary = False


	# def find_net_force(self, F_self, F_in, k, penguin_list, a):

	# 	critical_radius = 1.3 * a

	# 	F_self_propulsion = F_self * self.alignment

	# 	F_repulsion = np.zeros(3) 

	# 	for i in range(len(penguin_list)):

a = 1.0
penguin_list = []

for i in range(5):
	for j in range(5):

			x = i + random.uniform(-0.2,0.2)
			y = j + random.uniform(-0.2,0.2)

			radius = a

			position = np.array([x,y])

			alignment = np.array([1,1])

			penguin = Penguin(a, position, alignment)
			penguin_list.append(penguin)

# penguin1 = Penguin(a, np.array([-0.5,0]), np.array([1,1]))
# penguin2 = Penguin(a, np.array([0.5,0]), np.array([1,1]))
# penguin3 = Penguin(a, np.array([0,-0.5]), np.array([1,1]))
# penguin4 = Penguin(a, np.array([0,0.5]), np.array([1,1]))
# penguin5 = Penguin(a, np.array([0,0]), np.array([1,1]))

# penguin_list.append(penguin1)
# penguin_list.append(penguin2)
# penguin_list.append(penguin3)
# penguin_list.append(penguin4)
# penguin_list.append(penguin5)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

for penguin in penguin_list:

	print penguin

	exterior_bisector = penguin.find_exterior_bisector(penguin_list, a)

	print exterior_bisector

	# print penguin.boundary

	if penguin.boundary == True:

		plt.plot(penguin.position[0], penguin.position[1], "ro")

	else:

		plt.plot(penguin.position[0], penguin.position[1], "bo")

plt.xlim([-1,5])
plt.ylim([-1,5])
plt.show()

















