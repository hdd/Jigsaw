import os, sys
import networkx as nx

os.environ["DEBUG"]="1"

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

#CUSTOM
import hlog as log
import nodeViewer as nv

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
    G.add_edge(F,B)        
    return G

class DrawQt(QtGui.QGraphicsView):
    def __init__(self, Graph=None,parent=None):
        super(DrawQt,self).__init__(parent)
        log.debug("init DrawQt")
        
        self.__nodes=[]
        self.__connections=[]
        
        self.__graph=Graph
        self.__scene=None
        
        self.__layout = QtGui.QVBoxLayout()
        self.setLayout(self.__layout)
        
        self.__build_nodes()
        
    def __build_nodes(self):
        self.__create_qtscene()
        self.__add_nodes()
        self.__add_connections()
                
    def __create_qtscene(self):
        self.__scene = nv.NodeScene(parent=self)
        self.setScene(self.__scene)     
    
    def __add_nodes(self):
        nodes = self.__graph.nodes()
        print nodes
        for n in nodes:
            if n:
                log.debug("creating node %s"%n)
                job_node = nv.NodeItem(drq_job_object=n)
                self.__graph.node[n]["_qt_item"]=job_node
                
                self.__scene.addItem(job_node)
                self.__nodes.append(job_node)
    
    def __add_connections(self):
        edges=self.__graph.edges()
        for e in edges:
            if e:
                log.debug(e)
                source_node = self.__graph.node[e[0]]["_qt_item"]
                dest_node= self.__graph.node[e[1]]["_qt_item"]
                connection = nv.ConnectionItem(source_node,dest_node)
                self.__scene.addItem(connection)
                
     
     
class NodeViewer(QtGui.QDialog):
    def __init__(self,parent=None):
        super(NodeViewer,self).__init__(parent)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        
        G=DRAW_GRAPH()
        self.view = DrawQt(Graph=G,parent=self)
        icon = QtGui.QLabel()
        self.layout.addWidget(icon)
        self.layout.addWidget(self.view)
        self.setWindowTitle("Node Viewer")
    
    def add_node(self,drq_job_object):
        self.view.add_node(drq_job_object)        

def main():
    app = QtGui.QApplication(sys.argv)
    
    splash_image=QtGui.QPixmap("splash.jpg")
    splash=QtGui.QSplashScreen(splash_image)
    splash.show()
    
    app.processEvents()
    
    dialog = NodeViewer()
    dialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()       