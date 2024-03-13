#    MTUOC_guided_alignment_eflomal
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


def guided_alignment_eflomal(MTUOC="/MTUOC",ROOTNAME_ALI="train.sp",ROOTNAME_OUT="train.sp",weightsFile="weights.txt",SL="en",TL="es",SPLIT_LIMIT=1000000,VERBOSE=True):
    if VERBOSE: print("Alignment using eflomal:",ROOTNAME_ALI,SL,TL)
    sys.path.append(MTUOC)
    from MTUOC_check_guided_alignment import check_guided_alignment
    FILE1=ROOTNAME_ALI+"."+SL
    FILE2=ROOTNAME_ALI+"."+TL
    FILEOUT="corpus."+SL+"."+TL+"."+"fa"
    command="paste "+FILE1+" "+FILE2+" | sed 's/\t/ ||| /g' > "+FILEOUT
    if VERBOSE: print(command)
    os.system(command)
    command="split -l "+str(SPLIT_LIMIT)+" "+FILEOUT+" tempsplitted-"
    if VERBOSE: print(command)
    os.system(command)
    
    listfiles = os.listdir(".")
    print(listfiles)
    
    for file in listfiles:
        if file.startswith("tempsplitted-"):
            tempaliforward="tempaliforward-"+file.split("-")[1]
            tempalireverse="tempalireverse-"+file.split("-")[1]
            command=MTUOC+"/eflomal-align.py -i "+file+" --model 3 -f "+tempaliforward+" -r "+tempalireverse
            if VERBOSE: print(command)
            os.system(command)
    
    command="cat tempaliforward-* > "+ROOTNAME_OUT+"."+SL+"."+TL+".align"
    if VERBOSE: print(command)
    os.system(command)
    command="cat tempalireverse-* > todelete.align"
    if VERBOSE: print(command)
    os.system(command)
    if VERBOSE: print("Checking guided alignment")
    check_guided_alignment(FILE1,FILE2,weightsFile,ROOTNAME_OUT+"."+SL+"."+TL+".align")
    listfiles = os.listdir(".")
    os.remove("todelete.align")
    os.remove(FILEOUT)
    for file in listfiles:
        if file.startswith("tempsplitted-") or file.startswith("tempaliforward") or file.startswith("tempalireverse"):
            try:
                os.remove(file) 
            except:
                pass
    

if __name__ == "__main__":
    MTUOC=sys.argv[1]
    ROOTNAME_ALI=sys.argv[2]
    ROOTNAME_OUT=sys.argv[3]
    WEIGHTS_FILE=sys.argv[4] #None if not weights used
    SL=sys.argv[5]
    TL=sys.argv[6]
    SPLIT_LIMIT=sys.argv[7]
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
        
    guided_alignment_eflomal(MTUOC,ROOTNAME_ALI,ROOTNAME_OUT,WEIGHTS_FILE,SL,TL,SPLIT_LIMIT,VERBOSE)
