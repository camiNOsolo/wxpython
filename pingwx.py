#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import threading
import subprocess
import time
import wx
import wx.lib.sized_controls as sc

class HacerPing(sc.SizedDialog):

    def __init__(self, *args, **kwds):
        """Constructor"""
        sc.SizedDialog.__init__(self, None, title="www.toString.es",
                                size=(500,450))
 
        panel = self.GetContentsPane()
        panel.SetSizerType("form")

        label = wx.StaticText(panel, -1, "Direccion IP:")
        ip = wx.TextCtrl(panel)
        self.ip = ip
        ip.SetSizerProps(expand=True)
        
        text = wx.TextCtrl(self, -1, pos = (10, 90),
                            size=(480,300),
                            style= wx.TE_MULTILINE | wx.SUNKEN_BORDER)
        self.text = text
        boton = wx.Button(panel, -1, "Ping")
        boton.SetSizerProps(expand=True)
        exit = wx.Button(panel, -1, "Salir")
        exit.SetSizerProps(expand=True)
        exit.Bind(wx.EVT_BUTTON, self.closeWindow)
        func = functools.partial(self.on_button, 'ping')
        boton.Bind(wx.EVT_BUTTON, func)
    
    def on_button(self, event, button):
        # create a new thread when a button is pressed
        thread = threading.Thread(target=self.run, args=(button,))
        thread.setDaemon(True)
        thread.start()

    def closeWindow(self, event):
        self.Close()
        self.Destroy()
 
    def on_text(self, text):
        self.text.AppendText(text)
        
    def run(self, button):
        cmd = ['ping', '-c', '3']
        ip = self.ip.GetValue()
		
        cmd.append(ip)
        proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #time.sleep(2)
        for line in proc.stdout:
            wx.CallAfter(self.on_text, line)

if __name__ == "__main__":
    app = wx.App(False)
    dlg = HacerPing()
    dlg.ShowModal()
    app.MainLoop()
