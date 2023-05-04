import json
import argparse
import os.path

from models import Context, Parameter, Rule, Executor


def create_objects(json_data):
    """
    create all the objects that will be used in the program
    :param json_data: 
    """
    print('Ready to load the json...')
    data = json.loads(json_data)
    print('Json loaded successfully')
    print('Ready to create contexts...')
    create_context(data['contexts'])
    print('Contexts created successfully')
    print('Ready to create parameters...')
    create_parameter(data['parameters'])
    print('Parameters created successfully')
    print('Ready to create rules...')
    create_rule(data['rules'])
    print('Parameters created successfully')


def get_all_context(json_str):
    """
    fetch all the requried context name for launching
    :param json_str:
    :return:
    """
    data = json.loads(json_str)
    ret = []
    for context in data['contexts']:
        ret.append(context['name'])
    return ret


def config_args(json_dict, arg_tuple):
    """
    return args used to create object by referring to the loaded json
    :param json_dict:
    :param arg_tuple:
    :return:
    """
    args = {}
    for key, value in json_dict.items():
        # special case
        if key == 'param_type':
            if value == 'int':
                args[key] = int
            elif value == 'str':
                args[key] = str
            elif value == 'bool':
                args[key] = bool
            continue

        if key in arg_tuple:
            args[key] = value
    return args


def create_parameter(parameters):
    """
    create parameter objects
    :param parameters:
    """
    for parameter in parameters:
        args = config_args(parameter, ('ctx_name', 'param_type', 'ask_first', 'allowed_values'))
        Parameter(parameter['name'], **args)


def create_context(contexts):
    """
    create context objects
    :param contexts:
    """
    for context in contexts:
        name = context['name']
        args = config_args(context, ('initial_data', 'goals'))
        Context(name, **args)


def create_rule(rules):
    """
    create rule objects
    :param rules:
    """
    for rule in rules:
        args = config_args(rule, ('conditions', 'conclusions', 'cf'))
        Rule(**args)


def create_parser():
    """
    create parser by argparse
    :return:
    """
    parser = argparse.ArgumentParser(description="EMYCIN Configuration")
    parser.add_argument("--config", type=str, default='./organism.json', help="JSON file that defines the question")
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if not os.path.exists(args.config):
        print(f'config file not found: {args.config}')
        exit(0)
    print(f'Loading context, parameter, and rules from {args.config}...')
    json_str = open(args.config, 'r').read()
    print(f'Loading done successfully')
    create_objects(json_str)
    Executor.execute(get_all_context(json_str))
