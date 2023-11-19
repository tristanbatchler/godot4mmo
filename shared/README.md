# Shared
This folder contains files that are shared between the server and the client. Namely, the packet 
definition files, courtesy of [protobuf](https://developers.google.com/protocol-buffers/).

To generate the python files, run the following command from this folder:
```bash
protoc -I="." --python_out="../server" --mypy_out="../server" "./packets.proto"
```

To generate the Godot files, install the `godobuf` plugin and configure it by pointing the 
"Input protobuf file" to `shared/packets.proto` and the "Output GDScript file" to 
`client/packets.gd`.