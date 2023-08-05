# bountycountry-python
Python library for the Bounty Country API

The Bounty Country Python library provides convenient access to the Bounty Country API for applications written in the Python language. 

## Documentation

See the [Python API docs](https://bountycountry.com/apidocs/).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

    pip install --upgrade bountycountry

Install from source with:

    python setup.py install

### Requirements

- Python 3+ 
- Requests >= 2.20

## Usage

The library needs to be configured with your account's public key and secret key which are
available in your [Bounty Country Dashboard](https://bountycountry.com/api). 

Set `bountycountry.BC_PUBLIC_KEY` to your public key value. 
Set `bountycountry.BC_SECRET_KEY` to your secret key value. 


```python
import bountycountry

bountycountry.BC_PUBLIC_KEY = "....your.public.key.here...."
bountycountry.BC_SECRET_KEY = "....your.secret.key.here...."
```

### Stream a live dataset
```python
# First define a handler that will do 'something' (you decide) to each batch of items received.
def myHandler(batch):
  for item in batch:
    #do something with each item
    print(item)
  
bountycountry.getLiveStream('dataset-id-goes-here', BatchSize=250, StreamHandler=myHandler)
```
The `getLiveStream` function will indefinitely poll Bounty Country for the latest data and implement an exponential backoff (starting with a 2 second wait) if there is no new data before retrying. 


### Get a specific time range within a stream 

A specific time range in the last 24 hours of data in a stream can be queried using `bountycountry.getStreamRange`. 

Timestamps must be expressed in EpochTime format integers:
```python
import time 

# get the current time as integer epochtime
currenttime = int(time.time())

# convert ISO8601 time stamp to integer epochtime 
epochtime = int(time.mktime(time.strptime("2019-04-01 19:20:00", "%Y-%m-%d %H:%M:%S")))

```

The Stream Range is a **python generator** so you can iterate over each batch/page of items returned using any loop. 
By default a batch will return 250 items.   

```python
# create generator
results = bountycountry.getStreamRange('dataset-id-goes-here', FromTime = 1554106800, ToTime = 1554109000)

# iterate over batches/pages 
for batch in results:
    for item in batch:
        print(item)
```
#### OPTIONS
If a FromTime and ToTime are not provided the function returns the 250 newest items in the stream
* FromTime - epoch timestamp of the earliest point in time to query
* ToTime - epoch timestamp of the latest point in time to query
* Order - the order in which to return results (options = 'Newest','Oldest', default = 'Newest')
* Limit - function will stop when Limit number of items have been returned (default = None, format = integer)
* AutoPaginate - function will paginate through results until there are no more available OR until Limit is reached (default = True)
* Last - if AutoPaginate is False and there are more results to paginate ('Last' will be a key in results), you can manually pass the 'Last' result to function to begin new query time range (format = integer epoch timestamp)
* BatchSize - the number of results to return per request/page (maximum of 250, default=250, format = integer)


### Post items to a Stream

The `getLiveStream` function will upload your items in batches of 25. Items can be accepted in one of three formats:
* 'array' - accepts a python array of strings or objects. Objects will be json-serialized.
* 'lines' - reads a file (provide a string path) line by line and uploads each line as an individual item
* 'dir' - reads all files in a directory (provide a string path) and uploads the text contexts. Non-utf-8 encoded files are skipped.

```python
items = [
    {"somekey":[{"something nested":"value","somethingelsenested":"somevalue"}],
    "a string",
    "another string",
    "final string"
]

bountycountry.postStream('dataset-id-goes-here', items, format='array')
```

<!--
# vim: set tw=79:
-->
