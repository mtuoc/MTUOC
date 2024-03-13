#    MTUOC_guided_alignment_fast_align
#    Copyright (C) 2023  Antoni Oliver
#    29/06/2023
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import codecs
import sys


def guided_alignment_fast_align(MTUOC="/MTUOC",ROOTNAME_ALI="train.sp",ROOTNAME_OUT="train.sp",weightsFile="weights.txt",SL="en",TL="es",BOTH_DIRECTIONS=False,VERBOSE=True):
    if VERBOSE: print("Alignment using fast_align:",ROOTNAME_ALI,SL,TL)
    sys.path.append(MTUOC)
    from MTUOC_check_guided_alignment import check_guided_alignment
    FILE1=ROOTNAME_ALI+"."+SL
    FILE2=ROOTNAME_ALI+"."+TL
    FILEOUT="corpus."+SL+"."+TL+"."+"fa"
    FORWARDALI=ROOTNAME_OUT+"."+SL+"."+TL+".align"
    REVERSEALI=ROOTNAME_OUT+"."+TL+"."+SL+".align"
    command="paste "+FILE1+" "+FILE2+" | sed 's/\t/ ||| /g' > "+FILEOUT
    if VERBOSE: print(command)
    os.system(command)
    
    command=MTUOC+"/fast_align -vdo -i corpus."+SL+"."+TL+".fa > forward."+SL+"."+TL+".align"
    if VERBOSE: print(command)
    os.system(command)
    command=MTUOC+"/fast_align -vdor -i corpus."+SL+"."+TL+".fa > reverse."+SL+"."+TL+".align"
    if VERBOSE: print(command)
    os.system(command)
    command=MTUOC+"/atools -c grow-diag-final -i forward."+SL+"."+TL+".align -j reverse."+SL+"."+TL+".align > "+FORWARDALI
    if VERBOSE: print(command)
    os.system(command)
    if VERBOSE: print("Checking guided alignment")
    check_guided_alignment(FILE1,FILE2,weightsFile,ROOTNAME_OUT+"."+SL+"."+TL+".align")
    
    listfiles = os.listdir(".")
    try:
        os.remove(FILEOUT)
    except:
        pass
    try:
        os.remove("forward."+SL+"."+TL+".align")
    except:
        pass
    try:
        os.remove("reverse."+SL+"."+TL+".align")
    except:
        pass
    try:
        os.remove("forward."+TL+"."+SL+".align")
    except:
        pass
    try:
        os.remove("reverse."+TL+"."+SL+".align")
    except:
        pass
    

if __name__ == "__main__":
    MTUOC=sys.argv[1]
    ROOTNAME_ALI=sys.argv[2]
    ROOTNAME_OUT=sys.argv[3]
    WEIGHTS_FILE=sys.argv[4] #None if not weights used
    SL=sys.argv[5]
    TL=sys.argv[6]
    if len(sys.argv)>7:
        BOTH_DIRECTIONS=sys.argv[7]
    else:
        BOTH_DIRECTIONS=True
    if len(sys.argv)>8:
        VERBOSE=sys.argv[8]
    else:
        VERBOSE=True
    if WEIGHTS_FILE=="None":
        FILE1=ROOTNAME_ALI+"."+SL
        WEIGHTS_FILE="weights.temp"
        entrada=codecs.open(FILE1,"r",encoding="utf-8")
        sortida=codecs.open("weights.temp","w",encoding="utf-8")
        for linia in entrada:
            sortida.write("1\n")
    guided_alignment_fast_align(MTUOC,ROOTNAME_ALI,ROOTNAME_OUT,WEIGHTS_FILE,SL,TL,BOTH_DIRECTIONS,VERBOSE)
