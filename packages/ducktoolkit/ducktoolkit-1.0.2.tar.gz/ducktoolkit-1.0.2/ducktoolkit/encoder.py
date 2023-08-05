#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import os
import io
import sys
import json
import time
import binascii
from .common import convert_hex

major_version = sys.version_info[0]

DEBUG = False

def hidg_write(elements):
    values = bytearray(elements)
    not_hold = bytearray([0, 0, 0, 0, 0, 0, 0, 0])

    hidg = open("/dev/hidg0", "wb")
    hidg.write(values)
    hidg.write(not_hold)
    hidg.close()


def parse_text(duck_text, lang_file, bunny):
    
    if major_version == 3:
        # COnvert the lang file to bytes
        lang_file = { key.encode(): val.encode() for key, val in lang_file.items() }
    
    line_count = 0
    encoded_file = []
    duck_text = duck_text.replace(b"\r", b"")
    cmd = instruction = False

    default_delay = 0

    for line in duck_text.split(b'\n'):
        if len(line) > 0:

            # REM Comments
            if line.startswith(b'REM') or line.startswith(b'rem'):
                continue

            # Last Command
            last_command = cmd
            last_instruction = instruction

            line_count += 1
            line = line.lstrip().rstrip()
            parsed_line = line.split(b' ', 1)

            if len(parsed_line) >= 2:
                cmd = parsed_line[0].strip()
                instruction = parsed_line[1].rstrip()
            else:
                cmd = parsed_line[0].strip()
                instruction = False



            if DEBUG:
                print("CMD: ", cmd, "Instruction: ", instruction)

            # Default Delay
            if cmd in [b'DEFAULT_DELAY', b'DEFAULTDELAY']:
                try:
                    default_delay = int(instruction)
                    continue
                except Exception as e:
                    error_line = e
                    return error_line

            # Repeat
            repeat_count = 1
            if cmd.lower() in [b'repeat', b'replay']:
                try:
                    repeat_count = int(instruction)
                except Exception as e:
                    print(e)
                    error_line = b'Repeat value not valid'

                cmd = last_command
                instruction = last_instruction

            for i in range(repeat_count):
                if cmd == b'STRING':
                    for char in instruction:
                        
                        if major_version == 3:
                            char = bytes([char])
                        
                        elements = lang_file[char].split(b',')
                        elements = [int(i, 16) for i in elements]
                        # Bunny Support
                        if bunny:
                            for i in range(5):
                                elements.append(0)
                            hidg_write(elements)
                        else:
                            encoded_file.append(convert_hex(elements[2]))
                            encoded_file.append(convert_hex(elements[0]))
                        if DEBUG:
                            print(char, ': ', convert_hex(elements[2]), convert_hex(elements[0]))

                elif cmd == b'DELAY':
                    #Bunny Support
                    if bunny:
                        time.sleep(0.001 * int(instruction))
                    else:
                        delay = add_delay(int(instruction))
                        encoded_file.append(delay)

                

                elif cmd in iter(lang_file.keys()):

                    elements = lang_file[cmd].split(b',')
                    elements = [int(i, 16) for i in elements]
                    # Bunny Support
                    for i in range(5):
                        elements.append(0)

                    if instruction:
                        param = lang_file[instruction].split(b',')
                        param = [int(i, 16) for i in param]
                        elements[0] |= param[0]
                        elements[2] |= param[2]

                    # Bunny Support
                    if bunny:
                        hidg_write(elements)
                    else:
                        encoded_file.append(convert_hex(elements[2]))
                        encoded_file.append(convert_hex(elements[0]))

                    if DEBUG:
                        print(instruction, ': ', convert_hex(elements[2]), convert_hex(elements[0]))
                else:
                    err_line = "Command '{0}' is not in the Language File".format(cmd)
                    return err_line

                # Add Default Delay
                if default_delay:
                    if bunny:
                        time.sleep(0.001 * int(default_delay))
                    else:
                        encoded_file.append(add_delay(int(default_delay)))


    return encoded_file


def add_delay(delay_value):

    delay_return = ''

    # divide by 255 add that many 0xff
    # convert the reminder to hex
    # e.g. 750 = FF FF F0
    while delay_value > 0:
        if delay_value > 255:
            delay_return += '00FF'
            delay_value -= 255
        else:
            _delay = hex(delay_value)[2:].zfill(2)
            delay_return += '00{0}'.format(str(_delay))
            delay_value = 0
    return delay_return


def encode_script(duck_text, duck_lang, bunny=None):

    lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
    language_dict = os.path.join(lang_dir, '{0}.json'.format(duck_lang))
    lang_file = json.load(open(language_dict))


    try:
        encoded_file = parse_text(duck_text, lang_file, bunny)
    except Exception as e:
        print("Error parsing duck_text: {0}".format(e))
        return False
        

    if encoded_file and not bunny:
        if b'not in the Language' in encoded_file:
            return encoded_file
        else:
            try:
                encoded_file = "".join(encoded_file)
                duck_blob = io.BytesIO()
                write_bytes = encoded_file.encode()
                duck_blob.write(write_bytes)
                duck_bin = duck_blob.getvalue()
                duck_blob.close()
                return duck_bin

            except Exception as e:
                print("Error creating inject.bin: {0}".format(e))
                return False
