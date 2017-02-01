from getpass import getpass
from pathlib import Path
from binascii import hexlify
import os
import sys
import shutil

env_file = Path(".env")


def prompt(text):
    response = input(text + " [y/N]")
    if response == "y":
        return True
    else:
        return False


def setup():
    if env_file.exists():
        print("File .env already exists!")
        if prompt("Would you like to create a new one?"):
            env_file.unlink()
            env_file.touch()
        else:
            sys.exit(0)

    prod = prompt("Is this a production environment?")
    node_env = "production" if prod else "development"

    mailer_user = input("Enter a gmail mailer username: ")
    mailer_password = getpass("Enter a gmail mailer password: ")
    if not (mailer_user or mailer_password):
        print("WARNING: both a mailer username and password is needed to send emails")

    mysql_root_pw = getpass("Enter a password for the database. Defaults to 'banana': ") or "banana"

    host_media_dir = Path(
        input("Enter a location for media directory relative to the root directory. "
              "Defaults to '/media/lecture_viewer': ") or "/media/lecture_viewer"
    ).expanduser()
    if not (host_media_dir.exists() and host_media_dir.is_dir()):
        print("{} not found, creating directory".format(host_media_dir))
        os.makedirs(host_media_dir)

    signing_key = input("Enter a custom signing key (not suggested). Defaults to 64 character random string: ")
    if not signing_key:
        signing_key = hexlify(os.urandom(32)).decode()

    school_logo = host_media_dir.joinpath(Path(
        input("Enter a location for school logo to previously provided media directory {}/"
              .format(host_media_dir))).expanduser())
    if school_logo.is_file():
        shutil.copy((str(school_logo)), "./lv-client/client/src/images/logo.png")
    else:
        print("WARNING: school logo file does not exist")

    users_csv_path = Path(
        input("Enter a location for users csv path relative to previously provided media directory {}/"
              .format(host_media_dir))).expanduser()
    if not host_media_dir.joinpath(users_csv_path).is_file():
        print("WARNING: users csv file does not exist")
        users_csv_path = ""

    client_url = (input("Enter the host url for the Lecture Viewer. Defaults to 'http://localhost': ")
                  or "http://localhost")

    print("Generating .env file")
    env_file.write_text("""SIGNING_KEY={signing_key}
NODE_ENV={node_env}

# lv-db
MYSQL_HOSTNAME=lv-db
MYSQL_ROOT_PASSWORD={mysql_root_pw}
MYSQL_DATABASE=lecture_viewer
MYSQL_USER=root

# lv-media
MEDIA_HOSTNAME=lv-media
HOST_MEDIA_DIR={host_media_dir}
MEDIA_SERVER_PORT=5000
USERS_CSV_PATH={users_csv_path}

# lv-server
SERVER_HOSTNAME=lv-server
API_VERSION=v1
MAILER_USER={mailer_user}
MAILER_PASSWORD={mailer_password}

# lv-client
CLIENT_HOSTNAME=lv-client
CLIENT_BASE_URL={client_url}
SCHOOL_LOGO_PATH={school_logo}
""".format(signing_key=signing_key, node_env=node_env, mysql_root_pw=mysql_root_pw, host_media_dir=host_media_dir,
           users_csv_path=users_csv_path, mailer_user=mailer_user, mailer_password=mailer_password,
           client_url=client_url, school_logo=school_logo))

    if not prod and not Path(host_media_dir, "F16").exists():
        os.system("sudo mkdir -p {}/F16".format(host_media_dir))