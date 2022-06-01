# Hey Emacs, this is a -*- makefile -*-
#
#----------------------------------------------------------------------------
#    This file is based on ChipWhisperer Example Targets
#    Copyright (C) 2012-2017 NewAE Technology Inc.
#    Copyright (C) 2022 Stian Husum
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#----------------------------------------------------------------------------
# Makefile for ChipWhisperer SimpleSerial-AES Program
#
#----------------------------------------------------------------------------
# On command line:
#
# make all = Make software.
#
# make clean = Clean out built project files.
#
# make coff = Convert ELF to AVR COFF.
#
# make extcoff = Convert ELF to AVR Extended COFF.
#
# make program = Download the hex file to the device, using avrdude.
#                Please customize the avrdude settings below first!
#
# make debug = Start either simulavr or avarice as specified for debugging,
#              with avr-gdb or avr-insight as the front end for debugging.
#
# make filename.s = Just compile filename.c into the assembler code only.
#
# make filename.i = Create a preprocessed source file for use in submitting
#                   bug reports to the GCC project.
#
# To rebuild project do "make clean" then "make all".
#----------------------------------------------------------------------------

# Target file name (without extension).
# This is the base name of the compiled .hex file.
TARGET = simpleserial-aes-fix

# List C source files here.
# Header files (.h) are automatically pulled in.
SRC += simpleserial-aes-fix.c

ASRC += aes_encrypt.S aes_keyschedule_lut.S aes_keyschedule.S

OPT = 3

# -----------------------------------------------------------------------------

#Add simpleserial project to build
FIRMWAREPATH = ../../chipwhisperer/hardware/victims/firmware

include $(FIRMWAREPATH)/simpleserial/Makefile.simpleserial
include $(FIRMWAREPATH)/Makefile.inc

