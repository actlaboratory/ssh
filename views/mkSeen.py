# -*- coding: utf-8 -*-
# シーン作成

import wx
import globalVars
import views.ViewCreator
from logging import getLogger
from views.baseDialog import *
import seens
import simpleDialog

class Dialog(BaseDialog):
	def __init__(self):
		super().__init__("viewBroadcasterDialog")

	def Initialize(self):
		self.log.debug("created")
		super().Initialize(self.app.hMainView.hFrame,_("シーン作成"))
		self.InstallControls()
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode,self.panel,self.sizer,wx.VERTICAL,20)
		self.titleEdit,dummy = self.creator.inputbox(_("シーンタイトル"))
		self.ok = self.creator.button(_("ok"), self.create)
		self.ok.SetDefault()
		self.cancel = self.creator.cancelbutton(_("キャンセル"))

	def create(self, event):
		title = self.titleEdit.GetValue()
		if title == "":
			simpleDialog.errorDialog(_("タイトルになにか入力してください。"))
			return
		self.seen = seens.seen(title)
		self.wnd.EndModal(wx.ID_OK)

	def GetData(self):
		return self.seen
