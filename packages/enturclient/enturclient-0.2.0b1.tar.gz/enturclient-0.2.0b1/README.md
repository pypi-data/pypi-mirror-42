# Entur API client

Python client for fetching estimated departures from stop places in Norway from Entur.org's API. Information about stop places, platforms and real-time departures.

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

## Usage

```python
from enturclient import EnturPublicTransportData

API_CLIENT_ID = 'awesome_company-my_application' 

stops = ['NSR:StopPlace:548']
quays = ['NSR:Quay:48550']
data = EnturPublicTransportData(
        client_name=API_CLIENT_ID,
        stops=stops,
        quays=quays,
        expand_quays=False,
        omit_non_boarding=True,
        number_of_departures=5)
data.update()

bergen_train = data.get_stop_info('NSR:StopPlace:548')
bergen_train_delay = bergen_train.estimated_calls[0].delay
```

## Obtaining a stop id
 [Entur's travel planer](https://en-tur.no) has a map of all stops used in Norway. Use the map to find the stops you're interested in. When you have found one of your stops, click on it. 
 Now the web browser should contain an URL with the id in it. Such as this: 
 `https://en-tur.no/nearby-stop-place-detail?id=NSR:StopPlace:32376`
 The stop id is the content after id= parameter in the url. Copy paste this into the configuration. 

[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/heine
