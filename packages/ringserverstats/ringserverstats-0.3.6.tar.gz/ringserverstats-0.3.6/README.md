# ringserverstats

## Installation

ringserverstats is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel.

``` bash
    $ pip install ringserverstats
```

## Usage

To work properly, this program needs the following environment variables set :

  * `INFLUXDB_HOST` : The host name or adress of influxdb server
  * `INFLUXDB_PORT` : The port number of influxdb server
  * `INFLUXDB_USER` : The influxdb user to authenticate to
  * `INFLUXDB_PASS` : The password to authenticate with
  * `INFLUXDB_DB`   : The database name containing the metric
  * `INFLUXDB_VERIFY_SSL` : Set to `yes` or `no` to verify SSL connection

``` bash
$ python ringserstats txlogs.log
```

## Explanations

The TX logs from ringserver are metrics suitable for a timeserie database. The idea is to parse the logs, as in the exemple below, and to generate values to insert into an influxdb timeseries database.

The file grafana_dashboard.json can be imported into grafana to visualize this timeserie.

Used tags in influxdb :

``` sql
show tag keys from ringserver
```

The ringserver measure has several tags :

  * network, station, location, channel : which data was requested
  * geohash : location of the client in geohash format
  * hosthash : a hash of the client ip (usefull to correlate the clients requests)

## License

ringserverstats is distributed under the terms of the GPL v3 or later. See LICENSE file.

## Build

``` shell
python3 setup.py sdist bdist_wheel
```

## Test

``` shell
tox
```
