import wx
from password_generator import generate_password
from password_manager import create_connection, add_password
from database import init_db, db_file
from ui.passwords_dialog import PasswordsDialog

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        
        self.InitUI()
        self.InitDB()
        
    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Menu Bar
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewPasswordsItem = fileMenu.Append(wx.ID_ANY, 'View Saved Passwords', 'View Saved Passwords')
        menubar.Append(fileMenu, 'File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnViewPasswords, viewPasswordsItem)
        
        # Password Generator Section
        generateBox = wx.StaticBox(panel, label="Generate Password")
        generateSizer = wx.StaticBoxSizer(generateBox, wx.VERTICAL)
        
        self.lengthSpinBox = wx.SpinCtrl(panel, min=4, max=32, initial=12)
        self.symbolsCheckBox = wx.CheckBox(panel, label="Include Symbols")
        self.numbersCheckBox = wx.CheckBox(panel, label="Include Numbers")
        self.uppercaseCheckBox = wx.CheckBox(panel, label="Include Uppercase Letters")
        self.lowercaseCheckBox = wx.CheckBox(panel, label="Include Lowercase Letters")
        self.generatedPasswordLineEdit = wx.TextCtrl(panel)
        self.generateButton = wx.Button(panel, label="Generate Password")
        
        generateSizer.Add(wx.StaticText(panel, label="Length:"))
        generateSizer.Add(self.lengthSpinBox, flag=wx.EXPAND|wx.ALL, border=5)
        generateSizer.Add(self.symbolsCheckBox, flag=wx.ALL, border=5)
        generateSizer.Add(self.numbersCheckBox, flag=wx.ALL, border=5)
        generateSizer.Add(self.uppercaseCheckBox, flag=wx.ALL, border=5)
        generateSizer.Add(self.lowercaseCheckBox, flag=wx.ALL, border=5)
        generateSizer.Add(self.generatedPasswordLineEdit, flag=wx.EXPAND|wx.ALL, border=5)
        generateSizer.Add(self.generateButton, flag=wx.EXPAND|wx.ALL, border=5)
        
        self.generateButton.Bind(wx.EVT_BUTTON, self.OnGeneratePassword)
        
        # Password Manager Section
        managerBox = wx.StaticBox(panel, label="Manage Passwords")
        managerSizer = wx.StaticBoxSizer(managerBox, wx.VERTICAL)
        
        self.nameLineEdit = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.usernameLineEdit = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.saveButton = wx.Button(panel, label="Save Password")
        
        managerSizer.Add(wx.StaticText(panel, label="Name:"))
        managerSizer.Add(self.nameLineEdit, flag=wx.EXPAND|wx.ALL, border=5)
        managerSizer.Add(wx.StaticText(panel, label="Username:"))
        managerSizer.Add(self.usernameLineEdit, flag=wx.EXPAND|wx.ALL, border=5)
        managerSizer.Add(self.saveButton, flag=wx.EXPAND|wx.ALL, border=5)
        
        self.saveButton.Bind(wx.EVT_BUTTON, self.OnSavePassword)
        
        vbox.Add(generateSizer, flag=wx.EXPAND|wx.ALL, border=10)
        vbox.Add(managerSizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        
        panel.SetSizer(vbox)
        
    def InitDB(self):
        init_db()
        self.conn = create_connection(db_file)
    
    def OnGeneratePassword(self, event):
        length = self.lengthSpinBox.GetValue()
        include_symbols = self.symbolsCheckBox.GetValue()
        include_numbers = self.numbersCheckBox.GetValue()
        include_uppercase = self.uppercaseCheckBox.GetValue()
        include_lowercase = self.lowercaseCheckBox.GetValue()
        
        password = generate_password(length, include_symbols, include_numbers, include_uppercase, include_lowercase)
        self.generatedPasswordLineEdit.SetValue(password)
        
    def OnSavePassword(self, event):
        name = self.nameLineEdit.GetValue()
        username = self.usernameLineEdit.GetValue()
        password = self.generatedPasswordLineEdit.GetValue()
        
        if not name or not username or not password:
            wx.MessageBox("All fields must be filled!", "Warning", wx.OK | wx.ICON_WARNING)
            return
        
        password_entry = (name, username, password)
        add_password(self.conn, password_entry)
        
        self.nameLineEdit.Clear()
        self.usernameLineEdit.Clear()
        self.generatedPasswordLineEdit.Clear()
        
    def OnViewPasswords(self, event):
        dialog = PasswordsDialog(self, "Saved Passwords", self.conn)
        dialog.ShowModal()
        dialog.Destroy()
