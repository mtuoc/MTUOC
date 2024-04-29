#    MTUOC_tokenizer_eng 5.0
#    Copyright (C) 2024  Antoni Oliver
#    02/11/2023
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
        self.subs=["￭'s","￭'ll","￭'t","￭'cause","￭'d","￭'em","￭'ve","￭'dn","￭'m","￭'n","￭'re","￭'til","￭'tween","￭'all","ol'￭"]
        self.re_num = re.compile(r'[\d\,\.]+')
        self.abr=["a.a.","a.a.a.","a.a.u.","a.b.","a.b.a","abbr.","abr.","a.c.","acad.","aclu.","a.d.","adm.","a.e.c.","a.f.l.","afl-cio","afrik.","a.i.a.","a.k.c.","a.l.","a.l.a.","ala.","alt.","alta.","a.m.","a.m.a.","a.m.p.","a.m.u.","antilog.","a.p.","arab.","ariz.","ark.","a.s.","ascap.","at.no.","at.wt.","a.u.","aug.","a.v.","avdp.","ave.","b.a.","b.b.c.","b.c.","b.d.","b.lit.","b.mus.","b.p.","brig.gen.","b.s.","b.t.u.","bul.","bulg.","c.","cal.","calif.","cant.","capt.","c.c.","c.d.","cent.","cento.","c.e.o.","c.g.s.","chem.","chin.","chron.","cie.","c.i.a.","c.i.d.","c.i.o.","cl.","c.m.","cn.","co.","col.","coll.","colo.","comdr.","comp.","com.pop.","conn.","cor.","corp.","cos.","cot.","coul.","cp.","c.p.a.","c.p.l.","c.p.o.","c.s.c.","c.u.","dan.","dar.","d.c.","d.c.l.","d.d.","d.d.s.","d.d.t.","dec.","del.","dept.","deut.","dist.","div.","dr.","ds.","d.sc.","du.","e.c.","e.c.a.","eccles.","ecclus.","ed.","e.d.c.","e.e.","e.e.a.","e.e.c.","e.e.o.c.","e.f.t.a.","e.g.","e.m.f.","e.m.u.","eng.","enl.","eph.","e.r.a.","e.r.p.","e.s.c.","esp.","est.","e.u.","ev.","ex.","ezek.","f.a.a.","fac.","f.a.o.","f.b.i.","f.c.c.","f.d.a.","feb.","f.e.p.c.","finn.","fl.","fla.","floz.","f.m.","fr.","ft.","f.t.c.","g.","ga.","gal.","gall.","gatt.","g.d.p.","gen.","ger.","gm.","g.m.b.","g.m.t.","g.n.p.","g.o.p.","gov.","gr.","grad.","grm.","hab.","hag.","heb.","h.m.s.","hon.","hr.","hung.","hz.","i.a.u.","i.b.m.","i.b.t.","i.c.a.o.","i.c.b.m.","i.c.c.","icel.","i.e.","i.g.y.","ilgwu.","ill.","i.l.o.","i.m.f.","inc.","incl.","ind.","ing.","inst.","introd.","i.q.","i.r.a.","i.r.b.m.","i.r.s.","isa.","ital.","i.t.u.","i.u.p.a.c.","i.w.w.","jan.","jap.","j.d.","jer.","j.g.","jr.","j.","kc.","kg.","kgb.","kgm.","k.k.k.","kl.","km.","kw.","kwh.","ky.","l.","la.","lam.","lat.","lb.","lev.","l.h.d.","lib.","lith.","litt.b.","litt.d.","ll.b.","ll.d.","l.s.d.","lt.","lt.col.","ltd.","lt.gen.","lt.gov.","lts.","m.a.","mac.","maj.","maj.gen.","mal.","mass.","mass.no.","m.b.","m.d.","md.","m.e.","messrs.","mev.","mex.","mfg.","mg.","m.h.g.","mi.","mich.","min.","minn.","miss.","mks.","ml.","mlle.","mls.","mm.","mme.","mo.","mont.","m.p.","m.p.h.","mph.","mr.","mrs.","m.s.","ms.","msgr.","mss.","mt.","mts.","mus.","mus.b.","mus.d.","n.a.a.c.p.","n.a.f.t.a.","n.a.s.a.","n.a.s.d.a.q.","n.a.t.o.","n.b.","n.b.a.","n.c.","n.c.a.a.","n.c.o.","n.dak.","n.e.","n.e.a.","nebr.","neh.","nev.","n.f.","n.f.l.","n.h.","n.h.l.","n.j.","nl.","n.l.r.b.","n.mex.","nnw","no.","non-u.s.","nor.","nov.","n.r.a.","n.r.c.","n.s.","n.s.f.","num.","n.v.","n.y.","n.y.a.","n.y.s.e.","o.a.s.","obad.","oct.","o.e.","o.e.c.d.","o.e.o.","o.e.s.","o.fr.","o.h.g.","okla.","o.n.","ont.","op.","o.p.a.","o.s.","o.s.c.e.","o.s.s.","o.z.","oz.","pa.","p.a.u.","pd.d.","p.e.i.","pers.","p.f.c.","p.g.a.","ph.","ph.b.","ph.d.","philip.","pk.","pkg.","pl.","plc","p.m","p.m.","pn.","po.","pol.","pop.","port.","prof.","prov.","prov(s).","ps.","pseud.","pss.","pt.","pts.","pub.","pvt.","p.w.a.","q.t.","qt.","qts.","que.","r.a.","r.a.f.","rep.","reps.","repr.","rev.","r.i.","r.n.","r.n.a.","rom.","r.o.t.c.","r.p.m.","rpm.","r.r.","r.s.f.s.r.","r.s.v.","rt.rev.","rus.","r.v.","sam.","sask.","s.c.","sc.d.","s.dak.","s.e.","s.e.a.t.o.","sec.","sen.","sens.","sept.","ser.","sgt.","s.j.","skt.","sl.","s.o.s.","span.","s.p.a.","s.p.c.a.","s.p.c.c.","sp.gr.","s.q.","sr.","s.s.","s.s.r.","st.","s.t.d.","s.t.e.","s.t.p.","s.w.","swed.","t.","tablesp.","t.a.n.","t.a.s.s.","tb.","tbl.","tble.","tbles.","tbls.","tblsp.","tbs.","tbsn.","tbsp.","tbsps.","teas.","tenn.","thess.","tim.","t.n.t","tr.","ts.","tsp.","tsps.","turk.","t.v.a.","u.a.w.","u.h.f.","ukr.","u.m.w.","u.n.","uninc.","univ.","u.n.r.r.a.","u.p.i.","u.s.","u.s.a.","u.s.a.f.","u.s.c.g.","u.s.m.c.","u.s.n.","u.s.o.","u.s.s.","u.s.s.r.","u.t.","va.","var.","ved.","v.","v.f.w.","v.h.f.","vol.","vs.","vt.","w.a.c.","w.c.t.u.","w.e.u.","w.f.t.u.","wis.","wmo.","wpa.","wt.","wto.","w.va.","wyo.","yd.","y.m.c.a.","y.m.h.a.","y.w.c.a.","y.w.h.a.","zech.","zeph."]
        abr_aux=[]
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
    print("MTUOC_tokenizer_cat.py A tokenizer for Catalan, usage:")
    print("Simple tokenization:")
    print('    cat "sentence to tokenize." | python3 MTUOC_tokenizer_cat.py tokenize')
    print('    python3 MTUOC_tokenizer_cat.py tokenize < file_to_tokenize > tokenized_file')
    print()
    print("Simple detokenization:")
    print('    cat "sentence to tokenize." | python3 MTUOC_tokenizer_cat.py detokenize')
    print('    python3 MTUOC_tokenizer_cat.py detokenize < file_to_detokenize > detokenized_file')
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
        
