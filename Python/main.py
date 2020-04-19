from Python import client_web_based_blockchain_control

if __name__ == "__main__":
    file = open("logo.txt", "r")
    logo = file.read()
    print(logo)
    client_web_based_blockchain_control.knotenpunkt.run(host='localhost', port=2169)
