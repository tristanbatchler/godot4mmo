extends Node

# Imports
const Packets = preload("res://packets.gd")

var state: Callable = ENTRY

@onready var _network_client: Node = $NetworkClient
@onready var _chatbox: Control = $Chatbox

func ENTRY(packet: Packets.Packet):
	if packet.has_deny():
		var reason: String = packet.get_deny().get_reason()
		_chatbox.add_message("[color=#FFD943]%s[/color]" % [reason])
		
	if packet.has_ok():
		var message: String = packet.get_ok().get_msg()
		_chatbox.add_message("[color=#43FFD9]%s[/color]" % [message])

func _on_chatbox_chat_sent(message: String):
	var p: Packets.Packet = Packets.Packet.new()
	
	
	if message.begins_with("/login "):
		var args: Array = message.split(" ")
		if args.size() == 3:
			var c: Packets.LoginPacket = p.new_login()
			c.set_username(args[1])
			c.set_password(args[2])
			_network_client.send_packet(p)
		else:
			_chatbox.add_message("[color=#FFD943]Usage: /login <username> <password>[/color]")

	elif message.begins_with("/register "):
		var args: Array = message.split(" ")
		if args.size() == 3:
			var c: Packets.RegisterPacket = p.new_register()
			c.set_username(args[1])
			c.set_password(args[2])
			_network_client.send_packet(p)
		else:
			_chatbox.add_message("[color=#FFD943]Usage: /register <username> <password>[/color]")

	else:
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
