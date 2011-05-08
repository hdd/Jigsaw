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

__author__="Lorenzo Angeli"



import sys
import os
import math
import random
from pprint import pformat

os.environ["DEBUG"]="1"

try:
    # https://github.com/hdd/hlog
    import hlog as log
except:
    import logging as log

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
      
      
from springLayout import SpringLayout
      
class ConnectionItem(QtGui.QGraphicsPathItem ):
        
    Pi = math.pi
    TwoPi = 2.0 * Pi
    Type = QtGui.QGraphicsItem.UserType + 2
    
    def __init__(self,source_node =None, dest_node=None,parent=None):
        super(ConnectionItem,self).__init__(parent)
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
                
        self.arrowSize = 10.0
        
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()        
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        
        self.source_node=source_node
        self.dest_node=dest_node
        self.update()
        self.setZValue(-10000)     
        self.adjust()
        
    def adjust(self):
        if not self.source_node or not self.dest_node:
            return

        line = QtCore.QLineF(self.mapFromItem(self.source_node, 0, 0),
                self.mapFromItem(self.dest_node, 0, 0))
        length = line.length()

        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx() * 10) / length,
                (line.dy() * 10) / length)

        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset

         
    def paint(self, painter, option, widget):
        
        if not self.source_node or not self.dest_node:
            return 
        
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        
        # get the node position of the attribute
        nsource_pos = self.mapFromItem(self.source_node, self.pos())
        ndest_pos = self.mapFromItem(self.dest_node, self.pos())
        
        new_src_pos=QtCore.QPointF(nsource_pos.x()+(self.source_node.xsize/2)+5,nsource_pos.y())
        new_dst_pos=QtCore.QPointF(ndest_pos.x()-(self.dest_node.xsize/2)-5,ndest_pos.y())
        
        
        line = QtCore.QLineF(new_src_pos, new_dst_pos)
        
        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine,
                QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        
        painter.drawLine(line)

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = self.TwoPi - angle
        
        destArrowP1 = new_dst_pos + QtCore.QPointF(math.sin(angle - self.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - self.Pi / 3) * self.arrowSize)
        destArrowP2 = new_dst_pos + QtCore.QPointF(math.sin(angle - self.Pi + self.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - self.Pi + self.Pi / 3) * self.arrowSize)
        
        
        #painter.drawEllipse(line.p2(),3,3)
        
        painter.drawEllipse(new_dst_pos,4,4)
        
        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))
        
        painter.drawEllipse(new_src_pos,4,4)
        
        super(ConnectionItem,self).paint( painter, option, widget)
        
    def boundingRect(self):
        if not self.source_node or not self.dest_node:
            return QtCore.QRectF()

        penWidth = 2.0
        extra = (penWidth + self.arrowSize) / 2.0

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)


class NodeItem(QtGui.QGraphicsItem):
    xsize=120.0
    ysize=30.0
    
    def __init__(self,drq_job_object=None,parent=None):
        super(NodeItem,self).__init__(parent)
        
        self._drq_job_object = drq_job_object
        self._border_color=QtGui.QColor(QtCore.Qt.black)
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

        self.name=drq_job_object
            
        self.rect=QtCore.QRectF(-self.xsize/2,-self.ysize/2,self.xsize,self.ysize)
    
    def set_border_color(self,switch=0):
        color=QtCore.Qt.black
        
        if switch:
            color=QtCore.Qt.red
        
        self._border_color=QtGui.QColor(color)
        self.update()
    
    
    
    def set_name(self,name="Node"):
        self.name=name
        
    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setPen(QtGui.QPen(self._border_color, 1))                
        painter.setBrush(QtGui.QBrush(QtCore.Qt.gray, QtCore.Qt.SolidPattern))   
        painter.drawRoundedRect(self.rect,4,4)
        painter.setFont(QtGui.QFont("arial",4,3))                
        node_text=self.name
        painter.drawText(self.rect,node_text,QtGui.QTextOption(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignHCenter))  

                    
class NodeScene(QtGui.QGraphicsScene):
    
    def __init__(self,parent=None):
        super(NodeScene,self).__init__(parent)
        self.line=None
        self.line_mode=False
        
    def mousePressEvent(self, mouseEvent):
        
        if (mouseEvent.button() == QtCore.Qt.RightButton):
            log.debug("right click mouse Press event")
            self.line = QtGui.QGraphicsLineItem(QtCore.QLineF(mouseEvent.scenePos(),mouseEvent.scenePos()))
            start_points=self.items(self.line.line().p1())
        
            if len(start_points)==0:
                log.debug("line skip , not on an attribute")
                return
            
            start_mouse_item = self.itemAt(self.line.line().p1())
            if not isinstance(start_mouse_item,NodeItem):
                log.debug("line skip , %s not an attribute"%start_mouse_item)
                return
                
            end_mouse_item = self.itemAt(self.line.line().p2())
            if not isinstance(end_mouse_item,NodeItem):
                log.debug("line skip , %s not an attribute"%end_mouse_item)
                return
                
            self.line.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            
            
            log.debug(start_mouse_item)
            log.debug(end_mouse_item)
            
            self.addItem(self.line)
            self.line_mode=True
            
        else:
            log.debug("left click mouse Press event")
            self.line_mode=False
            
        super(NodeScene, self).mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if self.line_mode and self.line:
            newLine = QtCore.QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        else:
            super(NodeScene, self).mouseMoveEvent(mouseEvent)

        self.update()

    def mouseReleaseEvent(self, mouseEvent):
        log.debug("mouse relese event")
        
        if self.line and self.line_mode:
            
            startItems = self.items(self.line.line().p1())
            endItems = self.items(self.line.line().p2())
            
            
            self.removeItem(self.line)
            self.line = None
            
            if len(startItems) and len(endItems):
                
                startItem = startItems[0]
                endItem = endItems[0]
                                                
                startItem_attr = startItems[-1]              
                endItem_attr = endItems[-1]
                
                #print self.itemAt(endItem)
                if not isinstance(endItem_attr,NodeItem):
                    log.debug("no other attribute found at the end point")
                    log.debug("end object : %s"%type(endItem_attr))
                    self.update()
                    return
                
                if not isinstance(startItem_attr,NodeItem):
                    log.debug("no other attribute found at the end point")
                    log.debug("end object : %s"%type(startItem_attr))
                    self.update()
                    return
                                
                log.debug("create new connection from %s to %s"%(startItem, endItem))
                
                connection = ConnectionItem(startItem_attr, endItem_attr)
                self.addItem(connection)
                self.update()
                
        self.line = None
        super(NodeScene, self).mouseReleaseEvent(mouseEvent)

                                
class JigsawView(QtGui.QGraphicsView):
    def __init__(self, Graph=None,parent=None):
        super(JigsawView,self).__init__(parent)
        log.debug("init DrawQt")
        
        self.__nodes=[]
        self.__connections=[]
        
        self.__graph=Graph
        self.__scene=None
        
        self.__layout = QtGui.QVBoxLayout()
        self.setLayout(self.__layout)
        
        self.__build_nodes()
        
        self._last_point=QtCore.QPointF()
        
    def __build_nodes(self):
        self.__create_qtscene()
        self.__add_nodes()
        self.__add_connections()
                
    def __create_qtscene(self):
        self.__scene = NodeScene(parent=self)
        self.setScene(self.__scene)     
    
    def __add_nodes(self):
        
        S=SpringLayout(self.__graph)
        S.layout()
        upd_graph=S.get_updated_graph()
        self.__graph=upd_graph
        nodes = upd_graph.nodes()        
        prev_pos=QtCore.QPointF(0,0)
        
        mult=10
        
        for n in nodes:
            if n:
                log.debug("creating node %s"%n)
                job_node = NodeItem(drq_job_object=n)
                
                xpos= self.__graph.node[n]["layoutPosX"]
                ypos= self.__graph.node[n]["layoutPosY"]
#                
#                log.info("xpos %s ypos %s"%(xpos,ypos))
#                log.info("xsize %s ysizze %s"%(job_node.xsize,job_node.ysize))
#                
                out_pos=((xpos+job_node.xsize)*mult,(ypos+job_node.ysize)*mult)
                log.debug("final output %s %s"%(out_pos[0],out_pos[1]))
               
                job_node.setPos(QtCore.QPointF(out_pos[0],out_pos[1]))
                
                self.__graph.node[n]["_qt_item"]=job_node
                self.__scene.addItem(job_node)
                self.__nodes.append(job_node)
                prev_pos=job_node.pos()
    
    def __add_connections(self):
        edges=self.__graph.edges()
        for e in edges:
            if e:
                log.debug("creating connection %s"%"->".join(e))
                source_node = self.__graph.node[e[0]]["_qt_item"]
                dest_node= self.__graph.node[e[1]]["_qt_item"]
                connection = ConnectionItem(source_node,dest_node)
                self.__scene.addItem(connection)

    def mousePressEvent(self,mouseEvent):
        start_mouse_item = self.itemAt(mouseEvent.pos())
        self._last_point=   mouseEvent.pos()
        if (mouseEvent.button() == QtCore.Qt.LeftButton):       
            if isinstance(start_mouse_item,NodeItem):
                log.debug("on node %s"%start_mouse_item)
                start_mouse_item.set_border_color(switch=1)
             
        super(JigsawView,self).mousePressEvent(mouseEvent)
        
    
    def mouseReleaseEvent(self,mouseEvent):
        start_mouse_item = self.itemAt(mouseEvent.pos())
        if isinstance(start_mouse_item,NodeItem):
            log.debug("on node %s"%start_mouse_item)
            start_mouse_item.set_border_color(switch=0)
            
        self._last_point=QtCore.QPointF()    
        super(JigsawView,self).mouseReleaseEvent(mouseEvent)
        
    def mouseMoveEvent(self,mouseEvent):   
        
        if (mouseEvent.button() == QtCore.Qt.MidButton):               
            log.debug("DrawQt MouseMove")
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            
        super(JigsawView,self).mouseMoveEvent(mouseEvent)
        
    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, event.delta() / 240.0))
        
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)
                

