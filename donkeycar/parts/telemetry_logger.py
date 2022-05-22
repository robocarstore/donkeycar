"""
Used for getting telemetry from other parts and store them in a dict, which will be converted to json in web.py
"""


class TelemetryLogger(object):

    # This allows auto create a new key if its missing
    class Vividict(dict):
        def __missing__(self, key):
            value = self[key] = type(self)()
            return value

    infos = Vividict()

    def __init__(self):
        # Default infos
        self.infos["user_mode"]
        self.infos["throttle"]
        self.infos["angle"]

    def run(self, user_mode, user_throttle, user_angle, pilot_throttle, pilot_angle):
        # Update default infos
        try:
            user_throttle = round(user_throttle, 3)
            user_angle = round(user_angle, 3)
            pilot_throttle = round(pilot_throttle, 3)
            pilot_angle = round(pilot_angle, 3)
        except TypeError:
            pass

        self.infos["user_mode"] = user_mode
        if user_mode == "user":
            self.infos["throttle"] = user_throttle
            self.infos["angle"] = user_angle
        elif user_mode == "local":
            self.infos["throttle"] = pilot_throttle
            self.infos["angle"] = pilot_angle
        elif user_mode == "local_angle":
            self.infos["throttle"] = user_throttle
            self.infos["angle"] = pilot_angle

        return self.infos

    def shutdown(self):
        pass
