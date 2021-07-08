import cv2

info_list = []

class InfoOverlayLogger(object):
    '''
    Log infos
    ''' 
    
    def add(self,string):     
        info_list.append(string)

    def truncate(self, input):
        if input != None:
            input = str(input)[:4]
        return input
        
    def run(self, fps, user_mode, user_throttle, user_angle, pilot_throttle, pilot_angle):
        self.add("current fps = {}".format(fps))
        
        # truncate input so it won't cover up the screen
        user_throttle = self.truncate(user_throttle)
        user_angle = self.truncate(user_angle)
        pilot_throttle =  self.truncate(pilot_throttle)
        pilot_angle = self.truncate(pilot_angle)
        
        if user_mode == "user":
            self.add("user throttle = {}".format(user_throttle))
            self.add("user angle = {}".format(user_angle))
        elif user_mode == "local":
            self.add("pilot throttle = {}".format(pilot_throttle))
            self.add("pilot angle = {}".format(pilot_angle))
        elif user_mode == "local_angle":
            self.add("user throttle = {}".format(user_throttle))
            self.add("pilot angle = {}".format(pilot_angle))
            
        return info_list
        

class InfoOverlayWritter(object):
    '''
    Add a info overlay to the camera image
    ''' 
    
    def __init__(self, w, h):        
        self.img_width = w
        self.img_height = h
        
        # Overlay text's properties
        self.text_offset = (5, 100)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size_multiplier = 2
        self.text_color = (255, 0, 0)
        self.text_thickness = 1
        
    def debug(self):
        print("total info list size = " + str(len(info_list)))
        for info in info_list:
            print("writing info '{}' to img".format(info))              
        
    def writeToImg(self, img_arr, infos):
        text_x = int(self.text_offset[0])
        text_y = int(self.text_offset[1] * self.img_height/1000) # Text's gap relative to the image size 
        font = self.font
        font_size = self.font_size_multiplier * self.img_width/1000 # Font's size relative to the image size
        color = self.text_color
        thickness = self.text_thickness

        for idx, info in enumerate(infos):
            cv2.putText(img_arr, info, (text_x, text_y * (idx + 1)), font, font_size, color, thickness)

        # self.debug()
        return img_arr     
    
    def run(self, img_arr):       
        if len(info_list) > 0:
            self.writeToImg(img_arr, info_list)
            info_list.clear()
            
        return img_arr