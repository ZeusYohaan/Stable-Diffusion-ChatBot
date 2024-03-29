from pyowm import OWM
import os


class GetWeather:
    def __init__(self):
        self.OWM_KEY = "9baa21ea92fbb0f3d3111b0d421a5df9"
        self.owm = OWM(self.OWM_KEY)
        self.manager = self.owm.weather_manager()

    def getWeatherCity(self, city):
        weather_ = self.manager.weather_at_place(city)
        weather_data = weather_.weather
        dict_ = {'status': weather_data.detailed_status, 'humidity': weather_data.humidity,
                 'temperature': weather_data.temperature('celsius')['temp']}

        return dict_

