import os
import shutil


def main():
    properties_file = "properties.ini"
    input_mod_folder = "input"
    output_mod_folder = "output"
    profile = None

    with open(properties_file, 'r') as f:
        profile = "".join(f.readlines()).rstrip()

    print(f"Attempting to load the \"{profile}\" profile.")
    
    mod_grouper_folder_contents = os.listdir(input_mod_folder)
    mod_groups = [dir for dir in mod_grouper_folder_contents if os.path.isdir(input_mod_folder + "/" + dir) and dir != output_mod_folder and dir[0] != "."]

    if profile in mod_groups:
        shutil.rmtree(output_mod_folder)
        shutil.copytree(input_mod_folder + "/" + profile, output_mod_folder)
        print(f"Profile \"{profile}\" has been loaded!")
    else:
        print("Profile not found!")



if __name__ == "__main__":
    main()