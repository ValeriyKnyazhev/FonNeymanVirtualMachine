import sys
import struct

commands = {'STOP': (0xff, 0),
            'MV': (0x01, 2),
            'ADD': (0x02, 2),
            'INC': (0x03, 1),
            'JUMP': (0x10, 1),
            'CJUMP': (0x11, 1),
            'IFLESSEQ': (0x12, 2),
            'INP': (0x04, 1),
            'OUT': (0x05, 1)}

def getAddress(str):
    return int(str[str.find('[') + 1: str.find(']')])

def getName(str):
    return str[:str.find('=')].strip()

def getValue(str):
    return int(str[str.find('=') + 1:].strip())

def translateToBinary(code_lines):
    with open('instructions.bin', 'wb+') as code_file:
        # dictionary (name of variable, address)
        variables = {}

        for index in range(len(code_lines)):
            print('[DEBUG] ' + str(index + 1) + ' string of code')
            colon_index = code_lines[index].find(':')
            if (colon_index != -1):
                print('[DEBUG] it is variable')
                address = getAddress(code_lines[index][:colon_index])
                name = getName(code_lines[index][colon_index + 1:])
                value = getValue(code_lines[index][colon_index + 1:])
                variables[name] = address
                code_file.write((struct.pack(">i", value)))
            else:
                print('[DEBUG] it is instruction')
                tokens = code_lines[index].strip().split(' ')

                instruction_code = [commands[tokens[0]][0], 0, 0, 0]

                print('[DEBUG] ' + str(tokens[0]))
                if (commands[tokens[0]][1] == 1):
                    if variables.get(tokens[1]) is None:
                        instruction_code[3] = int(tokens[1])
                    else:
                        instruction_code[3] = variables[tokens[1]]
                else:
                    for i in range(1, len(tokens)):
                        if variables.get(tokens[i]) is None:
                            if tokens[i].isdigit():
                                instruction_code[2 * i - 1] = int(tokens[i])
                            else:
                                print('ERROR: address is not a number')
                                sys.exit(-1)
                        else:
                            instruction_code[2 * i - 1] = variables[tokens[i]]


                print('[DEBUG] ' + str(instruction_code))
                code_file.write(bytearray(instruction_code))

        print('[DEBUG] ' + str(variables))


if __name__ == '__main__':

    code_lines = []
    with open('fibonachi.code') as input_file:
        code_lines = input_file.readlines()
    translateToBinary(code_lines)

