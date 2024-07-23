import wx
import wx.grid as grid
from password_manager import fetch_passwords, delete_password

class PasswordsDialog(wx.Dialog):
    def __init__(self, parent, title, conn):
        super(PasswordsDialog, self).__init__(parent, title=title, size=(600, 400))
        
        self.conn = conn
        self.InitUI()
        self.LoadPasswords()
        
    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.passwordTable = grid.Grid(self)
        self.passwordTable.CreateGrid(0, 4)
        self.passwordTable.SetColLabelValue(0, "Name")
        self.passwordTable.SetColLabelValue(1, "Username")
        self.passwordTable.SetColLabelValue(2, "Password")
        self.passwordTable.SetColLabelValue(3, "Action")
        
        vbox.Add(self.passwordTable, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.SetSizer(vbox)
        
    def LoadPasswords(self):
        passwords = fetch_passwords(self.conn)
        if self.passwordTable.GetNumberRows() > 0:
            self.passwordTable.DeleteRows(pos=0, numRows=self.passwordTable.GetNumberRows())
        for password in passwords:
            self.AddPasswordToTable(password)
        
    def AddPasswordToTable(self, password_entry):
        self.passwordTable.AppendRows(1)
        row = self.passwordTable.GetNumberRows() - 1
        self.passwordTable.SetCellValue(row, 0, password_entry[1])
        self.passwordTable.SetCellValue(row, 1, password_entry[2])
        self.passwordTable.SetCellValue(row, 2, password_entry[3])
        
        self.passwordTable.SetCellRenderer(row, 3, wx.grid.GridCellBoolRenderer())
        self.passwordTable.SetCellEditor(row, 3, wx.grid.GridCellBoolEditor())
        self.passwordTable.SetCellValue(row, 3, "Delete")
        self.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, lambda event, row=row: self.OnDeletePassword(event, password_entry[0]))

    def OnDeletePassword(self, event, password_id):
        delete_password(self.conn, password_id)
        self.LoadPasswords()
