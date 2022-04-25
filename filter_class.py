#!/usr/bin/python3

# Importing python3 from local, just use "python3 <binary>" if is not the same location

# Imports
import sys
import argparse
import os
import cv2
import numpy as np
import random

from particle_class import Particle

# Global values


# Function declarations
class Filter:

	def __init__(self, particle_nb, particle_size, img_width, img_height):
		if img_width // 3 <= particle_size[0]:
			raise Exception("\033[1m" + "[ERROR] -> Particle size width is way to big" + "\033[0m")

		if img_height // 3 <= particle_size[1]:
			raise Exception("\033[1m" + "[ERROR] -> Particle size height is way to big" + "\033[0m")

		self.__particle_nb = particle_nb
		self.__particle_size = particle_size
		self.__img_width = img_width
		self.__img_height = img_height
		self.__particles = []
		self.__particles_perturbation = []
		self.__total_score = 0
		self.__last_chosen_particle = None

	# Randomly spawns particles in the image
	def intialise_random(self):
		if self.__last_chosen_particle and self.__particles_perturbation != []:
			self.__particles = self.__particles_perturbation
		else:
			self.__particles = []
			for i in range(self.__particle_nb):
				a = b = 0
				a2 = self.__img_width - self.__particle_size[0]
				b2 = self.__img_height - self.__particle_size[1]

				x_part = random.randint(a, a2)
				y_part = random.randint(b, b2)

				particle = Particle(x_part, y_part, self.__particle_size[0], self.__particle_size[1], i)
				self.__particles.append(particle)

	def perturbation(self, perturbation_differential):
		self.__particles_perturbation = []

		if self.__total_score > 0:
			ids = []
			scores = []
			x_max = 0
			y_max = 0
			x_min = 10000
			y_min = 10000
			nb_particle_positiv = 0

			for particle in self.__particles:

				ids.append(particle.get_id())
				scores.append(particle.get_score())
				print(particle.get_score())

				# Getting x, y in min and max position for gaussian perturbation
				if particle.get_score() > 0:
					x, y, w, h = particle.get_coords()
					x_max = max(x, x_max)
					y_max = max(y, y_max)
					x_min = min(x, x_min)
					y_min = min(y, y_min)
					nb_particle_positiv += 1

			# Doing the roulette method
			probs = np.array(scores, dtype=int) / int(sum(scores))
			sample_np = np.random.choice(ids, self.__particle_nb, p=probs)

			# Creating a particule for each perturbation
			for i, sample in enumerate(sample_np):
				x, y, w, h = self.__particles[sample].get_coords()

				print("X " + str(x_max + self.__particle_size[0] - x_min) + "  max" + str(x_max) + "  min" + str(x_min))
				print("Y " + str(y_max + self.__particle_size[1] - y_min) + "  max" + str(y_max) + "  min" + str(y_min))

				if perturbation_differential is not True:
					x = int(np.random.normal(x, 20))
					y = int(np.random.normal(y, 20))
				elif nb_particle_positiv <= 1:
					x = int(np.random.normal(x, (x_max + self.__particle_size[0] - x_min) // 2))
					y = int(np.random.normal(y, (y_max + self.__particle_size[1] - y_min) // 2))
				else:
					x = int(np.random.normal(x, (x_max - x_min) // 2))
					y = int(np.random.normal(y, (y_max - y_min) // 2))

				# Checking that no one of the perturbation is out of range than the image
				# If yes the particle is replaced at max possible range in image
				x = max(0, x)
				y = max(0, y)
				x = min(x, self.__img_width - self.__particle_size[0])
				y = min(y, self.__img_height - self.__particle_size[1])

				particle = Particle(x, y, w, h, i)
				self.__particles_perturbation.append(particle)

	def calculate_score(self, mask):
		nb_white_pxls = np.sum(mask == 255)
		score = 0
		total_score = 0

		# Calculating the score for each particle (white pixels)
		for particle in self.__particles:
			x, y, w, h = particle.get_coords()

			if nb_white_pxls > 0:
				crop = mask[y:y+h, x:x+w]
				score = np.sum(crop == 255)
				total_score += score

			particle.set_score(score)

		self.__total_score = total_score

	# Choose the particle with most score
	def choose_particle(self):
		if self.__total_score > 0:
			id = 0
			score = 0
			for particle in self.__particles:
				if particle.get_score() >= score:
					score = particle.get_score()
					id = particle.get_id()

			self.__particles[id].set_chosen(True)
			self.__last_chosen_particle = self.__particles[id]

	def get_particles(self):
		return self.__particles

	def get_last_chosen_particle(self):
		return self.__last_chosen_particle

	def get_particles_perturbation(self):
		return self.__particles_perturbation
