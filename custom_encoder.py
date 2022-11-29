# Since objects gotten from dynamodb is in decimals, json does not support decimals

# Hence, we need to create a custom encoder class to convert the decimals 

import json
from decimal import Decimal

#define a class that takes a JSONEncoder 
class CustomEncoder(json.JSONEncoder):
    # define a default that takes in an object
    def default(self,obj):
        #check if the object is an instance of a decimal
        if isinstance(obj, Decimal):
            #if it is true return a float version of the object
            return float(obj)

        #else return the default value of the object
        return json.JSONEncoder.default(self, obj)

        