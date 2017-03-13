import os
import mmap
from random import randint

commands = {0xff: ('STOP', 0),
            0x01: ('MV', 2),
            0x02: ('ADD', 2),
            0x03: ('INC', 1),
            0x10: ('JUMP', 1),
            0x11: ('CJUMP', 1),
            0x12: ('IFLESSEQ', 2),
            0x04: ('INP', 1),
            0x05: ('OUT', 1),
            0x00: ('VAR', 0),
            0x06: ('PRINT', 1)}

block_size = 4

def generateVariableName(count):
    return 'VAR_' + str(count), count + 1


def translateToAssembler(bin_file):
    # dictionary (address, name of variable)
    variables_count = 0
    variables = {}

    file_size = os.path.getsize(bin_file)
    file = os.open(bin_file, os.O_RDWR)
    file_in_memory = mmap.mmap(file, file_size, mmap.ACCESS_READ)

    lines_count = int(file_size / block_size)
    with open('new_fibonachi.code', 'w+') as code_file:
        for index in range(lines_count):
            command = file_in_memory[index * block_size]
            address = index * block_size
            first_arg = file_in_memory[index * block_size + 1]
            second_arg = file_in_memory[index * block_size + 3]
            if (commands[command][0] == 'VAR'):
                name, variables_count = generateVariableName(variables_count)
                variables[address] = name
                code_file.write('[' + str(address) + '] : ' + name + ' = ' + str(second_arg) + '\n')
            elif (commands[command][0] == "PRINT"):
                code_file.write(commands[command][0] + ' \'' + chr(second_arg) + '\'\n')
            elif (commands[command][0] == 'JUMP' or commands[command][0] == 'CJUMP'):
                code_file.write(commands[command][0] + ' ' + str(second_arg) + '\n')
            else:
                if (commands[command][1] == 0):
                    code_file.write(commands[command][0] + '\n')
                elif (commands[command][1] == 1):
                    code_file.write(commands[command][0] + ' ' + str(variables[second_arg]) + '\n')
                else:
                    code_file.write(commands[command][0] + ' ' + str(variables[first_arg]) + ' ' +
                                    str(variables[second_arg]) + '\n')


if __name__ == '__main__':
    bin_file = 'instructions.bin'
    translateToAssembler(bin_file)
