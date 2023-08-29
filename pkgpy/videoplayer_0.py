#!/usr/bin/env python


import sys
import os.path
from functools import partial
from PyQt5.QtCore import QEvent, QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QWidget, QSlider, QLabel,
                             QVBoxLayout)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

# Contendra la Ruta del archivo.
n_msource = ""


class PlayVideo(QMainWindow):
    
	def __init__(self):
		super().__init__()
		try:
			# Controles principales para organizar la ventana.
			self.widget = QWidget(self)
			self.layout = QVBoxLayout()
			self.bottom_layout = QHBoxLayout()
			self.laberror = QLabel('')

			# Control de reproducción de video de Qt.
			self.video_widget = QVideoWidget(self)
			self.media_player = QMediaPlayer()
			print(n_msource)
			self.media_player.setMedia( QMediaContent( QUrl.fromLocalFile(n_msource)) )
			self.media_player.setVideoOutput(self.video_widget)

			# Deslizadores para el volumen y transición del video.
			self.seek_slider = QSlider(Qt.Horizontal)
			self.seek_slider.sliderMoved.connect(self.media_player.setPosition)
			self.media_player.positionChanged.connect(self.seek_slider.setValue)
			self.media_player.durationChanged.connect(
			  partial(self.seek_slider.setRange, 0))

			# Acomodar controles en la pantalla.
			#self.layout.addWidget(self.video_widget)
			#self.layout.addWidget(self.seek_slider)

			# Conectar los eventos con sus correspondientes funciones.
			self.media_player.stateChanged.connect(self.state_changed)

			# Se utiliza installEventFilter() para capturar eventos
			# del mouse en el control de video.
			self.video_widget.installEventFilter(self)

			# Personalizar la ventana.
			self.setWindowTitle(n_msource)
			self.resize(800, 600)
			self.layout.setContentsMargins(0, 0, 0, 0)
			self.bottom_layout.setContentsMargins(0, 0, 0, 0)
			self.bottom_layout.addWidget(self.laberror)
			self.widget.setLayout(self.layout)
			#self.setCentralWidget(self.widget)
			self.move(100,100)
			# Reproducir el video.
			path = n_msource
			avail = os.path.isfile(path)
			print(avail)
			if avail:
				self.layout.addWidget(self.video_widget)
				self.layout.addWidget(self.seek_slider)
				self.setCentralWidget(self.widget)
				self.media_player.play()
			else:
				print('Archivo no encontrado')
				self.laberror.setText("     No se encontro archivo: "+n_msource)
				self.layout.addLayout(self.bottom_layout)
				self.setCentralWidget(self.widget)
		except Exception as error:
			traceback.print_exc()
	def state_changed(self, newstate):
		states = {
			print("Something change")
		}
if __name__ == "__main__":
	app = QApplication(sys.argv)
	n_msource = sys.argv[1]
	window = PlayVideo()
	window.show()
	sys.exit(app.exec_())
