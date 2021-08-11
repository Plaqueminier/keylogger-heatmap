#!/usr/bin/env python3

from pynput import keyboard as kb
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from PIL import Image, ImageChops
import numpy as np
from heatmapper.charmap import char_map

dir_path = os.path.dirname(os.path.realpath(__file__))

keyboard = Image.open(
    '{0}/heatmapper/keyboard.png'.format(dir_path)
)

heatmap_size = (146, 60)

class LogsReader():
	def __init__(self, filename: str = ".logs") -> None:
		self.filename = filename
		self.int_log = []
		self.readable_log = []

	def read_file(self):
		with open(self.filename, 'rb') as bin_logs:
			while (key := bin_logs.read(2)) != b'':
				self.int_log.append(int.from_bytes(key, byteorder="big"))
				try:
					self.readable_log.append(str(kb.Key(kb.KeyCode.from_vk(int.from_bytes(key, byteorder="big")))))
				except ValueError:
					self.readable_log.append(chr(int.from_bytes(key, byteorder="big")))

	def count_occurrences(self):
		pairs = [(x, self.readable_log.count(x)) for x in list(set(self.readable_log))]
		return sorted(pairs, key=lambda pair: pair[1], reverse=True)

	def heatmap_builder(self):
		heatmap = np.array([[0] * heatmap_size[0]] * heatmap_size[1])
		pairs = self.count_occurrences()
		for pair in pairs:
			if pair[0].lower() in char_map:
				x, y = char_map[pair[0].lower()]
				for i in range(y - 2, y + 3):
					for j in range(x - 2, x + 3):
						if (abs(i - y) <= 1 or abs(j - x) <= 1):
							heatmap[i][j] = pair[1]
		return heatmap

	def blend_images(self):
		plt.clf()
		plt.xticks([])
		plt.yticks([])
		plt.axis('off')
		heatmap_arr = self.heatmap_builder()
		plt.imshow(heatmap_arr, cmap="Reds",interpolation="spline36", zorder=1)
		plt.savefig('{0}/heatmapper/heatmap.png'.format(dir_path),
			dpi=None,
			pad_inches=0,
			transparent=True,
			bbox_inches='tight'
		)
		heatmap = Image.open('{0}/heatmapper/heatmap.png'.format(dir_path))
		heatmap = heatmap.resize(keyboard.size, Image.ANTIALIAS)
		heatmap.save('{0}/heatmapper/heatmap.png'.format(dir_path))
		blended = ImageChops.darker(keyboard.convert("RGBA"), heatmap.convert('RGBA'))
		blended.save('{0}/heatmapper/heatmap.png'.format(dir_path))


if __name__ == '__main__':
	if (len(sys.argv) > 1):
		reader = LogsReader(sys.argv[1])
	else:
		reader = LogsReader()
	reader.read_file()
	print(reader.count_occurrences())
	reader.blend_images()
