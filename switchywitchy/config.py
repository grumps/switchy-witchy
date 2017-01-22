import configparser



def dump_config(config):
    for section_name in parser:
        print('Section:', section_name)
        section = parser[section_name]
        print('  Options:', list(section.keys()))
        for name in section:
            print('  {} = {}'.format(name, section[name]))


def app_confs():
    parser = configparser.ConfigParser()
    parser.read("stuff.ini")
    return parser
