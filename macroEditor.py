import sys
import os
import genmacro
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from configobj import ConfigObj

class MACRO_EDITOR(QDialog):

    def __init__(self, name='Macro Editor', config_dict={}, parent=None):
        super(MACRO_EDITOR, self).__init__(parent)
        
        self.savepath="C:/pythonCustomCode/PythonWinService/macroconfig1.cfg"
        self.name = name
        self.action='action                                                                                                       '#lazy hack to resize dialog boxes until I do it properly
        self.macro_dictionary=config_dict
        self.setMinimumSize(550,550)
        self.listWidget = QListWidget()
        self.combobox = QComboBox()
        self.triggerbox=QComboBox()
        
        self.combobox.activated[str].connect(self.on_activated)
        self.populate_list()
        
        two_combo=QHBoxLayout()
        two_combo.addWidget(self.combobox)
        two_combo.addWidget(self.triggerbox)
        list_and_buttons = QHBoxLayout()    
        buttonLayout=self.add_buttons()
        list_and_buttons.addWidget(self.listWidget)
        list_and_buttons.addLayout(buttonLayout)

        self.main_vertical_layout=self.make_layout([two_combo,
                                                    list_and_buttons])
        
        self.setLayout(self.main_vertical_layout)
        self.setWindowTitle("%s" % self.name)
        
    def populate_list(self):
        
        for macro in self.macro_dictionary:
            self.combobox.addItem(macro)
            self.triggerbox.addItem(self.macro_dictionary[macro]['trigger'])

        ctext=self.combobox.currentText()
        if self.macro_dictionary.get(unicode(ctext)):
            macro_list=self.macro_dictionary.get(unicode(ctext))
            self.listWidget.addItems(macro_list['actions'].values())
            self.listWidget.setCurrentRow(0)        
        
        self.macro_dictionary=genmacro.dictionary_to_list(self.macro_dictionary)
        
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
                
    def add_buttons(self):
        
        buttonLayout = QVBoxLayout()
        for text, slot in (("&Add...", self.add),
                           ("Duplicate",self.duplicate),
                           ("&Edit...", self.edit),
                           ("&Remove...", self.remove),
                           ("&Up", self.up),
                           ("&Down", self.down),
                           ("&Rename\nMacro...", self.rename_macro),
                           ("Save As", self.file_dialog)
                           ):
            button = QPushButton(text)
            button.setFocusPolicy(Qt.NoFocus)
            if text == "Save As":
                buttonLayout.addStretch()
            buttonLayout.addWidget(button)
            self.connect(button, SIGNAL("clicked()"), slot)

        return buttonLayout  
                
    def rename_macro(self):
        macro_name=unicode(self.combobox.currentText())
        index=self.combobox.currentIndex()
        
        title = "Rename Macro"
        string, ok = QInputDialog.getText(self, title, title,
                            QLineEdit.Normal, macro_name)
        if ok and not string.isEmpty():
            self.combobox.setItemText(index,string)
            s=unicode(string)
            self.macro_dictionary[s]=self.macro_dictionary.pop(macro_name)

    def set_list(self):
        """Grabs the current macro name from the combobox and updates macro_dictionary action list to what's displayed in list widget"""
        
        current_macro=unicode(self.combobox.currentText())
        macro_actions=self.get_current_list()
        self.macro_dictionary[current_macro]['actions']=macro_actions
        
        
    def on_activated(self):
        """
        Upon changing the selection of a macro in the first combobox the list widget is cleared and new items 
        are displayed to reflect the current macro selection
        """
        
        current_macro=unicode(self.combobox.currentText())
        macro_actions=self.macro_dictionary.get(current_macro)
        self.listWidget.clear()
        
        trigger=self.macro_dictionary[current_macro]['trigger']
        index=self.triggerbox.findText(trigger)
        self.triggerbox.setCurrentIndex(index)  
        
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
    
    def file_dialog(self):
        """
        Opens a File dialog and saves a file
        """
        
        fileName = QFileDialog.getSaveFileName(parent=self,caption='Choose location to save csv',directory=self.savepath,filter='cfg files (*.cfg)')
        if fileName:
            self.savepath=fileName            
            genmacro.generate_macro(self.macro_dictionary,fileName)
        

if __name__ == "__main__":
    filename="macroconfig.cfg"
    fig=ConfigObj(filename,list_values=False)
    app = QApplication(sys.argv)
    form = MACRO_EDITOR(config_dict=fig)
    form.exec_()

