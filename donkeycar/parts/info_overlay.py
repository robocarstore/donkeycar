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
        
    def run(self, fps, userMode, userThrottle, userAngle, pilotThrottle, pilotAngle):
        self.add("current fps = {}".format(fps))
        
        # truncate input so it won't cover up the screen
        userThrottle = self.truncate(userThrottle)
        userAngle = self.truncate(userAngle)
        pilotThrottle =  self.truncate(pilotThrottle)
        pilotAngle = self.truncate(pilotAngle)
        
        if userMode == "user":
            self.add("user throttle = {}".format(userThrottle))
            self.add("user angle = {}".format(userAngle))
        elif userMode == "local":
            self.add("pilot throttle = {}".format(pilotThrottle))
            self.add("pilot angle = {}".format(pilotAngle))
        elif userMode == "local_angle":
            self.add("user throttle = {}".format(userThrottle))
            self.add("pilot angle = {}".format(pilotAngle))
            
        return info_list
        

class InfoOverlayWritter(object):
    '''
    Add a info overlay to the camera image
    ''' 
    
    def __init__(self, w, h):        
        self.imgWidth = w
        self.imgHeight = h
        
        # Overlay text's properties
        self.textOffset = (5, 100)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontSizeMultiplier = 2
        self.textColor = (255, 0, 0)
        self.textThickness = 1
        
    def debug(self):
        print("total info list size = " + str(len(info_list)))
        for info in info_list:
            print("writing info '{}' to img".format(info))              
        
    def writeToImg(self, img_arr, infos):
        textOrgX = int(self.textOffset[0])
        textOrgY = int(self.textOffset[1] * self.imgHeight/1000) # Text's gap relative to the image size 
        font = self.font
        fontSize = self.fontSizeMultiplier * self.imgWidth/1000 # Font's size relative to the image size
        color = self.textColor
        thickness = self.textThickness

        for idx, info in enumerate(infos):
            cv2.putText(img_arr, info, (textOrgX, textOrgY * (idx + 1)), font, fontSize, color, thickness)

        # self.debug()
        return img_arr     
    
    def run(self, img_arr):       
        if len(info_list) > 0:
            self.writeToImg(img_arr, info_list)
            info_list.clear()
            
        return img_arr