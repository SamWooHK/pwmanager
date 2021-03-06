# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QStringListModel
from ui import Ui_MainWindow
import sys
import sqlite3

#database
conn = sqlite3.connect("data.db") #for test use ':memory:' so no db created
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS password(
            site text unique,
            id text,
            password text
            )""")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.viewagent()
        self.setFixedSize(430,310)

        self.setWindowIcon(QtGui.QIcon('icon.png'))
        # set the title
        self.setWindowTitle("Icon")

        #button clicked
        self.ui.generate.clicked.connect(self.generate_pw)
        self.ui.new_btn.clicked.connect(self.clear_input)
        self.ui.del_btn.clicked.connect(self.del_data)
        self.ui.save_btn.clicked.connect(self.update_data)

    #viewList
    def viewagent(self):
        slm=QStringListModel()

        #get data from db
        self.ui.qList=[]
        agentlist=c.execute("SELECT site FROM password ORDER BY site").fetchall()
        for i in range(len(agentlist)):
            self.ui.qList.append(agentlist[i][0])

        slm.setStringList(self.ui.qList)
        self.ui.listView.setModel(slm)
        self.ui.listView.clicked.connect(self.list_clicked)

    #button function
    def clear_input(self):
        self.ui.site_input.setText("")
        self.ui.user_name_input.setText("")
        self.ui.pw_input.setText("")
        self.viewagent()

    def list_clicked(self,qModelIndex):
        global site_name, user
        site_name=self.ui.qList[qModelIndex.row()]
        fetch=c.execute("SELECT * FROM password WHERE site=:site",{"site":site_name}).fetchone()
        print(fetch)
        user=fetch[1]
        pw=fetch[2]
        self.ui.site_input.setText(site_name)
        self.ui.user_name_input.setText(user)
        self.ui.pw_input.setText(pw)
    
    def generate_pw(self):
        import string

        char = string.printable
        #0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
        pw_length = 12
        pw = ""
        import random
        for i in range(pw_length):
            pw += char[random.randint(0,90)]
        self.ui.pw_input.setText(pw)

    # def new_data(self):
    #     try:
    #         target=self.ui.site_input.text()
    #         user=self.ui.user_name_input.text()
    #         pw=self.ui.pw_input.text()
    #         c.execute(("INSERT OR REPLACE INTO password VALUES(?,?,?)"),(target,user,pw))
    #         conn.commit()
    #         self.ui.statusbar.showMessage(self.ui.site_input.text()+" is added",5000)
    #         self.clear_input()            
    #         self.viewagent()
    #     except:
    #         self.ui.statusbar.showMessage("Something wring! Please try again",5000)
    #         self.viewagent()

    
    def update_data(self,qModelIndex):
        if self.ui.site_input.text()!="":
            try:
                new_site=self.ui.site_input.text()
                new_user=self.ui.user_name_input.text()
                new_pw=self.ui.pw_input.text()
                print(type(new_site),new_user,new_pw)

                try:
                    c.execute("UPDATE password SET site=:new_site_name, id=:user, password=:pw WHERE site=:site_name",
                                {"new_site_name":new_site,"user":new_user,"pw":new_pw,"site_name":site_name})
                    
                    conn.commit()
                    self.ui.statusbar.showMessage(site_name+" is updated",5000)

                except:
                    c.execute(f"INSERT INTO password VALUES ({new_site},{new_user},{new_pw})")
                    conn.commit()
                    self.ui.statusbar.showMessage(new_site+" is added",5000)
                self.clear_input()  

            except Exception as e:
                self.ui.statusbar.showMessage(f"{e}",5000)
        else:
            self.ui.statusbar.showMessage("Please input the site name",5000)
        


    def del_data(self):
        try:
            c.execute("DELETE FROM password WHERE site=:site_name",{"site_name":site_name})
            conn.commit()
            self.clear_input()
            self.ui.statusbar.showMessage(site_name+" is deleted",5000)
        except:
            self.ui.statusbar.showMessage("No data to delete",5000)
            self.viewagent()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())
