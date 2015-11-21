#Sguigee

A GUI Library for Python

* A wrapper on TKInter
* Two levels:
	* Easy
	* Advanced
* Easy level overview available [here](https://tuomas56.github.io/sguigee-presentation)

##Projects using Sguigee

* [garrulous-octo-broccoli](https://github.com/tuomas56/garrulous-octo-broccoli)

##Documentation

###Easy Mode

####Windows

To create windows, use the ```window``` context manager.

This has several keyword options:

* ```title``` - set a title.
* ```set_minimum_size``` - make sure that the window cannot be resized below its original size.
* ```can_resize``` - set whether the window can be resized. (TODO: support different directions.)

> Note: the ```window``` context manager executes ```mainloop()``` *on exit!* So all program logic must be within functions called from inside the context manager, or within it itself.

####Rows

Windows are divided into rows. In order for elements to appear in order, all elements must be placed into rows, even if there is only one per row. Rows are created with the ```row``` context manager.  
This is used *within* the ```window``` context manager:

```python
	with window(**options):
		with row():
			pass

		with row():
			pass
```

####Labels

Within a row, you can place labels. They are created like this: 

```python
label(text)
```

Sguigee uses the pack geometry manager in TKInter, you can control which options are passed to ```pack``` by passing them to the widget constructor (or a function like ```label```) and prefixing them with ```pack_```, e.g) pack_fill, pack_expand, etc.

All options not recognized by Sguigee will be passed onto TKInter when the widget is instatiated.

####Textboxes

Textboxes - the Entry widget in TKInter - are created with the ```textbox``` function. This returns a StringVar attached to the widget.

####Buttons

These are provided via the ```button``` decorator:

```python
@button("Button text")
def on_button_click():
	pass
```

####Message Boxes

Sguigee provides the message box functions provided by the ```tkinter.message_box``` module. These are available in the ```message_box``` function. Which message box is displayed can be controlled via the ```type``` keyword argument. The title defaults to the title of the window, but an alternative can be specified via the ```title``` keyword argument.