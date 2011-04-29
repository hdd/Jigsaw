import os, sys
import networkx as nx
import math

os.environ["DEBUG"]="1"

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

#CUSTOM
import hlog as log
import nodedraw as nd

def DRAW_GRAPH():
    G=nx.DiGraph()
    
    A="Test1"
    B="TestA"
    C="PIPPO"
    D="PIPPA"
    E="ENNIO"
    F="ENNIO2"
    
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


def main():
    app = QtGui.QApplication(sys.argv)
    splash_image=QtGui.QPixmap("splash.jpg")
    splash=QtGui.QSplashScreen(splash_image)
    splash.show()
    app.processEvents()
    
    dialog = nd.NodeViewer()    
    G=DRAW_GRAPH()
    dialog.add_graph(G)  
    
    dialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()       