import argparse
import logging
import sys
import os

def getTemplate() -> str:
    """
    reads the template file and returns its data
    Returns: str
    """
    data = ''
    try:
        f = open('./RefTemplate.xml', 'r')
        data = f.read()
        f.close()
        logging.log(logging.DEBUG, "Done reading file")
    except IOError as e:
        print('Error while reading file!', e)
        logging.log(logging.ERROR, "Traceback: %s" %(sys.exc_info()))
        exit(1)
    return data

def addToTemplate(reference : dict, template : str) -> str:
    '''
    adds the data of the reference to the template, and returns the reference XML
    returns: reference XML data
    '''
    logging.log(logging.DEBUG, 'Started parsing the template with data: %s' % (reference))
    template = template.replace('{NAME}', reference['refname'])
    template = template.replace('{PATH}', reference['dllpath'])

    if reference.get('version') != None:
        template = template.replace('{IS_VERSION}', 'TRUE')
        template = template.replace('{VERSION}', reference.get('version')) 
    else:
        template = template.replace('Version="{VERSION}"', '')
        template = template.replace('{IS_VERSION}', 'FALSE')

    if reference.get('keyToken') != None:
        template = template.replace('{TOKEN}', reference.get('keyToken'))
    else:
        template = template.replace('publicKeyToken="{TOKEN}"', '')
    if reference.get('arch'):
        template = template.replace('{PROC}', reference.get('arch'))
    else:
        template = template.replace('processorArchitecture="{PROC}"', '')
    if reference.get('culture'):
        template = template.replace('{CULTURE}', reference.get('culture'))
    else:
        template = template.replace('culture="{CULTURE}"', '')
    logging.log(logging.DEBUG, 'Done parsing')
    return template

def getArgs() -> dict:
    '''
    parese the cmd args
    Returns: dictionary of args
    '''
    args_dict = {}
    parser = argparse.ArgumentParser(description='Simple tool to add local referances to .csproj files')
    parser.add_argument('ProjPath', action='store', type=str, help='Path of the .csproj file')
    parser.add_argument('refname', action='store', type=str, help='Name for the refernce')
    parser.add_argument('dllpath', action='store', type=str, help='Reletive or absolute path of the dll file')
    parser.add_argument('-V', action='store', type=str, help='Version of the dll')
    parser.add_argument('-K', action='store', type=str, help='Public key token for dll')
    parser.add_argument('-A', action='store', type=str, help='Processor architecture for dll')
    parser.add_argument('-C', action='store', type=str, help='Dll culture')
    parser.add_argument('--V', '--verbose', action='store_true', help='Logging level', dest='log')
    args = parser.parse_args()
    if args.A:
        args_dict['arch'] = args.A
    if args.C:
        args_dict['culture'] = args.C
    if args.K:
        args_dict['keyToken'] = args.K
    if args.V:
        args_dict['version'] = args.V
    args_dict['refname'] = args.refname
    args_dict['dllpath'] = args.dllpath
    args_dict['csproj'] = args.ProjPath
    args_dict['log'] = args.log
    return args_dict


def add_ref_to_file(path: str, ref: str)->None:
    '''
    adds the ref to the .csproj file
    Returns: None
    '''
    file_data = ''
    with open(path, 'r') as file:
        for line in file.readlines():
            if '</Project>' in line:
                file_data += ref
            file_data += line
    
    with open(path, 'w') as file:
        file.write(file_data)

def main():
    args = getArgs()
    if args['log']:
        logging.getLogger().setLevel(logging.DEBUG)
    if not os.path.isfile(args['csproj']) or not os.path.isfile(args['dllpath']):
        print('Could not find the .dll or the .csproj given')
        exit(1)
    template = getTemplate()
    refrence = addToTemplate(args, template)
    add_ref_to_file(args['csproj'], refrence)
    

if __name__ == '__main__':
    main()