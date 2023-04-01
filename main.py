import json
import os

from PyQt5 import QtWidgets, uic
import requests

cookies = None


class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('assets/ui/login.ui', self)
        self.save_psw = False
        self.pushButton_Login.clicked.connect(self.handle_login)
        self.pushButton_AutoLogin.clicked.connect(self.change_save_psw)

    def change_save_psw(self):
        self.save_psw = not self.save_psw
        self.pushButton_AutoLogin.setText(str(self.save_psw)[0])

    def handle_login(self):
        global cookies

        user_id = self.lineEdit_UserId.text()
        password = self.lineEdit_Password.text()

        self.pushButton_Login.setEnabled(False)
        self.pushButton_Login.setText('Logining...')
        self.repaint()

        try:
            x = requests.post('https://3455f9504d.goho.co/hcat-api/account/login',
                              data={'user_id': user_id, 'password': password})
            if x.json().get('status') == 'ok':
                cookies = x.cookies
                self.accept()
                if self.save_psw:
                    with open('config.json', 'r') as f:
                        config = json.load(f)
                    config['user_id'] = user_id
                    config['password'] = password
                    with open('config.json', 'w') as f:
                        json.dump(config, f)


            else:
                self.label_info.setText('User_id or password is wrong.')
                self.label_info.setStyleSheet('color: red')
        except requests.exceptions.ConnectionError:
            self.label_info.setText('Cannot connect to server.')
            self.label_info.setStyleSheet('color: red')

        self.pushButton_Login.setEnabled(True)
        self.pushButton_Login.setText('Login')
        self.repaint()
        return self.result()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('assets/ui/main.ui', self)


if __name__ == '__main__':
    auto_login_rst = 0
    app = QtWidgets.QApplication([])
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as f:
            json.dump({}, f)
    with open('config.json', 'r') as f:
        config: dict = json.load(f)
    dialog = LoginDialog()
    if 'user_id' in config and 'password' in config:
        dialog.lineEdit_UserId.setText(config['user_id'])
        dialog.lineEdit_Password.setText(config['password'])
        dialog.change_save_psw()
        auto_login_rst = dialog.handle_login()

    if auto_login_rst == 1 or dialog.exec() == 1:
        window = MainWindow()
        window.show()
        app.exec()
