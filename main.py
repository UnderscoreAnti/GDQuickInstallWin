import os
import zipfile as zf


def create_config():
    appdata_dir = os.getenv('APPDATA') + r"\Godot\app_userdata\GDQuickInstall"

    if not os.path.exists(appdata_dir):
        os.mkdir(appdata_dir)

    new_config = open(appdata_dir + r"\settings.txt", 'w')

    download_folder = input("Please enter the Godot ZIP download location\n")
    install_folder = input("Please enter the installation location\n")

    print("Thank you! \n\nSaving...")

    config_info = download_folder + "\n" + install_folder
    new_config.write(config_info)
    new_config.close()


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
        print("Using 1 or 2, please choose an option to edit:")
        choose_edit = input("1.) Downloads >> {0}\n2.) Installation >> {1}\n".format(con_set[0], con_set[1]))
        new_setting = input("Please enter the new directory:\n")
    else:
        print("This really shouldn't happen please dear lord don't let this happen")

    if choose_edit == '1':
        con_set[0] = new_setting
    elif choose_edit == '2':
        con_set[1] = new_setting
    else:
        print("Please enter a valid option.")
        change_config()

    config_dir = os.getenv('APPDATA') + "\\Godot\\app_userdata\\GDQuickInstall\\settings.txt"
    config_file = open(config_dir)

    config_file.write(con_set[0] + "\n" + con_set[1])
    config_file.close()


def get_commands():
    out_dict = {
        "-c": print_command_list(),
        "-create_cfg": create_config(),
        "-change_cfg": change_config(),
        "-install_gd": start_installation(),
        "-delete_gd": delete_installation(),
    }

    return out_dict


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


def move_godot_zip(curr, settings):
    print("Installing...")
    with zf.ZipFile("{0}\\{1}".format(settings[0], curr), 'r') as zip_obj:
        zip_obj.extractall(settings[1])

    print("Installed!")


def delete_old_godot():
    settings = get_config()
    # 


def print_command_list():
    commands_dict = get_commands()

    print("Commands:")
    for key in commands_dict.keys():
        print(key)

    print("\n")


def start_installation():
    current_version, removable = get_godot_zip()
    confirm_installation(current_version, removable)


def check_installation():
    pass


def confirm_installation(curr, rem):
    if curr == "":
        input("No version to install, please download a copy and try again...\n")
        return

    current_version_check = input("Use version '{0}' ? ('y' = yes, 'n' = no)\n".format(curr))

    if current_version_check == 'y':
        move_godot_zip(curr, get_config())
    elif current_version_check == 'n':
        rem.append(curr)
        curr, rem = get_godot_zip(rem)
        confirm_installation(curr, rem)
    else:
        print("Invalid entry, aborting and attempting operation again...")
        start_installation()


def delete_installation():
    pass


def new_command():
    commands_dict = get_commands()

    cmnd = input("Hello!\n")

    if cmnd in commands_dict:
        commands_dict[cmnd]

    else:
        print("Please enter a valid command. '-c' will show you the command list.")
        new_command()


if __name__ == '__main__':
    start_installation()
