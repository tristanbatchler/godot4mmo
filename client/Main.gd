extends Node

# Imports
const Packets = preload("res://packets.gd")

var state: Callable = PLAY
var previous_direction: Vector2 = Vector2.ZERO

@onready var _network_client: Node = $NetworkClient
@onready var _chatbox: Control = $Chatbox

func PLAY(packet: Packets.Packet):
	if packet.has_chat():
		var message: String = packet.get_chat().get_msg()
		_chatbox.add_message(message)
		
	if packet.has_disconnect():
		var reason: String = packet.get_disconnect().get_reason()
		_chatbox.add_message("[color=#42D9FF]%s[/color]" % [reason])

func _on_chatbox_chat_sent(message):
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
