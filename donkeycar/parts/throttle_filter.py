
class ThrottleFilter(object):
    '''
    allow reverse to trigger automatic reverse throttle
    '''

    def __init__(self):
        self.reverse_triggered = False
        self.last_throttle = 0.0

    def run(self, throttle_in):
        throttle_out = throttle_in
        # As pilot's throttle and angle maybe None type      
        if throttle_in != None:
            if throttle_out < 0.0:
                if not self.reverse_triggered and self.last_throttle < 0.0:
                    throttle_out = 0.0
                    self.reverse_triggered = True                
            else:
                self.reverse_triggered = False   

            self.last_throttle = throttle_out        
        return throttle_out

    def shutdown(self):
        pass
