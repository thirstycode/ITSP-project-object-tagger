# import the necessary packages
from supporting_files.panorama import Stitcher
import argparse
import imutils
import cv2


def stitch(initial,changing):
	# # load the two images and resize them to have a width of 400 pixels
	# # (for faster processing)
	# #	TODO
	stitcher = Stitcher()
	result= stitcher.stitch([initial, changing])
	return result
