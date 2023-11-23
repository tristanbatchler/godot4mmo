extends Node

# Imports
const Packets = preload("res://packets.gd")

var state: Callable = ENTRY

@onready var _network_client: Node = $NetworkClient
@onready var _chatbox: Control = $Chatbox
@onready var _entry: Control = $Entry

func _ready():
	_chatbox.disable_chat()

func ENTRY(packet: Packets.Packet):
	pass
	
func REGISTER(packet: Packets.Packet):
	if packet.has_deny():
		var reason: String = packet.get_deny().get_reason()
		_chatbox.add_message("[color=#FFD943]%s[/color]" % [reason])
		state = ENTRY
		
	elif packet.has_ok():
		var message: String = packet.get_ok().get_msg()
		_chatbox.add_message("[color=#43FFD9]%s[/color]" % [message])
		state = ENTRY
		
func LOGIN(packet: Packets.Packet):
	if packet.has_deny():
		var reason: String = packet.get_deny().get_reason()
		_chatbox.add_message("[color=#FFD943]%s[/color]" % [reason])
		state = ENTRY
		
	elif packet.has_ok():
		var message: String = packet.get_ok().get_msg()
		_chatbox.add_message("[color=#43FFD9]%s[/color]" % [message])
		_chatbox.enable_chat()
		remove_child(_entry)
		state = PLAY
		
func PLAY(packet: Packets.Packet):
	if packet.has_chat():
		var message: String = packet.get_chat().get_msg()
		_chatbox.add_message(message)
		
	elif packet.has_disconnect():
		var reason: String = packet.get_disconnect().get_reason()
		_chatbox.add_message("[color=#D943FF]%s[/color]" % [reason])

func _on_chatbox_chat_sent(message: String):
	var p: Packets.Packet = Packets.Packet.new()
	var c: Packets.ChatPacket = p.new_chat()
	c.set_msg(message)
	_network_client.send_packet(p)

func _on_network_client_connected():
	print("Client connected to server!")

func _on_network_client_disconnected(code, reason):
	printerr("Client disconnected from server with code %s and reason %s" % [code, reason])
	get_tree().quit()

func _on_network_client_error(code):
	printerr("Network error with code %s" % code)
	get_tree().quit()

func _on_network_client_received(packet):
	state.call(packet)

func _on_entry_login(username, password):
	state = LOGIN
	var p: Packets.Packet = Packets.Packet.new()
	var l: Packets.LoginPacket = p.new_login()
	l.set_username(username)
	l.set_password(password)
	_network_client.send_packet(p)

func _on_entry_register(username, password):
	state = REGISTER
	var p: Packets.Packet = Packets.Packet.new()
	var r: Packets.RegisterPacket = p.new_register()
	r.set_username(username)
	r.set_password(password)
	_network_client.send_packet(p)
