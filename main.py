import sys

from PyQt5.QtWidgets import \
    QApplication, QWidget, \
    QVBoxLayout, QLineEdit, \
    QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox
import mysql.connector

# MySQL database-ga ulash
conn = mysql.connector.connect(
    host="localhost",
    user="javod",
    password="hHh(26Y2%C~w",
    database="user_management"
)
cursor = conn.cursor()


# main window class yaratish
class UserManagementApp(QWidget):
    name_input: QLineEdit
    email_input: QLineEdit
    table: QTableWidget

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Management")

        # Layout
        layout = QVBoxLayout()

        # user name va email uchun input field-lar
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter email")
        layout.addWidget(self.email_input)

        # user qo'shish button-i
        add_button = QPushButton("Add User", self)
        add_button.clicked.connect(self.add_user)
        layout.addWidget(add_button)

        # user-ni update qilish button-i
        update_button = QPushButton("Update Selected User", self)
        update_button.clicked.connect(self.update_user)
        layout.addWidget(update_button)

        # user-ni delete qilish button-i
        delete_button = QPushButton("Delete Selected User", self)
        delete_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_button)

        # user-larni display qilish uchun table
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Email"])
        self.table.cellClicked.connect(self.select_user)
        layout.addWidget(self.table)

        # app start qilganda user-larni load qilish
        self.load_users()

        self.setLayout(layout)

    def load_users(self):
        self.table.setRowCount(0)  # birinchi
        # navbatda table-ni clear qilish
        cursor.execute("SELECT id, name, email FROM users")
        for row_idx, (user_id, name, email) in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(email))

    def select_user(self, row, column):
        name = self.table.item(row, 0).text()
        email = self.table.item(row, 1).text()
        self.name_input.setText(name)
        self.email_input.setText(email)

    def delete_user(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            user_id = self.get_selected_user_id()
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
            conn.commit()
            self.load_users()

    def update_user(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            user_id = self.get_selected_user_id()
            new_name = self.name_input.text()
            new_email = self.email_input.text()

            if new_name and new_email:
                cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (new_name, new_email, user_id))
                conn.commit()
                self.load_users()
                self.name_input.clear()
                self.email_input.clear()
            else:
                QMessageBox.warning(self, "Input Error", "Ikov input field-larni to'ldirish kerak")

    def get_selected_user_id(self):
        row = self.table.currentRow()
        name = self.table.item(row, 0).text()
        email = self.table.item(row, 1).text()

        cursor.execute("SELECT id from users WHERE name=%s and email=%s", (name, email))
        return cursor.fetchone()[0]

    def add_user(self):
        name = self.name_input.text()
        email = self.email_input.text()

        if name and email:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            self.load_users()
            self.name_input.clear()
            self.email_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Ikov input field-larni to'ldirish kerak")


def main():
    app = QApplication(sys.argv)
    window = UserManagementApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
