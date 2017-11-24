# author: Qianru Zhou (qz1@hw.ac.uk)

from bottle import get, run, template, response
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
import requests
import urllib
import time
import bottle

class TestRP():
    def __init__(self):
        self.g = Graph()
        self.n = Namespace('http://home.eps.hw.ac.uk/~qz1/')
        self.file_abs = '/Users/silvia/Documents/code/reverseProxy/db/knowledgeBase.rdf'
        self.clearGraph()
        self.getGraph()
        #self.run()

    #def __del__(self):
    #    pass

    def run(self):
        run(host='localhost', port=3333 )

    def clearGraph(self):
        with open(self.file_abs, 'w') as f:
            f.write('')

    def getGraph(self):
        with open(self.file_abs, 'rb') as f: 
            response = str(f.read())
        self.g.parse(data=response, format='turtle')

    def writeGraph(self):
        with open(self.file_abs, 'a') as f:
            f.write(self.g.serialize(format = 'turtle'))

 #   @get('/listAgency')
    def listAgency(self):
#        requests.get("http://127.0.0.1").elapsed.total_seconds()
#        nf = urllib.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList')
#        start = time.time()
#        page = nf.read()
#        end = time.time()
#        nf.close()
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList'
        r = requests.get(str(url))
        now = time.time()
        self.g.add(( self.n['query'+str(now)], RDF.type, self.n['Query'] ))
        self.g.add(( self.n['query'+str(now)], self.n.hasURL, Literal(url, datatype=XSD.string) ))
        self.g.add(( self.n['query'+str(now)], self.n.takesTime, Literal(r.elapsed.total_seconds(), datatype=XSD.float) ))
        self.writeGraph()
        self.g.remove(( self.n['query'+str(now)], None, None ))

        response.content_type = 'text/plain'
        return r.content

#    @get('/listRouteOf/<agent>')
    def listRoute(self, agent):
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=%s'%str(agent)
        r = requests.get(url)
        now = time.time()
        self.g.add(( self.n['query'+str(now)], RDF.type, self.n['Query'] ))
        self.g.add(( self.n['query'+str(now)], self.n.hasURL, Literal(url, datatype=XSD.string) ))
        self.g.add(( self.n['query'+str(now)], self.n.takesTime, Literal(r.elapsed.total_seconds(), datatype=XSD.float) ))
        self.writeGraph()
        self.g.remove( (self.n['query'+str(now)], None, None) )

        response.content_type = 'text/plain'
        return r.content

    def routeConfig(self, agent, route):
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=%s&r=%s'%(agent, route)
        r = requests.get(url)
        now = time.time()
        self.g.add(( self.n['query'+str(now)], RDF.type, self.n['Query'] ))
        self.g.add(( self.n['query'+str(now)], self.n.hasURL, Literal(url, datatype=XSD.string) ))
        self.g.add(( self.n['query'+str(now)], self.n.takesTime, Literal(r.elapsed.total_seconds(), datatype=XSD.float) ))
        self.writeGraph()
        self.g.remove(( self.n['query'+str(now)], None, None ))

        response.content_type='text/plain'
        return r.content

    def predict(self, agent, route, stopId):
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=%s&stopId=%s&routerTag=%s'%(agent, stopId, route)
        r = requests.get(url)
        now = time.time()
        self.g.add(( self.n['query'+str(now)], RDF.type, self.n['Query'] ))
        self.g.add(( self.n['query'+str(now)], self.n.hasURL, Literal(url, datatype=XSD.string) ))
        self.g.add(( self.n['query'+str(now)], self.n.takesTime, Literal(r.elapsed.total_seconds(), datatype=XSD.float) ))
        self.writeGraph()
        self.g.remove(( self.n['query'+str(now)], None, None ))

        response.content_type='text/plain'
        return r.content

    def run_query(self, qstring):
    # Code from Fetching Data and Parsing Data examples
        with open('/Users/silvia/Documents/code/reverseProxy/db/knowledgeBase.rdf', 'rb') as f: 
            response = str(f.read())

        graph = Graph()
        graph.parse(data=response, format='turtle')

        reverseProxy = Namespace("http://home.eps.hw.ac.uk/~qz1/")
        q = graph.query(qstring, initNs = {'':reverseProxy, 'RDF':RDF})

        for item in q.bindings:
            print item['n'], item['t'], item['u']

        return q

    def showStat(self, minTime):
        qstr = ''' 
SELECT ?t  ?u (COUNT (?u) AS ?n) 
  WHERE { ?s :takesTime ?t; :hasURL ?u. 
filter (?t > %s)} 
group by ?t ?u
        ''' % minTime

#        print qstr
        result = {'slow_queries':{}, 'queries':{}}

        for item in self.run_query(qstr).bindings:
            result['slow_queries'].update({item['u']:item['t']})
            result['queries'].update({item['u']:item['n']})
        return result

 
if __name__ == '__main__':
    test = TestRP()
    bottle.route('/listAgency')(test.listAgency)
    bottle.route('/listRouteOf/<agent>')(test.listRoute)
    bottle.route('/routeConfig/<agent>/<route>')(test.routeConfig)
    bottle.route('/predict/<agent>/<route>/<stopId>')(test.predict)
    bottle.route('/showStat/<minTime>')(test.showStat)
    run(host='localhost', port=3333 )