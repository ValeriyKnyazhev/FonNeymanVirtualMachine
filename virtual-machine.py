import os
import mmap
import struct

commands = {0xff: ('STOP', 0),
            0x01: ('MV', 2),
            0x02: ('ADD', 2),
            0x03: ('INC', 1),
            0x10: ('JUMP', 1),
            0x11: ('CJUMP', 1),
            0x12: ('IFLESSEQ', 2),
            0x04: ('INP', 1),
            0x05: ('OUT', 1),
            0x06: ('PRINT', 1)}

block_size = 4


def STOP(file_in_map, instruction_pointer, first_arg, second_arg):
    return False


def MV(file_in_map, instruction_pointer, first_arg, second_arg):
    file_in_map[first_arg:first_arg + block_size] = file_in_map[second_arg:second_arg + block_size]
    file_in_map[0:block_size] = struct.pack('>i', instruction_pointer + block_size)
    return True


def ADD(file_in_map, instruction_pointer, first_arg, second_arg):
    first_value = struct.unpack('>i', file_in_map[first_arg:first_arg + block_size])[0]
    second_value = struct.unpack('>i', file_in_map[second_arg:second_arg + block_size])[0]
    file_in_map[first_arg:first_arg + block_size] = struct.pack('>i', first_value + second_value)
    file_in_map[0:block_size] = struct.pack('>i', instruction_pointer + block_size)
    return True


def INC(file_in_map, instruction_pointer, first_arg, second_arg):
    file_in_map[second_arg:second_arg + block_size] = \
        struct.pack('>i', struct.unpack('>i', file_in_map[second_arg:second_arg + block_size])[0] + 1)
    file_in_map[0:block_size] = struct.pack('>i', instruction_pointer + block_size)
    return True


def JUMP(file_in_map, instruction_pointer, first_arg, second_arg):
    file_in_map[0:block_size] = struct.pack('>i', second_arg)
    return True


def CJUMP(file_in_map, instruction_pointer, first_arg, second_arg):
    if (struct.unpack('>i', file_in_map[block_size:block_size + block_size])[0]):
        file_in_map[0:block_size] = struct.pack('>i', second_arg)
    else:
        file_in_map[0:block_size] = struct.pack('>i', instruction_pointer + block_size)
    return True


def IFLESSEQ(file_in_map, instruction_pointer, first_arg, second_arg):
    if (struct.unpack('>i', file_in_map[first_arg:first_arg + block_size])[0] <=
            struct.unpack('>i', file_in_map[second_arg:second_arg + block_size])[0]):
        file_in_map[block_size:block_size + block_size] = struct.pack('>i', 1)
    else:
        file_in_map[block_size:block_size + block_size] = struct.pack('>i', 0)
    file_in_map[0:block_size] = struct.pack('>i', instruction_pointer + block_size)
    return True


def INP(file_in_map, instruction_pointer, first_arg, second_arg):
    value = int(input())
    file_in_map[second_arg:second_arg + block_size] = struct.pack('>i', value)
    file_in_map[0:block_size] = struct.pack('>i', instruction_pointer + block_size)
    return True


def OUT(file_in_map, instruction_pointer, first_arg, second_arg):
    print(struct.unpack('>i', file_in_map[second_arg:second_arg + block_size])[0])
    file_in_map[0:block_size] = struct.pack('>i', instruction_pointer + block_size)
    return True

def PRINT(file_in_map, instruction_pointer, first_arg, second_arg):
    print(chr(second_arg), end='')
    file_in_map[0:block_size] = struct.pack('>i', instruction_pointer + block_size)
    return True

def execute_code(file_in_map):
    is_running = True

    while is_running:
        instruction_pointer = struct.unpack('>i', file_in_map[0: block_size])[0]
        function = commands[file_in_map[instruction_pointer]][0]
        first_arg = file_in_map[instruction_pointer + 1]
        second_arg = file_in_map[instruction_pointer + 3]
        # print('[DEBUG]', str(instruction_pointer), str(function), str(first_arg), str(second_arg), sep=' ')
        is_running = globals()[function](file_in_map, instruction_pointer, first_arg, second_arg)


if __name__ == '__main__':
    bin_file = 'instructions.bin'
    file_size = os.path.getsize(bin_file)
    file = os.open(bin_file, os.O_RDWR)
    file_in_memory = mmap.mmap(file, file_size, mmap.ACCESS_WRITE)

    execute_code(file_in_memory)

    file_in_memory.close()
