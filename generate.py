#!/usr/bin/env python

"""
APRS Symbol Look Up Table Generator

Creates a pretty LUT from APRS symbols

Each table entry will be the symbol code, the primary symbol, and the secondary symbol
+---------+
|code     |
+---------+
|primary  |
+---------+
|secondary|
+---------+
"""

from PIL import Image
import numpy

symbol_size = 64
symbolcount_x = 16
symbolcount_y = 6

line_heavy = 8
line_heavy_y = 16
line_light = 2

# Calculate final output dimensions
output_x = symbol_size * (symbolcount_x+1) + (symbolcount_x + 2) * line_heavy
output_y = symbol_size * symbolcount_y * 3 + (symbolcount_y + 1) * line_heavy_y + symbolcount_y * 2 * line_light

prim_img = Image.open("aprs-symbols-64-0.png")
prim_img = prim_img.convert("RGBA")
prim_pix = numpy.array(prim_img)

sec_img = Image.open("aprs-symbols-64-1.png")
sec_img = sec_img.convert("RGBA")
sec_pix = numpy.array(sec_img)

code_img = Image.open("codes.png")
code_img = code_img.convert("RGBA")
code_pix = numpy.array(code_img)
#Where are the table codes in the code table?
primcode_x = 14 * symbol_size
primcode_y = 0
seccode_x = 11 * symbol_size
seccode_y = 3 * symbol_size
blankcode_x = 11 * symbol_size
blankcode_y = 5 * symbol_size

final = numpy.zeros((output_y, output_x, 4), dtype=numpy.uint8)
# Blank out the alpha
final[:,:,3] = 255

for y in range(0, symbolcount_y):
	row_y = (y+1) * line_heavy_y + y * (symbol_size * 3 + line_light*2)
	final[row_y:row_y+symbol_size, line_heavy:line_heavy+symbol_size,:] = code_pix[blankcode_y:blankcode_y+symbol_size, blankcode_x:blankcode_x+symbol_size,:]
	final[row_y+symbol_size+line_light:row_y+2*symbol_size+line_light, line_heavy:line_heavy+symbol_size,:] = code_pix[primcode_y:primcode_y+symbol_size, primcode_x:primcode_x+symbol_size,:]
	final[row_y+2*(symbol_size+line_light):row_y+3*symbol_size+2*line_light, line_heavy:line_heavy+symbol_size,:] = code_pix[seccode_y:seccode_y+symbol_size, seccode_x:seccode_x+symbol_size,:]
	for x in range(0, symbolcount_x):
		print("Symbol ", x, y)
		# Calculate the top left corner of the code label
		grid_x = (x+2)*line_heavy + (x+1) * symbol_size
		grid_y = (y+1)*line_heavy_y + y * (symbol_size * 3 + line_light*2)

		src_x = x * symbol_size
		src_y = y * symbol_size
		# Symbol code
		final[grid_y:grid_y+symbol_size, grid_x:grid_x+symbol_size,:] = code_pix[src_y:src_y+symbol_size,src_x:src_x + symbol_size, :]
		# primary symbol
		prim_x = grid_x
		prim_y = grid_y + symbol_size + line_light
		final[prim_y:prim_y+symbol_size,prim_x:prim_x+symbol_size,:] = prim_pix[src_y:src_y+symbol_size,src_x:src_x + symbol_size, :]
		
		# secondary symbol
		sec_x = grid_x
		sec_y = grid_y + 2 * symbol_size + 2 * line_light
		final[sec_y:sec_y+symbol_size,sec_x:sec_x+symbol_size,:] = sec_pix[src_y:src_y+symbol_size,src_x:src_x + symbol_size, :]


finalimg = Image.fromarray(final)
finalimg.save("test.png")

print("Final output ", output_x, output_y)
