#!/usr/bin/env python3
import pefile
from capstone import *


def main():
    # Load the target PE file
    pe = pefile.PE("ircbot.exe")

    # Get the address of the program entry point from the program header
    entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint

    # Compute memory address where the entry code will be loaded into memory
    entry_point_address = entry_point + pe.OPTIONAL_HEADER.ImageBase

    # Get the binary code from the PE file object
    binary_code = pe.get_memory_mapped_image()[entry_point:entry_point + 100]

    # Initialize disassembler to disassemble 32-bit x86 binary code
    disassembler = Cs(CS_ARCH_X86, CS_MODE_32)

    # Disassemble the code
    for instruction in disassembler.disasm(binary_code, entry_point_address):
        print(f"{instruction.mnemonic}\t{instruction.op_str}")


if __name__ == "__main__":
    main()
