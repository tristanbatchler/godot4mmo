from server.net.packets_pb2 import Packet, OkPacket, DenyPacket, LoginPacket, RegisterPacket, ChatPacket, PositionPacket, DirectionPacket

def create_deny_packet(reason: str):
    deny_packet = DenyPacket()
    deny_packet.reason = reason
    packet = Packet()
    packet.deny.CopyFrom(deny_packet)
    return packet

def create_ok_packet(reason: str):
    ok_packet = OkPacket()
    ok_packet.reason = reason
    packet = Packet()
    packet.ok.CopyFrom(ok_packet)
    return packet

def create_login_packet(user: str, password: str):
    login_packet = LoginPacket()
    login_packet.username = user
    login_packet.password = password
    packet = Packet()
    packet.login.CopyFrom(login_packet)
    return packet

def create_register_packet(user: str, password: str):
    register_packet = RegisterPacket()
    register_packet.username = user
    register_packet.password = password
    packet = Packet()
    packet.register.CopyFrom(register_packet)
    return packet

def create_chat_packet(user: str, message: str):
    chat_packet = ChatPacket()
    chat_packet.name = user
    chat_packet.message = message
    packet = Packet()
    packet.chat.CopyFrom(chat_packet)
    return packet

def create_position_packet(x: int, y: int):
    position_packet = PositionPacket()
    position_packet.x = x
    position_packet.y = y
    packet = Packet()
    packet.position.CopyFrom(position_packet)
    return packet

def create_direction_packet(dx: int, dy: int):
    direction_packet = DirectionPacket()
    direction_packet.dx = dx
    direction_packet.dy = dy
    packet = Packet()
    packet.direction.CopyFrom(direction_packet)
    return packet