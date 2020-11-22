# -*- coding: utf-8 -*-
#main view
#Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
#Copyright (C) 2019-2020 yamahubuki <itiro.ishino@gmail.com>

import logging
import os
import sys
import wx
import re
import ctypes
import pywintypes
import stage
import simpleDialog
from views import stage_manager
from views import changeDevice
import constants
import errorCodes
import globalVars
import menuItemsStore

from simpleDialog import dialog
from .base import *
from simpleDialog import *

from views import mkDialog


class MainView(BaseView):
	def __init__(self):
		super().__init__("mainView")
		self.log.debug("created")
		self.app=globalVars.app
		self.events=Events(self,self.identifier)
		title=constants.APP_NAME
		super().Initialize(
			title,
			self.app.config.getint(self.identifier,"sizeX",800,400),
			self.app.config.getint(self.identifier,"sizeY",600,300),
			self.app.config.getint(self.identifier,"positionX",50,0),
			self.app.config.getint(self.identifier,"positionY",50,0)
		)
		self.InstallMenuEvent(Menu(self.identifier,keyFilter=keymap.KeyFilter().SetDefault(False,True,True)),self.events.OnMenuSelect)
		self.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_START"), False)
		self.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_STOP"), False)
		self.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_RESET"), False)
		self.menu.hFileMenu.Enable(menuItemsStore.getRef("SEEN_RESET"), False)
		self.menu.hFileMenu.Enable(menuItemsStore.getRef("SAVE_STAGE"), False)
		self.menu.hFileMenu.Enable(menuItemsStore.getRef("SAVE_EXIST_STAGE"), False)
		self.menu.hFileMenu.Enable(menuItemsStore.getRef("EDIT_STAGE"), False)
		self.menu.hMenuBar.EnableTop(1,False)


class Menu(BaseMenu):
	def Apply(self,target):
		"""指定されたウィンドウに、メニューを適用する。"""

		#メニューの大項目を作る
		self.hFileMenu = wx.Menu()
		self.hCtrlMenu = wx.Menu()
		self.hSettingsMenu = wx.Menu()
		self.hHelpMenu=wx.Menu()
		#ファイルメニューの中身
		self.RegisterMenuCommand(self.hFileMenu, "NEW", _("新規(&n)"))
		self.RegisterMenuCommand(self.hFileMenu, "OPEN", _("開く(&o)"))
		self.RegisterMenuCommand(self.hFileMenu, "STAGE_START", _("スタート"))
		self.RegisterMenuCommand(self.hFileMenu, "STAGE_STOP", _("ストップ"))
		self.RegisterMenuCommand(self.hFileMenu, "STAGE_RESET", _("最初に戻る(&r)"))
		self.RegisterMenuCommand(self.hFileMenu, "SEEN_RESET", _("シーンの最初に戻る(&b)"))
		self.RegisterMenuCommand(self.hFileMenu, "SAVE_STAGE", _("名前を付けて保存(&s)"))
		self.RegisterMenuCommand(self.hFileMenu, "SAVE_EXIST_STAGE", _("上書き保存(&s)"))
		self.RegisterMenuCommand(self.hFileMenu, "EDIT_STAGE", _("ステージの編集"))
		self.RegisterMenuCommand(self.hFileMenu, "EXIT", _("終了(&x)"))

		#コントロールメニューの中身
		self.RegisterMenuCommand(self.hCtrlMenu, "NEXTSEEN", _("次のシーン"))
		self.RegisterMenuCommand(self.hCtrlMenu, "PREVSEEN", _("前のシーン"))
		self.RegisterMenuCommand(self.hCtrlMenu, "PLAY_BGM", _("bgm再生"))
		self.RegisterMenuCommand(self.hCtrlMenu, "FX_PLAY", _("効果音再生"))
		self.RegisterMenuCommand(self.hCtrlMenu, "STOP_BGM", _("BGM停止"))
		self.RegisterMenuCommand(self.hCtrlMenu, "BGM_VOLUME_DOWN", _("BGMの音量を下げる"))
		self.RegisterMenuCommand(self.hCtrlMenu, "BGM_VOLUME_UP", _("BGMの音量を上げる"))
		#設定メニューの中身
		self.RegisterMenuCommand(self.hSettingsMenu, "CHANGE_DEVICE", _("デバイスの変更"))
		#ヘルプメニューの中身
		self.RegisterMenuCommand(self.hHelpMenu,"EXAMPLE",_("テストダイアログを閲覧"))
		#メニューバーの生成
		self.hMenuBar.Append(self.hFileMenu, _("ファイル(&f)"))
		self.hMenuBar.Append(self.hCtrlMenu,_("コントロール"))
		self.hMenuBar.Append(self.hSettingsMenu,_("設定"))
		self.hMenuBar.Append(self.hHelpMenu,_("ヘルプ"))
		target.SetMenuBar(self.hMenuBar)

class Events(BaseEvents):
	def OnMenuSelect(self,event):
		"""メニュー項目が選択されたときのイベントハンドら。"""
		#ショートカットキーが無効状態のときは何もしない
		if not self.parent.shortcutEnable:
			event.Skip()
			return

		selected=event.GetId()#メニュー識別しの数値が出る
		if selected == menuItemsStore.getRef("NEW"):
			globalVars.stage = stage.stage()
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_START"), True)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_STOP"), False)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_RESET"), False)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("SAVE_STAGE"), True)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("EDIT_STAGE"), True)
			globalVars.app.currentFile = None
			return
		if selected == menuItemsStore.getRef("OPEN"):
			stage.load_stage()
			return
		if selected == menuItemsStore.getRef("SAVE_STAGE"):
			stage.save_stage()
			return
		if selected == menuItemsStore.getRef("SAVE_EXIST_STAGE"):
			if globalVars.app.currentFile == None:
				return
			stage.save_stage(globalVars.app.currentFile)
			return
		if selected == menuItemsStore.getRef("STAGE_START"):
			if globalVars.stage.current == None:
				simpleDialog.dialog("シーンがありません。編集画面でシーンを追加してください。")
				return
			globalVars.stage.start_stage()
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_RESET"), True)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("SEEN_RESET"), True)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_START"), False)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_STOP"), True)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("EDIT_STAGE"), False)
			self.parent.menu.hMenuBar.EnableTop(1,True)
		if selected == menuItemsStore.getRef("STAGE_STOP"):
			globalVars.stage.stop()
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_RESET"), False)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("SEEN_RESET"), False)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_START"), True)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("STAGE_STOP"), False)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("SAVE_STAGE"), True)
			self.parent.menu.hFileMenu.Enable(menuItemsStore.getRef("EDIT_STAGE"), True)
			self.parent.menu.hMenuBar.EnableTop(1,False)
		if selected == menuItemsStore.getRef("STAGE_RESET"):
			globalVars.stage.reset()
			return
		if selected == menuItemsStore.getRef("SEEN_RESET"):
			globalVars.stage.current.stop()
			globalVars.stage.current.start()
		if selected == menuItemsStore.getRef("EDIT_STAGE"):
			if not hasattr(globalVars, "stage"):
				simpleDialog.errorDialog("ステージがロードされていません。")
				return
			dialog = stage_manager.Dialog()
			dialog.Initialize()
			dialog.Show()
			
		if selected == menuItemsStore.getRef("EXIT"):
			self.Exit()
		if selected == menuItemsStore.getRef("NEXTSEEN"):
			globalVars.stage.setNext()

		if selected == menuItemsStore.getRef("PREVSEEN"):
			globalVars.stage.setprevious()

		if selected == menuItemsStore.getRef("STOP_BGM"):
			globalVars.stage.current.stopBgm()
		if selected == menuItemsStore.getRef("PLAY_BGM"):
			globalVars.stage.current.playBgm()
		if selected == menuItemsStore.getRef("BGM_VOLUME_DOWN"):
			globalVars.bgmPlayer.setVolumeByDiff(-1)
		if selected == menuItemsStore.getRef("BGM_VOLUME_UP"):
			globalVars.bgmPlayer.setVolumeByDiff(1)
		if selected == menuItemsStore.getRef("FX_PLAY"):
			globalVars.stage.current.playFx()

		if selected == menuItemsStore.getRef("CHANGE_DEVICE"):
			dialog =  changeDevice.Dialog()
			dialog.Initialize()
			if dialog.Show() == wx.ID_CANCEL:
				return
			globalVars.app.config["player"]["device"] = dialog.GetValue()
			return

		if selected==menuItemsStore.getRef("EXAMPLE"):
			d = mkDialog.Dialog()
			d.Initialize(_("テスト"), _("テストダイアログ"), (_("Hello World! を表示"), _("キャンセル")))
			r = d.Show()
			if r == 0:
				print("Hello World!")
