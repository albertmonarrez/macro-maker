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
        
        if self.macro_dictionary.get('triggers'):
            for key in self.macro_dictionary.get('triggers'):
                self.combobox.addItem(key)

        ctext=self.combobox.currentText()
        if self.macro_dictionary.get(unicode(ctext)):
            macro_list=self.macro_dictionary.get(unicode(ctext))
            self.listWidget.addItems(macro_list.values())
            self.listWidget.setCurrentRow(0)
            
        main_vertical_layout=QVBoxLayout()
        buttonLayout = QVBoxLayout()
        layout = QHBoxLayout()        
        for text, slot in (("&Add...", self.add),
                           ("Duplicate",self.duplicate),
                           ("&Edit...", self.edit),
                           ("&Remove...", self.remove),
                           ("&Up", self.up),
                           ("&Down", self.down),
                           ("&Sort", self.listWidget.sortItems),
                           ("Close", self.accept)
                           ):
            button = QPushButton(text)
            button.setFocusPolicy(Qt.NoFocus)
            if text == "Close":
                buttonLayout.addStretch()
            buttonLayout.addWidget(button)
            self.connect(button, SIGNAL("clicked()"), slot)
            

        layout.addWidget(self.listWidget)
        layout.addLayout(buttonLayout)
        main_vertical_layout.addWidget(self.combobox)
        main_vertical_layout.addLayout(layout)
        
        self.setLayout(main_vertical_layout)
        self.setWindowTitle("%s" % self.name)


    def add(self):
        row = self.listWidget.currentRow()
        title = "Add %s" % self.action
        string, ok = QInputDialog.getText(self, title, title)
        if ok and not string.isEmpty():
            self.listWidget.insertItem(row, string)

    def duplicate(self):
        """Duplicates an item and adds it to the row below current"""
        
        row=self.listWidget.currentRow()
        item=self.listWidget.item(row)
        if item is not None:
            self.listWidget.insertItem(row,item.text())
        
    def edit(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        if item is not None:
            title = "Edit %s" % self.action
            string, ok = QInputDialog.getText(self, title, title,
                                QLineEdit.Normal, item.text())
            if ok and not string.isEmpty():
                item.setText(string)

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

    def up(self):
        row = self.listWidget.currentRow()
        if row >= 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, item)
            self.listWidget.setCurrentItem(item)

    def down(self):
        row = self.listWidget.currentRow()
        if row < self.listWidget.count() - 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row + 1, item)
            self.listWidget.setCurrentItem(item)

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
    fruit = ["Banana", "Apple", "Elderberry", "Clementine", "Fig",
             "Guava", "Mango", "Honeydew Melon", "Date", "Watermelon",
             "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi",
             "Lemon", "Nectarine", "Plum", "Raspberry", "Strawberry",
             "Orange"]
    app = QApplication(sys.argv)
    form = MACRO_EDITOR(config_dict=fig)
    form.exec_()

