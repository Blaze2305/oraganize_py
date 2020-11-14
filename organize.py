# IMPORTS
from os import listdir, chdir, mkdir, getcwd
from pathlib import Path

# CONSTANTS
FOLDERS = ["Videos","Images","Executables","Zips","Documents","Torrents","Excels","Random"]


# Extension folder name mapping
EXTENSION_MAP = {
    "Videos" : ['.mp4','.mkv','.avi'],
    "Images" : [".png",".jpg",".jpeg",".bmp",".gif"],
    "Executables":['.msi','.exe'],
    "Zips":['.tar','.gzip','.7z','.zip','.rar',".tar.gz"],
    "Documents":[".pdf",".docx",".ppt",".pptx"],
    "Torrents":['.torrent'],
    "Excels":['.xlsx','.csv']
}


# Create all the folders required
def folder_init()->None:
    for folder in FOLDERS:
        try:
            mkdir(folder)
        except FileExistsError:
            pass

# move a file
def move_file(fromPath:str,toPath:str)->bool:
    try:
        # Move the file from the old path to the new path
        Path(fromPath).rename(toPath)
        return True
    # If the file does not exist throw an error
    except FileNotFoundError:
        print("File does not exist")
        return False
    # If the file already exists in the new path append a _1 / _2 ....  to the end of the file and try moving again untill success
    except FileExistsError:
        # Split the new path by . to remove the extension
        new_path_list = toPath.split(".")
        print(new_path_list)
        last_digit = new_path_list[0].split("_")[-1]
        # if it already was a copy inc the number at the end and move again
        if last_digit.isdigit():
            new_path_list[0]+="_"+str(int(last_digit)+1)
        else:
            new_path_list[0] += "_1"
        new_path = ".".join(new_path_list)
        print(new_path)
        status = move_file(fromPath,new_path)
        return status

# Actual code to organize all the files
def organize_files(path:str)->None:

    # Switch to the folder mentioned , if it doesnt exist say so and exit
    try:
        chdir(path)
    except FileNotFoundError:
        print("Path does not exist")
        return

    # create the folders
    folder_init()
    
    # get list of all files in the folder
    files = listdir()
    for file in files:
        # Get the files extension
        extension = Path(file).suffix
        # if it doesnt exist it means its a folder so we can just skip it
        if not extension:
            continue
        # Else get the proper folder for the extension and move it
        for folder in EXTENSION_MAP:
            if extension in EXTENSION_MAP[folder]:
                move_file(file,f"{folder}\\{file}")
                break
        else:
            move_file(file,f"Random\\{file}")


    print("DONE")


def main():
    path = input()
    organize_files(path)


if __name__ == '__main__':
    main()