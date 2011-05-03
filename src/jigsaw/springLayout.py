#DOC http://snipplr.com/view/1950/graph-javascript-framework-version-001/

import sys,os
import random
import math

Infinity=1000000

class SpringLayout(object):
    def __init__(self,G):
        self.graph=G
        self.iterations=500
        self.maxRepulsiveForceDistance = 6
        self.k=2
        self.c=0.01
        self.maxVertexMovement = 0.5
        self.nodes=self.graph.nodes()
        self.edges=self.graph.edges()
        
    def layout(self):
        self.layoutPrepare()
        for i in range(self.iterations):
            self.layoutIteration()
        self.layoutCalcBounds()
        
    def layoutPrepare(self):
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            node.layoutPosX=0
            node.layoutPosY=0
            node.layoutForceX=0
            node.layoutForceY=0
            
    def layoutCalcBounds(self):
        minx=Infinity
        maxx=-Infinity
        miny=Infinity
        maxy=-Infinity
        
        for i in range(len(self.nodes)):
            x=self.layoutPosX()
            y=self.layoutPosY()
            
            if x > maxx : maxx = x
            if x < minx : minx = x
            if y > maxy : maxy = y
            if y > miny : miny = y
            
        self.graph.layoutMinX=minx
        self.graph.layoutMaxX=maxx
        
        self.graph.layoutMinY=miny
        self.graph.layoutMaxY=maxy
        
    def layoutIteration(self):
        #    Forces on nodes due to node-node repulsions
        for i in range(len(self.nodes)):
            node1=self.nodes[i]
            j = i+1
            for j in range(len(self.nodes)):
                node2=self.nodes[j]
                self.layoutRepulsive(node1,node2)
        #    Forces on nodes due to edge attractions        
        for i in range(len(self.edges)):
            edge=self.edges[i]
            self.layoutActractive(edge)

        # Move by the given force
        for i in range(len(self.nodes)):
            node=self.nodes[i]
            xmove=self.c * node.layoutForceX        
            ymove=self.c * node.layoutForceY  
            
            max= self.maxVertexMovement
            if xmove > max : xmove = max
            if xmove < -max : xmove = -max      
            
            if ymove > max : ymove = max
            if ymove < -max : ymove = -max             
            
            node.layoutPosX += xmove
            node.layoutPosY += xmove
            
            node.layoutForceX=0
            node.layoutForceY=0
            
    def layoutRepulsive(self,node1,node2):
        dx=node2.layoutPosX - node1.layoutPosX
        dy=node2.layoutPosY - node1.layoutPosY
        d2=dx*dx+dy*dy
        
        if d2 < 0.01:
            dx=0.1 + random.random()+ 0.1
            dy=0.1 + random.random()+ 0.1
            d2=dx*dx+dy*dy
            
        d= math.sqrt(d2)
        if d < self.maxRepulsiveForceDistance:
            repulsiveForce = self.k * self.k / d
            node2.layoutForceX += repulsiveForce *dx/d
            node2.layoutForceY += repulsiveForce *dy/d
            
            node1.layoutForceX += repulsiveForce *dx/d
            node1.layoutForceY += repulsiveForce *dy/d            
                    
    def layoutAttractive(self,edge):
        node1=edge[1]
        node2=edge[2]
        
        dx=node2.layoutPosX - node1.layoutPosX
        dy=node2.layoutPosY - node1.layoutPosY
        
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
        
        if not edge.weight or edge.weight < 1 : edge.weight = 1
        
        node2.layoutForceX -= attractiveForce * dx / d
        node2.layoutForceY -= attractiveForce * dy / d

        node1.layoutForceX += attractiveForce * dx / d
        node1.layoutForceY += attractiveForce * dy / d   
        

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