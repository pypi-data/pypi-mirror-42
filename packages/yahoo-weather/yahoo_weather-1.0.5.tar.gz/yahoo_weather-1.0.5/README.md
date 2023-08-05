# Python Library for Yahoo Weather New API
Since 3,Jan 2019 yahoo has changed its Weather API with Oauth1 Authentication. This new method has added an authentication to use the API. This library helps you to handle the new API.
In order to use the new API you have to get API key from [YAHOO](https://developer.yahoo.com/weather/?guccounter=1)


```
from yahoo_weather import yahoo_weather
from yahoo_weather.config.units import Unit

data = Yahoo_Weather(APP_ID="Your App ID",
                     apikey="Your API KEY",
                     apisecret="Your API secret")
data.get_yahoo_weather_by_city("tehran", Unit.celsius)
print(data.condition.text)
print(data.condition.temperature)
data.get_yahoo_weather_by_location(35.67194, 51.424438)
```

