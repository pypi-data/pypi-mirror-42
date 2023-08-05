[![PyPI version](https://badge.fury.io/py/tapclipy.svg)](https://badge.fury.io/py/tapclipy) [![https://img.shields.io/badge/license-Apache%202.0-blue.svg](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

# TapCliPy
Python Client Library for [TAP](https://github.com/heta-io/tap)

# What is Tap Client?
The Tap client is a python library for accessing [TAP](https://github.com/heta-io/tap) (Text Analytics Pipeline)
This allows you to use all the available queries easily from python or command line.

# Benefits of Tap Client
- The client can be hosted online enabling large scale development
- The client can be run with the command line enabling you to pipe the output to any other applications you need.
- The ability to chain multiple queries together and pass in the results from one queries into another.
- The ability to batch queries together and analyse hundreds if not thousands of documents hosted on an s3 bucket.

# Who Uses Tap?
Tap is used by many organisations to analyse large volumes of text and provide analytics on the types of language used. 
This is useful for analysing feedback and/ or surveys provided by staff or students and provide useful information.

# Frequently Asked Questions

## Can i use it locally?
Sure can, You are able to run TAP using Docker locally or even just run it on command line. See the current docs [here](https://heta-io.github.io/tap/overview/quick_start.html#get-started-locally-without-docker)

## Can i host it online?
Sure can, You are able to host it online with a simple Droplet from Digital Ocean, AWS or any hosted Docker instance. See the current docs [here](https://heta-io.github.io/tap/overview/quick_start.html#run-docker-on-digital-ocean)

## Is the client required to use TAP?
Nope, The client enables you to easily interact with TAP, however it is not required to use and run queries with TAP. You can interact with TAP using the command line or using the GraphQl interface. See the [TAP docs](https://heta-io.github.io/tap/index.html) for more info

## Does Tap client scale well?
Yes! It scales very well and is able to batch many queries together and process large volumes of data asynchronously.

### Installation

Install with pip:

```bash
> pip install tapclipy
```

### Basic Example

```python

from tapclipy import tap_connect

# Create TAP Connection
tap = tap_connect.Connect('http://tap.yourdomain.com')

# Get and print the Current Schema
tap.fetch_schema()
for query,type in tap.schema_query_name_types().items():
    print("{} >> {}".format(query, type))
print("----------------------------------------------")

# Analyse some text for some basic metrics
query = tap.query('metrics')
text = "This is a very small test of TAP. It should produce some metrics on these two sentences!"
json = tap.analyse_text(query, text)

print()
print("METRICS:\n", json)

```

should output:

```

visible >> StringResult
clean >> StringResult
cleanPreserve >> StringResult
cleanMinimal >> StringResult
cleanAscii >> StringResult
annotations >> SentencesResult
vocabulary >> VocabResult
metrics >> MetricsResult
expressions >> ExpressionsResult
syllables >> syllables
spelling >> SpellingResult
posStats >> PosStatsResult
reflectExpressions >> ReflectExpressionsResult
moves >> StringListResult
----------------------------------------------

METRICS:
 {'data': {'metrics': {'analytics': {'words': 17, 'sentences': 2, 'sentWordCounts': [8, 9], 'averageSentWordCount': 8.5}}}}

Process finished with exit code 0

```

### Currently available queries

| Query | Return Type |
|-------|-------------|
| visible | `StringResult` |
| clean | `StringResult` |
| cleanPreserve | `StringResult` |
| cleanMinimal | `StringResult` |
| cleanAscii | `StringResult` |
| annotations | `SentencesResult` |
| vocabulary | `VocabResult` |
| metrics | `MetricsResult` |
| expressions | `ExpressionsResult` |
| syllables | `syllables` |
| spelling | `SpellingResult` |
| posStats | `PosStatsResult` |
| reflectExpressions | `ReflectExpressionsResult` |
| moves | `StringListResult` |
