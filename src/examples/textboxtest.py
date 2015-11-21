from sguigee import window, textbox, button, row

with window(title='Textbox'):
	with row():
		t = textbox()

		@button("Go")
		def go_button_click():
			print(t.get(), flush=True)
