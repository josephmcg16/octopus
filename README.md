# octopus

A python library for interfacing with the [Octopus Energy API](https://developer.octopus.energy/).

To setup the directory, navigate to the root folder

`cd <root-directory>\octopus`

Then to install dependencies using pip:

`pip install -r requirements.txt`

To configure the `main.py` script for useage, create a file called `config.yaml` then populate with your details. E.g.:

```
api_key: $API_KEY
electricity_meterpoint_mpan: your_electricity_meter_mpan
electricity_serial_number: your_electricity_meter_serial_number
gas_meterpoint_mpan: your_gas_meter_mpan
gas_serial_number: your_electricity_meter_serial_number
```

The `$API_KEY variable can be generated directly from Octopus [here](https://octopus.energy/dashboard/new/accounts/personal-details/api-access).