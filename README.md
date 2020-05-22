<img src="https://github.com/4AT-TP-19-20/projekt-kyas-coin/blob/master/Logo/Kyas%20ReadMe.png" width="100%"  class="center"/>

# Introduction
Kyas Coin is a deflationary cryptocurrency written from scratch in Python.

This repository contains:
- Python CLI Client of both client nodes and master node
- JavaFX Wallet Client and Miner
- Android Wallet

# Installation

## Python Node and Python Client

### Prerequisites
A working `Python 3.7` environment with the following packages:
- `flask`
- `urllib`
- `requests`
- `multiprocessing`
- `random`
- `hashlib`
- `json`
- `time`

They can all be installed by running `pip3.7 install <package>`

### Running the code
After installing all the prerequisites you can run the Kyas Node and Client programs as you would any other Python program. 
To start the local node, execute `python3.7 client_main.py`. To start a master node, execute
`python3.7 masternode_main.py`. 

## JavaFx Wallet Client and Miner

### Prerequisites
A working `JavaFX SDK`installation. You will need a version of Java installed that is newer or equal to `Java 14`. 
You can check your currently active java version by running the command `java -version`. You will also need `JavaFX SDK` matching
the Java 14 version.
### Running the JAR
You can execute the Client by typing the following command into a console:
`java --module-path "PATH_TO_JAVAFX_LIB_DIR" --add-modules javafx.controls,javafx.fxml,javafx.base,javafx.graphics,javafx.web,javafx.swing -jar PATH_TO_JAR`

## Android Wallet

### Prerequisites
Android 6 (Lollipop) or higher.

### APK Installation
Installing the app by tapping on the APK.

Note: Currently there is a bug that may stop the app from working on non-rooted devices. This is being addressed in [Issue #2][i2]

# Note on ongoing development
Currently, all master nodes and the block chain are offline, so it is not possible to actively execute transactions. 
This release serves as a concept for a later, more complete release. The master branch contains a more complete image of the project. 
Future releases will introduce full synchronization of the node network to decentralize the crypto currency. 
The development team would like to thank everyone who provided input for the development of the crypto currency.









[i2]: https://github.com/4AT-TP-19-20/projekt-kyas-coin/issues/2
