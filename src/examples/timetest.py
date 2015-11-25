from sguigee import canvas, window, row, button, after, show_message
import random

with window(title="Memory Game"):
	with row():
		c = canvas(width=200, height=200)
		c.create_text((100, 100), text="Press 'Go' to begin\n the Memory Game.")

	with row():
		@button("Go")
		def go_button():
			c.clear()
			word = random.choice(["hi", "hello"])
			c.create_text((100, 100), text=word)
			@after(5)
			def on_timer():
				c.clear()
				c.create_text((100, 100), text="Now, can you remember\n what the word was?\n Click 'Guess' to try.")
				go_button.destroy()
				@button("Guess")
				def guess_button():
					c.destroy()
					guess_button.destroy()
					a = textbox()
					@button("Continue")
					def continue_button():
						if a.get() == word:
							show_message("Well Done!")

