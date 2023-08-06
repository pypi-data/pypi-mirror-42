from . import fontcell_main as fm


def run(config_path):
    conf = str(config_path.split('file:')[1])
    fm.fontcell(conf)
    return

