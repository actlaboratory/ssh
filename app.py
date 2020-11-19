# -*- coding: utf-8 -*-
#Application Main

import AppBase
from views import main
from soundPlayer import player
import globalVars
import defaultKeymap
import sys

class Main(AppBase.MainBase):
	def __init__(self):
		super().__init__()
		self.currentFile = None

	def initialize(self):
		self.setGlobalVars()
		# メインビューを表示
		self.hMainView=main.MainView()
		self.hMainView.Show()
		return True

	def setGlobalVars(self):
		globalVars.bgmPlayer = player.player()
		globalVars.fxPlayer = player.player()
		return


	def OnExit(self):
		#設定の保存やリソースの開放など、終了前に行いたい処理があれば記述できる
		#ビューへのアクセスや終了の抑制はできないので注意。
		globalVars.bgmPlayer.exit()
		globalVars.fxPlayer.exit()


		#戻り値は無視される
		return 0
