import time

class FpsTimer(object):
    '''sss
    Watch a specific file and give a signal when it's modifiedfff
    '''
    def __init__(self):
        self.last_timestamp = None
        self.counter = 0
        self.fps = 0
        self.fps_list = []

    def run(self):
        '''
        return True when file changed. Keep in mind that this does not mean that the
        file is finished with modification.
        '''

        if (self.last_timestamp is None):
            self.last_timestamp = time.time()

        if (time.time() - self.last_timestamp) > 1:
            self.fps = self.counter
            self.fps_list.append(self.counter)
            self.counter = 0
            self.last_timestamp = time.time()
        else:
            self.counter += 1

        return self.fps, self.fps_list

class FpsLogger(object):
    def __init__(self):
        self.fps_list = None


    def run(self, fps, fps_list):
        '''
        Log current, min and max of fps value
        '''
        print("fps = {}".format(fps))
        self.fps_list = fps_list

    def shutdown(self):
        if self.fps_list is not None:
            print("fps (min/max) = {:2d} / {:2d}".format(min(self.fps_list), max(self.fps_list)))
            print("fps list {}".format(self.fps_list))
        self.running = False
        time.sleep(0.1)
