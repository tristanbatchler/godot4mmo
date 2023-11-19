extends Node
const Packet = preload("res://packets.gd")

signal connected
signal received(packet_type, packet: Packet.Packet)
signal disconnected(code: int, reason: String)
signal error(code: int)

var socket = WebSocketPeer.new()
const hostname: String = "localhost"
const port: int = 8081


func _ready():
	var url: String = "wss://%s:%d" % [hostname, port]
	var err: int = socket.connect_to_url(url)
	
	if err != OK:
		printerr("Websocket unable to connect to %s" % url)
		set_process(false)
		error.emit(err)

	print("Websocket connected to %s successfully" % url)
	connected.emit()
	

func _process(delta):
	socket.poll()
	var state: int = socket.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			var data: PackedByteArray = socket.get_packet()

			# Receive the generic packet first, which will contain the specific type of packet we received
			var packet: Packet.Packet = Packet.Packet.new()
			var result_code: int = packet.from_bytes(data)
			if result_code != Packet.PB_ERR.NO_ERRORS:
				printerr("Error parsing packet: %d" % result_code)
				set_process(false)
				emit_signal("error", result_code)

			# Now unpack the specific packet type
			var packet_type = packet.get_type()
			received.emit(packet_type, packet)
			
	elif state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass

	elif state == WebSocketPeer.STATE_CLOSED:
		var code: int = socket.get_close_code()
		var reason: String = socket.get_close_reason()
		printerr("WebSocket closed with code: %d, reason %s" % [code, reason])
		set_process(false)
		disconnected.emit(code, reason)
