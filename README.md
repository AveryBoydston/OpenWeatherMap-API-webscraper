# OpenWeatherMap API webscraper
Accesses the OpenWeatherMap API and gathers the next 48 hours of relevant weather information. The program sends the requested information as a text message to any cell phone number via an SMS gateway. Finally, it stores the resulting information locally each time the program runs for later data analysis.

The Driver file can be executed to run the entire program. The openweathermap_api performs the collection of the data and the calculations, as well as creates the final output message. If the program fails in any way, it notifies me that a problem has occurred so that I can debug it.

This program requires specific file location names and will not work correctly on unsupported devices. It is best executed at the start of the day or in the middle of the day for helpful information.

This program originally accessed 5 weather API's (Meteo, Tomorrow.IO, VisualCrossing, OpenWeatherMap, Weather.gov) results and the combined data was intended to be more accurate and helpful for the user, but the data from other free weather APIs turned out to be less accurate, updated less frequently, and was over all not as consistent as OpenWeatherMap.

You can ignore the pickcomputer.py as it is for personal use and all other files referring to other weather APIs that are not OpenWeatherMap