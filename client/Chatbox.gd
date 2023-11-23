extends Control

@onready var chat_log: RichTextLabel = $CanvasLayer/VBoxContainer/RichTextLabel
@onready var input_field: LineEdit = $CanvasLayer/VBoxContainer/HBoxContainer/LineEdit
@onready var chat_bar: HBoxContainer = $CanvasLayer/VBoxContainer/HBoxContainer

signal chat_sent(message: String)

func disable_chat():
	chat_bar.hide()
	
func enable_chat():
	chat_bar.show()

func _input(event: InputEvent):
	if event is InputEventKey and event.pressed:
		match event.keycode:
			KEY_ENTER:
				input_field.grab_focus()
			KEY_ESCAPE:
				input_field.release_focus()

func add_message(text: String):
	chat_log.append_text(text + "\n")

func _on_line_edit_text_submitted(new_text):
	if len(new_text) > 0:
		input_field.clear()
		add_message(new_text)
		chat_sent.emit(new_text)
