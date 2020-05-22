<img src="https://github.com/4AT-TP-19-20/projekt-kyas-coin/blob/master/Logo/Kyas%20ReadMe.png" width="100%"  class="center"/>

# Introduction
Kyas Coin is a deflationary cryptocurrency written from scratch in Python.

This repository contains:
- Python Node
- Python CLI Client
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

## JavaFx Wallet Client and Miner

### Prerequisites
A working `JavaFX SDK`installation. You will need a version of Java installed that is newer or equal to `Java 14`. 
You can check your currently active java version by running the command `java -version`.
### Running the JAR
You can execute the Client by typing the following command into a console:
`java --module-path "PATH_TO_JAVAFX_LIB_DIR" --add-modules javafx.controls,javafx.fxml,javafx.base,javafx.graphics,javafx.web,javafx.swing -jar PATH_TO_JAR`

## Android Wallet

### Prerequisites
Android 6 (Lollipop) or higher.

### APK Installation
Installing the app by tapping on the APK.

Note: Currently there is a bug that may stop the app from working on non-rooted devices. This is being addressed in [Issue #2][i2]








[i2]: https://github.com/4AT-TP-19-20/projekt-kyas-coin/issues/2
