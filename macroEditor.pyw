#!python2.7
import sys
import os
import genmacro
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from configobj import ConfigObj
import keyboard as k
import config

class MACRO_EDITOR(QMainWindow):

    def __init__(self, name='', config_dict={}, parent=None,file_name=None):
        super(MACRO_EDITOR, self).__init__(parent)
        
        self.main_widget=QWidget(self)#widget for holding my layout
        
        self.savepath=file_name
        self.name = 'Macro Editor: '+self.savepath
        self.action='action'+' '*130#lazy hack to resize dialog boxes until I do it properly
        self.macro_dictionary=config_dict
        self.setMinimumSize(550,550)
        self.count=1
        
        self.listWidget = QListWidget()
        self.macrobox = QComboBox()
        self.triggerbox=QComboBox()
        self.triggerbox2=QComboBox()
        self.triggerbox3=QComboBox()
        self.statusBar()
   
        
        self.tbox_list=[self.triggerbox,self.triggerbox2,self.triggerbox3]
        
        #connect activites to functions
        self.listWidget.doubleClicked.connect(self.edit)        
        self.macrobox.activated[str].connect(self.on_activated)        
        for combobox in self.tbox_list:
            combobox.activated[str].connect(self.update_macro_dictionary)
        
        #menubar
        menu_bar=self.menuBar()
        
        f=menu_bar.addMenu('&File')
        e=menu_bar.addMenu('&Edit')
        self.menu_item(f,'Save',self.save,tooltip='Saves file to default directory.')
        self.menu_item(f,'Save As',self.file_dialog,tooltip='Saves file to specified path.')
        self.menu_item(f,'Load',self.load,tooltip='Loads a macro file.')
        self.menu_item(e,'Add Macro',self.add_new_macro,tooltip='Create a new empty macro')
        self.menu_item(e,'Duplicate Current Macro',self.duplicate_macro,tooltip='Makes a copy of the current macro')
        self.menu_item(e,'Delete Current Macro',self.delete_macro,tooltip='Deletes the current macro')
        
        #shorcuts
        save_as=QShortcut(QKeySequence("Ctrl+Shift+S"),self,self.file_dialog)
        save=QShortcut(QKeySequence("Ctrl+S"),self,self.save)
        duplicate=QShortcut(QKeySequence("Ctrl+D"),self,self.duplicate)
        delete=QShortcut(QKeySequence("Del"),self,self.remove)
        up=QShortcut(QKeySequence("Cntrl+Up"),self,self.up)
        down=QShortcut(QKeySequence("Cntrl+Down"),self,self.down)
        
        #layout
        two_combo=QHBoxLayout()
        two_combo.addWidget(self.macrobox,1)
        two_combo.addWidget(self.triggerbox)
        two_combo.addWidget(self.triggerbox2)
        two_combo.addWidget(self.triggerbox3)
        list_and_buttons = QHBoxLayout()    
        buttonLayout=self.add_buttons()
        list_and_buttons.addWidget(self.listWidget)
        list_and_buttons.addLayout(buttonLayout)

        self.main_vertical_layout=self.make_layout([two_combo,
                                                    list_and_buttons])
        
        self.main_widget.setLayout(self.main_vertical_layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("%s" % self.name)
        self.initialize_fields()
        
    def menu_item(self,menubar,action_name,method,shortcut=None,tooltip=''):
        "Easier way to add menu items with function attached"
        
        action = QAction(action_name, self)
        if shortcut:
            action.setShortcut(shortcut)
        action.setStatusTip(tooltip)
        action.triggered.connect(method)
        menubar.addAction(action)
        
    def load(self):
        fileName =QFileDialog.getOpenFileName(parent=self,caption='Choose file to load',directory=self.savepath,filter='cfg files (*.cfg)')
        if fileName:
            fig=ConfigObj(unicode(fileName),list_values=False)
            self.macro_dictionary=fig
            self.savepath=fileName
            self.initialize_fields()
    
    def set_triggers(self,current_macro,combobox_list):
        
        triggers=[]
        for combobox in combobox_list:
            current_text=unicode(combobox.currentText())
            if current_text!='':
                triggers.append(current_text)
                
        self.macro_dictionary[current_macro]['trigger']=','.join(triggers)
        
    def update_macro_dictionary(self):
        
        current_macro=unicode(self.macrobox.currentText())
        self.set_triggers(current_macro, self.tbox_list)
        self.set_list()
        
    def initialize_fields(self):
        self.setWindowTitle("%s" % "Macro Editor: "+self.savepath)
        self.populate_combobox_marco(self.macrobox)
        self.populate_combobox_trigger(self.tbox_list)
        self.on_activated()
        
    def populate_combobox_marco(self,combobox):
        combobox.clear()
        for macro in self.macro_dictionary:
            combobox.addItem(macro)

        macro_name=combobox.currentText()
        if self.macro_dictionary.get(unicode(macro_name)):
            macro_list=self.macro_dictionary.get(unicode(macro_name))
            try:
                self.listWidget.addItems(macro_list['actions'].values())
                self.macro_dictionary=genmacro.dictionary_to_list(self.macro_dictionary)                
            except AttributeError:
                self.listWidget.addItems(macro_list['actions'])
                
            self.listWidget.setCurrentRow(0)
        
        
    def populate_combobox_trigger(self,combobox_list):
        for combobox in combobox_list:
            combobox.clear()
            combobox.addItem('')
            combobox.addItems(k.codes.keys())
            
    def make_layout(self,layout_items,layoutType='vertical'):
        """Creates the main body of the layout"""
        
        if layoutType=='vertical':
            main_layout=QVBoxLayout()
        else:
            main_layout=QHBoxLayout()
        for item in layout_items:
            try:
                main_layout.addWidget(item)
            except TypeError:
                main_layout.addLayout(item)
        return main_layout
    
    def add_new_macro(self):
        pass
    
    def duplicate_macro(self):
        macro=str(self.macrobox.currentText())
        
        copy=dict(self.macro_dictionary[macro])
        self.macro_dictionary[macro+str(self.count)]=copy
        self.initialize_fields()
        index=self.macrobox.findText(macro+str(self.count))
        self.macrobox.setCurrentIndex(index)
        self.count+=1
        
    def delete_macro(self):
        macro=str(self.macrobox.currentText())
        if macro:
            self.macro_dictionary.pop(macro)
            self.initialize_fields()
        
    def add_buttons(self):
        
        buttonLayout = QVBoxLayout()
        for text, slot in (("&Add...", self.add),
                           ("Duplicate",self.duplicate),
                           ("&Edit...", self.edit),
                           ("Remove...", self.remove),
                           ("Up", self.up),
                           ("Down", self.down),
                           ("&Rename\nMacro...", self.rename_macro),
                           ("Save As", self.file_dialog),
                           ("Save",self.save)                           
                           ):
            button = QPushButton(text)
            button.setFocusPolicy(Qt.NoFocus)
            if text == "Save As":
                buttonLayout.addStretch()
            buttonLayout.addWidget(button)
            self.connect(button, SIGNAL("clicked()"), slot)

        return buttonLayout  
                
    def rename_macro(self):
        macro_name=unicode(self.macrobox.currentText())
        index=self.macrobox.currentIndex()
        
        title = "Rename Macro"
        string, ok = QInputDialog.getText(self, title, title,
                            QLineEdit.Normal, macro_name)
        if ok and not string.isEmpty():
            self.macrobox.setItemText(index,string)
            s=unicode(string)
            self.macro_dictionary[s]=self.macro_dictionary.pop(macro_name)

    def set_list(self):
        """Grabs the current macro name from the combobox and updates macro_dictionary action list to what's displayed in list widget"""
        
        current_macro=unicode(self.macrobox.currentText())
        macro_actions=self.get_current_list()
        self.macro_dictionary[current_macro]['actions']=macro_actions
        
    def combobox_trigger_display(self,trigger,combobox_list):
        triggers=trigger.replace(' ','').split(',')
        
        for i in range(len(combobox_list)):
            try:
                index=combobox_list[i].findText(triggers[i])
                combobox_list[i].setCurrentIndex(index)
            except IndexError:#set to index zero: 'None'
                combobox_list[i].setCurrentIndex(0)
            
        
    def on_activated(self):
        """
        Upon changing the selection of a macro in the first combobox the list widget is cleared and new items 
        are displayed to reflect the current macro selection
        """
        
        current_macro=unicode(self.macrobox.currentText())
        macro_actions=self.macro_dictionary.get(current_macro)
        self.listWidget.clear()
        try:
            trigger=self.macro_dictionary[current_macro]['trigger']
            self.combobox_trigger_display(trigger, self.tbox_list)
        except KeyError:
            return False
        
        try:
            macro_actions.get('actions').values()
        except AttributeError:
            self.listWidget.addItems(macro_actions['actions'])
        else:
            self.listWidget.addItems(macro_actions['actions'].values())
            
    def add(self):
        """Adds a new item to the list widget"""
        
        row = self.listWidget.currentRow()
        title = "Add %s" % self.action
        string, ok = QInputDialog.getText(self, title, title)
        if ok and not string.isEmpty():
            self.listWidget.insertItem(row, string)
            self.set_list()

    def duplicate(self):
        """Duplicates selected item and adds it to the row below current"""
        
        row=self.listWidget.currentRow()
        item=self.listWidget.item(row)
        if item is not None:
            self.listWidget.insertItem(row,item.text())
            self.set_list()
        
    def edit(self):
        """Pops up a dialog box with text of the currently selected item in the list widget and lets you edit it"""
        
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        if item is not None:
            title = "Edit %s" % self.action
            string, ok = QInputDialog.getText(self, title, title,
                                QLineEdit.Normal, item.text())
            if ok and not string.isEmpty():
                item.setText(string)
                self.set_list()

    def remove(self):
        """Removes currently selected entry"""
        
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        if item is None:
            return
        reply = QMessageBox.question(self, "Remove %s" % self.action,
                        "Remove %s `%s'?" % (
                        self.action, unicode(item.text())),
                        QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            item = self.listWidget.takeItem(row)
            del item
            self.set_list()

    def up(self):
        """Moves currently selected item up 1"""
        
        row = self.listWidget.currentRow()
        if row >= 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, item)
            self.listWidget.setCurrentItem(item)
            self.set_list()

    def down(self):
        """Moves currently selected item down 1"""
        
        row = self.listWidget.currentRow()
        if row < self.listWidget.count() - 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row + 1, item)
            self.listWidget.setCurrentItem(item)
            self.set_list()

    def reject(self):
        self.accept()

    def accept(self):
        self.stringlist = QStringList()
        for row in range(self.listWidget.count()):
            self.stringlist.append(self.listWidget.item(row).text())
        self.emit(SIGNAL("acceptedList(QStringList)"), self.stringlist)
        QDialog.accept(self)
    
    def get_current_list(self):
        """Runs a loop on the listwidget to get all the items displayed in it and returns them."""
        
        items = []
        for index in xrange(self.listWidget.count()):
            items.append('%s'%self.listWidget.item(index).text())
        
        return items
    
    def save(self,filename=None):
        if not filename:filename=self.savepath
        genmacro.generate_macro(self.macro_dictionary,filename)
        self.statusBar().showMessage('Saved file: %s'%filename,3000)
        
        self.setWindowTitle("%s" % "Macro Editor: "+self.savepath)
        

    def file_dialog(self):
        """
        Opens a File dialog and saves a file
        """
        
        fileName = QFileDialog.getSaveFileName(parent=self,caption='Choose location to save csv',directory=self.savepath,filter='cfg files (*.cfg)')
        if fileName:
            self.savepath=fileName            
            self.save(fileName)
            
        

if __name__ == "__main__":
    filename=config.DEFAULT_PROFILE
    fig=ConfigObj(filename,list_values=False)
    
    app = QApplication(sys.argv)
    form = MACRO_EDITOR(config_dict=fig,file_name=filename)
    form.show()
    sys.exit(app.exec_())
