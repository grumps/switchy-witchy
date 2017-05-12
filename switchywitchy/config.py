import configparser
import os

package_path = os.path.dirname(__file__)


def dump_config(config):
    for section_name in config:
        print('Section:', section_name)
        section = config[section_name]
        print('  Options:', list(section.keys()))
        for name in section:
            print('  {} = {}'.format(name, section[name]))


def app_confs():
    parser_file = os.path.join(package_path, "stuff.ini")
    parser = configparser.ConfigParser()
    parser.read(parser_file)
    return parser
