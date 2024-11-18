#!/usr/bin/python3

import struct

with open('src/main.elf', 'rb') as f:
    data = f.read()

elf_header_fields = [
    ['magic',0x00,'bbbb'],
    ['class',0x04,'b'],
    ['data',0x05,'b'],
    ['version',0x06,'b'],
    ['osabi',0x07,'b'],
    ['abiversion',0x08,'b'],
    ['type',0x10,'<H'],
    ['machine',0x12,'<H'],
    ['version',0x14,'b'],
    ['process entry point',0x18,'<I'],
    ['program header table offset',0x1C,'<I'],
    ['section header table offset',0x20,'<I'],
    ['flags',0x24,'<I'],
    ['ehsize',0x28,'<H'],
    ['program header table size',0x2A,'<H'],
    ['program header table entries',0x2C,'<H'],
    ['section header table size',0x2E,'<H'],
    ['section header table entries',0x30,'<H'],
    ['shstrndx',0x32,'<H'],
#    ['',,''],
]

program_header_fields = [
    ['type',0x00,'<I'],
    ['offset of segment in file image',0x04,'<I'],
    ['virtual address',0x08,'<I'],
    ['physical address',0x0C,'<I'],
    ['size of segment in file image',0x10,'<I'],
    ['size of segment in memory',0x14,'<I'],
    ['flags',0x18,'<I'],
    ['alignment',0x1C,'<I'],
]

section_header_fields = [
    ['offset of section name',0x00,'<I'],
    ['type',0x04,'<I'],
    ['flags',0x08,'<I'],
    ['virtual address of the section in memory',0x0C,'<I'],
    ['offset of the section in the file image',0x10,'<I'],
    ['size of the segment',0x14,'<I'],
    ['section index',0x18,'<I'],
    ['section info',0x1C,'<I'],
    ['alignment',0x20,'<I'],
    ['size of entries in the section',0x24,'<I'],
]

elf_header = {}
for field in elf_header_fields:
    unpacked = struct.unpack(field[2], data[field[1]:(field[1]+struct.calcsize(field[2]))])

    elf_header[field[0]] = unpacked[0]


program_headers = []
for i in range(0,elf_header['program header table entries']):
    addr = elf_header['program header table offset'] + i*elf_header['program header table size']

    program_header = {}
    for field in program_header_fields:
        start = addr + field[1]
        end = addr + field[1] + struct.calcsize(field[2])
        unpacked = struct.unpack(field[2], data[start:end])
        program_header[field[0]] = unpacked[0]
    program_headers.append(program_header)

section_headers = []
for i in range(0,elf_header['section header table entries']):
    addr = elf_header['section header table offset'] + i*elf_header['section header table size']

    section_header = {}
    for field in section_header_fields:
        start = addr + field[1]
        end = addr + field[1] + struct.calcsize(field[2])
        unpacked = struct.unpack(field[2], data[start:end])
        section_header[field[0]] = unpacked[0]
    section_headers.append(section_header)

print('elf_header:')
for key,val in elf_header.items():
    print('   ', key, ':', hex(val))

#index = 0
#for program_header in program_headers:
#    print('program_header:', hex(index))
#    for key,val in program_header.items():
#        print('   ', key, ':', hex(val))
#    print('')
#    index += 1

shstrndx_header = section_headers[elf_header['shstrndx']]

def get_shstring(sh_name):
    address = shstrndx_header['offset of the section in the file image'] + sh_name

    val = bytearray()

    while True:
        n = data[address]
        if n == 0:
            return val
        val.append(n)
        address += 1

#index = 0
#for section_header in section_headers:
#    print('section_header:', hex(index), get_shstring(section_header['offset of section name']))
#    for key,val in section_header.items():
#        print('   ', key, ':', hex(val))
#    print('')
#    index += 1

def decode_block(block_data, block_address):
    image_def_sections = [
        {
            'offset':0,
            'bits':4,
            'vals':{
                0:'IMAGE_TYPE_INVALID',
                1:'IMAGE_TYPE_EXE',
                2:'IMAGE_TYPE_DATA',
            }
        },
        {
            'offset':4,
            'bits':2,
            'vals':{
                0:'EXE_SECURITY_UNSPECIFIED',
                1:'EXE_SECURITY_NS',
                2:'EXE_SECURITY_S',
            }
        },
        {
            'offset':8,
            'bits':3,
            'vals':{
                0:'EXE_CPU_ARM',
                1:'EXE_CPU_RISCV',
            }
        },
        {
            'offset':12,
            'bits':3,
            'vals':{
                0:'EXE_CHIP_RP2040',
                1:'EXE_CHIP_RP2350',
            }
        },
        {
            'offset':15,
            'bits':1,
            'vals':{
                0:'TBYB unset',
                1:'TBYB set',
            }
        },
    ]

    decoded = []

    i = 0
    while True:
        val = struct.unpack('<I', block_data[i:i+4])[0]
        vals = list(struct.unpack('<BBBB', block_data[i:i+4]))

        if val == 0xffffded3:
            decoded.append({'data':vals, 'type':'start marker'})
        elif val == 0xab123579:
            decoded.append({'data':vals, 'type':'end marker'})
        elif decoded[-1]['type'] == 'last item':
            pointer = (block_address+val)%(1<<32)
            decoded.append({'data':vals, 'type':f"pointer to next block, address:{pointer:08x}"})
        elif vals[0] == 0x42:
            flags = []

            image_type_flags_data = (vals[3]<<8) + vals[2]
            for image_def_section in image_def_sections:
                section_data = (image_type_flags_data>>image_def_section['offset'])&((1<<image_def_section['bits']) - 1)
                if section_data in image_def_section['vals']:
                    flags.append(image_def_section['vals'][section_data])

            decoded.append({'data':vals, 'type':f"Image def, flags:{flags}"})
        elif vals[0] == 0xFE:
            decoded.append({'data':vals, 'type':'Ignored item'})
        elif vals[0] == 0xFF:
            decoded.append({'data':vals, 'type':'last item'})
        else:
            decoded.append({'data':vals, 'type':'unknown'})
    #000001fe, ['0xfe', '0x1', '0x0', '0x0']
    #000001ff, ['0xff', '0x1', '0x0', '0x0']
    #ffffe9b4, ['0xb4', '0xe9', '0xff', '0xff']

        i+=4

        if val == 0xab123579:
            return decoded


# Look for IMAGE_DEF blocks in the program memory
index = 0
for program_header in program_headers:
    print('header', index)
    virtual_start = program_header['virtual address']
    start= program_header['offset of segment in file image']
    stop = start + program_header['size of segment in file image']

    d = data[start:stop]

#    # Note: might clip the last 15 bytes from the section
#    for offset in range(0,len(d),16):
#        virtual_address = virtual_start + offset
#        print(f'{virtual_address:04x}  ', ' '.join([f'{i:02x}' for i in d[offset:offset+16]]))


    offset = 0
    while offset < stop - start:
        val = struct.unpack('<I', d[offset:offset+4])[0]
        if val == 0xffffded3:
            virtual_address = virtual_start + offset

            print('    Found block at:', f'{virtual_address:04x}')
            decoded_blocks = decode_block(d[offset:], virtual_address)

            for decoded_block in decoded_blocks:
                print('      ', ' '.join([f'{i:02x}' for i in decoded_block['data']]), ':  ', decoded_block['type'])

        offset +=4

    index += 1

