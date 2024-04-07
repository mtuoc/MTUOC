#    MTUOC-addweights
#    Copyright (C) 2024  Antoni Oliver
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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import codecs
import sys

if len(sys.argv)<4:
    print("MTUOC-addweigts: a script to add weights to a tabbed parallel corpus. It needs three arguments:")
    print("   (1) the input file. It should be a tabbed parallel corpus: source_segment tabulator target segment.")
    print("   (2) the output file. It will be the tabbed parllel corpus with the given weight as a 3rd field.")
    print("   (3) the weight.")
    print("Example: python3 MTUOC-addweights.py inputcorpus.txt outputcorpus.txt 0.75")
    sys.exit()
    
fentrada=sys.argv[1]
fsortida=sys.argv[2]
weight=sys.argv[3]



entrada=codecs.open(fentrada,"r",encoding="utf-8")
sortida=codecs.open(fsortida,"w",encoding="utf-8")

for linia in entrada:
    linia=linia.strip()
    linia=linia+"\t"+str(weight)
    sortida.write(linia+"\n")
entrada.close()
sortida.close()
