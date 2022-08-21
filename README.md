# Intoduction
This is a flask app with an api that gets average rates between two ports/regions.

Just to preface this, I learned flask for this task since I decided it would be the best tool for the task (creating a simple api). So there may be a few flask specific things that I have missed.

# Database Setup for non-docker installs

1. Build image
   
       docker build -t ratestask ./postgres

2. Create container
   
       docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask

# How to run the app

## How to run with docker
1. Use docker compose
        
       docker-compose up

## How to run without docker
1. Set the Virtual enviroment

       python -m venv venv

2. Activate the virtual enviroment
   
       Linux
              source venv/Scripts/activate 
       
       Windows
              .\venv\Scripts\activate.bat

3. Install required packaged

       pip install -r requirements.txt
    
4. Run the app (Assuming postgres is running)

       python ratestask/app.py

## Using the api
Now you can use access the api at port 80 and 5432 for the database

Using Curl

    curl "http://127.0.0.1/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"

Result

    [
        {
            "day": "2016-01-01",
            "average_price": 1112
        },
        {
            "day": "2016-01-02",
            "average_price": 1112
        },
        {
            "day": "2016-01-03",
            "average_price": null
        },
        ...
    ]

# How to test the app

## Testing with docker
1. Docker compose up

       docker-compose -f docker-compose.test.yml up


## Testing without docker

1. Set up the virtual enviroment

       python -m venv venv

2. Activate the virtual environment

       - for linux
              source venv/Scripts/activate
       - for windows
              .\venv\Scripts\activate.bat

3. Install the required packages

       pip install -r requirements.txt
    
4. Run the tests (Assuming postgres is running)

       python -m unittest

# Database Data definition

<!-- We are providing you with a small set of simplified real-world data. A
database dump is provided that includes the following information: -->

## Ports

Information about ports, including:

* 5-character port code
* Port name
* Slug describing which region the port belongs to

## Regions

A hierarchy of regions, including:

* Slug - a machine-readable form of the region name
* The name of the region
* Slug describing which parent region the region belongs to

Note that a region can have both ports and regions as children, and the region
tree does not have a fixed depth.

## Prices

Individual daily prices between ports, in USD.

* 5-character origin port code
* 5-character destination port code
* The day for which the price is valid
* The price in USD
