from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QSpinBox, QCheckBox, QLineEdit, QPushButton, QMenuBar, QMenu, QTableWidget, QTableWidgetItem, \
    QHeaderView, QMessageBox, QDialog, QSplashScreen
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from password_generator import generate_password
from password_manager import create_connection, add_password, fetch_passwords, delete_password
from database import init_db, db_file

class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap('resources/icon.png')  # Path to your splash screen image
        super(SplashScreen, self).__init__(pixmap)
        self.setMask(pixmap.mask())
        self.show()

    def finish(self, main_window):
        super(SplashScreen, self).finish(main_window)
        main_window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.initDB()

    def initUI(self):
        self.setWindowTitle("Mensah Passwords")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('resources/icon.ico'))  # Set the app icon here

        # Menu Bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        viewPasswordsAction = fileMenu.addAction('View Saved Passwords')
        viewPasswordsAction.triggered.connect(self.onViewPasswords)

        developerMenu = menubar.addMenu('Developer')
        developerInfoAction = developerMenu.addAction('Developer Info')
        developerInfoAction.triggered.connect(self.showDeveloperInfo)

        # Central Widget
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        vbox = QVBoxLayout()

        # Password Generator Section
        generateBox = QVBoxLayout()
        generateBox.addWidget(self.createSectionTitle("Generate Password"))

        self.lengthSpinBox = QSpinBox()
        self.lengthSpinBox.setRange(4, 32)
        self.lengthSpinBox.setValue(12)
        generateBox.addWidget(self.wrapWithWidget(self.createLabeledWidget("Length:", self.lengthSpinBox)))

        self.symbolsCheckBox = QCheckBox("Include Symbols")
        generateBox.addWidget(self.symbolsCheckBox)

        self.numbersCheckBox = QCheckBox("Include Numbers")
        generateBox.addWidget(self.numbersCheckBox)

        self.uppercaseCheckBox = QCheckBox("Include Uppercase Letters")
        generateBox.addWidget(self.uppercaseCheckBox)

        self.lowercaseCheckBox = QCheckBox("Include Lowercase Letters")
        generateBox.addWidget(self.lowercaseCheckBox)

        self.generatedPasswordLineEdit = QLineEdit()
        generateBox.addWidget(self.generatedPasswordLineEdit)

        self.generateButton = QPushButton("Generate Password")
        self.generateButton.clicked.connect(self.onGeneratePassword)
        generateBox.addWidget(self.generateButton)

        # Collapsible Bar for Manage Passwords
        self.managePasswordsButton = QPushButton("Manage Passwords")
        self.managePasswordsButton.setStyleSheet("background-color: brown; color: white; border: none; border-radius: 4px; padding: 10px;")
        self.managePasswordsButton.clicked.connect(self.showManagePasswordsDialog)

        vbox.addLayout(generateBox)
        vbox.addWidget(self.managePasswordsButton)
        centralWidget.setLayout(vbox)

        # Apply styles
        self.applyStyles()

    def createSectionTitle(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        return label

    def createLabeledWidget(self, labelText, widget):
        layout = QHBoxLayout()
        label = QLabel(labelText)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def wrapWithWidget(self, layout):
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def applyStyles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
                margin: 5px;
            }
            QSpinBox, QCheckBox, QLineEdit, QPushButton {
                font-size: 14px;
                padding: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                font-size: 14px;
            }
        """)

    def initDB(self):
        init_db()
        self.conn = create_connection(db_file)

    def onGeneratePassword(self):
        length = self.lengthSpinBox.value()
        include_symbols = self.symbolsCheckBox.isChecked()
        include_numbers = self.numbersCheckBox.isChecked()
        include_uppercase = self.uppercaseCheckBox.isChecked()
        include_lowercase = self.lowercaseCheckBox.isChecked()

        password = generate_password(length, include_symbols, include_numbers, include_uppercase, include_lowercase)
        self.generatedPasswordLineEdit.setText(password)

    def onSavePassword(self, name, username, password):
        if not name or not username or not password:
            QMessageBox.warning(self, "Warning", "All fields must be filled!")
            return

        password_entry = (name, username, password)
        add_password(self.conn, password_entry)

    def onViewPasswords(self):
        dialog = PasswordsDialog(self, self.conn)
        dialog.exec()

    def showManagePasswordsDialog(self):
        dialog = ManagePasswordsDialog(self, self.conn, self.onSavePassword)
        dialog.exec()

    def showDeveloperInfo(self):
        dialog = DeveloperInfoDialog(self)
        dialog.exec()

class ManagePasswordsDialog(QDialog):
    def __init__(self, parent, conn, saveCallback):
        super(ManagePasswordsDialog, self).__init__(parent)
        self.conn = conn
        self.saveCallback = saveCallback
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Manage Passwords")
        self.setGeometry(150, 150, 400, 300)
        
        layout = QVBoxLayout()

        self.nameLineEdit = QLineEdit()
        layout.addWidget(self.wrapWithWidget(self.createLabeledWidget("Name:", self.nameLineEdit)))

        self.usernameLineEdit = QLineEdit()
        layout.addWidget(self.wrapWithWidget(self.createLabeledWidget("Username:", self.usernameLineEdit)))

        self.generatedPasswordLineEdit = QLineEdit()
        layout.addWidget(self.wrapWithWidget(self.createLabeledWidget("Password:", self.generatedPasswordLineEdit)))

        self.saveButton = QPushButton("Save Password")
        self.saveButton.clicked.connect(self.onSavePassword)
        layout.addWidget(self.saveButton)

        self.setLayout(layout)

    def createLabeledWidget(self, labelText, widget):
        layout = QHBoxLayout()
        label = QLabel(labelText)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def wrapWithWidget(self, layout):
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def onSavePassword(self):
        name = self.nameLineEdit.text()
        username = self.usernameLineEdit.text()
        password = self.generatedPasswordLineEdit.text()
        self.saveCallback(name, username, password)
        self.close()

class PasswordsDialog(QDialog):
    def __init__(self, parent, conn):
        super(PasswordsDialog, self).__init__(parent)
        self.conn = conn
        self.initUI()
        self.loadPasswords()

    def initUI(self):
        self.setWindowTitle("Saved Passwords")
        self.setGeometry(150, 150, 600, 400)

        vbox = QVBoxLayout()
        self.passwordTable = QTableWidget()
        self.passwordTable.setColumnCount(4)
        self.passwordTable.setHorizontalHeaderLabels(["Name", "Username", "Password", "Action"])
        self.passwordTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.passwordTable)
        self.setLayout(vbox)

    def loadPasswords(self):
        passwords = fetch_passwords(self.conn)
        self.passwordTable.setRowCount(0)
        for password in passwords:
            self.addPasswordToTable(password)

    def addPasswordToTable(self, password_entry):
        row = self.passwordTable.rowCount()
        self.passwordTable.insertRow(row)
        self.passwordTable.setItem(row, 0, QTableWidgetItem(password_entry[1]))
        self.passwordTable.setItem(row, 1, QTableWidgetItem(password_entry[2]))
        self.passwordTable.setItem(row, 2, QTableWidgetItem(password_entry[3]))

        deleteButton = QPushButton("Delete")
        deleteButton.setStyleSheet("background-color: #dc3545; color: white; border: none; border-radius: 4px;")
        deleteButton.clicked.connect(lambda: self.onDeletePassword(password_entry[0], row))
        self.passwordTable.setCellWidget(row, 3, deleteButton)

    def onDeletePassword(self, password_id, row):
        reply = QMessageBox.question(self, 'Delete Password', 'Are you sure you want to delete this password?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_password(self.conn, password_id)
            self.passwordTable.removeRow(row)

class DeveloperInfoDialog(QDialog):
    def __init__(self, parent):
        super(DeveloperInfoDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Developer Information")
        self.setFixedSize(500, 600)  # Set width and height to ensure height is greater than width

        layout = QVBoxLayout()

        # Profile Image
        self.profileImage = QLabel()
        self.profileImage.setPixmap(QPixmap('resources/profile_photo.jpg').scaledToHeight(300))  # Adjust height as needed
        self.profileImage.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.profileImage)

        # Information Label
        infoLabel = QLabel("""
        <h2>Elijah Ekpen Mensah</h2>
        <p>Elijah Ekpen Mensah is a software developer with Nigerian <br> and Ghanaian heritage.<br>
        He is passionate about creating innovative solutions<br> in the technology space.</p>
                           <br>
            <b>For Employment, Co-founding and Donations Please Contact </b>
                          <p>Email:<a href="mailto:stebarbara53@gmail.com">stebarbara53@gmail.com</a><br>
                        Whatsapp:<a href="tel:">+2348155314343</a></p>
                           
                           
                           
        """)
        infoLabel.setOpenExternalLinks(True)
        infoLabel.setStyleSheet("font-size: 14px;")  # Ensure the text fits well within the dialog
        layout.addWidget(infoLabel)

        # LinkedIn Profile Button
        linkedinButton = QPushButton("LinkedIn Profile")
        linkedinButton.setStyleSheet("background-color: #0077b5; color: white; border: none; border-radius: 4px; padding: 10px;")
        linkedinButton.clicked.connect(self.openLinkedInProfile)
        layout.addWidget(linkedinButton)

        # Personal Website Button
        websiteButton = QPushButton("Personal Website")
        websiteButton.setStyleSheet("background-color: #1a73e8; color: white; border: none; border-radius: 4px; padding: 10px;")
        websiteButton.clicked.connect(self.openPersonalWebsite)
        layout.addWidget(websiteButton)

        self.setLayout(layout)

    def openLinkedInProfile(self):
        QDesktopServices.openUrl(QUrl("https://www.linkedin.com/in/elijah-ekpen-mensah"))

    def openPersonalWebsite(self):
        QDesktopServices.openUrl(QUrl("https://elijahmensahcreates.netlify.app/"))

if __name__ == '__main__':
    app = QApplication([])
    splash = SplashScreen()
    mainWindow = MainWindow()
    splash.finish(mainWindow)
    app.exec()
