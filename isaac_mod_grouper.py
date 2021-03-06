#!/usr/bin/env python

import os
import shutil
import json
import pathlib
import sys

'''
TODO features to add:
Copy the enabled mods currently in your mod folder into a mod profile
Property where 

'''
version = "1.0.0"
command_list = ["help", "import", "export", "remove", "list", "exit"]
command_info = {"help": "Generates documentation for a given command.\nSyntax: \"help <command>\"",\
                "import": "Enables only the mods associated with an existing mod profile on the user\'s Isaac instance.\nSyntax: \"import <profile_name>\"", \
                "export": "Exports the currently enabled mods from the user\'s Isaac instance into a mod profile.\nSyntax: \"export <profile_name>\"", \
                "remove": "Removes a mod profile from the list of existing mod profiles.\nSyntax: \"remove <profile_name>\"", \
                "list": "Lists off all existing mod profiles.\nSyntax: \"list\"", \
                "exit": "Exits the program.\nSyntax: \"exit\""}
isaac_mods_folder = ""

def main():
    properties_file = "properties.ini"
    input_mod_folder = "input"
    output_mod_folder = "output"
    profile = None

    if not os.path.isdir(input_mod_folder):
        os.mkdir(input_mod_folder)
        print(f"Creating the input mod directory \"{input_mod_folder}\". Put your mod groups in here!\n")
        return

    with open(properties_file, 'r') as f:
        profile = "".join(f.readlines()).rstrip()

    print(f"Attempting to load the \"{profile}\" profile.")
    
    mod_grouper_folder_contents = os.listdir(input_mod_folder)
    mod_groups = [dir for dir in mod_grouper_folder_contents if os.path.isdir(input_mod_folder + "/" + dir) and dir != output_mod_folder and dir[0] != "."]

    if profile in mod_groups:
        shutil.rmtree(output_mod_folder)
        shutil.copytree(input_mod_folder + "/" + profile, output_mod_folder)
        print(f"Profile \"{profile}\" has been loaded!\n")
    else:
        print("Profile not found!\n")

def load_profiles():
    open("profiles.json", "a+").close()
    profiles_text = ""
    with open("profiles.json", "r") as f:
        profiles_text = f.read()
    return json.loads(profiles_text) if profiles_text != "" else {}

def export_mod_group(profile):
    profiles = load_profiles()
    installed_mods = [dir.name for dir in isaac_mods_folder.iterdir() if (isaac_mods_folder / dir).is_dir() and dir.name[0] != "."]
    profiles[profile] = [mod for mod in installed_mods if not "disable.it" in os.listdir(isaac_mods_folder / mod)]
    with open("profiles.json", "w+") as f:
        json.dump(profiles, f, indent=4)
        print(f"Exported enabled mods to {profile} profile successfully.\n")

def import_mod_group(profile):
    profiles = load_profiles()
    if not profile in profiles:
        print("Unknown profile, try again.\n")
        return
    installed_mods = [dir.name for dir in isaac_mods_folder.iterdir() if (isaac_mods_folder / dir).is_dir() and dir.name[0] != "."]
    enabled_mods = [mod for mod in installed_mods if not "disable.it" in os.listdir(isaac_mods_folder / mod)]
    for mod in installed_mods:
        #Enable disabled mods in the profile
        if mod in profiles[profile] and not mod in enabled_mods:
            if os.path.isfile(isaac_mods_folder / mod / "disable.it"):
                os.remove(isaac_mods_folder / mod / "disable.it")
        #Disable enabled mods not in the profile
        if not mod in profiles[profile] and mod in enabled_mods:
            try:
                with open(isaac_mods_folder / mod / "disable.it", "x"):
                    pass
            except FileExistsError:
                pass
    print(f"Imported enabled mods from {profile} profile successfully.\n")

def remove_mod_group(profile):
    profiles = load_profiles()
    if not profile in profiles:
        print("Unknown profile, try again.\n")
        return
    profiles.pop(profile)
    with open("profiles.json", "w+") as f:
        json.dump(profiles, f, indent=4)
        print(f"Removed {profile} profile successfully.\n")

if __name__ == "__main__":
    user_input = []
    print(f"isaac_mod_grouper v{version}")

    #TODO check that the mods folder loc is actually here
    if not os.path.isfile("properties.ini"):
        print("Please input your isaac mods folder.")
        path = input(">")
        with open("properties.ini", "w+") as f:
            f.write(path)

    with open("properties.ini", "r") as f:
        isaac_mods_folder = pathlib.Path(f.readline())
    if not os.path.isdir(isaac_mods_folder):
        print("Invalid isaac mods folder location! Try again..\n")
        os.remove("properties.ini")
        exit() #TODO do this better......

    print(f"Available commands: {command_list}\n")
    while user_input != "exit":
        user_input = input(">").split(" ")
        command = user_input[0]
        args = user_input[1:]
        if command == "help":
            if len(args) == 0:
                print("Use \"help <command>\" for help with a specific command.\n")
                print(f"Available commands: {command_list}\n")
            elif len(args) == 1:
                command_for_help = args[0]
                if command_for_help in command_info.keys():
                    print(command_info[command_for_help])
                else:
                    print(f"Unknown command \"{command_for_help}\"")
                    print(f"Available commands: {command_list}\n")
            else:
                print("Incorrect syntax, use \"help <command>\".\n")
        elif command == "exit":
            print("Goodbye.")
            sys.exit(0)
        elif command == "export":
            if len(args) == 1:
                mod_group_name = args[0]
                export_mod_group(mod_group_name)
            else:
                print("Incorrect syntax, use \"export <profile_name>\".\n")
        elif command == "import":
            if len(args) == 1:
                mod_group_name = args[0]
                import_mod_group(mod_group_name)
            else:
                print("Incorrect syntax, use \"import <profile_name>\".\n")
        elif command == "remove":
            if len(args) == 1:
                mod_group_name = args[0]
                remove_mod_group(mod_group_name)
            else:
                print("Incorrect syntax, use \"remove <profile_name>\".\n")
        elif command == "list":
            print(f"Profiles: {list(load_profiles().keys())}\n")
        else:
            print("Unknown command, please try again.\n")
    