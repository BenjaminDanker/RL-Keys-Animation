from os import walk
from copy import copy
from win32api import GetAsyncKeyState
import numpy
import cv2


# reads respective images from path and places numpy image arrays into lists
def read_images(file_format):
	image_keydown_lst, image_keyup_lst = [], []
	image_mouse_dic = {}

	for num, (path, directory_names, file_names) in enumerate(walk("CompositePics")):
		if num != 0:
			if path == "CompositePics\\KeyboardDown":
				for c in file_names:
					image_keydown_lst.append(numpy.array(cv2.imread(path + "\\" + c, cv2.IMREAD_UNCHANGED)))

			if path == "CompositePics\\KeyboardUp":
				for c in file_names:
					image_keyup_lst.append(numpy.array(cv2.imread(path + "\\" + c, cv2.IMREAD_UNCHANGED)))

			if path == "CompositePics\\Mouse":
				for c in file_names:
					image_mouse_dic.update({c.replace(file_format, "") : numpy.array(cv2.imread(path + "\\" + c, cv2.IMREAD_UNCHANGED))})
	
	return image_keydown_lst, image_keyup_lst, image_mouse_dic


# checks keyboard and mouse positions
def keys_position():
	lstkeyboard = [
			GetAsyncKeyState(0x51), # Q
			GetAsyncKeyState(0x57), # W
			GetAsyncKeyState(0x45), # E
			GetAsyncKeyState(0x41), # A
			GetAsyncKeyState(0x53), # S
			GetAsyncKeyState(0x44), # D
			GetAsyncKeyState(0x46), # F
			GetAsyncKeyState(0xA0), # Shift
			GetAsyncKeyState(0x20), # Space
			]
	lstmouse = [
			GetAsyncKeyState(0x01), # Left Mouse
			GetAsyncKeyState(0x02), # Right Mouse
			GetAsyncKeyState(0x04), # Middle Mouse
			]


	return lstkeyboard,lstmouse


# places all keys and mouse images into numpy array 
def create_image(lstkeyboard, lstmouse, image_keydown_lst, image_keyup_lst, image_mouse_dic, alpha_image):
	display_image = copy(alpha_image)
	for check, img_down, img_up in zip(lstkeyboard, image_keydown_lst, image_keyup_lst):
		if check:
			img = img_down
		else:
			img = img_up
		
		numpy.copyto(display_image, img, where=img != 0)
	

	tmp_name = ""
	lstmousebuttons = ["M1","M2","M3"]
	for check, mouse in zip(lstmouse, lstmousebuttons):
		if check:
			tmp_name += mouse
	if not tmp_name:
		tmp_name = "Mouse"
	img = image_mouse_dic[tmp_name]

	numpy.copyto(display_image, img, where=img != 0)


	return display_image


# OpenCV animation
def animation(display_image):
	cv2.imshow("RL GUI", display_image)

	cv2.waitKey(20)



if __name__ == "__main__":
	file_format = ".png"
	image_keydown_lst, image_keyup_lst, image_mouse_dic = read_images(file_format)
	alpha_image = cv2.imread("CompositePics/Alpha.png", cv2.IMREAD_UNCHANGED)

	while 1:
		lstkeyboard, lstmouse = keys_position()
		display_image = create_image(lstkeyboard, lstmouse, image_keydown_lst, image_keyup_lst, image_mouse_dic, alpha_image)
		animation(display_image)