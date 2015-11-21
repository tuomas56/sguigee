from gui import window, row, button, textbox
import operator as op

def make_button(text):
	@button(text)
	def _button():
		output.set(output.get() + text)
	return _button

def make_operator(t, op):
	@button(t, expand=False, use_monospace_font=True)
	def _button():
		stack.append(float(output.get()))
		output.set('')
		stack.append(op)

stack = []
with window(title="Calculator", set_minimum_size=True, can_resize=False):
	with row():
		output = textbox()

	with row():
		make_button('1')
		make_button('2')
		make_button('3')
		make_operator('+', op.add)

	with row():
		make_button('4')
		make_button('5')
		make_button('6')
		make_operator('-', op.sub)

	with row():
		make_button('7')
		make_button('8')
		make_button('9')
		make_operator('*', op.mul)

	with row():
		make_button('0')
		make_button('.')
		make_operator('/', op.truediv)

	with row():
		@button('Clear')
		def clear():
			output.set('')

		@button('Clear All')
		def clear_all():
			stack = []
			output.set('')

		@button('=')
		def compute():
			while len(stack) >= 2:
				op, lhs = stack.pop(), stack.pop()
				output.set(op(lhs, float(output.get())))
