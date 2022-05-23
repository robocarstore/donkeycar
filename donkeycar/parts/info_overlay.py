"""
Add a info overlay to the camera image
"""

import cv2


class InfoOverlayer(object):

    def __init__(self, w, h):

        # Store the infos which will be write to image
        self.info_list = []

        # Camera image's size
        self.img_width = w
        self.img_height = h

        # Overlay text's properties
        self.text_offset = (5, 50)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size_multiplier = 1
        self.text_color = (255, 255, 255)
        self.text_thickness = 1

    def getInfos(self, input_dict, parents=""):
        # Recursively convert the dict into string and add it into the info list
        for key, value in input_dict.items():
            new_parents = parents + str(key) + ": "
            if isinstance(value, dict):
                self.getInfos(value, new_parents)
            else:
                info = str(new_parents) + str(value)
                self.info_list.append(info)

    def writeToImg(self, input_img):
        # Config overlay texts
        text_x = int(self.text_offset[0])       
        text_y = int(self.text_offset[1] * self.img_height / 1000)      # Text's gap relative to the image size
        font = self.font
        font_size = self.font_size_multiplier * self.img_width / 1000   # Font's size relative to the image size
        color = self.text_color
        thickness = self.text_thickness

        # Write each info onto images
        for idx, info in enumerate(self.info_list):
            cv2.putText(input_img, info, (text_x, text_y * (idx + 1)),
                        font, font_size, color, thickness)

    def run(self, img_arr, infos):

        if infos is not None:
            self.getInfos(infos)

            # Write infos
            new_img_arr = None
            if img_arr is not None:
                new_img_arr = img_arr.copy()

            if len(self.info_list) > 0:
                self.writeToImg(new_img_arr)
                self.info_list.clear()

            return new_img_arr
        else:
            print("no info received")
            return img_arr
