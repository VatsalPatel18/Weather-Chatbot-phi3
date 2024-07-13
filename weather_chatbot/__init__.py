from .download_model import download_model
from .functions import get_weather_info, get_forecast, restructure_forecast, shutdown

# Ensure the model is downloaded when the package is imported
download_model()
