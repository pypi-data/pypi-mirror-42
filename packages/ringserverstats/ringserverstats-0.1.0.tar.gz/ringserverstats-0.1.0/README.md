# ringserverstats

## Installation

ringserverstats is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 2.7/3.5+ and PyPy.

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
$ python ringser_stats tlogs.log
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
  * clienthash : a hash of the client ip (usefull to correlate the clients requests)

## License

ringserver_stats is distributed under the terms of the GPL v3 or later
