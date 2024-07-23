import wx
import wx.grid as grid

class ButtonRenderer(grid.GridCellRenderer):
    def __init__(self):
        super().__init__()
        self.default = wx.Button()

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetBrush(wx.Brush(wx.WHITE))
        dc.SetPen(wx.Pen(wx.WHITE, 1))
        dc.DrawRectangle(rect)
        self.default.SetPosition((rect.x + 2, rect.y + 2))
        self.default.SetSize((rect.width - 4, rect.height - 4))
        self.default.SetLabel("Delete")
        self.default.Draw(dc, (rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4), 0)

class ButtonEditor(grid.GridCellEditor):
    def __init__(self):
        super().__init__()
        self.btn = None

    def Create(self, parent, id, evtHandler):
        self.btn = wx.Button(parent, label="Delete", id=id)
        self.SetControl(self.btn)
        if evtHandler:
            self.btn.PushEventHandler(evtHandler)

    def SetSize(self, rect):
        if self.btn:
            self.btn.SetSize(rect.x, rect.y, rect.width, rect.height)

    def Show(self, show, attr):
        if self.btn:
            self.btn.Show(show)

    def BeginEdit(self, row, col, grid):
        pass

    def EndEdit(self, row, col, grid, oldVal):
        return None

    def Reset(self):
        pass
