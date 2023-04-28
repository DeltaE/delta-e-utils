# Creating an Executable File for a Tkinter Python Program Using PyInstaller

To create an executable file for a Tkinter Python program that uses the OS and directory modules, PyInstaller can be used. PyInstaller is a third-party tool that can convert a Python program into a standalone executable file, including all the necessary Python modules, libraries, and resources required for the program to run. 

## Steps

1. Install PyInstaller: You can install PyInstaller using pip by running the following command:

    ```
    pip install pyinstaller
    ```
    or 
    ```
    pip3 install pyinstaller
    ```

2. Create a spec file: A spec file tells PyInstaller how to package your program. You can create a spec file by running the following command in your terminal or command prompt:

    ```
    pyinstaller --name=dataForm --onefile form.py
    ```

    This command will create a spec file named "dataForm.spec" in the same directory as your program.


3. Generate the executable: Run the following command to generate the executable file:

    ```
    pyinstaller dataForm.spec
    ```

    This command will create a standalone executable file named `dataForm.exe` in the `dist` directory, **move the executable from `dist` directory to the main diretory and simply run it :-)**
