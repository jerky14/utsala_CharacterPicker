from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from functools import partial
import json
from shiboken2 import wrapInstance




global app
app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication(sys.argv)


def getMayaMainWindow():
    mayaWin = next(w for w in app.topLevelWidgets() if w.objectName()=='MayaWindow')

    return mayaWin
    
    

class PickerUi (QtWidgets.QDialog): 
    def __init__(self, parent=getMayaMainWindow()):
        super(PickerUi, self).__init__(parent)

        self.setWindowTitle("UTS|ALA :: CharacterPicker")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.create_layout()
        self.fill_layout_bodyTab()
        self.fill_layout()

        
    #---------------
    # UI
    #---------------

    def create_layout(self):
        
        self.pick_gridLayout = QtWidgets.QGridLayout()
        self.globalLayout = QtWidgets.QVBoxLayout()
        
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        
        self.tabs.addTab(self.tab1,"Body")
        self.tabs.addTab(self.tab2, "Fingers")
        self.tabs.addTab(self.tab3, "Face")

        self.tab1.layout = QtWidgets.QGridLayout()

    
    def fill_layout_bodyTab(self):
        
         #--- Body Tab

        headCtrls = self.getHeadControls()
        gridNum = 0
        for item in headCtrls:
            headBtn = QtWidgets.QPushButton(item)
            headBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = headCtrls.get(item)
            headBtn.clicked.connect(partial(self.runSelect, value))
            self.tab1.layout.addWidget(headBtn, gridNum, 1)
            gridNum+=1
        self.tab1.layout.setRowMinimumHeight(gridNum, 40)
        gridNum+=1
        
        startShoulderGridRef = gridNum
        
        spineCtrls = self.getSpineControls()
        for item in spineCtrls:
            spineBtn = QtWidgets.QPushButton(item)
            spineBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = spineCtrls.get(item)
            spineBtn.clicked.connect(partial(self.runSelect, value))
            self.tab1.layout.addWidget(spineBtn, gridNum, 1)
            gridNum+=1


        lArmGridRef = startShoulderGridRef
        leftArmCtrls = []
        self.lArm_fkikBox = QtWidgets.QComboBox()
        self.lArm_fkikBox.addItems(["FK", "IK"])
        if self.check_FKIK("lArm") < 0.5:
            self.lArm_fkikBox.setCurrentText("FK")
            leftArmCtrls = self.getLeftArmControlsFK()
        elif self.check_FKIK("lArm") > 0.5:
            self.lArm_fkikBox.setCurrentText("IK")
            leftArmCtrls = self.getLeftArmControlsIK()
        self.lArm_fkikBox.currentIndexChanged.connect(partial(self.toggleFKIK, "lArm"))
        self.tab1.layout.addWidget(self.lArm_fkikBox, lArmGridRef, 2)
        lArmGridRef+=1
        
        if leftArmCtrls is not None:
                for item in leftArmCtrls:
                    lArmBtn = QtWidgets.QPushButton(item)
                    lArmBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
                    value = leftArmCtrls.get(item)
                    lArmBtn.clicked.connect(partial(self.runSelect, value))
                    self.tab1.layout.addWidget(lArmBtn, lArmGridRef, 2)
                    lArmGridRef+=1


        rArmGridRef = startShoulderGridRef
        rightArmCtrls = []
        self.rArm_fkikBox = QtWidgets.QComboBox()
        self.rArm_fkikBox.addItems(["FK", "IK"])
        if self.check_FKIK("rArm") < 0.5:
            self.rArm_fkikBox.setCurrentText("FK")
            rightArmCtrls = self.getRightArmControlsFK()
        elif self.check_FKIK("rArm") > 0.5:
            self.rArm_fkikBox.setCurrentText("IK")
            rightArmCtrls = self.getRightArmControlsIK()
        self.rArm_fkikBox.currentIndexChanged.connect(partial(self.toggleFKIK, "rArm"))
        self.tab1.layout.addWidget(self.rArm_fkikBox, rArmGridRef, 0)
        rArmGridRef+=1


        for item in rightArmCtrls:
            rArmBtn = QtWidgets.QPushButton(item)
            rArmBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = rightArmCtrls.get(item)
            rArmBtn.clicked.connect(partial(self.runSelect, value))
            self.tab1.layout.addWidget(rArmBtn, rArmGridRef, 0)
            rArmGridRef+=1
            
        cogRef = max([rArmGridRef, lArmGridRef, gridNum])+1
        cogCtrls = self.getCogControls()
        for item in cogCtrls:
            cogBtn = QtWidgets.QPushButton(item)
            cogBtn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = cogCtrls.get(item)
            cogBtn.clicked.connect(partial(self.runSelect, value))
            self.tab1.layout.addWidget(cogBtn, cogRef, 1)
            cogRef+=1
            
        
        lLegGridRef = cogRef
        leftLegCtrls = self.getLeftLegControls()
        for item in leftLegCtrls:
            lLegBtn = QtWidgets.QPushButton(item)
            lLegBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = leftLegCtrls.get(item)
            lLegBtn.clicked.connect(partial(self.runSelect, value))
            self.tab1.layout.addWidget(lLegBtn, lLegGridRef, 2)
            lLegGridRef+=1
            
        rLegGridRef = cogRef
        rightLegCtrls = self.getRightLegControls()
        for item in rightLegCtrls:
            rLegBtn = QtWidgets.QPushButton(item)
            rLegBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = rightLegCtrls.get(item)
            rLegBtn.clicked.connect(partial(self.runSelect, value))
            self.tab1.layout.addWidget(rLegBtn, rLegGridRef, 0)
            rLegGridRef+=1
            
        self.tab1.setLayout(self.tab1.layout)


    def fill_layout(self):
        
        #--- Fingers Tab
        
        self.tab2.layout = QtWidgets.QGridLayout()
        
        leftFingerCtrls = self.getLeftFingerControls()
        
        lThumbGridRef = 0
        for item in leftFingerCtrls.get("thumbCtrls"):
            lThumbxBtn = QtWidgets.QPushButton(item)
            lThumbxBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = leftFingerCtrls.get("thumbCtrls").get(item)
            lThumbxBtn.clicked.connect(partial(self.runSelect, value))
            self.tab2.layout.addWidget(lThumbxBtn, lThumbGridRef, 0)
            lThumbGridRef+=1


        lIndexGridRef = 1
        for item in leftFingerCtrls.get("indexCtrls"):
            lIndexBtn = QtWidgets.QPushButton(item)
            lIndexBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = leftFingerCtrls.get("indexCtrls").get(item)
            lIndexBtn.clicked.connect(partial(self.runSelect, value))
            self.tab2.layout.addWidget(lIndexBtn, lIndexGridRef, 1)
            lIndexGridRef+=1
            
        lMiddleGridRef = 1
        for item in leftFingerCtrls.get("middleCtrls"):
            lMiddleBtn = QtWidgets.QPushButton(item)
            lMiddleBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = leftFingerCtrls.get("middleCtrls").get(item)
            lMiddleBtn.clicked.connect(partial(self.runSelect, value))
            self.tab2.layout.addWidget(lMiddleBtn, lMiddleGridRef, 2)
            lMiddleGridRef+=1
            
        lRingGridRef = 1
        for item in leftFingerCtrls.get("ringCtrls"):
            lRingBtn = QtWidgets.QPushButton(item)
            lRingBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = leftFingerCtrls.get("ringCtrls").get(item)
            lRingBtn.clicked.connect(partial(self.runSelect, value))
            self.tab2.layout.addWidget(lRingBtn, lRingGridRef, 3)
            lRingGridRef+=1
            
        lPinkyGridRef = 1
        for item in leftFingerCtrls.get("pinkyCtrls"):
            lPinkyBtn = QtWidgets.QPushButton(item)
            lPinkyBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = leftFingerCtrls.get("pinkyCtrls").get(item)
            lPinkyBtn.clicked.connect(partial(self.runSelect, value))
            self.tab2.layout.addWidget(lPinkyBtn, lPinkyGridRef, 4)
            lPinkyGridRef+=1
            
            
        self.tab2.setLayout(self.tab2.layout)
        
        
        #--- Global Layout
            
        
        self.globalLayout.addWidget(self.tabs)    

        self.setLayout(self.globalLayout)
        
    def clear_layout(self, _layout):
        if _layout is not None:
            for i in reversed(range(_layout.count())):
                _layout.itemAt(i).widget().deleteLater()


    #---------------
    # FUNCTION
    #---------------
    
    def runSelect(self, value):
        mod = cmds.getModifiers()
        if (mod & 1) > 0:
            cmds.select( "*" + value, add=True )
        else:
            cmds.select( "*" + value, r=True )
        

        
    def toggleFKIK(self, ctrl, val):

        if ctrl is ("lArm"):
            
            lArmCtrl = cmds.ls("*L_FKIK_Switch_ctrl")
            if lArmCtrl[0] is not None:
                    if val is 0:
                        cmds.setAttr(lArmCtrl[0] + ".FKIKBlend", 0)
                    elif val is 1:
                        cmds.setAttr(lArmCtrl[0] + ".FKIKBlend", 1)
            self.clear_layout(self.tab1.layout)
            self.fill_layout_bodyTab()

        if ctrl is ("rArm"):
            rArmCtrl = cmds.ls("*R_FKIK_Switch_ctrl")
            if rArmCtrl[0] is not None:
                    if val is 0:
                        cmds.setAttr(rArmCtrl[0] + ".FKIKBlend", 0)
                    elif val is 1:
                        cmds.setAttr(rArmCtrl[0] + ".FKIKBlend", 1)
            self.clear_layout(self.tab1.layout)
            self.fill_layout_bodyTab()
            
    
    def check_FKIK(self, ctrl):
        
        if ctrl is ("lArm"):
            lArmCtrl = cmds.ls("*L_FKIK_Switch_ctrl")
            value = cmds.getAttr(lArmCtrl[0] + ".FKIKBlend")
            
            return value
        
        if ctrl is ("rArm"):
            rArmCtrl = cmds.ls("*R_FKIK_Switch_ctrl")
            value = cmds.getAttr(rArmCtrl[0] + ".FKIKBlend")
            
            return value

       
    #---------------
    # DATA
    #---------------
        
    def getHeadControls(self):
        headCtrls = {"Head":"head_ctrl", "Neck":"neck_ctrl"}
        return headCtrls
        
    def getSpineControls(self):
        spineCtrls = {"Spine Master":"spine_master_ctrl", "Upper Spine":"upperspine_IK_ctrl", "Lower Spine":"lowerspine_IK_ctrl", "Hips":"hips_IK_ctrl"}
        return spineCtrls
    
    def getLeftArmControlsIK(self):
        lArmCtrls = {"Left Clavicle":"L_clavicle_ctrl","Left Elbow Ctrl":"L_elbow_IK_ctrl","Left Arm IK":"L_arm_IK_ctrl"}
        return lArmCtrls
    def getLeftArmControlsFK(self):
        lArmCtrls = {"Left Clavicle":"L_clavicle_ctrl","Left Shoulder":"L_shoulder_FK_ctrl", "Left Elbow":"L_elbow_FK_ctrl", "Left Wrist":"L_wrist_FK_ctrl"}
        return lArmCtrls
        
    def getRightArmControlsIK(self):
        rArmCtrls = {"Right Clavicle":"R_clavicle_ctrl","Right Elbow Ctrl":"R_elbow_IK_ctrl","Right Arm IK":"R_arm_IK_ctrl"}
        return rArmCtrls
    def getRightArmControlsFK(self):
        rArmCtrls = {"Right Clavicle":"R_clavicle_ctrl","Right Shoulder":"R_shoulder_FK_ctrl", "Right Elbow":"R_elbow_FK_ctrl", "Right Wrist":"R_wrist_FK_ctrl"}
        return rArmCtrls
        
    def getRightLegControls(self):
        rLegCtrls = {"Right Leg IK":"R_leg_IK_ctrl","Right Leg Knee":"R_knee_IK_ctrl","Toe":"R_toe_ctrl", "Toe Pivot":"R_toePivot_ctrl", "Heel Pivot":"R_heelPivot_ctrl"}
        return rLegCtrls
        
    def getCogControls(self):
        cogCtrls = {"Cog Ctrl":"COG_ctrl"}
        return cogCtrls
        
    def getLeftLegControls(self):
        leftLegCtrls = {"Knee":"L_knee_IK_ctrl", "Foot IK Ctrl":"L_leg_IK_ctrl", "Toe":"L_toe_ctrl", "Toe Pivot":"L_toePivot_ctrl"}
        return leftLegCtrls
        
    def getRightLegControls(self):
        rightLegCtrls = {"Knee":"R_knee_IK_ctrl", "Foot IK Ctrl":"R_leg_IK_ctrl", "Toe":"R_toe_ctrl", "Toe Pivot":"R_toePivot_ctrl"}
        return rightLegCtrls
        
    def getLeftFingerControls(self):
        indexCtrls = {"Knuckle":"L_index1_ctrl", "Mid":"L_index2_ctrl", "Distal":"L_index3_ctrl"}
        middleCtrls = {"Knuckle":"L_middle1_ctrl", "Mid":"L_middle2_ctrl", "Distal":"L_middle3_ctrl"}
        ringCtrls = {"Knuckle":"L_ring1_ctrl", "Mid":"L_ring2_ctrl", "Distal":"L_ring3_ctrl"}
        pinkyCtrls = {"Knuckle":"L_pinke1_ctrl", "Mid":"L_pinke2_ctrl", "Distal":"L_pinke3_ctrl"}
        thumbCtrls = {"Knuckle":"L_thumb1_ctrl", "Mid":"L_thumb2_ctrl", "Distal":"L_thumb3_ctrl"}
        
        leftFingerCtrls = {"indexCtrls":indexCtrls, "middleCtrls":middleCtrls,"ringCtrls":ringCtrls,"pinkyCtrls":pinkyCtrls,"thumbCtrls":thumbCtrls,}
        return leftFingerCtrls
    
    

        


try:
    ui.close()
except:
    pass

ui = PickerUi()
ui.show()



