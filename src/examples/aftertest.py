from sguigee import *

with window():
	with row():
		c = canvas(height=200, width=200)

	with row():
		@button("Go")
		def click():
			c.create_text((100, 100), text='apple')
			@after(5)
			def a():
				c.clear()
