# -*- coding: utf-8 -*-
# シーン編集

import wx
import globalVars
import views.ViewCreator
from logging import getLogger
from views.baseDialog import *
import copy
import os
import keymap
import defaultKeymap
import menuItemsStore
import clipboard

class Dialog(BaseDialog):
	def __init__(self):
		super().__init__("editSeenDialog")

	def Initialize(self, seen):
		self.log.debug("created")
		super().Initialize(self.app.hMainView.hFrame,_("シーンの編集"))
		self.seen = seen
		self.InstallControls()
		self.load()
		return True

	def InstallControls(self):
		"""いろんなwidgetを設置する。"""
		self.creator=views.ViewCreator.ViewCreator(self.viewMode,self.panel,self.sizer,wx.VERTICAL,20)
		self.bgmEdit,dummy = self.creator.inputbox(_("bgm"), style = wx.TE_READONLY, event = self.onSetBgm)
		self.bgmChangeButton = self.creator.button(_("参照"), self.onChangeBgm)
		self.bgmResetButton = self.creator.button(_("bgmを削除"), self.onDeleteBgm)
		self.bgmResetButton.Disable()
		self.isFadeOut = self.creator.checkbox(_("BGMのフェードアウト"))
		self.isRepeat = self.creator.checkbox(_("bgmのリピート"))
		self.fxList, dummy = self.creator.listbox(_("効果音"), event = self.onSelectFx)
		handler = keymap.KeymapHandler(defaultKeymap.defaultKeymap)
		acceleratorTable = handler.GetTable("fxList")
		self.fxList.SetAcceleratorTable(acceleratorTable)
		self.fxList.Bind(wx.EVT_MENU, self.onMenuSelect)
		self.addFx = self.creator.button(_("効果音追加"), self.onAddFx)
		self.insertFxButton = self.creator.button(_("選択位置に効果音を挿入"), self.onInsertFx)
		self.deleteFx = self.creator.button(_("効果音削除"), self.onDeleteFx)
		self.bgmVolSlider, dummy = self.creator.slider(_("BGMの音量"))
		self.ok = self.creator.okbutton(_("OK"), event = self.save)
		self.cancel = self.creator.cancelbutton(_("キャンセル"))
		return

	def onChangeBgm(self, event):
		dialog = wx.FileDialog(None, _("bgmを選択"), style=wx.FD_OPEN)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		self.bgmEdit.SetValue(dialog.GetPath())
		return

	def onSetBgm(self, event):
		self.bgmResetButton.Enable()

	def onDeleteBgm(self, event):
		self.bgmEdit.Clear()
		self.bgmResetButton.Disable()

	def onAddFx(self, event):
		dialog = wx.FileDialog(None, _("効果音追加"), style=wx.FD_OPEN | wx.FD_MULTIPLE)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		path = dialog.GetPath()
		self.fxList.Append(os.path.basename(path))
		self.fx.append(path)
		return

	def onInsertFx(self, event):
		dialog = wx.FileDialog(None, _("効果音追加"), style=wx.FD_OPEN)
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		path = dialog.GetPath()
		self.fxList.Insert(os.path.basename(path), self.fxList.Selection)
		self.fx.insert(self.fxList.Selection, path)

	def onSelectFx(self, event):
		self.insertFxButton.Enable()

	def onDeleteFx(self, event):
		select = self.fxList.GetSelection()
		if select == -1:
			return
		del self.fx[select]
		self.fxList.Delete(select)

	def onMenuSelect(self, event):
		selected = event.GetId()
		if selected == menuItemsStore.getRef("PAST_FX"):
			self.pastFx()

	def pastFx(self):
		error = False
		pos = self.fxList.Selection + 1
		c=clipboard.ClipboardFile()
		fileList = c.GetFileList()
		if pos <= self.fxList.GetCount():
			for path in fileList:
				if os.path.isdir(path):error = True
				self.fxList.Insert(os.path.basename(path), pos)
				self.fx.insert(self.fxList.Selection, path)
		else:
			for path in fileList:
				if os.path.isdir(path):error = True
				self.fxList.Append(os.path.basename(path))
				self.fx.append(path)
		if error:
			simpleDialog.errorDialog(_("ディレクトリが除外されました。"))
		return


	def load(self):
		if self.seen.bgm is not None:
			self.bgmEdit.SetValue(self.seen.bgm)
		self.isFadeOut.SetValue(self.seen.fadeOut)
		self.isRepeat.SetValue(self.seen.repeat)
		self.fx = copy.deepcopy(self.seen.fx)
		for fx in self.fx:
			self.fxList.Append(os.path.basename(fx))
		self.bgmVolSlider.SetValue(self.seen.bgmVol)
		return

	def save(self, event):
		bgm = self.bgmEdit.GetValue()
		self.seen.bgm = bgm
		self.seen.fadeOut = self.isFadeOut.GetValue()
		self.seen.repeat = self.isRepeat.GetValue()
		self.seen.fx = self.fx
		self.seen.bgmVol = self.bgmVolSlider.GetValue()
		event.Skip()
		return

	def GetData(self):
		return self.seen
