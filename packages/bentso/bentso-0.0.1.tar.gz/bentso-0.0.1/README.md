# bentso

A library to process ENTSO-E electricity data for use in industrial ecology and life cycle assessment. Developed as part of the [BONSAI](https://bonsai.uno/) network.

## Installation

### Pip/virtualenv

Create a new virtual environment, and install the development version of bentso:

    pip install https://github.com/BONSAMURAIS/bentso/archive/master.zip

### Conda

Create a new Conda environment:

    conda create -n bentso -y -q -c conda-forge python=3.7 requests pytz pandas beautifulsoup4 appdirs docopt

Install development version of bentso:

    pip install https://github.com/BONSAMURAIS/bentso/archive/master.zip

### Developers

Create a new Conda environment:

    conda create -n bentso -y -q -c conda-forge python=3.7 requests pytz pandas beautifulsoup4 pytest appdirs docopt

Install entsoe-py:

    pip install entsoe-py

Then clone the [Github repo](https://github.com/BONSAMURAIS/bentso) to a working directory.

## Example living life cycle inventory model

Living life cycle inventory models can:

* Automatically update themselves
* Provide results on multiple spatial scales
* Provide results on multiple time scales

This particular model is quite simple - we will gather the necessary data from the [ENTSO-E API](https://github.com/BONSAMURAIS/hackathon-2019),
and return it in the specified RDF format. The model should support the following capabilities:

* Be able to specify what kind of input parameters it accepts
* Validate inputs and return sensible error messages
* Cache data to avoid unncessary ENTSO-E API calls
* Function both as a command-line utility and a normal Python library

Inputs can be a list of countries (default is all countries in ENTSO-E), and a time period (default is a given year - maybe 2018?).

This model should also follow the [BONSAI Python library skeleton](https://github.com/BONSAMURAIS/python-skeleton).
