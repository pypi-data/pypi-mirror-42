# Overview

SDK to assist in connecting to AirTM API.

# Setup

## Requirements

* Python 3.6+

## Installation

Install AirTM SDK with pip:

```sh
$ pip install airtm
```

or directly from the source code:

```sh
$ git clone git@bitbucket.org:airtm/payments-sdk-python.git
$ cd payments-sdk-python
$ python setup.py install
```

## Testing the Installation

After installation, you can verify everything installed correctly using the simple sequence of commands:

```sh
$ python
>>> import airtm
>>> airtm.__version__
```

# Usage

## Initializing the API Client

To make any call successfully, developers need to initialize the API client with the following:

* Partner ID
* Partner Secret
* API Host, i.e. sandbox or production

The manner in which these values are stored is up to the developer. 

### Using a Configuration File

The SDK comes with a file called `airtm.ini.template`. You can use this file as the basis for your own configuration file. The config file groups properties by environment, allowing developers to maintain credentials for all their environments in one place. 

Load the config file as follows:

```python
import configparser
config = configparser.ConfigParser()
config.read('airtm.ini')
id     = config['sandbox']['PartnerID']
secret = config['sandbox']['PartnerSecret']
host   = config['sandbox']['ServiceHost']
api = AirTM( id, secret, host )
```

### Using Environment Variables

```python
import os
id     = os.environ['AIRTM_PARTNER_ID']
secret = os.environ['AIRTM_PARTNER_SECRET']
host   = os.environ['AIRTM_SERVICE_HOST']
api = AirTM( id, secret, host )
```

## Debug Mode

Developers can turn on debug mode to help troubleshoot problems using the API by setting the debug flag to true. This can be done upon initialization:

```python
api = AirTM( id, secret, host, True )
```

Or, manually:

```python
api.debug = True
```

## Creating a Purchase

```python
api = AirTM( id, secret, host, True )
p1 = Purchase()
p1.code         = "a1b2c3d4e5f6g7h8i9j0"
p1.description  = "A description for this purchase"
p1.redirect_uri = "https://yourcompany.com/purchase/success"
p1.cancel_uri   = "https://yourcompany.com/purchase/canceled"
p1.add_item('some description',1.00,1)
p1.add_item('some other description',6.00,1)
p1.add_item('yet another description',14.25,1)
try:
    p2 = api.create_purchase(p1)
    print p2.id
except APIError as e:
    print "An error occurred: " + e.value
```

Don't forget, once the purchase has been created, you will need to redirect the user to the following URL in order to confirm the transaction:

`http://purchases.airtm.io/checking/:id`

# Registering 

In order to access the API, you will need to contact [partners@airtm.io](mailto:partners@airtm.io) to obtain the necessary credentials for your account. 

# Support

If you experience trouble using the API or this SDK, please contact [partners@airtm.io](mailto:partners@airtm.io) with a detailed description of your problem. 