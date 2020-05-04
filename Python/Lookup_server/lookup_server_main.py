from Python.Lookup_server import lookup_server

if __name__ == "__main__":
    # Change host address to own static ip
    lookup_server.server.run(host="192.168.1.200", port=6921)
