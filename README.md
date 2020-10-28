# Python Wrapper for RenoWeb Garbage System API

A module to retrieve Garbage Collection data for Danish Municipalities that are using RenoWeb

You need a Municipality ID and a Address ID to get the Sensor Data. In order to get this run the following in exactly this order:

1. `renoweb.py kommuner` - Check if your Municipality is supported and get the ID if they are.
2. `renoweb.py vej <municipality_id> <road name>` - Use the ID from step 1 and type the name of the road you live on. This returns a Road ID for use in step 3.
3. `renoweb.py adresse <municipality_id> <road_id> <house number>` - Use ID from step 2 as road_id and type your House Number. Returns an Address ID, that you need for getting the sensor data.

After this you have to ID's you need to retrieve Pick Up data:

* *Municipality ID* from Step 1
* *Address ID* from Step 3

Now you can test and validate the sensor data, by running `renoweb.py data <Municipality ID> <Address ID>`. This should output the data for your address.

This module is solely based on the work done by @esbenr and @AngelFreak, who did all the work in sniffing out the API and Keys, thank you Guys.
