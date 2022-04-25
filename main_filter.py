#!/usr/bin/python3

# Importing python3 from local, just use "python3 <binary>" if is not the same location

# Imports
import sys
import argparse
import os
import cv2
import numpy as np
from filter_class import Filter


# Global values
initial_img = None
first_finded_img = None
first_finded_img_bool = False
particle_nb = 30
particle_size = [30, 30]


# Function declarations
def hsv_filter_detection(img):
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	lower_hsv = np.array([0, 35, 190])
	upper_hsv = np.array([179, 255, 255])
	return cv2.inRange(img_hsv, lower_hsv, upper_hsv)


def draw_squares(img, particles_class, mode):

	if mode == "perturbation":
		particles_array = particles_class.get_particles_perturbation()
		for particle in particles_array:
			x, y, w, h = particle.get_coords()

			cv2.rectangle(img, (x, y), (x + w, y + h), (234, 160, 86), 2)
	else:
		particles_array = particles_class.get_particles()
		for particle in particles_array:
			x, y, w, h = particle.get_coords()

			if particle.get_score() > 0 and mode == "selection":
				cv2.rectangle(img, (x, y), (x + w, y + h), (234, 160, 86), 2)
			if particle.get_chosen() and mode == "chosen":
				cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
			if mode == "all":
				cv2.rectangle(img, (x, y), (x + w, y + h), (178, 178, 178), 2)


def get_img_sequence(dir_path):
	if dir_path[-1] != "/":
		dir_path += "/"

	imgs_path = [name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))]
	imgs_path = sorted(imgs_path, key=lambda x: int(os.path.splitext(x)[0]))

	imgs_path = [dir_path + i for i in imgs_path]

	return imgs_path


def first_frame_initialisation(img_shape):
	global particle_nb
	global particle_size

	return Filter(particle_nb, particle_size, img_shape[1], img_shape[0])


def draw_title(img, text):
	font = cv2.FONT_HERSHEY_SIMPLEX
	org = (10, 30)
	font_scale = 1
	color = (255, 0, 0)
	thickness = 2
	cv2.putText(img, text, org, font, font_scale, color, thickness, cv2.LINE_AA)
	return


def draw_all_images(filter_class, original_img, mask, i):
	global initial_img
	global first_finded_img
	global first_finded_img_bool

	black_img = np.zeros((original_img.shape[0], original_img.shape[1], 3), np.uint8)

	mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
	prediction_img = mask_rgb.copy()
	selection_img = mask_rgb.copy()
	chosen_img = mask_rgb.copy()
	perturbation_img = mask_rgb.copy()

	draw_squares(prediction_img, filter_class, "all")
	draw_squares(selection_img, filter_class, "selection")
	draw_squares(chosen_img, filter_class, "chosen")
	draw_squares(perturbation_img, filter_class, "perturbation")

	if i == 0:
		initial_img = prediction_img.copy()
		draw_title(initial_img, "Initialisation")

	if first_finded_img_bool is False:
		if filter_class.get_last_chosen_particle() is not None:
			first_finded_img = prediction_img.copy()
			first_finded_img_bool = True
		else:
			first_finded_img = black_img.copy()
		draw_title(first_finded_img, "First finded")

	draw_title(original_img, "Original")
	draw_title(mask_rgb, "Mask")
	draw_title(prediction_img, "Prediction")
	draw_title(selection_img, "Selection")
	draw_title(chosen_img, "Estimation")
	draw_title(perturbation_img, "Perturbation")

	tmp1 = cv2.hconcat([original_img, mask_rgb, initial_img])
	tmp2 = cv2.hconcat([first_finded_img, prediction_img, selection_img])
	tmp3 = cv2.hconcat([chosen_img, perturbation_img, black_img])
	final_img = cv2.vconcat([tmp1, tmp2, tmp3])

	cv2.imshow('hsv', final_img)
	cv2.waitKey()


def get_arguments():
	ap = argparse.ArgumentParser()

	ap.add_argument("-d", "--directory", required=True, help="Path of the data directory")
	ap.add_argument("-p", "--perturbation_differential", required=False, help="Apply perturbation with a differential method", action='store_true')

	args = vars(ap.parse_args())
	dir_path = args['directory']
	perturbation_differential = args['perturbation_differential']

	if not os.path.isdir(dir_path):
		print("[ERROR] Data directory not found")
		exit(84)

	return dir_path, perturbation_differential


def main():
	dir_path, perturbation_differential = get_arguments()
	imgs_path = get_img_sequence(dir_path)

	for i, img_path in enumerate(imgs_path):
		img = cv2.imread(img_path)
		mask = hsv_filter_detection(img)

		if i == 0:
			filter_class = first_frame_initialisation(img.shape)

		filter_class.intialise_random()

		filter_class.calculate_score(mask)
		filter_class.choose_particle()
		filter_class.perturbation(perturbation_differential)

		draw_all_images(filter_class, img, mask, i)


# Main body
if __name__ == '__main__':
	main()
