from PyQt5 import QtWidgets, uic
import requests


class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)

        self.loginButton.clicked.connect(self.handle_login)

    def handle_login(self):
        # 这里编写处理登录的代码
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        # ...

        # 发送请求
        try:
            x = requests.post('https://3455f9504d.goho.co/hcat-api/account/login',
                              data={'user_id': username, 'password': password})
        except requests.exceptions.ConnectionError:
            QtWidgets.QMessageBox.warning(self, '错误', '无法连接到服务器')
            return

        if x.json().get('status') == 'ok':
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, '错误', '用户名或密码错误')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        # 这里编写处理登录的代码
        # ...


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dialog = LoginDialog()
    dialog.show()
    if dialog.exec() == 1:
        window = MainWindow()
        window.show()
        app.exec()
