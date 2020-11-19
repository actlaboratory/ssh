import customList
import seens
import pickle
import globalVars
import menuItemsStore
import simpleDialog
import os
import copy
import wx

class stage(customList.customList):
	def __init__(self, *args):
		super().__init__(*args)
		self.started = False
	def start_stage(self):
		self.started = True
		self.current.start()
	def setNext(self):
		if len(self) == self.pointer+1:
			return False
		self.current.stop()
		self.pointer += 1
		self.current.start()
		return True

	def stop(self):
		self.started = False
		self.current.stop()
		self.pointer = 0
		return

	def reset(self):
		self.current.stop()
		self.pointer = 0
		self.current.start()

def load_stage(fileName = None):
	if fileName == None:
		dialog = wx.FileDialog(None, _("ステージを選択"), style=wx.FD_OPEN, wildcard = "ステージファイル(*.stg;) | *.stg;")
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		fileName = dialog.GetPath()

	with open(fileName, mode = "rb") as f:
		try:
			obj = pickle.load(f)
		except exception as e:
			print(e)
			simpleDialog.errorDialog(_("読み込み中にエラーが発生しました。"))
			return
		if not isinstance(obj, stage):
			simpleDialog.errorDialog(_("ステージファイルではありません。"))
			return
		globalVars.stage = obj
		globalVars.app.hMainView.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_START"), True)
		globalVars.app.hMainView.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_STOP"), False)
		globalVars.app.hMainView.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_RESET"), False)
		globalVars.app.hMainView.menu.hFileMenu.Enable(menuItemsStore.getRef("SAVE_STAGE"), True)
		globalVars.app.hMainView.menu.hFileMenu.Enable(menuItemsStore.getRef("EDIT_STAGE"), True)
		globalVars.app.currentFile = fileName
		globalVars.app.hMainView.menu.hFileMenu.Enable(menuItemsStore.getRef("SAVE_EXIST_STAGE"), True)
		return

def save_stage(fileName = None):
	if fileName == None:
		dialog = wx.FileDialog(None, _("保存ファイルを選択"), style=wx.FD_SAVE, wildcard = "ステージファイル(*.stg;) | *.stg;")
		if dialog.ShowModal() == wx.ID_CANCEL:
			return
		fileName = dialog.GetPath()
	save_obj = copy.deepcopy(globalVars.stage)
	save_obj.stop()
	with open(fileName, mode = "wb") as f:
		try:
			pickle.dump(save_obj, f)
		except Exception as e:
			print(e)
			simpleDialog.errorDialog(_("ファイルの書き込み中にエラーが発生しました。"))
			return
	globalVars.app.currentFile = fileName
	globalVars.app.hMainView.menu.hFileMenu.Enable(menuItemsStore.getRef("SAVE_EXIST_STAGE"), True)
	return
