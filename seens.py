from customList import customList
from soundPlayer.constants import *
import globalVars
import time
from soundPlayer import player

class seen():
	"""各シーンの情報が入ったクラス。
	それぞれのシーンはbgmで分けられる。bgmが必要ないときはNoneを指定する。
	シーンは効果音一覧をcustomList型で持っている。
	"""
	def __init__(self, title, bgm = "", fadeIn = False, fadeOut = False, repeat = False, fx = [], fxVol = 100, bgmVol = 100):
		"""クラスを初期化する。
		パラメーター:
		title string: シーンの名前
		bgm string: シーンで仕様するBGM default = None
		fadeIn: bgmのフェードインの有無 default = False
		fadeOut: bgmのフェードアウトの有無 default = False
		repeat: リピート再生の有無 default = False
		"""
		self.title = title
		self.bgm = bgm
		self.fadeIn = fadeIn
		self.fadeOut = fadeOut
		self.repeat = repeat
		self.fx = customList(*fx)
		self.bgmVol = bgmVol
		self.fxVol = fxVol
		self.__started = False
		self.__played = False
		self.time = 0

	def insertFx(self, path, pos = None):
		if pos == None:
			self.fx.append(path)
			return
		self.fx.insert(pos, path)

	def start(self):
		self.__started = True
		if self.bgm == "":
			return
		globalVars.bgmPlayer.setSource(self.bgm)
		if self.repeat:
			globalVars.bgmPlayer.setRepeat(True)
		else:
			globalVars.bgmPlayer.setRepeat(False)
		globalVars.bgmPlayer.setVolume(self.bgmVol)
		
		return

	def playBgm(self):
		globalVars.bgmPlayer.play()

	def stopBgm(self):
		if self.fadeOut:
			while globalVars.bgmPlayer.setVolumeByDiff(-2):
				time.sleep(0.07)
		globalVars.bgmPlayer.stop()

	def playFx(self):
		if self.__started == False:
			return
		if self.__played:
			self.fx.setNext()
		else:
			self.__played = True
		if self.fx.current == None:
			return
		globalVars.fxPlayer.setSource(self.fx.current)
		globalVars.fxPlayer.play()

	def stop(self):
		self.fx.pointer = -1
		self.stopBgm()
		globalVars.bgmPlayer.exit()
		globalVars.bgmPlayer = player.player()
		self.__started = False
		return

	def __del__(self):
		if self.__started:
			self.stop()

	def __str__(self):
		return self.title
