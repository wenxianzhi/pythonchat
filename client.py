# encoding: utf-8

import wx
# 看这个应该是telnet协议吧
import telnetlib
from time import sleep
import thread

# 哦我搞忘了，class的名括号内接收的参数是继承的意思
class LoginFrame(wx.Frame):
    """
    登录窗口
    """
    
    def __init__(self, parent, id, title, size):
        '初始化，添加控件并绑定事件'
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()

        self.serverAddressLabel = wx.StaticText(self, label = "Server Address", pos = (10, 50), size = (120, 25))
        self.userNameLabel = wx.StaticText(self, label = "UserName", pos = (40, 100), size = (120, 25))
        # wx.TextCtrl是可编辑的文本控制
        self.serverAddress = wx.TextCtrl(self, pos = (120, 47), size = (150, 25))
        self.userName = wx.TextCtrl(self, pos = (120, 97), size = (150, 25))
        self.loginButton = wx.Button(self, label = 'Login', pos = (80, 145), size = (130, 30))
        # 讲这个Button的事件监听处理函数为login
        self.loginButton.Bind(wx.EVT_BUTTON, self.onLogin)
        # 为这个Frame绑定移动时的响应函数
        #self.Bind(wx.EVT_MOVE, self.OnMove)
        self.Show()

    def onLogin(self, event):
        '登录处理'
        try:
            '用冒号来分割IP和端口'
            serverAddress = self.serverAddress.GetLineText(0).split(':')
            'serverAddress是一个元组吧'
            con.open(serverAddress[0], port = int(serverAddress[1]), timeout = 10)
            response = con.read_some()
            if response != 'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (95, 20))
                return
            con.write('login ' + str(self.userName.GetLineText(0)) + '\n')
            response = con.read_some()
            # 用户名是否为空居然要在服务端验证。。。应放到客户端
            if response == 'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (135, 20))
            # 若用户名已存在
            elif response == 'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (135, 20))
            # 若上述两种情况都没有出现，就认为登录成功了。先关掉当前Frame,再新建ChatFrame
            else:
                self.Close()
                ChatFrame(None, -2, title = 'Python Chat Client', size = (500, 350))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (95, 20))

    def onMove(self, e):
        '处理窗口移动事件'
        x, y = e.GetPosition() 
        print "current window position x = ",x," y= ",y 
    
    def showDialog(self, title, content, size):
        '显示错误信息对话框'
        dialog = wx.Dialog(self, title = title, size = size)
        dialog.Center()
        wx.StaticText(dialog, label = content)
        dialog.ShowModal()

class ChatFrame(wx.Frame):
    """
    聊天窗口
    """

    def __init__(self, parent, id, title, size):
        '初始化，添加控件并绑定事件'
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.chatFrame = wx.TextCtrl(self, pos = (5, 5), size = (490, 310), style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(self, pos = (5, 320), size = (300, 25))
        self.sendButton = wx.Button(self, label = "Send", pos = (310, 320), size = (58, 25))
        self.usersButton = wx.Button(self, label = "Users", pos = (373, 320), size = (58, 25))
        self.closeButton = wx.Button(self, label = "Close", pos = (436, 320), size = (58, 25))
        # "Send按钮"
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        # "Users按钮"
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)
        # "Close按钮"
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        thread.start_new_thread(self.receive, ())
        self.Show()
    
    def send(self, event):
        '发送消息'
        message = str(self.message.GetLineText(0)).strip()
        if message != '':
            con.write('say ' + message + '\n')
            self.message.Clear()
        
    def lookUsers(self, event):
        '查看当前在线用户'
        con.write('look\n')
        
    def close(self, event):
        '关闭窗口'
    	con.write('logout\n')
    	con.close()
    	self.Close()
        
    def receive(self):
        '接受服务器的消息'
        while True:
        	sleep(0.6)
        	result = con.read_very_eager()
        	if result != '':
        		self.chatFrame.AppendText(result)
        		
'程序运行'
if __name__ == '__main__':
    app = wx.App()
    con = telnetlib.Telnet()
    LoginFrame(None, -1, title = "Login", size = (280, 200))
    app.MainLoop()
