from Python.Client_node import client_web_based_blockchain_control

if __name__ == "__main__":
    # Print kyas logo into console
    file = open("../Design/logo.txt", "r")
    logo = file.read()
    print(logo)
    # Start flask server
    client_web_based_blockchain_control.node.run(host='192.168.1.21', port=21569)
