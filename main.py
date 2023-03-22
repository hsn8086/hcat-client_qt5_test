from PyQt5 import QtWidgets, uic
import requests

cookies = None


class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)

        self.pushButton_Login.clicked.connect(self.handle_login)

    def handle_login(self):
        global cookies

        username = self.lineEdit_UserId.text()
        password = self.lineEdit_Password.text()

        self.pushButton_Login.setEnabled(False)
        self.pushButton_Login.setText('Logining...')
        self.repaint()

        try:
            x = requests.post('https://3455f9504d.goho.co/hcat-api/account/login',
                              data={'user_id': username, 'password': password})
            if x.json().get('status') == 'ok':
                cookies = x.cookies
                self.accept()
            else:
                self.label_info.setText('User_id or password is wrong.')
                self.label_info.setStyleSheet('color: red')
        except requests.exceptions.ConnectionError:
            self.label_info.setText('Cannot connect to server.')
            self.label_info.setStyleSheet('color: red')

        self.pushButton_Login.setEnabled(True)
        self.pushButton_Login.setText('Login')
        self.repaint()
        return


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dialog = LoginDialog()
    dialog.show()
    if dialog.exec() == 1:
        window = MainWindow()
        window.show()
        app.exec()
