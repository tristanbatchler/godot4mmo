class_name NetworkClient
extends Node
const Packets = preload("res://packets.gd")

signal connected
signal received(packet: Packets.Packet)
signal disconnected(code: int, reason: String)
signal error(code: int)

var _socket: WebSocketPeer = WebSocketPeer.new()

@export var hostname: String = "localhost"
@export var port: int = 8081

func _ready() -> void:
	set_process(false)	# Don't poll until a connection has been made
	connect_to_server()
	
func connect_to_server() -> void:
	var url: String = "ws://%s:%d" % [hostname, port]
	var options: TLSOptions = TLSOptions.client_unsafe()
	var err: int = _socket.connect_to_url(url, options)
	
	if err:
		printerr("Websocket unable to connect to %s" % url)
		error.emit(err)
		return
	
	_socket.poll()
	var ready_state: int = _socket.get_ready_state()
	while ready_state == WebSocketPeer.STATE_CONNECTING:
		_socket.poll()
		ready_state = _socket.get_ready_state()
	
	if ready_state != WebSocketPeer.STATE_OPEN:
		printerr("Websocket unable to connect to %s" % url)
		error.emit(ready_state)
		return
		
	print("Websocket connected to %s successfully" % url)
	connected.emit()
	set_process(true)
	

func _process(delta) -> void:
	_socket.poll()
	
	var state: int = _socket.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		while _socket.get_available_packet_count():
			var data: PackedByteArray = _socket.get_packet()

			var packet: Packets.Packet = Packets.Packet.new()
			var result_code: int = packet.from_bytes(data)
			if result_code != Packets.PB_ERR.NO_ERRORS:
				printerr("Error parsing packet: %d" % result_code)
				set_process(false)
				emit_signal("error", result_code)

			received.emit(packet)
			
	elif state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass

	elif state == WebSocketPeer.STATE_CLOSED:
		var code: int = _socket.get_close_code()
		var reason: String = _socket.get_close_reason()
		printerr("WebSocket closed with code: %d, reason %s" % [code, reason])
		set_process(false)
		disconnected.emit(code, reason)

func send_packet(packet: Packets.Packet) -> void:
	var data: PackedByteArray = packet.to_bytes()
	var err: int = _socket.send(data)
	if err:
		printerr("Error sending data. Error code: ", err)
		set_process(false)
		error.emit(err)
