import wx
from ui.main_window import MainFrame

def main():
    app = wx.App(False)
    frame = MainFrame(None, "Mensah Passwords")
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
