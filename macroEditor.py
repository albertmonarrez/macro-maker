import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from configobj import ConfigObj



class MACRO_EDITOR(QDialog):

    def __init__(self, name='Macro Editor', config_dict={}, parent=None):
        super(MACRO_EDITOR, self).__init__(parent)

        self.name = name
        self.action='action'
        self.macro_dictionary=config_dict
        self.setMinimumSize(500,400)
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
        
        if self.macro_dictionary.get('triggers'):
            for key in self.macro_dictionary.get('triggers'):
                self.combobox.addItem(key)

        ctext=self.combobox.currentText()
        if self.macro_dictionary.get(unicode(ctext)):
            macro_list=self.macro_dictionary.get(unicode(ctext))
            self.listWidget.addItems(macro_list.values())
            self.listWidget.setCurrentRow(0)        
        
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
        
        
    def append_items(self,dictionary):
        """Takes a list of items and appends them to the model"""
        for macro in dictionary:
            qmacro=QStandardItem(macro)
            self.root_node.appendRow(qmacro)
            for item in dictionary[macro].values():
                qitem=QStandardItem(item)
                qmacro.appendRow(qitem)
                
    def add_buttons(self):
        
        buttonLayout = QVBoxLayout()
        for text, slot in (("&Add...", self.add),
                           ("Duplicate",self.duplicate),
                           ("&Edit...", self.edit),
                           ("&Remove...", self.remove),
                           ("&Up", self.up),
                           ("&Down", self.down),
                           ("&Rename\nMacro...", self.rename_macro),
                           ("Close", self.accept)
                           ):
            button = QPushButton(text)
            button.setFocusPolicy(Qt.NoFocus)
            if text == "Close":
                buttonLayout.addStretch()
            buttonLayout.addWidget(button)
            self.connect(button, SIGNAL("clicked()"), slot)

        return buttonLayout  
                
    def rename_macro(self):
        pass

    def set_list(self):
        current_macro=unicode(self.combobox.currentText())
        macro_actions=self.get_current_list()
        self.macro_dictionary[current_macro]=macro_actions
        print self.macro_dictionary
        
    def on_activated(self):
        current_macro=self.combobox.currentText()
        macro_actions=self.macro_dictionary.get(unicode(current_macro))
        self.listWidget.clear()
        try:
            self.listWidget.addItems(macro_actions.values())
        except AttributeError:
            self.listWidget.addItems(macro_actions)
                
    def add(self):
        row = self.listWidget.currentRow()
        title = "Add %s" % self.action
        string, ok = QInputDialog.getText(self, title, title)
        if ok and not string.isEmpty():
            self.listWidget.insertItem(row, string)
            self.set_list()

    def duplicate(self):
        """Duplicates an item and adds it to the row below current"""
        
        row=self.listWidget.currentRow()
        item=self.listWidget.item(row)
        if item is not None:
            self.listWidget.insertItem(row,item.text())
            self.set_list()
        
    def edit(self):
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
        row = self.listWidget.currentRow()
        if row >= 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, item)
            self.listWidget.setCurrentItem(item)
            self.set_list()

    def down(self):
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
        items = []
        for index in xrange(self.listWidget.count()):
            items.append('%s'%self.listWidget.item(index).text())
        
        return items


if __name__ == "__main__":
    filename="C:/pythonCustomCode/PythonWinService/macroconfig.cfg"
    fig=ConfigObj(filename,list_values=False)
    lightclaws=fig.get('LightClaws')
    app = QApplication(sys.argv)
    form = MACRO_EDITOR(config_dict=fig)
    form.exec_()

