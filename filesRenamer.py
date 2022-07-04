from classes import cmdArguments
from classes import directory
from classes import menu

import sys

def manageCmd() -> cmdArguments.CmdArgs:
    def validinput(cmd):
            if not cmd.isValidInputQty(1,1):
                if cmd.inputsQty() > 1:
                    print('🔴 - Only one input is required\n')
                else:
                    print('🔴 - One input is required\n')
                sys.exit()
            elif not cmd.inputs[0].isValidInputType('dir'):
                print('🔴 - Invalid input type. Please use a Directory as an input.\n')
                sys.exit()

    cmd = cmdArguments.CmdArgs()
    option_without_inputs = ['-h', '--help']
    print()
    if not cmd.isValidOptQty(1):
        print('🔴 - Only one option is permited\n')
        sys.exit()
    if cmd.optionsQty() != 0:
        for option in cmd.options:
            if not option.isValidOption('-h', '--help'):
                print('🔴 - Invalid option. Available options: [-h, --help].\n')
                sys.exit()
            elif not option.name in option_without_inputs:
                validinput(cmd)
    else:
        validinput(cmd)
    return cmd

def help():
    print('HELP')

def addtoNames(dirPath):
    print('Enter the text to rename the files insade the directory\n')
    text = input('Your text: ')
    print('\n')
    dir = directory.Directory(dirPath)

    for file in dir.files.values():
        new_name = f'{file.name}{text}'
        try:
            file.rename(new_name)
            print(f'🟢 - File renamed successfully to {file.name}{file.extension}')
        except OSError as e:
            print(f'🔴 - {e}')

def cmdMenu(input, option = ''):
    m = menu.CommandMenu()

    op1 = menu.Option('-h', lambda: help())
    op2 = menu.Option('--help', lambda: help())
    op3 = menu.Option('', lambda: addtoNames(input))

    m.addOptions(op1, op2, op3).ask(option)

def main():
    cmd = manageCmd()
    if cmd.inputsQty() == 0:
        cmdMenu('', cmd.options[0].name)
    elif cmd.optionsQty() == 0:
        cmdMenu(cmd.inputs[0].path)
    else:
        cmdMenu(cmd.inputs[0].path, cmd.options[0].name)

if __name__ == '__main__':
    main()