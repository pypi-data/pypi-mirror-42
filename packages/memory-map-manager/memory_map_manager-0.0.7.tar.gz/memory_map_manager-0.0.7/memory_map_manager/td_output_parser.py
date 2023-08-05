#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""This module generates output files based on typedefs."""
import datetime
from copy import deepcopy


def _metadata_to_h_intro(config):
    metadata = config['metadata']
    intro_str = "/**\n"
    intro_str += " ***********************************************************"
    intro_str += "*******************\n"
    intro_str += " * @file       : {}_typedef.h\n".format(metadata["app_name"])
    intro_str += " * @author     : {}\n".format(metadata["author"])
    intro_str += " * @version    : {}\n".format(metadata["version"])
    intro_str += " * @date       : {}\n".format(datetime.date.today())
    if "description" in metadata:
        intro_str += " * @brief      : {}\n".format(metadata["description"])
    intro_str += " * @addtogroup : {}_Typedefs\n".format(metadata["app_name"])
    intro_str += " * @{\n"
    intro_str += " ***********************************************************"
    intro_str += "*******************\n"
    intro_str += " */\n\n"
    intro_str += "#ifndef %s_TYPEDEF_H\n" % (metadata["app_name"].upper())
    intro_str += "#define %s_TYPEDEF_H\n" % (metadata["app_name"].upper())
    return intro_str


def _try_key(try_dict, try_key):
    if try_key not in try_dict:
        return ''
    return try_dict[try_key]


def _bitfields_to_c_struct(config):
    bf_str = ''
    for bitfield in config["bitfields"]:
        bf_str += "/** @brief  : {} */\n".format(_try_key(bitfield,
                                                          "description"))
        bf_str += "typedef struct {\n"
        for element in bitfield["elements"]:
            bf_str += "\t{} {} : {};".format(bitfield["type"],
                                             element["name"],
                                             element["bits"])
            bf_str += " /**< {} */\n".format(_try_key(element, "description"))
        bf_str += "} %s;\n\n" % (bitfield["type_name"])
    return bf_str


def _typedefs_to_c_struct(config):
    c_str = ''
    for typedef in config['typedefs']:
        c_str += "/** @brief  : {} */\n".format(_try_key(typedef,
                                                         "description"))
        c_str += "typedef union {\n"
        c_str += "\tstruct {\n"
        for element in typedef["elements"]:
            if 'array_size' in element:
                c_str += "\t\t{} {}[{}];".format(element["type"],
                                                 element["name"],
                                                 element["array_size"])
            else:
                c_str += "\t\t{} {};".format(element["type"],
                                             element["name"])
            c_str += " /**< {} */\n".format(_try_key(element, "description"))
        c_str += "\t};\n"
        c_str += "\tuint8_t data8[{}];".format(typedef["type_size"])
        c_str += "/**< array for padding */\n"
        c_str += "} %s;\n\n" % (typedef["type_name"])
    return c_str


def parse_typedefs_to_h(config):
    """Parses the typedef to a c header containing typedef structs."""
    metadata = config['metadata']
    local_config = deepcopy(config)
    td_str = ""
    td_str += _metadata_to_h_intro(local_config)
    td_str += "\n"
    td_str += "#include <stdint.h>\n"
    td_str += "\n"
    td_str += "#pragma pack(1)\n"
    td_str += _bitfields_to_c_struct(local_config)
    td_str += _typedefs_to_c_struct(local_config)
    td_str += "#pragma pack()\n"
    td_str += "#endif /* %s_TYPEDEF_H */\n" % (metadata["app_name"].upper())
    td_str += "/** @} */\n"
    return td_str
