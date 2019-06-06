# ColorBasicToolChain
Setup for a toolchain for ColorBasic, Notepad++ and Xroar

Warning:
- This setup has been tried on Windows only

Tools involved:
- Notepad++
- XROAR
- Mame
- Toolshed
- Python

Requirements:
For Notepad++
a) for the source code file, encoding must be set to ANSI - option acessible on the "Encoding" menu.
b) for the source code file, EOL Convesion must be set to Windows (CR LF) - option acessible on the "Edit" >> "EOL Conversion" menu.

Once file is saved, use following options to place the file in a dsk file.
C) mame imgtool --ftype=basic --filter=cocobas;
D) toolshed decb -l -a -a;
E) toolshed decb -l -0 -b -t.
F) toolshed decb -l -3 -a.

OPTION 1 - using Mame imgtool

imgtool put coco_jvc_rsdos test.dsk source.bas TARGET.BAS --ftype=basic --filter=cocobas 

test.dsk - this is the dsk file where the source file needs to be copied to
source.bas - this is the source file to be copied to the dsk. any name or extension is valid.
TARGET.BAS - this is the name of the file in the dsk. Upper case is needed as ColorBasic can't handle lower case names well.

OPTION 2 - using Toolshed decb

decb copy -l -0 -b -t source.bas test.dsk,TARGET.BAS 

This option will place the file in the dsk as a binary basic file

source.bas - this is the source file to be copied to the dsk. 
test.dsk - this is the dsk file where the source file needs to be copied to
TARGET.BAS - this is the name of the file in the dsk. Upper case is needed as ColorBasic can't handle lower case names well.
!!! The comma is critical. Do not remove it.

OPTION 3 - using Toolshed decb

decb copy -l -3 -a -t source.bas test.dsk,TARGET.BAS

This option will place the file in the dsk as a ASC file

source.bas - this is the source file to be copied to the dsk. 
test.dsk - this is the dsk file where the source file needs to be copied to
TARGET.BAS - this is the name of the file in the dsk. Upper case is needed as ColorBasic can't handle lower case names well.
!!! The comma is critical. Do not remove it.

The scripts configured on this toolchain use OPTION 1 described above.

To automatically execute the basic file in XROAR from Notepad, use the F6 (Execute) command.

On the command description, use the following:
cls
// save current file
NPP_SAVE
// construct the script name to be called
SET Compiler = [A_FOLDER_LOCATION]\build_and_run$(EXT_PART).txt
// call the script
NPP_EXEC "$(Compiler)"

Inside the [A_FOLDER_LOCATION] place the files available on this repository. Make sure to adjust any file path names. 
Pay attention to folder names with spaces. Use "" to define them.


The scripts will run the basic file in XROAR and copy the file into a dsk. 

ASSUMPTIONS:

The dsk file is located in the same folder as the source file. 

The dsk file name is the same as the source file namme.


