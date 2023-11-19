extends Node
const Packets = preload("res://packets.gd")

signal connected
signal received(packet_type: int, packet: Packets.Packet)
signal disconnected(code: int, reason: String)
signal error(code: int)

var _socket: WebSocketPeer = WebSocketPeer.new()

func _ready() -> void:
	set_process(false)	# Don't poll until a connection has been made
	
func connect_to_server(hostname: String, port: int) -> void:
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
	

func _process(delta) -> void:
	_socket.poll()
	
	var state: int = _socket.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		while _socket.get_available_packet_count():
			var data: PackedByteArray = _socket.get_packet()

			# Receive the generic packet first, which will contain the specific type of packet we received
			var packet: Packets.Packet = Packets.Packet.new()
			var result_code: int = packet.from_bytes(data)
			if result_code != Packets.PB_ERR.NO_ERRORS:
				printerr("Error parsing packet: %d" % result_code)
				set_process(false)
				emit_signal("error", result_code)

			# Now unpack the specific packet type
			var packet_type: int = packet.get_type()
			received.emit(packet_type, packet)
			
	elif state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass

	elif state == WebSocketPeer.STATE_CLOSED:
		var code: int = _socket.get_close_code()
		var reason: String = _socket.get_close_reason()
		printerr("WebSocket closed with code: %d, reason %s" % [code, reason])
		set_process(false)
		disconnected.emit(code, reason)

func send_packet(packet_type: int, specific_packet) -> void:
	var packet: Packets.Packet = Packets.Packet.new()

	packet.set_type(packet_type)

	# The key of packet._data we need to worry about is the value of packet_type + 2, since the 
	# keys start at 1, and the first is the packet_type itself
	var idx: int = packet_type + 2
	packet.data[idx].state = Packets.PB_SERVICE_STATE.FILLED

	# Now we need to set the value of the member variable for the specific packet to the data we 
	# want to send
	var ref_ctr: int = -1	# Set to -1 to skip the first ref, which is _type
	var member_var_name: String
	for property in packet.get_property_list():
		if property["class_name"] == &"RefCounted":
			if ref_ctr == packet_type:
				member_var_name = property["name"]
				break
			ref_ctr += 1

	var member_var: Variant = packet.get(member_var_name)
	member_var.value = specific_packet

	# Now we can serialize the packet and send it
	var data: PackedByteArray = packet.to_bytes()
	var err: int = _socket.send(data)
	if err:
		printerr("Error sending data. Error code: ", err)
		set_process(false)
		error.emit(err)

