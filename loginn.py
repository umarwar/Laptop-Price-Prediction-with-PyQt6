from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import APT_project
app = QtWidgets.QApplication(sys.argv)
class LoginPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setFixedSize(400, 300)

        # Add background image
        background_image = QtGui.QPixmap("background.jpg")
        background_label = QtWidgets.QLabel(self)
        background_label.setPixmap(background_image)
        background_label.setGeometry(0, 0, 400, 300)

        # Add title label
        title_label = QtWidgets.QLabel(self)
        title_label.setText("Laptop Price\n Prediction Program")
        title_label.setGeometry(50, 50, 300, 30)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)

        # Add username label and line edit
        username_label = QtWidgets.QLabel(self)
        username_label.setText("Username:")
        username_label.setGeometry(50, 100, 80, 20)
        username_font = QtGui.QFont()
        username_font.setPointSize(12)
        username_label.setFont(username_font)
        self.username_edit = QtWidgets.QLineEdit(self)
        self.username_edit.setGeometry(150, 100, 200, 20)
        self.username_edit.setFont(username_font)

        # Add password label and line edit
        password_label = QtWidgets.QLabel(self)
        password_label.setText("Password:")
        password_label.setGeometry(50, 140, 80, 20)
        password_label.setFont(username_font)
        self.password_edit = QtWidgets.QLineEdit(self)
        self.password_edit.setGeometry(150, 140, 200, 20)
        self.password_edit.setFont(username_font)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Add login button
        login_button = QtWidgets.QPushButton(self)
        login_button.setText("Login")
        login_button.setGeometry(150, 200, 100, 30)
        login_font = QtGui.QFont()
        login_font.setPointSize(14)
        login_button.setFont(login_font)
        login_button.setStyleSheet("background-color: #008080; color: white; border-radius: 10px;")
        login_button.clicked.connect(self.login)

    def login(self):
        # Check if username and password are correct
        username = self.username_edit.text()
        password = self.password_edit.text()
        if username == "admin" and password == "password":
            self.apt = APT_project.MyWindow()
            self.apt.show()
            # Replace with code to open the main window of the program
        else:
            print("Login failed. Please try again.")
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Incorrect username or password. Please try again.")

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     loginn = LoginPage()
#     loginn.show()
#     sys.exit(app.exec_())
