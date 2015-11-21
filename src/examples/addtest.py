from sguigee import window, row, textbox, button, show_message

with window(title="Add"):
	with row():
		a = textbox()
		b = textbox()

	with row():
		@button("Add")
		def add_button_click():
			show_message(int(a.get()) + int(b.get()))