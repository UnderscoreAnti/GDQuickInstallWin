import os


def create_config():

    appdata_dir = os.getenv('APPDATA') + "\\Godot\\app_userdata\\GDQuickInstall"

    if not os.path.exists(appdata_dir):
        os.mkdir(appdata_dir)

    new_config = open("settings.txt", 'w')

    download_folder = input("Please enter the Godot ZIP download location")
    install_folder = input("Please enter the installation location")

    print("Thank you! \n\nSaving...")

    config_info = download_folder + "\n" + install_folder
    new_config.write(config_info)
    new_config.close()


def get_config():

    settings = []
    config_dir = os.getenv('APPDATA') + "\\Godot\\app_userdata\\GDQuickInstall\\settings.txt"

    if os.path.exists(config_dir):
        config_file = open(config_dir)

    else:
        print("There was an error loading the config file...")
        create_config()
        return

    for line in config_file.readlines():
        settings.append(line)

    config_file.close()
    return settings


def change_config():
    con_set = get_config()

    if con_set:
        print("Using 1 or 2, please choose an option to edit:")
        choose_edit = input("1.) Downloads >> {0}\n2.) Installation >> {1}".format(con_set[0], con_set[1]))
        new_setting = input("Please enter the new directory:")

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


def get_godot_zip():
    pass


def move_godot_zip():
    pass


def delete_old_godot():
    pass


if __name__ == '__main__':
    create_config()
