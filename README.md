# reverseProxy_NextBus
A semantic reverse proxy service for NextBus, the San Francisco’s public transportation information feed.
This is a reverse proxy for NextBus (http://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf), written in Python. It could redirect the queries to the server, without explosing the information of the server. The reverse proxy service is provided via REST API. Besides, an statistic of slow queries are also provided with an customer configurable time value. 
It uses semantic knowledge base at the backend, with the support of an ontology and SPARQL.

### Software Required:
#### Requests: 
$ sudo pip install requests

#### rdflib:
$ sudo pip install rdflib

#### bottle:
$ sudo pip install bottle

## Run:
$ sudo sh run.sh

## Test:
$ sudo sh test.sh

## REST APIs:
To query the list of agencies:
http://localhost:3333/listAgency

To obtain a list of routes for an agency:
http://localhost:3333/listRouteOf/<agency>

To obtain the route information of a specific route for an agency:
http://localhost:3333/routeConfig/<agency>/<route>

To obtain the stop prediction information for a specific stop of a route for an angency:
http://localhost:3333/predict/<agency>/<route>/<stopId>

To obtain the statistic information of queries slower than a customer configurable time value:
http://localhost:3333/showStat/<time>
It will show a list of endpoints with query time slower than the specfic value, and the number of requests for each endpoint.

### example:
{"slow_queries": 
{"http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=ecu": "0.523815", 
"http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ecu&stopId=chrisgym&routerTag=507": "0.574047", 
"http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList": "0.434237", 
"http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ecu&r=507": "0.593672"
}, 
"queries": {
"http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=ecu": "1", 
"http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ecu&stopId=chrisgym&routerTag=507": "1", 
"http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList": "1", 
"http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ecu&r=507": "1"
}
}

### Author: Qianru Zhou 
### Email: qz1@hw.ac.uk
