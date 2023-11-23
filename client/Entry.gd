extends Control

@onready var username_field: LineEdit = $CanvasLayer/VBoxContainer/GridContainer/LineEdit_Username
@onready var password_field: LineEdit = $CanvasLayer/VBoxContainer/GridContainer/LineEdit_Password

signal login(username: String, password: String)
signal register(username: String, password: String)

func _on_button_login_pressed():
	login.emit(username_field.text, password_field.text)

func _on_button_register_pressed():
	register.emit(username_field.text, password_field.text)
