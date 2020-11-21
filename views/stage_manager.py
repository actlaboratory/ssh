# -*- coding: utf-8 -*-
# stage manager dialog
import wx
import globalVars
import views.ViewCreator
from logging import getLogger
from views.baseDialog import *
from views import edit
from views import mkSeen

class Dialog(BaseDialog):
	def __init__(self):
		super().__init__("stage_managerDialog")
		self.id = 1

	def Initialize(self):
		self.log.debug("created")
		super().Initialize(self.app.hMainView.hFrame,_("ステージ編集"))
		self.InstallControls()
		self.update()
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode,self.panel,self.sizer,wx.VERTICAL,20)
		self.seens, dummy = self.creator.listbox(_("シーン一覧"), event = self.onSeenSelected)
		self.addButton = self.creator.button(_("シーンを追加"), self.add)
		self.editButton = self.creator.button(_("編集"), self.edit)
		self.deleteButton = self.creator.button(_("削除"), self.onDelete)
		self.editButton.Disable()
		self.close = self.creator.okbutton(_("閉じる(&c)"))

	def add(self, event):
		dialog = mkSeen.Dialog()
		dialog.Initialize()
		if dialog.Show() == wx.ID_CANCEL:
			return
		globalVars.stage.append(dialog.GetValue())
		self.update()
		return

	def edit(self, event):
		select = self.seens.GetSelection()
		if select == -1:
			return
		dialog = edit.Dialog()
		dialog.Initialize(globalVars.stage[select])
		dialog.Show()
		self.update()
		return

	def update(self):
		self.seens.Clear()
		for seen in globalVars.stage:
			text = ""
			text += "id:%d;" % globalVars.stage.index(seen)
			text += "説明:%s;" % (seen.title,)
			if seen.bgm == "":
				text += "bgm:無し;"
			else:
				text += "bgm:%s" % (seen.bgm,)
			self.seens.Append(text)

	def onSeenSelected(self, event):
		self.editButton.Enable()

	def onDelete(self, event):
		select = self.seens.GetSelection()
		if select == -1:
			return
		self.seens.Delete(select)
		del globalVars.stage[select]
		self.update()

	def GetData(self):
		return None
