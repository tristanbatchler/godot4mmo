extends Control

@onready var chat_log: RichTextLabel = get_node("CanvasLayer/VBoxContainer/RichTextLabel")
@onready var input_field: LineEdit = get_node("CanvasLayer/VBoxContainer/HBoxContainer/LineEdit")

signal chat_sent(message: String)

func _ready():
	input_field.connect("text_submitted", _handle_chat_submitted)
	
func _input(event: InputEvent):
	if event is InputEventKey and event.pressed:
		match event.keycode:
			KEY_ENTER:
				input_field.grab_focus()
			KEY_ESCAPE:
				input_field.release_focus()

func add_message(text: String):
	chat_log.append_text(text + "\n")
	
func _handle_chat_submitted(text: String):
	if len(text) > 0:
		input_field.text = ""
		add_message(text)
		chat_sent.emit(text)
