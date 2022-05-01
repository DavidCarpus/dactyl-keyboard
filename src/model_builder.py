import os
import copy
import importlib
from generate_configuration import *


base = shape_config

config_options = [
    {
        'name': '{}', 'vars': ['ball_side'], # set ball side to both, other half can come from other renders
        'vals': ['right'],
        'val_names': ['']
    },
    {
        'name': '{}x{}', 'vars': ['nrows', 'ncols'],
        'vals':[(4, 6)],
    },
    {
        'name': '{}PLT', 'vars': ['plate_style'],
        'vals': ['HS_NUB'],
        # 'vals': ['NUB', 'NOTCH', 'HS_NUB', 'HS_NOTCH'],
    },
    {
        'name': '{}TMB', 'vars': ['thumb_style'],
         'vals': ['TRACKBALL_ORBYL'],
    #    'vals': ['DEFAULT', 'MINIDOX', 'TRACKBALL_ORBYL'],
        'val_names': ['DEF', 'MDOX', 'ORBY']
        # 'vals': ['DEFAULT', 'MINI', 'CARBONFET', 'MINIDOX'],
        # 'val_names': ['DEF', 'MINI', 'CF', 'MDOX']
    },
    {
        'name': '{}', 'vars': ['oled_mount_type'],
        'vals': ['CLIP', 'NONE'],
        'val_names': ['OLED', 'NOLED']
    },
    {
        'name': '{}CTRL', 'vars': ['controller_mount_type'],
        # 'vals': ['EXTERNAL', 'RJ9_USB_WALL'],
         'vals': ['EXTERNAL'],
       'val_names': ['EXT', 'DEF'],
    },
]


def create_config(config_options):
    configurations = [{
        'config_name': 'DM',
        'save_dir': 'DM',
    }]
    config_options = copy.deepcopy(config_options)
    for opt in config_options:
        new_configurations = []
        for config in configurations:
            # config['vals'] = []
            for i_vals, vals in enumerate(opt['vals']):
                temp_opt = copy.deepcopy(opt)
                new_config = copy.deepcopy(config)
                if len(temp_opt['vars']) == 1:
                    vals=[vals]
                    if 'val_names' in temp_opt:
                        temp_opt['val_names'][i_vals] = [temp_opt['val_names'][i_vals]]
                for i_val, val in enumerate(vals):
                    new_config[opt['vars'][i_val]] = val


                if 'val_names' in temp_opt:
                    n_input = temp_opt['val_names'][i_vals]
                else:
                    n_input = vals

                name_ext = temp_opt['name'].format(*n_input)
                if not name_ext == '':
                    new_config['config_name'] += "_" + name_ext
                new_config['save_dir'] = new_config['config_name']
                new_configurations.append(new_config)
        configurations = new_configurations

    return configurations



def build_release(base, configurations, engines=('solid', 'cadquery')):
    init = True
    for config in configurations:
        shape_config = copy.deepcopy(base)
        for item in config:
            shape_config[item] = config[item]
    
        for engine in engines:
            shape_config['ENGINE'] = engine
            with open('run_config.json', mode='w') as fid:
                json.dump(shape_config, fid, indent=4)
    
            if init:
                import dactyl_manuform as dactyl_manuform
                dactyl_manuform.run()
                init = False
            else:
                importlib.reload(dactyl_manuform)
                dactyl_manuform.run()

if __name__ == '__main__':
    configurations = create_config(config_options)

    # ENGINES = ['solid', 'cadquery']
    ENGINES = ['solid']

    build_release(base, configurations, ENGINES)
