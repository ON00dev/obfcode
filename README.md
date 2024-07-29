# OBFCODE

OBFCODE is a graphical user interface (GUI) tool for obfuscating source code written in multiple programming languages. The tool allows users to select a source file, choose the number of obfuscation iterations, and specify the target programming language. The obfuscation process is executed using different tools for each language, and the progress is displayed in real-time.

## Features

- Multi-language Support: Supports obfuscation for Python, C, C++, C#, and Java.
- Iteration Control: Allows users to specify the number of times the obfuscation process should be repeated.
- Real-time Logging: Displays the progress of the obfuscation process in a dedicated window.
- Error Handling: Provides detailed error messages if the obfuscation process fails.

## Requirements available in your system's PATH

- Python 3.10+
- pip
- iwwerc
- Confuser.CLI.exe
- proguard
  
## Installation

Clone the repository:
- `git clone https://github.com/ON00dev/obfcode.git`
- `cd obfcode`
- `pip install -r requirements.txt`

## Usage

Run the script:
- `cd src`
- `python obfcode.py`

Select the file to be obfuscated.
Choose the save directory where the obfuscated file will be stored.
Specify the number of iterations for the obfuscation process.
Select the programming language of the source code.
Click the "Obfuscate" button to start the obfuscation process. A new window will open showing the progress.

--------------------------------------------------------------------------------------------------------------------------
## License

This project is licensed under the MIT License.

--------------------------------------------------------------------------------------------------------------------------
Feel free to adjust the description to better suit your repository's needs.
