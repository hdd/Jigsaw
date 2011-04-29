import sys
import os
import math
import random

os.environ["DEBUG"]="1"

try:
    # https://github.com/hdd/hlog
    import hlog as log
except:
    import logging as log

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
      
class ConnectionItem(QtGui.QGraphicsPathItem ):

    def __init__(self,source_node =None, dest_node=None,parent=None):
        super(ConnectionItem,self).__init__(parent)
        
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()        
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        
        self.source_node=source_node
        self.dest_node=dest_node
        self.update()
        self.setZValue(-100000)     
         
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        
        # get the node position of the attribute         
        nsource_pos = self.mapFromItem(self.source_node, self.pos())
        ndest_pos = self.mapFromItem(self.dest_node, self.pos())
        
        qpath = QtGui.QPainterPath()
        self.setPath(qpath)
                
        line = QtCore.QLineF(nsource_pos, ndest_pos)
        
        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine,
                QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        
        painter.drawLine(line)

    def boundingRect(self):
        if not self.source_node or not self.dest_node:
            return QtCore.QRectF()

        penWidth = 2.0
        extra = (penWidth/ 2.0)

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)


class NodeItem(QtGui.QGraphicsItem ):
    xsize=120.0
    ysize=30.0
    
    def __init__(self,drq_job_object=None,parent=None):
        super(NodeItem,self).__init__(parent)
        
        self._drq_job_object = drq_job_object

        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.name=drq_job_object
            
        self.setScale(1.4)
        self.rect=QtCore.QRectF(-self.xsize/2,-self.ysize/2,self.xsize,self.ysize)
    
    def set_name(self,name="Node"):
        self.name=name
        
    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.gray, QtCore.Qt.SolidPattern))   
        painter.drawRoundedRect(self.rect,10,10)
        painter.setFont(QtGui.QFont("arial",4,3))
                
        node_text=self.name

        painter.drawText(self.rect,node_text,QtGui.QTextOption(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignHCenter))  

                    
class NodeScene(QtGui.QGraphicsScene):
    
    itemSelected = QtCore.pyqtSignal(QtGui.QGraphicsItem)

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
            
        elif (mouseEvent.button() == QtCore.Qt.MidButton):
            log.debug("adding a new node")
            item = NodeItem()
            self.addItem(item)
            item.setPos(mouseEvent.scenePos())
            
            self.itemInserted.emit(item)
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
#                startItem_attr.addConnection(connection)
#                endItem_attr.addConnection(connection)
                self.addItem(connection)
                connection.update()
                
        self.line = None
        super(NodeScene, self).mouseReleaseEvent(mouseEvent)
                                                                          
class NodeView(QtGui.QGraphicsView):
    def __init__(self,parent=None):
        super(NodeView,self).__init__(parent)
        self.scene = NodeScene(parent=self)
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-200, -200, 400, 400)
                
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        self.setScene(self.scene)
        
    def deleteItem(self):
        for item in self.scene.selectedItems():
            if isinstance(item, ConnectionItem):
                item.removeArrows()
            self.scene.removeItem(item)
 
    def sceneScaleChanged(self, scale):
        newScale = scale.left(scale.indexOf("%")).toDouble()[0] / 100.0
        oldMatrix = self.view.matrix()
        self.view.resetMatrix()
        self.view.translate(oldMatrix.dx(), oldMatrix.dy())
        self.view.scale(newScale, newScale)

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))
        
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

    def add_node(self,drq_job_object):
        log.debug("adding node...%s"%drq_job_object)
        job_node = NodeItem(drq_job_object=drq_job_object)
        self.scene.addItem(job_node)
                                            
        
class NodeViewer(QtGui.QDialog):
    def __init__(self,parent=None):
        super(NodeViewer,self).__init__(parent)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.view = NodeView(parent=self)
        icon = QtGui.QLabel()
        self.layout.addWidget(icon)
        self.layout.addWidget(self.view)
        self.setWindowTitle("DrQueue Node Viewer")
    
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


