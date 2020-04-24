from Python import client_web_based_blockchain_control

if __name__ == "__main__":
    # Print kyas logo into console
    file = open("logo.txt", "r")
    logo = file.read()
    print(logo)
    # Start flask server
    client_web_based_blockchain_control.node.run(host='localhost', port=2169)
