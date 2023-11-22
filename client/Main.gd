extends Node

# Imports
const NetworkClient = preload("res://websocket_client.gd")
const Packets = preload("res://packets.gd")

var _network_client: NetworkClient
var state: Callable
var previous_direction: Vector2 = Vector2.ZERO


func _ready():
	_network_client = NetworkClient.new()
	_network_client.connected.connect(_handle_client_connected)
	_network_client.received.connect(_handle_network_data)
	_network_client.disconnected.connect(_handle_client_disconnected)
	_network_client.error.connect(_handle_network_error)
	
	add_child(_network_client)
	_network_client.connect_to_server("localhost", 8081)

	state = PLAY
	


func _process(delta):
	# Press SPACE to send a chat packet to the server
	if Input.is_action_just_pressed("ui_accept"):
		var my_packet: Packets.Packet = Packets.Packet.new()
		var my_chat_packet = my_packet.new_chat()
		my_chat_packet.set_msg("Hello world!")
		_network_client.send_packet(my_packet)

	# Press arrow keys to send direction packets to the server
	var direction: Vector2 = Vector2.ZERO
	if Input.is_action_pressed("ui_right"):
		direction.x += 1
	if Input.is_action_pressed("ui_left"):
		direction.x -= 1
	if Input.is_action_pressed("ui_down"):
		direction.y += 1
	if Input.is_action_pressed("ui_up"):
		direction.y -= 1

	if direction != Vector2.ZERO and direction != previous_direction:
		var p: Packets.Packet = Packets.Packet.new()
		var my_direction_packet: Packets.DirectionPacket = p.new_direction()
		my_direction_packet.set_dx(direction.x)
		my_direction_packet.set_dy(direction.y)
		_network_client.send_packet(p)
	
	previous_direction = direction

func PLAY(packet_type: String, packet: Packets.Packet):
	print("Received a %s packet" % [packet_type])


func _handle_client_connected():
	print("Client connected to server!")


func _handle_client_disconnected(code: int, reason: String):
	printerr("Client disconnected from server with code %s and reason %s" % [code, reason])
	get_tree().quit()


func _handle_network_data(packet_type: String, packet: Packets.Packet):
	state.call(packet_type, packet)


func _handle_network_error(code: int):
	printerr("Network error with code %s" % code)
	get_tree().quit()
