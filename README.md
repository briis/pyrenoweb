# Python Wrapper for RenoWeb Garbage System API

A module to retrieve Garbage Collection data for Danish Municipalities that are using RenoWeb

You need a Municipality ID and a Address ID to get the Sensor Data. In order to get this run the following:

`renoweb.py find <municipality name> <road name> <house number>` - this will return the following, if the data is found:

```txt
ID NUMBERS
**************************
MUNICIPALITY ID: XXX
ADDRESS ID: YYYYY
ADDRESS: Streetname number, ZipCode City
````

You will need the *MUNICIPALITY ID* and *ADDRESS ID* to retrieve your Pick-Up Schedule.

Now you can test and validate the sensor data, by running `renoweb.py data <Municipality ID> <Address ID>`. This should output the data for your address.

There is also the possibility to run some individual processes, that are all steps in the *find* process above:

1. `renoweb.py municipality` - Check if your Municipality is supported and get the ID if they are.
2. `renoweb.py road <municipality id> <road name>` - Use the ID from step 1 and type the name of the road you live on. This returns a Road ID for use in step 3.
3. `renoweb.py address <municipality id> <road id> <house number>` - Use ID from step 2 as road_id and type your House Number. Returns an Address ID, that you need for getting the sensor data.

## CREDITS

This module is solely based on the work done by **Jacob Henriksen**, **@esbenr** and **@AngelFreak**, who did all the work in sniffing out the API and Keys. I took their work and just converted it in to a Home Assistant Integration.
