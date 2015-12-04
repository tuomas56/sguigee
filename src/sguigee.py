import tkinter as tk
from functools import partial, wraps
from contextlib import contextmanager
import tkinter.messagebox as tkm
import tkinter.simpledialog as tks
from threading import Thread
import time

def wrapmethod(name):
	def _method(self, *args, **kwargs):
		return getattr(self.get(), name)(*args, **kwargs)
	return _method

class _tkwrapper:
	config = wrapmethod('config')
	destroy = wrapmethod('destroy')
	hide = wrapmethod('pack_forget')

	def __init__(self, **kwargs):
		self._can_pack = True
		self.nargs = {}
		self.pargs = {}
		self.children = []
		for name, value in kwargs.items():
			if name.startswith('pack_'):
				self.pargs[name[5:]] = value
			elif name == 'use_monospace_font':
				if value:
					self.nargs['font'] = 'Courier'
			else:
				self.nargs[name] = value

	def set_parent(self, parent):
		self._value = self._class(parent, **self.nargs)
		self._parent = parent

	def append(self, element):
		element.set_parent(self.get())
		self.children.append(element)

	def __lshift__(self, child):
		self.append(child)
		return self

	def pack(self, **kwargs):
		for child in self.children:
			child.pack()

		if self._can_pack:
			kwargs.update(self.pargs)
			self.get().pack(**kwargs)
			self._can_pack = False

	def show(self, **kwargs):
		return self.pack(**kwargs)

	def get(self):
		return self._value

class Button(_tkwrapper):
	_class = tk.Button

class Canvas(_tkwrapper):
	_class = tk.Canvas
	create_arc = wrapmethod('create_arc')
	create_bitmap = wrapmethod('create_bitmap')
	create_image = wrapmethod('create_image')
	create_line = wrapmethod('create_line')
	create_oval = wrapmethod('create_oval')
	create_polygon = wrapmethod('create_polygon')
	create_rectangle = wrapmethod('create_rectangle')
	create_text = wrapmethod('create_text')

	def clear(self):
		self.get().delete("all")

class Entry(_tkwrapper):
	_class = tk.Entry

class Label(_tkwrapper):
	_class = tk.Label

class Menu(_tkwrapper):
	_class = tk.Menu

	def pack(self, **kwargs):
		pass

class Frame(_tkwrapper):
	_class = tk.Frame

class Tk:
	def __init__(self, **kwargs):
		self._minsize = False
		if 'set_minsize' in kwargs:
			self._minsize = kwargs['set_minsize']
			del kwargs['set_minsize']
		if 'title' in kwargs:
			title = kwargs['title']
			del kwargs['title']
		else:
			title = 'tk'
		self.tk = tk.Tk(**kwargs)
		self.tk.title(title)
		self.children = []

	def append(self, child):
		child.set_parent(self.tk)
		self.children.append(child)

	def __lshift__(self, child):
		self.append(child)
		return self

	def pack(self):
		for child in self.children:
			child.pack()

	def get(self):
		return self.tk

	def mainloop(self):
		self.pack()
		if self._minsize:
			self.tk.update()
			self.tk.minsize(self.tk.winfo_width(), self.tk.winfo_height())
		self.tk.mainloop()

class StringVar(_tkwrapper, tk.StringVar):
	def __init__(self, *args, **kwargs):
		tk.StringVar.__init__(self, *args, **kwargs)
	
	def set_element(self, parent):
		self._value = parent

@contextmanager
def frame(parent, **kwargs):
	f = Frame(**kwargs)
	f.set_parent(parent.get())
	f.pack()
	yield f
	for child in f.children:
		child.pack(side=tk.LEFT)

@contextmanager
def window(title='tk', *, set_minimum_size=False, can_resize=True, height=None, width=None, **kwargs):
	global root
	root = Tk(title=title, set_minsize=set_minimum_size, **kwargs)
	if not can_resize:
		root.get().resizable(False, False)
	if height is not width is not None:
		root.get().geometry("%sx%s" % (width, height))
	yield root
	root.mainloop()

@contextmanager
def row(*, expand=True, fill="x", **kwargs):
	global root
	old_root = root
	with frame(root, pack_expand=expand, pack_fill=fill, **kwargs) as f:
		root = f
		yield root
	root = old_root

def button(func=None, *, expand=True, fill="x", side='left', use_monospace_font=False, **kwargs):
	if callable(func):
		x = Button(pack_expand=expand, pack_fill=fill, command=func, pack_side=side,
			use_monospace_font=use_monospace_font, **kwargs)
		root << x
		return x
	elif func is None:
		def _button(func):
			x = Button(pack_expand=expand, pack_fill=fill, command=func, pack_side=side,
				use_monospace_font=use_monospace_font, **kwargs)
			root << x
			return x
		return _button
	elif isinstance(func, str):
		def _button(f):
			x = Button(text=func, pack_expand=expand, pack_fill=fill, command=f, pack_side=side,
			use_monospace_font=use_monospace_font, **kwargs)
			root << x
			return x
		return _button

def canvas(*, expand=True, fill="both", side="left", **kwargs):
	c = Canvas(pack_expand=expand, pack_fill=fill, pack_side=side, **kwargs)
	root << c
	return c
		

def label(text='', *, expand=True, fill="x", side='left', **kwargs):
	x = Label(text=text, pack_expand=expand, pack_fill=fill, pack_side=side, **kwargs)
	root << x
	return x

def textbox(*, expand=True, fill="x", side='left', **kwargs):
	s = StringVar()
	x = Entry(textvariable=s, pack_fill=fill, pack_expand=expand, pack_side=side, **kwargs)
	root << x
	s.set_element(x)
	return s

def show_message(*message, sep=' ', type='info', title=None):
	message = sep.join(map(lambda x: x.get() if isinstance(x, tk.StringVar) else str(x), message))
	if title is None:
		global root
		title = root.get().title()
	if type == 'info':
		tkm.showinfo(title=title, message=message)
	elif type == 'warning':
		tkm.showwarning(title=title, message=message)
	elif type == 'error':
		tkm.showerror(title=title, message=message)

def ask_message(*message, sep=' ', title=None, **kwargs):
	message = sep.join(map(lambda x: x.get() if isinstance(x, tk.StringVar) else str(x), message))
	if title is None:
		global root
		title = root.get().title()
	return tks.askstring(title, message, **kwargs)

def after(secs):
	def _after(func):
		global root
		root.get().after(secs * 1000, func)
	return _after

	

__all__ = ['frame', 'Button', 'Canvas', 'Entry', 'Label', 'Menu', 'Frame',
		   'Tk', 'row', 'button', 'window', 'label', 'textbox',
	       'show_message', 'canvas', 'after', 'ask_message']