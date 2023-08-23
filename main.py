import os
import stat
import winshell
import shutil
import win32com.client
import zipfile as zf

# Copyright underscoreAnti (c) 2023
# Run with admin rights

## Tested with Godot Mono, Windows 10, GD ver 3.5+
## Move freshly downlooaded GD zip files to your chosen destination
## Create shortcuts with EASE
## Please let me know if you find any issues.


def create_config():
    appdata_dir = os.getenv('APPDATA') + r"\Godot\app_userdata\GDQuickInstall"

    if not os.path.exists(appdata_dir):
        os.mkdir(appdata_dir)

    new_config = open(appdata_dir + r"\settings.txt", 'w')

    download_folder = input("Please enter the Godot ZIP download location\n:) >>  ")
    install_folder = input("Please enter the installation location\n:) >>  ")
    shortcut_folder = input("Please enter the desired shortcut location (hit 'enter' to use the desktop)\n:) >>  ")

    print("Thank you! \n\nChecking for directories...")

    check1 = False
    check2 = False
    check3 = False

    if os.path.exists(download_folder):
        check1 = True

    if os.path.exists(install_folder):
        check2 = True

    if os.path.exists(shortcut_folder) or shortcut_folder == "":
        check3 = True

    if check1 and check2 and check3:
        print("Entries are valid! Saving...\n")

    else:
        print("One or more of the entries were not valid. Please try again. Aborting process...")
        create_config()

    if shortcut_folder == "":
        shortcut_folder = winshell.desktop()

    config_info = download_folder + "\n" + install_folder + "\n" + shortcut_folder
    new_config.write(config_info)
    new_config.close()

    new_command()


def get_config():
    settings = []
    config_dir = os.getenv('APPDATA') + r"\Godot\app_userdata\GDQuickInstall\settings.txt"

    if os.path.exists(config_dir):
        config_file = open(config_dir, "r")
    else:
        print("There was an error loading the config file...")
        create_config()
        return

    # Parse the file to make the contents usable.
    for line in config_file.readlines():
        raw_line = repr(line)[1:-1]
        raw_line = raw_line.replace(r"\\", r"'\'"[1:-1])

        if r"\n" in raw_line:
            raw_line = raw_line.removesuffix(r"\n")

        settings.append(raw_line)

    config_file.close()
    return settings


def change_config():
    con_set = get_config()

    if con_set:
        print("Using 1, 2, or 3, please choose an option to edit:")
        choose_edit = input("1.) Downloads >> {0}\n2.) Installation >> {1}\n".format(con_set[0], con_set[1]) +
                            "3.) Shortcut >> {0}\n:) >>  ".format(con_set[2]))
        new_setting = input("Please enter the new directory:\n:) >>  ")
    else:
        print("This really shouldn't happen please dear lord don't let this happen")

    if choose_edit == '1':
        con_set[0] = new_setting
    elif choose_edit == '2':
        con_set[1] = new_setting
    elif choose_edit == '3':
        con_set[2] = new_setting
    else:
        print("Please enter a valid option.")
        change_config()

    print("Saving...")

    config_dir = os.getenv('APPDATA') + "\\Godot\\app_userdata\\GDQuickInstall\\settings.txt"
    config_file = open(config_dir, "w")

    config_file.write(con_set[0] + "\n" + con_set[1] + "\n" + con_set[2])
    config_file.close()

    print("Config has been saved!\n")
    new_command()


def delete_old_godot():
    settings = get_config()
    contents = os.listdir(settings[1])

    # Windows is giving me a stupid amount of problems with this code. It SHOULD work.
    if contents and os.name != 'nt':
        for tent in contents:
            full = os.path.join(settings[1], tent)
            os.chmod(settings[1], stat.S_IWRITE)
            os.remove(full)

    # Destroying the universe, beginning anew. Yotta, yotta.
    elif contents and os.name == 'nt':
        shutil.rmtree(settings[1], ignore_errors=True)

    os.mkdir(settings[1])


def create_engine_shortcut():
    settings = get_config()
    shortcut_path = settings[2]

    out_path = os.path.join(shortcut_path, 'Godot Engine.lnk')
    temp = os.listdir(settings[1])
    tar = ""

    for ent in temp:
        if ent.endswith(".exe") and "_console" not in ent:
            tar = ent
        else:
            pass

    exec = os.path.join(settings[1], tar)

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(out_path)
    shortcut.Targetpath = exec
    shortcut.IconLocation = exec

    shortcut.save()
    print("Shortcut has been created!\n")

    new_command()


def get_godot_zip(removable=[]):
    settings = get_config()

    size_check = []

    contents = os.listdir(settings[0])
    for tent in contents:
        if "Godot_v" in tent and tent not in removable and tent not in size_check and tent.endswith(".zip"):
            size_check.append(tent)

    newest_version = ""
    for vers in size_check:
        if newest_version == "":
            newest_version = vers
        else:
            if newest_version < vers:
                newest_version = vers

    return newest_version, removable


def copy_util(src, dst):
    files = os.listdir(src)

    for file in files:
        try:
            temp_src = os.path.join(src, file)
            temp_dst = os.path.join(dst, file)
            shutil.copy2(temp_src, temp_dst)

        except FileNotFoundError:
            shutil.copytree(temp_src, temp_dst)

        except PermissionError:
            shutil.copytree(temp_src, temp_dst)


def install_godot_files(curr, settings):
    print("Installing...")

    if os.listdir(settings[1]):
        delete_old_godot()

    elif not os.path.exists(settings[1]):
        os.mkdir(settings[1])

    with zf.ZipFile("{0}\\{1}".format(settings[0], curr), 'r') as zip_obj:
        zip_obj.extractall(settings[0])

    temp_dir = os.path.join(settings[0], curr.removesuffix(".zip"))

    copy_util(temp_dir, settings[1])

    shutil.rmtree(temp_dir)
    og_zip = os.path.join(settings[0], curr)
    os.remove(og_zip)

    print("Installed!\n")

    new_command()


def print_command_list():
    commands_help = {
        "--c": "Prints the command list and a brief description of what the command does.",
        "--create-cfg": "Creates a new config file. Execute this command if this is your first time using this script.",
        "--change-cfg": "Change the config file. Please only execute this if a config file already exists.",
        "--install-gd": "Begin the installation Godot installation process.",
        "--delete-gd": "Delete the current installation of Godot. Please only execute this if an"
                      + " installation already exists",
        "--create-stct": "Creates a shortcut in the specified directory",
        "--delete-data": "Deletes the config directory for this script.",
        "--clear": "Clears the screen. Now supports Windows!",
        "--q": "Quits the program.",
    }

    print("Commands:")
    for key in commands_help:
        print(key, commands_help[key])

    print("\n")
    new_command()


def start_installation():
    current_version, removable = get_godot_zip()
    confirm_installation(current_version, removable)


def confirm_installation(curr, rem):
    if curr == "":
        input("No version to install, please download a copy and try again...\n:) >>  ")
        return

    current_version_check = input("Use version '{0}' ? ('y' = yes, 'n' = no)\n:) >>  ".format(curr))

    if current_version_check == 'y':
        install_godot_files(curr, get_config())
    elif current_version_check == 'n':
        rem.append(curr)
        curr, rem = get_godot_zip(rem)
        confirm_installation(curr, rem)
    else:
        print("Invalid entry, aborting and attempting operation again...\n")
        start_installation()


def delete_installation():
    settings = get_config()
    shutil.rmtree(settings[1], ignore_errors=True)
    print("Godot Installation has been deleted!\n")

    new_command()


def delete_config_data():
    shutil.rmtree(os.getenv('APPDATA') + r"\Godot\app_userdata\GDQuickInstall", ignore_errors=True)
    print("Config data has been deleted!\n")

    new_command()


def clear_screen():
    if os.name == "nt":
        os.system('cls')

    else:
        os.system('clear')

    new_command()


def get_commands():
    out_dict = {
        "--c": print_command_list,
        "--create-cfg": create_config,
        "--change-cfg": change_config,
        "--install-gd": start_installation,
        "--delete-gd": delete_installation,
        "--clear": clear_screen,
        "--delete-data": delete_config_data,
        "--create-stct": create_engine_shortcut,
        "--q": quit
    }

    return out_dict


def new_command():
    comm_dict = get_commands()
    cmnd = input(";) >>  ")

    if cmnd in comm_dict:
        comm_dict[cmnd]()

    else:
        print("Please enter a valid command. '--c' will show you the command list.\n")
        new_command()


if __name__ == '__main__':
    print("Hello!")
    new_command()
