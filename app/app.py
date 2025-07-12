import sys
import uuid
import logging
import json


LOGFILE = "/var/logs/app/app.log"
CONFIG_FILE = "/var/config/config.json"
FLOW = "xtls-rprx-vision"
PUBLIC_KEY = "/var/config/public.key"
PRIVATE_KEY = "/var/config/private.key"
IP_ADDRESS = "/var/config/address.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    filename=LOGFILE
)
logger = logging.getLogger(__name__)

def main(args):
    if (len(args) < 2):
        print("App is up and running.")
        put_private_key_to_config()
    for i, j in enumerate(args[1:]):
        if j == "-n" or i == "--new_user":
            new_uuid = generate_uuid()
            logger.info(f"New user uuid: {new_uuid}")
            add_client_to_config(new_uuid)
            try:
                name = args[i+2]
            except IndexError:
                name = "jpVPN"
            print(generate_link(new_uuid, get_short_key(CONFIG_FILE), name))
            

def generate_uuid():
    return str(uuid.uuid4())

def add_client_to_config(new_uuid, config_file=CONFIG_FILE, flow=FLOW):
    as_json = get_json_config(config_file)
    add_client_to_json(new_uuid, flow, as_json)
    write_json_config(as_json, config_file)
    logger.info(f"Client {new_uuid} added to config file")

def get_json_config(file):
    with open(file, "r") as f:
        return json.load(f)

def add_client_to_json(uuid, flow, json_obj):
    clients_list = json_obj["inbounds"][0]["settings"]["clients"]
    new_client = {"id":uuid, "flow":flow}
    clients_list.append(new_client)
    return json_obj
    
def write_json_config(as_json, file):
    with open(file, "w") as f:
        f.write(json.dumps(as_json, indent=4))

def generate_link(client_uuid, short_key, name):
    link = f"vless://{client_uuid}@{get_vps_address()}:443"
    link += f"?encryption=none"
    link += f"&flow={FLOW}"
    link += f"&security=reality"
    link += f"&sni=www.cloudflare.com"
    link += f"&fp=chrome"
    link += f"&pbk={get_public_key()}"
    link += f"&sid={short_key}"
    link += f"&type=tcp"
    link += f"#{name}"
    logger.info(f"Link {name} for {client_uuid} generated: {link}")
    return link

def put_private_key_to_config():
    json_obj = get_json_config(CONFIG_FILE)
    json_obj["inbounds"][0]["streamSettings"]["realitySettings"]["privateKey"] = get_private_key()
    write_json_config(json_obj, CONFIG_FILE)
    logger.info("Private key added to config.json")

def get_private_key():
    try:
        with open(PRIVATE_KEY, "r") as f:
            return f.readline().strip()
    except FileNotFoundError as e:
        print(f"Error! {e}")
        logger.error(e.with_traceback())

def get_public_key():
    try:
        with open(PUBLIC_KEY, "r") as f:
            return f.readline().strip()
    except FileNotFoundError as e:
        print(f"Error! {e}")
        logger.error(e.with_traceback())

def get_short_key(file):
    json_obj = get_json_config(file)
    return json_obj["inbounds"][0]["streamSettings"]["realitySettings"]["shortIds"][0]

def get_vps_address():
    with open(IP_ADDRESS, "r") as f:
        return f.readline().strip()


if __name__ == "__main__":
    main(sys.argv)