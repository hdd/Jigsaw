#!/usr/bin/env python

#DOC http://snipplr.com/view/1950/graph-javascript-framework-version-001/

#    
import sys,os
import random
import math
from pprint import pformat
import networkx as nx

os.environ["DEBUG"]="0"

import hlog as log

Infinity=1000000

class SpringLayout(object):
    node_attributes=["layoutPosX","layoutPosY","layoutForceX","layoutForceY"]
    edge_attributes=["weight"]

    def __init__(self,G):
        self.graph=G
        self.iterations=500
        self.maxRepulsiveForceDistance = 6
        self.k=2
        self.c=0.01
        self.maxVertexMovement = 0.5
        self.nodes=self.graph.nodes()
        self.edges=self.graph.edges()
        
        self.layoutMinX=0.0
        self.layoutMaxX=0.0
        
        self.layoutMinY=0.0
        self.layoutMaxY=0.0        
        
        
    def layoutPrepare(self):
        for node in self.nodes:
            for attr in self.node_attributes:
                self.graph.node[node][attr]=0.0
                log.debug("adding to node %s -> attr:%s =%s"%(node,attr,self.graph.node[node][attr]))
                
        for edge in self.edges:
            for attr in self.edge_attributes:
                log.debug("edge %s"%(pformat(edge)))
                self.graph[edge[0]][edge[1]][attr]=0.0
                
    def layout(self):
        self.layoutPrepare()
        for i in range(self.iterations):
            self.layoutIteration()
        self.layoutCalcBounds()
        print pformat(self.graph.nodes(data=True))
        
    def layoutCalcBounds(self):
        minx=Infinity
        maxx=-Infinity
        miny=Infinity
        maxy=-Infinity
        
        for node in self.nodes:
            

            x=self.graph.node[node]["layoutPosX"]
            y=self.graph.node[node]["layoutPosY"]
            
            if x > maxx : maxx = x
            if x < minx : minx = x
            if y > maxy : maxy = y
            if y > miny : miny = y

        self.layoutMinX=minx
        self.layoutMaxX=maxx
        self.layoutMinY=miny
        self.layoutMaxY=maxy 
            
        
    def layoutIteration(self):
        #    Forces on nodes due to node-node repulsions
        for i in range(len(self.nodes)):
            node1=self.nodes[i]
            j = i+1
            for j in range(len(self.nodes)):
                node2=self.nodes[j]
                log.debug("repulsive on %s %s "%(node1,node2))
                self.layoutRepulsive(node1,node2)
        #    Forces on nodes due to edge attractions        
        for i in range(len(self.edges)):
            edge=self.edges[i]
            self.layoutAttractive(edge)

        # Move by the given force
        for node in self.nodes:
            xmove=self.c * self.graph.node[node]["layoutForceX"]   
            ymove=self.c * self.graph.node[node]["layoutForceY"]    
            
            max= self.maxVertexMovement
            if xmove > max : xmove = max
            if xmove < -max : xmove = -max      
            
            if ymove > max : ymove = max
            if ymove < -max : ymove = -max             
            
            self.graph.node[node]["layoutPosX"] += xmove
            self.graph.node[node]["layoutPosY"] += xmove
            
            self.graph.node[node]["layoutForceX"] =0
            self.graph.node[node]["layoutForceY"] =0
            
    def layoutRepulsive(self,node1,node2):
        dx=self.graph.node[node1]["layoutPosX"] - self.graph.node[node2]["layoutPosX"]        
        dy=self.graph.node[node1]["layoutPosY"] - self.graph.node[node2]["layoutPosY"]     
        d2=dx*dx+dy*dy
        
        if d2 < 0.01:
            dx=0.1 + random.random()+ 0.1
            dy=0.1 + random.random()+ 0.1
            d2=dx*dx+dy*dy
            
        d= math.sqrt(d2)
        if d < self.maxRepulsiveForceDistance:
            repulsiveForce = self.k * self.k / d
            self.graph.node[node2]["layoutForceX"] += repulsiveForce *dx/d
            self.graph.node[node2]["layoutForceY"]  += repulsiveForce *dy/d
            
            self.graph.node[node1]["layoutForceX"] += repulsiveForce *dx/d
            self.graph.node[node1]["layoutForceY"]  += repulsiveForce *dy/d         
                    
    def layoutAttractive(self,edge):
        
        node1=self.graph.node[edge[0]]
        node2=self.graph.node[edge[1]]
                
        dx=node2["layoutPosX"] - node1["layoutPosX"]
        dy=node2["layoutPosY"] - node1["layoutPosY"]
        
        d2=dx*dx + dy*dy
        
        if d2 < 0.01:
            dx=0.1 + random.random()+ 0.1
            dy=0.1 + random.random()+ 0.1
            d2=dx*dx+dy*dy        
                
        d= math.sqrt(d2)    
        if d > self.maxRepulsiveForceDistance:
            d=self.maxRepulsiveForceDistance
            d2=d*d
            
        attractiveForce  =(d2 -self.k *self.k)/self.k
            
        log.debug("edge weight : %s "%self.graph[edge[0]][edge[1]]["weight"])
        
        if not self.graph[edge[0]][edge[1]]["weight"] or self.graph[edge[0]][edge[1]]["weight"] < 1 :  self.graph[edge[0]][edge[1]]["weight"] = 1
        
        node2["layoutForceX"] -= attractiveForce * dx / d
        node2["layoutForceY"] -= attractiveForce * dy / d

        node1["layoutForceX"] += attractiveForce * dx / d
        node1["layoutForceY"] += attractiveForce * dy / d   
        

import networkx as nx       
def DRAW_GRAPH():
    G=nx.DiGraph(name="Test")
    
    A="Test1"
    B="TestA"
    C="PIPPO"
    D="PIPPA"
    E="ENNIO"
    F="ENNIO2"

    A1="Test2"
    B1="Test3"
    C1="PIPP4"
    D1="PIPP5"
    E1="ENNI6"
    F1="ENNIO7"
        
    G.add_node(A)
    G.add_node(B)
    G.add_edge(A,B)   
    
    G.add_node(C)
    G.add_edge(A,C)      
    
    G.add_node(D)
    G.add_edge(B,D)

    G.add_node(E)
    G.add_node(F)
    
    G.add_edge(B,E)
    G.add_edge(D,F)
    
    return G     


Spring = SpringLayout(DRAW_GRAPH())
Spring.layout()