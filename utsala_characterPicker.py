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
        self.tab4 = QtWidgets.QWidget()
        
        self.tabs.addTab(self.tab1,"Body")
        self.tabs.addTab(self.tab2, "L_Hand")
        self.tabs.addTab(self.tab3, "R_Hand")
        self.tabs.addTab(self.tab4, "Face")

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
        RightArmCtrls = []
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
        
        #--- L_Hand Tab
        
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
        
        #--- R_Hand Tab
        
        self.tab3.layout = QtWidgets.QGridLayout()
        
        rightFingerCtrls = self.getRightFingerControls()
        
        rThumbGridRef = 0
        for item in rightFingerCtrls.get("thumbCtrls"):
            rThumbxBtn = QtWidgets.QPushButton(item)
            rThumbxBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = rightFingerCtrls.get("thumbCtrls").get(item)
            rThumbxBtn.clicked.connect(partial(self.runSelect, value))
            self.tab3.layout.addWidget(rThumbxBtn, rThumbGridRef, 4)
            rThumbGridRef+=1


        rIndexGridRef = 1
        for item in rightFingerCtrls.get("indexCtrls"):
            rIndexBtn = QtWidgets.QPushButton(item)
            rIndexBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = rightFingerCtrls.get("indexCtrls").get(item)
            rIndexBtn.clicked.connect(partial(self.runSelect, value))
            self.tab3.layout.addWidget(rIndexBtn, rIndexGridRef, 3)
            rIndexGridRef+=1
            
        rMiddleGridRef = 1
        for item in rightFingerCtrls.get("middleCtrls"):
            rMiddleBtn = QtWidgets.QPushButton(item)
            rMiddleBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = rightFingerCtrls.get("middleCtrls").get(item)
            rMiddleBtn.clicked.connect(partial(self.runSelect, value))
            self.tab3.layout.addWidget(rMiddleBtn, rMiddleGridRef, 2)
            rMiddleGridRef+=1
            
        rRingGridRef = 1
        for item in rightFingerCtrls.get("ringCtrls"):
            rRingBtn = QtWidgets.QPushButton(item)
            rRingBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = rightFingerCtrls.get("ringCtrls").get(item)
            rRingBtn.clicked.connect(partial(self.runSelect, value))
            self.tab3.layout.addWidget(rRingBtn, rRingGridRef, 1)
            rRingGridRef+=1
            
        rPinkyGridRef = 1
        for item in rightFingerCtrls.get("pinkyCtrls"):
            rPinkyBtn = QtWidgets.QPushButton(item)
            rPinkyBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = rightFingerCtrls.get("pinkyCtrls").get(item)
            rPinkyBtn.clicked.connect(partial(self.runSelect, value))
            self.tab3.layout.addWidget(rPinkyBtn, rPinkyGridRef, 0)
            rPinkyGridRef+=1
            
        self.tab3.setLayout(self.tab3.layout)
        
        #--- Face Tab
        
        self.tab4.layout = QtWidgets.QGridLayout()
        
        faceCtrls = self.getFaceControls()

        rEyebrowMassGridRef = 0
        for item in faceCtrls.get("R_eyebrowMassCtrl"):
            rEyebrowMassBtn = QtWidgets.QPushButton(item)
            rEyebrowMassBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("R_eyebrowMassCtrl").get(item)
            rEyebrowMassBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyebrowMassBtn, rEyebrowMassGridRef, 0,1,4)
            rEyebrowMassGridRef+=1
            
        lEyebrowMassGridRef = 0
        for item in faceCtrls.get("L_eyebrowMassCtrl"):
            lEyebrowMassBtn = QtWidgets.QPushButton(item)
            lEyebrowMassBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("L_eyebrowMassCtrl").get(item)
            lEyebrowMassBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyebrowMassBtn, lEyebrowMassGridRef, 7,1,4)
            lEyebrowMassGridRef+=1
            
        cEyebrowGridRef = 0
        for item in faceCtrls.get("C_eyebrowCtrl"):
            cEyebrowBtn = QtWidgets.QPushButton(item)
            cEyebrowBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("C_eyebrowCtrl").get(item)
            cEyebrowBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(cEyebrowBtn, cEyebrowGridRef, 5)
            cEyebrowGridRef+=1
            
        rEyebrow1GridRef = 1
        for item in faceCtrls.get("R_eyebrowCtrl1"):
            rEyebrow1Btn = QtWidgets.QPushButton(item)
            rEyebrow1Btn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyebrowCtrl1").get(item)
            rEyebrow1Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyebrow1Btn, rEyebrow1GridRef, 0)
            rEyebrow1GridRef+=1
        
        rEyebrow2GridRef = 1
        for item in faceCtrls.get("R_eyebrowCtrl2"):
            rEyebrow2Btn = QtWidgets.QPushButton(item)
            rEyebrow2Btn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyebrowCtrl2").get(item)
            rEyebrow2Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyebrow2Btn, rEyebrow2GridRef, 1)
            rEyebrow2GridRef+=1
            
        rEyebrow3GridRef = 1
        for item in faceCtrls.get("R_eyebrowCtrl3"):
            rEyebrow3Btn = QtWidgets.QPushButton(item)
            rEyebrow3Btn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyebrowCtrl3").get(item)
            rEyebrow3Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyebrow3Btn, rEyebrow3GridRef, 2)
            rEyebrow3GridRef+=1
            
        rEyebrow4GridRef = 1
        for item in faceCtrls.get("R_eyebrowCtrl4"):
            rEyebrow4Btn = QtWidgets.QPushButton(item)
            rEyebrow4Btn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyebrowCtrl4").get(item)
            rEyebrow4Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyebrow4Btn, rEyebrow4GridRef, 3)
            rEyebrow4GridRef+=1
            
        lEyebrow1GridRef = 1
        for item in faceCtrls.get("L_eyebrowCtrl1"):
            lEyebrow1Btn = QtWidgets.QPushButton(item)
            lEyebrow1Btn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyebrowCtrl1").get(item)
            lEyebrow1Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyebrow1Btn, lEyebrow1GridRef, 7)
            lEyebrow1GridRef+=1
        
        lEyebrow2GridRef = 1
        for item in faceCtrls.get("L_eyebrowCtrl2"):
            lEyebrow2Btn = QtWidgets.QPushButton(item)
            lEyebrow2Btn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyebrowCtrl2").get(item)
            lEyebrow2Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyebrow2Btn, lEyebrow2GridRef, 8)
            lEyebrow2GridRef+=1
            
        lEyebrow3GridRef = 1
        for item in faceCtrls.get("L_eyebrowCtrl3"):
            lEyebrow3Btn = QtWidgets.QPushButton(item)
            lEyebrow3Btn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyebrowCtrl3").get(item)
            lEyebrow3Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyebrow3Btn, lEyebrow3GridRef, 9)
            lEyebrow3GridRef+=1
            
        lEyebrow4GridRef = 1
        for item in faceCtrls.get("L_eyebrowCtrl4"):
            lEyebrow4Btn = QtWidgets.QPushButton(item)
            lEyebrow4Btn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyebrowCtrl4").get(item)
            lEyebrow4Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyebrow4Btn, lEyebrow4GridRef, 10)
            lEyebrow4GridRef+=1
            
        rEyeCorner_outerGridRef = 3
        for item in faceCtrls.get("R_eyeCorner_outerCtrl"):
            rEyeCorner_outerBtn = QtWidgets.QPushButton(item)
            rEyeCorner_outerBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyeCorner_outerCtrl").get(item)
            rEyeCorner_outerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyeCorner_outerBtn, rEyeCorner_outerGridRef, 0)
            rEyeCorner_outerGridRef+=1
            
        rEyeLid_UpperOuterGridRef = 2
        for item in faceCtrls.get("R_eyeLid_UpperOuterCtrl"):
            rEyeLid_UpperOuterBtn = QtWidgets.QPushButton(item)
            rEyeLid_UpperOuterBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyeLid_UpperOuterCtrl").get(item)
            rEyeLid_UpperOuterBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyeLid_UpperOuterBtn, rEyeLid_UpperOuterGridRef, 1)
            rEyeLid_UpperOuterGridRef+=1
            
        rEyeLid_UpperMiddleGridRef = 2
        for item in faceCtrls.get("R_eyeLid_UpperMiddleCtrl"):
            rEyeLid_UpperMiddleBtn = QtWidgets.QPushButton(item)
            rEyeLid_UpperMiddleBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyeLid_UpperMiddleCtrl").get(item)
            rEyeLid_UpperMiddleBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyeLid_UpperMiddleBtn, rEyeLid_UpperMiddleGridRef, 2)
            rEyeLid_UpperMiddleGridRef+=1
            
        rEyeLid_UpperInnerGridRef = 2
        for item in faceCtrls.get("R_eyeLid_UpperInnerCtrl"):
            rEyeLid_UpperInnerBtn = QtWidgets.QPushButton(item)
            rEyeLid_UpperInnerBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyeLid_UpperInnerCtrl").get(item)
            rEyeLid_UpperInnerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyeLid_UpperInnerBtn, rEyeLid_UpperInnerGridRef, 3)
            rEyeLid_UpperInnerGridRef+=1
            
        rEyeLid_LowerOuterGridRef = 4
        for item in faceCtrls.get("R_eyeLid_LowerOuterCtrl"):
            rEyeLid_LowerOuterBtn = QtWidgets.QPushButton(item)
            rEyeLid_LowerOuterBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyeLid_LowerOuterCtrl").get(item)
            rEyeLid_LowerOuterBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyeLid_LowerOuterBtn, rEyeLid_LowerOuterGridRef, 1)
            rEyeLid_LowerOuterGridRef+=1
            
        rEyeLid_LowerMiddleGridRef = 4
        for item in faceCtrls.get("R_eyeLid_LowerMiddleCtrl"):
            rEyeLid_LowerMiddleBtn = QtWidgets.QPushButton(item)
            rEyeLid_LowerMiddleBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyeLid_LowerMiddleCtrl").get(item)
            rEyeLid_LowerMiddleBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyeLid_LowerMiddleBtn, rEyeLid_LowerMiddleGridRef, 2)
            rEyeLid_LowerMiddleGridRef+=1
            
        rEyeLid_LowerInnerGridRef = 4
        for item in faceCtrls.get("R_eyeLid_LowerInnerCtrl"):
            rEyeLid_LowerInnerBtn = QtWidgets.QPushButton(item)
            rEyeLid_LowerInnerBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyeLid_LowerInnerCtrl").get(item)
            rEyeLid_LowerInnerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyeLid_LowerInnerBtn, rEyeLid_LowerInnerGridRef, 3)
            rEyeLid_LowerInnerGridRef+=1
            
        rEyeCorner_innerGridRef = 3
        for item in faceCtrls.get("R_eyeCorner_innerCtrl"):
            rEyeCorner_innerBtn = QtWidgets.QPushButton(item)
            rEyeCorner_innerBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_eyeCorner_innerCtrl").get(item)
            rEyeCorner_innerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(rEyeCorner_innerBtn, rEyeCorner_innerGridRef, 4)
            rEyeCorner_innerGridRef+=1
            
        lEyeCorner_outerGridRef = 3
        for item in faceCtrls.get("L_eyeCorner_outerCtrl"):
            lEyeCorner_outerBtn = QtWidgets.QPushButton(item)
            lEyeCorner_outerBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyeCorner_outerCtrl").get(item)
            lEyeCorner_outerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyeCorner_outerBtn, lEyeCorner_outerGridRef, 10)
            lEyeCorner_outerGridRef+=1
            
        lEyeLid_UpperOuterGridRef = 2
        for item in faceCtrls.get("L_eyeLid_UpperOuterCtrl"):
            lEyeLid_UpperOuterBtn = QtWidgets.QPushButton(item)
            lEyeLid_UpperOuterBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyeLid_UpperOuterCtrl").get(item)
            lEyeLid_UpperOuterBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyeLid_UpperOuterBtn, lEyeLid_UpperOuterGridRef, 9)
            lEyeLid_UpperOuterGridRef+=1
            
        lEyeLid_UpperMiddleGridRef = 2
        for item in faceCtrls.get("L_eyeLid_UpperMiddleCtrl"):
            lEyeLid_UpperMiddleBtn = QtWidgets.QPushButton(item)
            lEyeLid_UpperMiddleBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyeLid_UpperMiddleCtrl").get(item)
            lEyeLid_UpperMiddleBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyeLid_UpperMiddleBtn, lEyeLid_UpperMiddleGridRef, 8)
            lEyeLid_UpperMiddleGridRef+=1
            
        lEyeLid_UpperInnerGridRef = 2
        for item in faceCtrls.get("L_eyeLid_UpperInnerCtrl"):
            lEyeLid_UpperInnerBtn = QtWidgets.QPushButton(item)
            lEyeLid_UpperInnerBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyeLid_UpperInnerCtrl").get(item)
            lEyeLid_UpperInnerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyeLid_UpperInnerBtn, lEyeLid_UpperInnerGridRef, 7)
            lEyeLid_UpperInnerGridRef+=1
            
        lEyeLid_LowerOuterGridRef = 4
        for item in faceCtrls.get("L_eyeLid_LowerOuterCtrl"):
            lEyeLid_LowerOuterBtn = QtWidgets.QPushButton(item)
            lEyeLid_LowerOuterBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyeLid_LowerOuterCtrl").get(item)
            lEyeLid_LowerOuterBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyeLid_LowerOuterBtn, lEyeLid_LowerOuterGridRef, 9)
            lEyeLid_LowerOuterGridRef+=1
            
        lEyeLid_LowerMiddleGridRef = 4
        for item in faceCtrls.get("L_eyeLid_LowerMiddleCtrl"):
            lEyeLid_LowerMiddleBtn = QtWidgets.QPushButton(item)
            lEyeLid_LowerMiddleBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyeLid_LowerMiddleCtrl").get(item)
            lEyeLid_LowerMiddleBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyeLid_LowerMiddleBtn, lEyeLid_LowerMiddleGridRef, 8)
            lEyeLid_LowerMiddleGridRef+=1
            
        lEyeLid_LowerInnerGridRef = 4
        for item in faceCtrls.get("L_eyeLid_LowerInnerCtrl"):
            lEyeLid_LowerInnerBtn = QtWidgets.QPushButton(item)
            lEyeLid_LowerInnerBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyeLid_LowerInnerCtrl").get(item)
            lEyeLid_LowerInnerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyeLid_LowerInnerBtn, lEyeLid_LowerInnerGridRef, 7)
            lEyeLid_LowerInnerGridRef+=1
            
        lEyeCorner_innerGridRef = 3
        for item in faceCtrls.get("L_eyeCorner_innerCtrl"):
            lEyeCorner_innerBtn = QtWidgets.QPushButton(item)
            lEyeCorner_innerBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_eyeCorner_innerCtrl").get(item)
            lEyeCorner_innerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(lEyeCorner_innerBtn, lEyeCorner_innerGridRef, 6)
            lEyeCorner_innerGridRef+=1
            
        R_upperCheekTweaker_001GridRef = 5
        for item in faceCtrls.get("R_upperCheekTweaker_001Ctrl"):
            R_upperCheekTweaker_001Btn = QtWidgets.QPushButton(item)
            R_upperCheekTweaker_001Btn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = faceCtrls.get("R_upperCheekTweaker_001Ctrl").get(item)
            R_upperCheekTweaker_001Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_upperCheekTweaker_001Btn, R_upperCheekTweaker_001GridRef, 0)
            R_upperCheekTweaker_001GridRef+=1
            
        R_upperCheekTweaker_002GridRef = 6
        for item in faceCtrls.get("R_upperCheekTweaker_002Ctrl"):
            R_upperCheekTweaker_002Btn = QtWidgets.QPushButton(item)
            R_upperCheekTweaker_002Btn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = faceCtrls.get("R_upperCheekTweaker_002Ctrl").get(item)
            R_upperCheekTweaker_002Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_upperCheekTweaker_002Btn, R_upperCheekTweaker_002GridRef, 1)
            R_upperCheekTweaker_002GridRef+=1
            
        R_upperCheekTweaker_003GridRef = 5
        for item in faceCtrls.get("R_upperCheekTweaker_003Ctrl"):
            R_upperCheekTweaker_003Btn = QtWidgets.QPushButton(item)
            R_upperCheekTweaker_003Btn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = faceCtrls.get("R_upperCheekTweaker_003Ctrl").get(item)
            R_upperCheekTweaker_003Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_upperCheekTweaker_003Btn, R_upperCheekTweaker_003GridRef, 2)
            R_upperCheekTweaker_003GridRef+=1
            
        L_upperCheekTweaker_001GridRef = 5
        for item in faceCtrls.get("L_upperCheekTweaker_001Ctrl"):
            L_upperCheekTweaker_001Btn = QtWidgets.QPushButton(item)
            L_upperCheekTweaker_001Btn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = faceCtrls.get("L_upperCheekTweaker_001Ctrl").get(item)
            L_upperCheekTweaker_001Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_upperCheekTweaker_001Btn, L_upperCheekTweaker_001GridRef, 10)
            L_upperCheekTweaker_001GridRef+=1
            
        L_upperCheekTweaker_002GridRef = 6
        for item in faceCtrls.get("L_upperCheekTweaker_002Ctrl"):
            L_upperCheekTweaker_002Btn = QtWidgets.QPushButton(item)
            L_upperCheekTweaker_002Btn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = faceCtrls.get("L_upperCheekTweaker_002Ctrl").get(item)
            L_upperCheekTweaker_002Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_upperCheekTweaker_002Btn, L_upperCheekTweaker_002GridRef, 9)
            L_upperCheekTweaker_002GridRef+=1
            
        L_upperCheekTweaker_003GridRef = 5
        for item in faceCtrls.get("L_upperCheekTweaker_003Ctrl"):
            L_upperCheekTweaker_003Btn = QtWidgets.QPushButton(item)
            L_upperCheekTweaker_003Btn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = faceCtrls.get("L_upperCheekTweaker_003Ctrl").get(item)
            L_upperCheekTweaker_003Btn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_upperCheekTweaker_003Btn, L_upperCheekTweaker_003GridRef, 8)
            L_upperCheekTweaker_003GridRef+=1
            
        R_nostrilGridRef = 6
        for item in faceCtrls.get("R_nostrilCtrl"):
            R_nostrilBtn = QtWidgets.QPushButton(item)
            R_nostrilBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_nostrilCtrl").get(item)
            R_nostrilBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_nostrilBtn, R_nostrilGridRef, 4)
            R_nostrilGridRef+=1
            
        R_noseGridRef = 7
        for item in faceCtrls.get("R_noseCtrl"):
            R_noseBtn = QtWidgets.QPushButton(item)
            R_noseBtn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = faceCtrls.get("R_noseCtrl").get(item)
            R_noseBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_noseBtn, R_noseGridRef, 4)
            R_noseGridRef+=1
            
        L_nostrilGridRef = 6
        for item in faceCtrls.get("L_nostrilCtrl"):
            L_nostrilBtn = QtWidgets.QPushButton(item)
            L_nostrilBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_nostrilCtrl").get(item)
            L_nostrilBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_nostrilBtn, L_nostrilGridRef, 6)
            L_nostrilGridRef+=1
            
        L_noseGridRef = 7
        for item in faceCtrls.get("L_noseCtrl"):
            L_noseBtn = QtWidgets.QPushButton(item)
            L_noseBtn.setStyleSheet('background-color: rgb(70, 108, 232);color: black')
            value = faceCtrls.get("L_noseCtrl").get(item)
            L_noseBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_noseBtn, L_noseGridRef, 6)
            L_noseGridRef+=1
            
        C_noseGridRef = 6
        for item in faceCtrls.get("C_noseCtrl"):
            C_noseBtn = QtWidgets.QPushButton(item)
            C_noseBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("C_noseCtrl").get(item)
            C_noseBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(C_noseBtn, C_noseGridRef, 5)
            C_noseGridRef+=1
            
        C_noseTipGridRef = 7
        for item in faceCtrls.get("C_noseTipCtrl"):
            C_noseTipBtn = QtWidgets.QPushButton(item)
            C_noseTipBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("C_noseTipCtrl").get(item)
            C_noseTipBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(C_noseTipBtn, C_noseTipGridRef, 5)
            C_noseTipGridRef+=1
            
        R_cheekGridRef = 8
        for item in faceCtrls.get("R_cheekCtrl"):
            R_cheekBtn = QtWidgets.QPushButton(item)
            R_cheekBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_cheekCtrl").get(item)
            R_cheekBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_cheekBtn, R_cheekGridRef, 0)
            R_cheekGridRef+=1
            
        L_cheekGridRef = 8
        for item in faceCtrls.get("L_cheekCtrl"):
            L_cheekBtn = QtWidgets.QPushButton(item)
            L_cheekBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_cheekCtrl").get(item)
            L_cheekBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_cheekBtn, L_cheekGridRef, 10)
            L_cheekGridRef+=1
            
        R_mouthCornerGridRef = 11
        for item in faceCtrls.get("R_mouthCornerCtrl"):
            R_mouthCornerBtn = QtWidgets.QPushButton(item)
            R_mouthCornerBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_mouthCornerCtrl").get(item)
            R_mouthCornerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_mouthCornerBtn, R_mouthCornerGridRef, 2)
            R_mouthCornerGridRef+=1
            
        R_mouthCornerTweakerGridRef = 11
        for item in faceCtrls.get("R_mouthCornerTweakerCtrl"):
            R_mouthCornerTweakerBtn = QtWidgets.QPushButton(item)
            R_mouthCornerTweakerBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_mouthCornerTweakerCtrl").get(item)
            R_mouthCornerTweakerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_mouthCornerTweakerBtn, R_mouthCornerTweakerGridRef, 3)
            R_mouthCornerTweakerGridRef+=1
            
        R_upperlipTweakerGridRef = 10
        for item in faceCtrls.get("R_upperlipTweakerCtrl"):
            R_upperlipTweakerBtn = QtWidgets.QPushButton(item)
            R_upperlipTweakerBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_upperlipTweakerCtrl").get(item)
            R_upperlipTweakerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_upperlipTweakerBtn, R_upperlipTweakerGridRef, 4)
            R_upperlipTweakerGridRef+=1
            
        R_lowerlipTweakerGridRef = 12
        for item in faceCtrls.get("R_lowerlipTweakerCtrl"):
            R_lowerlipTweakerBtn = QtWidgets.QPushButton(item)
            R_lowerlipTweakerBtn.setStyleSheet('background-color: rgb(205,51,51);color: black')
            value = faceCtrls.get("R_lowerlipTweakerCtrl").get(item)
            R_lowerlipTweakerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(R_lowerlipTweakerBtn, R_lowerlipTweakerGridRef, 4)
            R_lowerlipTweakerGridRef+=1
            
        L_mouthCornerGridRef = 11
        for item in faceCtrls.get("L_mouthCornerCtrl"):
            L_mouthCornerBtn = QtWidgets.QPushButton(item)
            L_mouthCornerBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_mouthCornerCtrl").get(item)
            L_mouthCornerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_mouthCornerBtn, L_mouthCornerGridRef, 8)
            L_mouthCornerGridRef+=1
            
        L_mouthCornerTweakerGridRef = 11
        for item in faceCtrls.get("L_mouthCornerTweakerCtrl"):
            L_mouthCornerTweakerBtn = QtWidgets.QPushButton(item)
            L_mouthCornerTweakerBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_mouthCornerTweakerCtrl").get(item)
            L_mouthCornerTweakerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_mouthCornerTweakerBtn, L_mouthCornerTweakerGridRef, 7)
            L_mouthCornerTweakerGridRef+=1
            
        L_upperlipTweakerGridRef = 10
        for item in faceCtrls.get("L_upperlipTweakerCtrl"):
            L_upperlipTweakerBtn = QtWidgets.QPushButton(item)
            L_upperlipTweakerBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_upperlipTweakerCtrl").get(item)
            L_upperlipTweakerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_upperlipTweakerBtn, L_upperlipTweakerGridRef, 6)
            L_upperlipTweakerGridRef+=1
            
        L_lowerlipTweakerGridRef = 12
        for item in faceCtrls.get("L_lowerlipTweakerCtrl"):
            L_lowerlipTweakerBtn = QtWidgets.QPushButton(item)
            L_lowerlipTweakerBtn.setStyleSheet('background-color: rgb(102,205,0);color: black')
            value = faceCtrls.get("L_lowerlipTweakerCtrl").get(item)
            L_lowerlipTweakerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(L_lowerlipTweakerBtn, L_lowerlipTweakerGridRef, 6)
            L_lowerlipTweakerGridRef+=1
            
        C_upperlipGridRef = 9
        for item in faceCtrls.get("C_upperlipCtrl"):
            C_upperlipBtn = QtWidgets.QPushButton(item)
            C_upperlipBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("C_upperlipCtrl").get(item)
            C_upperlipBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(C_upperlipBtn, C_upperlipGridRef, 5)
            C_upperlipGridRef+=1
            
        C_lowerlipGridRef = 13
        for item in faceCtrls.get("C_lowerlipCtrl"):
            C_lowerlipBtn = QtWidgets.QPushButton(item)
            C_lowerlipBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("C_lowerlipCtrl").get(item)
            C_lowerlipBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(C_lowerlipBtn, C_lowerlipGridRef, 5)
            C_lowerlipGridRef+=1
            
        C_upperlipTweakerGridRef = 10
        for item in faceCtrls.get("C_upperlipTweakerCtrl"):
            C_upperlipTweakerBtn = QtWidgets.QPushButton(item)
            C_upperlipTweakerBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("C_upperlipTweakerCtrl").get(item)
            C_upperlipTweakerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(C_upperlipTweakerBtn, C_upperlipTweakerGridRef, 5)
            C_upperlipTweakerGridRef+=1
            
        C_lowerlipTweakerGridRef = 12
        for item in faceCtrls.get("C_lowerlipTweakerCtrl"):
            C_lowerlipTweakerBtn = QtWidgets.QPushButton(item)
            C_lowerlipTweakerBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("C_lowerlipTweakerCtrl").get(item)
            C_lowerlipTweakerBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(C_lowerlipTweakerBtn, C_lowerlipTweakerGridRef, 5)
            C_lowerlipTweakerGridRef+=1
            
        mouthRegionGridRef = 11
        for item in faceCtrls.get("mouthRegionCtrl"):
            mouthRegionBtn = QtWidgets.QPushButton(item)
            mouthRegionBtn.setStyleSheet('background-color: rgb(255,193,37);color: black')
            value = faceCtrls.get("mouthRegionCtrl").get(item)
            mouthRegionBtn.clicked.connect(partial(self.runSelect, value))
            self.tab4.layout.addWidget(mouthRegionBtn, mouthRegionGridRef, 4,1,3)
            mouthRegionGridRef+=1
        
        self.tab4.setLayout(self.tab4.layout)
        
        
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
        headCtrls = {"Head":"*head_ctrl", "Neck":"*neck_ctrl"}
        return headCtrls
        
    def getSpineControls(self):
        spineCtrls = {"Spine Master":"*spine_master_ctrl", "Upper Spine":"*upperspine_IK_ctrl", "Lower Spine":"*lowerspine_IK_ctrl", "Hips":"*hips_IK_ctrl"}
        return spineCtrls
    
    def getLeftArmControlsIK(self):
        lArmCtrls = {"Left Clavicle":"*L_clavicle_ctrl","Left Elbow Ctrl":"*L_elbow_IK_ctrl","Left Arm IK":"*L_arm_IK_ctrl"}
        return lArmCtrls
    def getLeftArmControlsFK(self):
        lArmCtrls = {"Left Clavicle":"*L_clavicle_ctrl","Left Shoulder":"*L_shoulder_FK_ctrl", "Left Elbow":"*L_elbow_FK_ctrl", "Left Wrist":"*L_wrist_FK_ctrl"}
        return lArmCtrls
        
    def getRightArmControlsIK(self):
        rArmCtrls = {"Right Clavicle":"*R_clavicle_ctrl","Right Elbow Ctrl":"*R_elbow_IK_ctrl","Right Arm IK":"*R_arm_IK_ctrl"}
        return rArmCtrls
    def getRightArmControlsFK(self):
        rArmCtrls = {"Right Clavicle":"*R_clavicle_ctrl","Right Shoulder":"*R_shoulder_FK_ctrl", "Right Elbow":"*R_elbow_FK_ctrl", "Right Wrist":"*R_wrist_FK_ctrl"}
        return rArmCtrls
        
    def getRightLegControls(self):
        rLegCtrls = {"Right Leg IK":"*R_leg_IK_ctrl","Right Leg Knee":"*R_knee_IK_ctrl","Toe":"*R_toe_ctrl", "Toe Pivot":"*R_toePivot_ctrl", "Heel Pivot":"*R_heelPivot_ctrl"}
        return rLegCtrls
        
    def getCogControls(self):
        cogCtrls = {"Cog Ctrl":"*COG_ctrl"}
        return cogCtrls
        
    def getLeftLegControls(self):
        leftLegCtrls = {"Knee":"*L_knee_IK_ctrl", "Foot IK Ctrl":"*L_leg_IK_ctrl", "Toe":"*L_toe_ctrl", "Toe Pivot":"*L_toePivot_ctrl"}
        return leftLegCtrls
        
    def getRightLegControls(self):
        rightLegCtrls = {"Knee":"*R_knee_IK_ctrl", "Foot IK Ctrl":"*R_leg_IK_ctrl", "Toe":"*R_toe_ctrl", "Toe Pivot":"*R_toePivot_ctrl"}
        return rightLegCtrls
        
    def getLeftFingerControls(self):
        indexCtrls = {"Knuckle":"*L_index1_ctrl", "Mid":"*L_index2_ctrl", "Distal":"*L_index3_ctrl"}
        middleCtrls = {"Knuckle":"*L_middle1_ctrl", "Mid":"*L_middle2_ctrl", "Distal":"*L_middle3_ctrl"}
        ringCtrls = {"Knuckle":"*L_ring1_ctrl", "Mid":"*L_ring2_ctrl", "Distal":"*L_ring3_ctrl"}
        pinkyCtrls = {"Knuckle":"*L_pinke1_ctrl", "Mid":"*L_pinke2_ctrl", "Distal":"*L_pinke3_ctrl"}
        thumbCtrls = {"Knuckle":"*L_thumb1_ctrl", "Mid":"*L_thumb2_ctrl", "Distal":"*L_thumb3_ctrl"}
        
        leftFingerCtrls = {"indexCtrls":indexCtrls, "middleCtrls":middleCtrls,"ringCtrls":ringCtrls,"pinkyCtrls":pinkyCtrls,"thumbCtrls":thumbCtrls,}
        return leftFingerCtrls
        
    def getRightFingerControls(self):
        indexCtrls = {"Knuckle":"*R_index1_ctrl", "Mid":"*R_index2_ctrl", "Distal":"*R_index3_ctrl"}
        middleCtrls = {"Knuckle":"*R_middle1_ctrl", "Mid":"*R_middle2_ctrl", "Distal":"*R_middle3_ctrl"}
        ringCtrls = {"Knuckle":"*R_ring1_ctrl", "Mid":"*R_ring2_ctrl", "Distal":"*R_ring3_ctrl"}
        pinkyCtrls = {"Knuckle":"*R_pinke1_ctrl", "Mid":"*R_pinke2_ctrl", "Distal":"*R_pinke3_ctrl"}
        thumbCtrls = {"Knuckle":"*R_thumb1_ctrl", "Mid":"*R_thumb2_ctrl", "Distal":"*R_thumb3_ctrl"}
        
        rightFingerCtrls = {"indexCtrls":indexCtrls, "middleCtrls":middleCtrls,"ringCtrls":ringCtrls,"pinkyCtrls":pinkyCtrls,"thumbCtrls":thumbCtrls,}
        return rightFingerCtrls
    
    def getFaceControls(self):
        R_eyebrowMassCtrl = {" ":"*R_eyebrow_ctrl"}
        L_eyebrowMassCtrl = {" ":"*L_eyebrow_ctrl"}
        R_eyebrowCtrl1 = {" ":"*R_eyebrowOuter_ctrl"}
        R_eyebrowCtrl2 = {" ":"*R_eyebrowMid2_ctrl"}
        R_eyebrowCtrl3 = {" ":"*R_eyebrowMid1_ctrl"}
        R_eyebrowCtrl4 = {" ":"*R_eyebrowInner_ctrl"}
        L_eyebrowCtrl1 = {" ":"*L_eyebrowOuter_ctrl"}
        L_eyebrowCtrl2 = {" ":"*L_eyeBrowMid2_ctrl"}
        L_eyebrowCtrl3 = {" ":"*L_eyeBrowMid1_ctrl"}
        L_eyebrowCtrl4 = {" ":"*L_eyebrowInner_ctrl"}
        C_eyebrowCtrl = {" ":"*C_eyeBrowMiddle_ctrl"}
        R_eyeCorner_outerCtrl = {" ":"*R_eyeCorner_outer_ctrl"}
        R_eyeLid_UpperOuterCtrl = {" ":"*R_eyeLid_UpperOuter_ctrl"}
        R_eyeLid_UpperMiddleCtrl = {" ":"*R_eyeLid_UpperMiddle_ctrl"}
        R_eyeLid_UpperInnerCtrl = {" ":"*R_eyeLid_UpperInner_ctrl"}
        R_eyeCorner_innerCtrl = {" ":"*R_eyeCorner_inner_ctrl"}
        R_eyeLid_LowerOuterCtrl = {" ":"*R_eyeLid_LowerOuter_ctrl"}
        R_eyeLid_LowerMiddleCtrl = {" ":"*R_eyeLid_LowerMiddle_ctrl"}
        R_eyeLid_LowerInnerCtrl = {" ":"*R_eyeLid_LowerInner_ctrl"}
        L_eyeCorner_outerCtrl = {" ":"*L_eyeCorner_outer_ctrl"}
        L_eyeLid_UpperOuterCtrl = {" ":"*L_eyeLid_UpperOuter_ctrl"}
        L_eyeLid_UpperMiddleCtrl = {" ":"*L_eyeLid_UpperMiddle_ctrl"}
        L_eyeLid_UpperInnerCtrl = {" ":"*L_eyeLid_UpperInner_ctrl"}
        L_eyeCorner_innerCtrl = {" ":"*L_eyeCorner_inner_ctrl"}
        L_eyeLid_LowerOuterCtrl = {" ":"*L_eyeLid_LowerOuter_ctrl"}
        L_eyeLid_LowerMiddleCtrl = {" ":"*L_eyeLid_LowerMiddle_ctrl"}
        L_eyeLid_LowerInnerCtrl = {" ":"*L_eyeLid_LowerInner_ctrl"}
        R_upperCheekTweaker_001Ctrl = {" ":"*R_upperCheekTweaker_001_ctrl"}
        R_upperCheekTweaker_002Ctrl = {" ":"*R_upperCheekTweaker_002_ctrl"} 
        R_upperCheekTweaker_003Ctrl = {" ":"*R_upperCheekTweaker_003_ctrl"}
        L_upperCheekTweaker_001Ctrl = {" ":"*L_upperCheekTweaker_001_ctrl"}
        L_upperCheekTweaker_002Ctrl = {" ":"*L_upperCheekTweaker_002_ctrl"} 
        L_upperCheekTweaker_003Ctrl = {" ":"*L_upperCheekTweaker_003_ctrl"}
        R_nostrilCtrl = {" ":"*R_nostril_ctrl"}
        R_noseCtrl = {" ":"*R_nose_ctrl"}
        L_nostrilCtrl = {" ":"*L_nostril_ctrl"}
        L_noseCtrl = {" ":"*L_nose_ctrl"}
        C_noseCtrl = {" ":"*C_nose_ctrl"}
        C_noseTipCtrl = {" ":"*C_noseTip_ctrl"}
        R_cheekCtrl = {" ":"*R_cheek_ctrl"}
        L_cheekCtrl = {" ":"*L_cheek_ctrl"}
        R_mouthCornerCtrl = {" ":"*R_mouthCorner_ctrl"}
        R_mouthCornerTweakerCtrl = {" ":"*R_lowerlipCornerTweaker_ctrl"}
        R_upperlipTweakerCtrl = {" ":"*R_upperlipTweaker_ctrl"}
        R_lowerlipTweakerCtrl = {" ":"*R_lowerlipTweaker_ctrl"}
        L_mouthCornerCtrl = {" ":"*L_mouthCorner_ctrl"}
        L_mouthCornerTweakerCtrl = {" ":"*L_lowerlipCornerTweaker_ctrl"}
        L_upperlipTweakerCtrl = {" ":"*L_upperlipTweaker_ctrl"}
        L_lowerlipTweakerCtrl = {" ":"*L_lowerlipTweaker_ctrl"}
        mouthRegionCtrl = {" ":"*mouthRegion_ctrl"}
        C_upperlipCtrl = {" ":"*C_upperlip_ctrl"}
        C_upperlipTweakerCtrl = {" ":"*C_upperlipTweaker_ctrl"}
        C_lowerlipCtrl = {" ":"*C_lowerlip_ctrl"}
        C_lowerlipTweakerCtrl = {" ":"*C_lowerlipTweaker_ctrl"}
        C_jawCtrl = {" ":"*C_jaw_ctrl"}
        
        
        faceCtrls = {"R_eyebrowMassCtrl":R_eyebrowMassCtrl, "L_eyebrowMassCtrl":L_eyebrowMassCtrl, 
        "R_eyebrowCtrl1":R_eyebrowCtrl1, "R_eyebrowCtrl2":R_eyebrowCtrl2, "R_eyebrowCtrl3":R_eyebrowCtrl3, "R_eyebrowCtrl4":R_eyebrowCtrl4, 
        "L_eyebrowCtrl1":L_eyebrowCtrl1, "L_eyebrowCtrl2":L_eyebrowCtrl2, "L_eyebrowCtrl3":L_eyebrowCtrl3, "L_eyebrowCtrl4":L_eyebrowCtrl4, 
        "C_eyebrowCtrl":C_eyebrowCtrl, 
        "R_eyeCorner_outerCtrl":R_eyeCorner_outerCtrl, "R_eyeLid_UpperOuterCtrl":R_eyeLid_UpperOuterCtrl, "R_eyeLid_UpperMiddleCtrl":R_eyeLid_UpperMiddleCtrl, "R_eyeLid_UpperInnerCtrl":R_eyeLid_UpperInnerCtrl, "R_eyeCorner_innerCtrl":R_eyeCorner_innerCtrl, 
        "R_eyeLid_LowerOuterCtrl":R_eyeLid_LowerOuterCtrl, "R_eyeLid_LowerMiddleCtrl":R_eyeLid_LowerMiddleCtrl, "R_eyeLid_LowerInnerCtrl":R_eyeLid_LowerInnerCtrl, 
        "L_eyeCorner_outerCtrl":L_eyeCorner_outerCtrl, "L_eyeLid_UpperOuterCtrl":L_eyeLid_UpperOuterCtrl, "L_eyeLid_UpperMiddleCtrl":L_eyeLid_UpperMiddleCtrl, "L_eyeLid_UpperInnerCtrl":L_eyeLid_UpperInnerCtrl, "L_eyeCorner_innerCtrl":L_eyeCorner_innerCtrl, 
        "L_eyeLid_LowerOuterCtrl":L_eyeLid_LowerOuterCtrl, "L_eyeLid_LowerMiddleCtrl":L_eyeLid_LowerMiddleCtrl, "L_eyeLid_LowerInnerCtrl":L_eyeLid_LowerInnerCtrl, 
        "R_upperCheekTweaker_001Ctrl":R_upperCheekTweaker_001Ctrl, "R_upperCheekTweaker_002Ctrl":R_upperCheekTweaker_002Ctrl, "R_upperCheekTweaker_003Ctrl":R_upperCheekTweaker_003Ctrl, 
        "L_upperCheekTweaker_001Ctrl":L_upperCheekTweaker_001Ctrl, "L_upperCheekTweaker_002Ctrl":L_upperCheekTweaker_002Ctrl, "L_upperCheekTweaker_003Ctrl":L_upperCheekTweaker_003Ctrl, 
        "R_nostrilCtrl":R_nostrilCtrl, "R_noseCtrl":R_noseCtrl, 
        "L_nostrilCtrl":L_nostrilCtrl, "L_noseCtrl":L_noseCtrl, 
        "C_noseTipCtrl":C_noseTipCtrl, "C_noseCtrl":C_noseCtrl, 
        "R_cheekCtrl":R_cheekCtrl, 
        "L_cheekCtrl":L_cheekCtrl, 
        "R_mouthCornerCtrl":R_mouthCornerCtrl, "R_mouthCornerTweakerCtrl":R_mouthCornerTweakerCtrl, "R_upperlipTweakerCtrl":R_upperlipTweakerCtrl, "R_lowerlipTweakerCtrl":R_lowerlipTweakerCtrl, 
        "L_mouthCornerCtrl":L_mouthCornerCtrl, "L_mouthCornerTweakerCtrl":L_mouthCornerTweakerCtrl, "L_upperlipTweakerCtrl":L_upperlipTweakerCtrl, "L_lowerlipTweakerCtrl":L_lowerlipTweakerCtrl, 
        "mouthRegionCtrl":mouthRegionCtrl, 
        "C_upperlipCtrl":C_upperlipCtrl, "C_upperlipTweakerCtrl":C_upperlipTweakerCtrl, 
        "C_lowerlipCtrl":C_lowerlipCtrl, "C_lowerlipTweakerCtrl":C_lowerlipTweakerCtrl, 
        "C_jawCtrl":"*C_jawCtrl",}
        return faceCtrls
    

        


try:
    ui.close()
except:
    pass

ui = PickerUi()
ui.show()


