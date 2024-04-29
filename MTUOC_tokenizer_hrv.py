#    MTUOC_tokenizer_hrv 5.0
#    Copyright (C) 2024  Antoni Oliver
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


import string
import re
import sys
import html

QUOTES = (
#adapted from: https://gist.github.com/goodmami/ quotes.py
    '\u0022'  # quotation mark (")
    '\u0027'  # apostrophe (')
    '\u00ab'  # left-pointing double-angle quotation mark
    '\u00bb'  # right-pointing double-angle quotation mark
    '\u2018'  # left single quotation mark
    '\u2019'  # right single quotation mark
    '\u201a'  # single low-9 quotation mark
    '\u201b'  # single high-reversed-9 quotation mark
    '\u201c'  # left double quotation mark
    '\u201d'  # right double quotation mark
    '\u201e'  # double low-9 quotation mark
    '\u201f'  # double high-reversed-9 quotation mark
    '\u2039'  # single left-pointing angle quotation mark
    '\u203a'  # single right-pointing angle quotation mark
    '\u300c'  # left corner bracket
    '\u300d'  # right corner bracket
    '\u300e'  # left white corner bracket
    '\u300f'  # right white corner bracket
    '\u301d'  # reversed double prime quotation mark
    '\u301e'  # double prime quotation mark
    '\u301f'  # low double prime quotation mark
    '\ufe41'  # presentation form for vertical left corner bracket
    '\ufe42'  # presentation form for vertical right corner bracket
    '\ufe43'  # presentation form for vertical left corner white bracket
    '\ufe44'  # presentation form for vertical right corner white bracket
    '\uff02'  # fullwidth quotation mark
    '\uff07'  # fullwidth apostrophe
    '\uff62'  # halfwidth left corner bracket
    '\uff63'  # halfwidth right corner bracket
)

HYPENS = ('\u2010','\u2011','\u2012','\u2013')

class Tokenizer():
    def __init__(self):
        self.specialchars=["¿","¡",]
        self.specialchars.extend(QUOTES)
        self.specialchars.extend(HYPENS)
        self.subs=[]
        self.re_num = re.compile(r'[\d\,\.]+')
        self.abr=["admin.","agr.","akad.","anal.","anat.","ant.","antrop.","aor.","arh.","arheol.","arhit.","astron.","augm.","autom.","bank.","bibl.","biol.","bl.","bot.","br.","bud.","burz.","crkv.","čest.","čit.","dem.","dijal.","dipl.","dosl.","dr.","ekol.","ekon.","engl.","enkl.","etn.","etnol.","eufem.","fam.","farm.","fil.","filat.","film.","fiz.","fiziol.","fon.","fr.","g.","gener.","genet.","geod.","geogr.","geol.","gl.","glazb.","god.","gosp.","gov.","građ.","graf.","gram.","hidr.","hind.","hip.","hrv.","ideol.","im.","imp.","impf.","indiv.","inform.","ing.","int.","iron.","isl.","itd.","izg.","izv.","jud.","kajk.","kalk.","kat.","kazal.","kem.","kinol.","knjiš.","knjiž.","komp.","krat.","kršć.","kulin.","l.","lik.","lingv.","log.","lokal.","lov.","m.","mat.","med.","metaf.","meteor.","meton.","mil.","min.","mit.","mlrd.","mons.","musl.","nar.","pj.","neob.","neodr.","neol.","nesvrš.","neutr.","npr.","odn.","odr.","onom.","opr.","op.","orij.","pat.","pčel.","pejor.","pleon.","poč.","podr.","poet.","po.","Kr.","pol.","pom.","pom.","gl.","posl.","posr.","potenc.","pov.","pr.","pravn.","pravosl.","pren.","prez.","prid.","rad.","trp.","prij.","pr.","pril.","sad.","priv.","prom.","prof.","psih.","publ.","r.","razg.","razr.","red.","refer.","reg.","rel.","retor.","rib.","rij.","rn.","rud.","slav.","slov.","služb.","sociol.","sred.","srp.","stan.","stom.","st.","str.","supl.","sv.","svrš.","tehn.","teol.","term.","tj.","tipogr.","tisk.","top.","trg.","tzv.","umj.","usp.","uzv.","v.","vet.","vezn.","vlč.","vojn.","vulg.","zam.","zast.","zb.","zn.","znanstv.","zool.","ž.","žarg."]
        abr_aux=[]
        for a in self.abr:
            am1=a.capitalize()
            am2=a.upper()
            abr_aux.append(am1)
            abr_aux.append(am2)
        self.abr.extend(abr_aux)
        self.setabr=set(self.abr)
        self.abrsig=()
    def split_numbers(self,segment):
        xifres = re.findall(self.re_num,segment)
        for xifra in xifres:
            xifrastr=str(xifra)
            xifrasplit=xifra.split()
            xifra2=[]
            contpos=0
            for x in xifrastr:
                if not contpos==0: xifra2.append(" ￭")
                xifra2.append(x)
                contpos+=1
            xifra2="".join(xifra2)
            segment=segment.replace(xifra,xifra2)
        return(segment)



    def protect_tags(self, segment):
        tags=re.findall(r'<[^>]+>',segment)
        for tag in tags:
            ep=False
            ef=False
            if segment.find(" "+tag)==-1:ep=True
            if segment.find(tag+" ")==-1:ef=True
            tagmod=tag.replace("<","&#60;").replace(">","&#62;").replace("=","&#61;").replace("'","&#39;").replace('"',"&#34;").replace("/","&#47;").replace(" ","&#32;")
            if ep: tagmod=" ￭"+tagmod
            if ef: tagmod=tagmod+"￭ "
            segment=segment.replace(tag,tagmod)
        tags=re.findall(r'\{[0-9]+\}',segment)
        for tag in tags:
            ep=False
            ef=False
            if segment.find(" "+tag)==-1:ep=True
            if segment.find(tag+" ")==-1:ef=True
            tagmod=tag.replace("{","&#123;").replace("}","&#125;")
            if ep: tagmod=" ￭"+tagmod
            if ef: tagmod=tagmod+"￭ "
            segment=segment.replace(tag,tagmod)
        return(segment) 
    
    def protect_abr(self,cadena):
        setcadena=set(cadena.split(" "))
        common=(self.setabr & setcadena)
        self.abrsig=list(common)
        for a in common:
            amod=a+" "
            apro=a.replace(".","&#46;")
            cadena=cadena.replace(amod,apro)
        sigles=re.findall(r'((\w\.){2,})',cadena)
        for s in sigles:
            a=s[0]
            self.abrsig.append(a)
            amod=a+" "
            apro=a.replace(".","&#46;")
            cadena=cadena.replace(amod,apro)
        return(cadena)
    
    def unprotect(self, cadena):
        cadena=cadena.replace("&#39;","'").replace("&#45;","-").replace("&#60;","<").replace("&#62;",">").replace("&#34;",'"').replace("&#61;","=").replace("&#32;","▁").replace("&#47;","/").replace("&#123;","{").replace("&#125;","}")
        return(cadena)
    
    def unprotect_tags(self, cadena):
        cadena=cadena.replace("&#60;","<").replace("&#62;",">")
        return(cadena)
    
    def unprotect_abr(self,cadena):
        for a in self.abrsig:
            amod=a+" "
            apro=a.replace(".","&#46;")
            cadena=cadena.replace(apro,amod)
        return(cadena)

    def main_tokenizer(self,segment):
        segment=" "+segment+" "
        cadena=self.protect_tags(segment)
        cadena=self.protect_abr(cadena)
        for s in self.subs:
            sA=s.replace("￭","")
            sB=s.replace("'","&#39;").replace("-","&#45;")
            if s.startswith("￭"):sB=" "+sB
            if s.endswith("￭"):sB=sB+" "
            cadena = re.sub(sA+r'\b', sB, cadena)
            cadena = re.sub(r'\b'+sA, sB, cadena)
            cadena = re.sub(sA.upper()+r'\b', sB.upper(), cadena)
            cadena = re.sub(r'\b'+sA.upper(), sB.upper(), cadena)
        punt=list(string.punctuation)
        exceptions=["&",";","#"]
        for e in exceptions:
            punt.remove(e)
        
        for p in punt:
            ppre=" ￭"+p
            ppost=p+"￭ "
            try:
                expr1="(\\S)\\"+p+"(\\s)"
                expr2=r"\1"+ppre+r"\2"
                cadena = re.sub(expr1,expr2, cadena)
                expr1="(\\s)\\"+p+"(\\S)"
                expr2=r"\1"+ppost+r"\2"
                cadena = re.sub(expr1,expr2, cadena)
            except:
                pass
        cadena=self.unprotect_tags(cadena)
        cadena=self.unprotect_abr(cadena)
        
        for p in self.specialchars:
            pmod=p+" "
            if cadena.find(pmod)>=-1:
                pmod2=p+"￭ "
                cadena=cadena.replace(p,pmod2)
            pmod=" "+p
            if cadena.find(pmod)>=-1:
                pmod2=" ￭"+p
                cadena=cadena.replace(p,pmod2)

        cadena=self.unprotect(cadena)
        
        for p in exceptions:
            pmod=p+" "
            if cadena.find(pmod)>=-1:
                pmod2=p+"￭ "
                cadena=cadena.replace(p,pmod2)
            pmod=" "+p
            if cadena.find(pmod)>=-1:
                pmod2=" ￭"+p
                cadena=cadena.replace(p,pmod2)    
        
        cadena=cadena.replace("▁"," ")
        cadena=' '.join(cadena.split())   
        return(cadena)

    def tokenize(self,segment):
        tokenized=self.main_tokenizer(segment)
        tokenized=tokenized.replace("￭","")
        tokenized=' '.join(tokenized.split()) 
        return(tokenized)
        
    def detokenize(self, segment):
        for sub in self.subs:
            subA=sub.replace("￭"," ")
            subB=sub.replace("￭","")
            segment=segment.replace(subA,subB)
            segment=segment.replace(subA.capitalize(),subB.capitalize())
            segment=segment.replace(subA.upper(),subB.upper())
        segment=segment.replace(" .",".")
        segment=segment.replace(" ,",",")
        segment=segment.replace(" :",":")
        segment=segment.replace(" ;",";")
        segment=segment.replace(" :",":")
        segment=segment.replace(" )",")")
        segment=segment.replace("( ","(")
        segment=segment.replace(" ]","]")
        segment=segment.replace("[ ","[")
        segment=segment.replace(" }","}")
        segment=segment.replace("{ ","{")
        segment=segment.replace(" !","!")
        segment=segment.replace("¡ ","¡")
        segment=segment.replace(" ?","?")
        segment=segment.replace("¿ ","¿")
        segment=segment.replace(" »","»")
        segment=segment.replace("« ","«")
        segment=segment.replace("‘ ","‘")
        segment=segment.replace(" ’","’")
        segment=segment.replace("“ ","“")
        segment=segment.replace(" ”","”")
        segment=' '.join(segment.split()) 
        return(segment)

    def tokenize_j(self,segment):
        tokenized=self.main_tokenizer(segment)
        tokenized=' '.join(tokenized.split()) 
        return(tokenized)

    def detokenize_j(self,segment):
        segment=segment.replace(" ￭","")
        segment=segment.replace("￭ ","")
        segment=segment.replace("￭","")
        detok=segment
        detok=' '.join(detok.split()) 
        return(detok)
        
    def tokenize_jn(self,segment):
        tokenized=self.tokenize_j(segment)
        tokenized=self.split_numbers(tokenized)
        tokenized=' '.join(tokenized.split()) 
        return(tokenized)

    def detokenize_jn(self,segment):
        segment=self.detokenize_j(segment)
        return(segment)
        
    def tokenize_s(self,segment):
        tokenized=self.main_tokenizer(segment)
        tokenized=tokenized.replace("￭ ","￭")
        tokenized=tokenized.replace(" ￭","￭")
        tokenized=tokenized.replace(" "," ▁")
        tokenized=tokenized.replace("￭"," ")
        tokenized=' '.join(tokenized.split()) 
        return(tokenized)
        
    def detokenize_s(self,segment):
        segment=segment.replace(" ","")
        segment=segment.replace("▁"," ")
        detok=segment
        detok=' '.join(detok.split()) 
        return(detok)

    def tokenize_sn(self,segment):
        tokenized=self.main_tokenizer(segment)
        tokenized=self.split_numbers(tokenized)
        tokenized=tokenized.replace("￭ ","￭")
        tokenized=tokenized.replace(" ￭","￭")
        tokenized=tokenized.replace(" "," ▁")
        tokenized=tokenized.replace("￭"," ")
        tokenized=' '.join(tokenized.split()) 
        return(tokenized)

    def detokenize_sn(self,segment):
        segment=self.detokenize_s(segment)
        return(segment)        
    
def print_help():
    print("MTUOC_tokenizer_cat.py A tokenizer for Croatian, usage:")
    print("Simple tokenization:")
    print('    cat "sentence to tokenize." | python3 MTUOC_tokenizer_hrv.py tokenize')
    print('    python3 MTUOC_tokenizer_hrv.py tokenize < file_to_tokenize > tokenized_file')
    print()
    print("Simple detokenization:")
    print('    cat "sentence to tokenize." | python3 MTUOC_tokenizer_hrv.py detokenize')
    print('    python3 MTUOC_tokenizer_hrv.py detokenize < file_to_detokenize > detokenized_file')
    print()
    print("Advanced options:")
    print("    tokenization/detokenization with joiner marks (￭): tokenize_j / detokenize_j")
    print("    tokenization/detokenization with joiner marks (￭) and number splitting: tokenize_jn / detokenize_jn")
    print("    tokenization/detokenization with splitter marks (▁): tokenize_s / detokenize_s")
    print("    tokenization/detokenization with splitter marks (▁) and number splitting: tokenize_sn / detokenize_sn")
        

if __name__ == "__main__":
    if len(sys.argv)>1:
        if sys.argv[1]=="-h" or sys.argv[1]=="--help":
            print_help()
            sys.exit()
        action=sys.argv[1]
    else:
        action="tokenize"
    tokenizer=Tokenizer()
    for line in sys.stdin:
        line=line.strip()
        #normalization of apostrophe
        line=line.replace("’","'")
        line=html.unescape(line)
        if action=="tokenize":
            outsegment=tokenizer.tokenize(line)
        elif action=="detokenize":
            outsegment=tokenizer.detokenize(line)
        
        elif action=="tokenize_s":
            outsegment=tokenizer.tokenize_s(line)
        elif action=="detokenize_s":
            outsegment=tokenizer.detokenize_s(line)
        elif action=="tokenize_sn":
            outsegment=tokenizer.tokenize_sn(line)
        elif action=="detokenize_sn":
            outsegment=tokenizer.detokenize_sn(line)
        
        elif action=="tokenize_j":
            outsegment=tokenizer.tokenize_j(line)
        elif action=="detokenize_j":
            outsegment=tokenizer.detokenize_j(line)
        elif action=="tokenize_jn":
            outsegment=tokenizer.tokenize_jn(line)
        elif action=="detokenize_jn":
            outsegment=tokenizer.detokenize_jn(line)
        
        print(outsegment)
        
