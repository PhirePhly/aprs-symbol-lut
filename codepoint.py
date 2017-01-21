#!/usr/bin/env python

"""
APRS Symbol Look Up Table Generator
Code point extractor from v1 LUT

Extracts just the symbol codes so I don't have to manually replace them
with every iteration of the table.
"""

from PIL import Image
import numpy

symbol_size = 64
symbolcount_x = 16
symbolcount_y = 6

line_heavy = 8
line_light = 2

# aprs-symbols-64-0.png: PNG image data, 1024 x 384, 8-bit/color RGBA, non-interlaced

src = Image.open("KWFAPRS_LUTv1.png")
src = src.convert("RGBA")
src_pix = numpy.array(src)

final = numpy.zeros((384, 1024, 4), dtype=numpy.uint8)
# Blank out the alpha
final[:,:,3] = 255

for x in range(0, symbolcount_x):
	for y in range(0, symbolcount_y):
		print("Symbol ", x, y)
		# Calculate the top left corner of the code label
		grid_x = (x+1)*line_heavy + x * symbol_size
		grid_y = (y+1)*line_heavy + y * (symbol_size * 3 + line_light*2)
		out_x = symbol_size * x
		out_y = symbol_size * y

		final[out_y:out_y+symbol_size,out_x:out_x+symbol_size,:] = src_pix[grid_y:grid_y+symbol_size,grid_x:grid_x+symbol_size,:]


finalimg = Image.fromarray(final)
finalimg.save("test.png")

