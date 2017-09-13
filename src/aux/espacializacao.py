#-*- coding: utf-8 -*-
import numpy as n, pylab as p, Image

im = Image.open('../../figuras/cabeca.png')

height = im.size[1]

# We need a float array between 0-1, rather than
# a uint8 array between 0-255
im2 = n.array(im).astype(n.float) / 255

fig = p.figure()

ax=p.subplot(111)

from matplotlib._png import read_png
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data

#fn = get_sample_data("../figuras/cabeca.png")
arr_lena = read_png("../../figuras/cabeca.png")

imagebox = OffsetImage(arr_lena, zoom=0.2)

xy = (0.5, 0.7)

ab = AnnotationBbox(imagebox, xy,
		xybox=(120., -80.),
		xycoords='data',
		boxcoords="offset points",
		pad=0.5,
		arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=3")
		   )


ax.add_artist(ab)

# With newer (1.0) versions of matplotlib, you can 
# use the "zorder" kwarg to make the image overlay
# the plot, rather than hide behind it... (e.g. zorder=10)
fig.figimage(im2, 100, fig.bbox.ymax - height-100, zorder=10)


p.xlim(0,200)
p.ylim(-100,100)

p.show()


