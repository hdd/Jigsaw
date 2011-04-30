'''
Copyright 2011 lorenzo angeli. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY LORENZO ANGELI ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL LORENZO ANGELI OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of lorenzo angeli.
'''


import os, sys
import networkx as nx
import math

os.environ["DEBUG"]="1"

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

#CUSTOM
import hlog as log
import jigsaw.lib as nd


def DRAW_GRAPH():
    G=nx.DiGraph()
    
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


class NodeViewer(QtGui.QDialog):
    def __init__(self,parent=None):
        super(NodeViewer,self).__init__(parent)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Node Viewer")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint|QtCore.Qt.WindowMaximizeButtonHint|QtCore.Qt.WindowCloseButtonHint)
        
        icon = QtGui.QLabel()
        iconspath=os.path.join(os.path.dirname(__file__),"icons","jigsaw.png")
        if not os.path.exists(iconspath):
            log.warning("icon %s doesnt' exists"%iconspath)
            
        log.debug(iconspath)
        icon.setPixmap(QtGui.QPixmap(iconspath))
        self.layout.addWidget(icon)     
           
    def add_graph(self,G):
        self.view = nd.JigsawView(Graph=G,parent=self)
        self.layout.addWidget(self.view)    

def main():
    app = QtGui.QApplication(sys.argv)
    splash_image=QtGui.QPixmap("splash.jpg")
    splash=QtGui.QSplashScreen(splash_image)
    splash.show()
    app.processEvents()
    
    dialog = NodeViewer()    
    G=DRAW_GRAPH()
    dialog.add_graph(G)  
    dialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        main()
    except:
        log.error("Jigsaw test failed...")       