import os, sys


def get_config():
    """Calls the load configuration method and checks for cml args"""
    if len(sys.argv) < 2:
        print("Missing Configuration Argument")
        sys.exit(1)

    elif len(sys.argv) > 2:
        print("Too many arguments")
        sys.exit(1)

    else:
        filename = sys.argv[1]

    #parse config
    config, message = parse_config(filename)

    #config invalid
    if config == -1:
        print(message)
        sys.exit(1)

    return config


def parse_config(filename):
    """Parse a confiugration file and returns a dictionary of key value fields"""

    config_dict = {
        "staticfiles": None,
        "cgibin": None,
        "port": None,
        "exec": None
    }

    if not os.path.exists(filename):
        return -1, "Unable To Load Configuration File"

    try:
        with open(filename, "r") as f:
            content = f.readlines()

            for ln in content:
                try:
                    key_pair = ln.strip().split("=")

                    #missing either key or value field
                    if not key_pair[0] or not key_pair[1]:
                        raise IndexError

                    if key_pair[0] in config_dict:
                        config_dict[key_pair[0]] = key_pair[1]
                    #unknown key
                    else:
                        return -1, f"Invalid key: {ln}"

                except IndexError:
                    return -1, f"Missing field on line: {ln}"

            # check that all fields have been set
            for key, val in config_dict.items():
                if val == None:
                    return -1, f"Missing Field From Configuration File"

            return config_dict, None

    except OSError:
        return -1, "Unable To Load Configuration File"

    return -1, f"Unspecified error parsing configuration file {filename}"
