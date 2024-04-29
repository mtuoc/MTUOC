#    MTUOC_tokenizer_spa 5.0
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
        self.abr=["aa.rr.","abr.","abrev.","a.c.","adj.","adm.","admón.","afma.","afmas.","afmo.","afmos.","ag.","ago.","am.","ap.","apdo.","art.","arts.","arz.","arzbpo.","assn.","atte.","av.","avda.","bros.","bv.","cap.","caps.","cg.","cgo.","cia.","cía.","cit.","co.","col.","corp.","cos.","cta.","cte.","ctra.","cts.","d.c.","dcha.","dept.","depto.","dic.","doc.","docs.","dpt.","dpto.","dr.","dra.","dras.","dres.","dto.","dupdo.","ed.","ee.uu.","ej.","emma.","emmas.","emmo.","emmos.","ene.","entlo.","entpo.","esp.","etc.","ex.","excm.","excma.","excmas.","excmo.","excmos.","fasc.","fdo.","feb.","fig.","figs.","fol.","fra.","gb.","gral.","hnos.","hros.","ib.","ibid.","ibíd.","id.","íd.","ilm.","ilma.","ilmas.","ilmo.","ilmos.","iltre.","inc.","intr.","ít.","izq.","izqda.","izqdo.","jr.","jul.","jun.","lám.","lda.","ldo.","lib.","lim.","loc.","ltd.","ltda.","mar.","máx.","may.","mín.","mons.","mr.","mrs.","ms.","mss.","mtro.","nov.","ntra.","ntro.","núm.","ob.","obpo.","oct.","op.","pág.","págs.","párr.","pd.","ph.","pje.","pl.","plc.","pm.","pp.","ppal.","pral.","prof.","pról.","prov.","ps.","pta.","ptas.","pte.","pts.","pza.","rda.","rdo.","ref.","reg.","rel.","rev.","revda.","revdo.","rma.","rmo.","r.p.m.","rte.","sdad.","sec.","secret.","sep.","sig.","smo.","sr.","sra.","sras.","sres.","srs.","srta.","ss.mm.","sta.","sto.","sust.","tech.","tel.","teléf.","telf.","ten.","tfono.","tít.","tlf.","ud.","uds.","vda.","vdo.","vid.","vol.","vols.","vra.","vro.","vta.","abr.","adj.","admón.","admor.","admora.","admtvo.","admvo.","advo.","ag.","ago.","agt.","a.m.","ap.","apdo.","apénd.","aprox.","aptdo.","art.","asoc.","att.","av.","avda.","ayto.","bach.","bibl.","bol.","calif.","cast.","cat.","c.c.","cc.oo.","cf.","cfr.","cjón.","cta.","ctra.","d.","dª.","dcha.","d.e.p.","depto.","dic.","dicbre.","dir.","disp.","dña.","do.","doc.","dom.","dr.","dra.","dto.","dupl.","e.","ed.","ej.","emmo.","ene.","entlo.","epitomadamente.","esc.","esp.","etc.","excma.","excmo.","exp.","expte.","ext.","fac.","facs.","fasc.","fdo.","feb.","febr.","fig.","fra.","gob.","gral.","hble.","hnos.","hosp.","ib.","ibid.","ibíd.","id.","íd.","il.","ilma.","ilmo.","iltre.","inc.","intr.","izq.","izqda.","j.","j.c.","ju.","jue.","jul.","jun.","k.o.","lcdo.","lda.","ldo.","lic.","ltda.","lu.","lun.","ma.","mar.","mart.","máx.","may.","mi.","mié.","miérc.","min.","mín.","mn.","mons.","my.","mzo.","n.b.","nº.","nov.","novbre.","nro.","n.s.","ntra.","ntro.","núm.","núms.","oct.","op.","pág.","pár.","párr.","p.ej.","pl.","p.m.","p.o.","pp.","pp.","pral.","proc.","prof.","ps.","p.s.","pte.","pts.","p.v.p.","pza.","q.d.e.p.","q.e.g.e.","r.d.","r.d.l.","rdo.","ref.","r.i.p.","r.o.","r.p.m.","rvdo.","s.","s.a.","sa.","s.a.","sáb.","sdad.","sep.","sept.","setbre.","s.l.","s.l.u.","s.m.","sr.","sra.","sras.","sres.","s.s.","ss.mm.","ssp.","stmo.","subsp.","tel.","trad.","ud.","ud.","udes.","uds.","urb.","v.a.","v.a.r.","vd.","vda.","vds.","vi.","vid.","vie.","vnes.","vol."]
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
    print("MTUOC_tokenizer_cat.py A tokenizer for Spanish, usage:")
    print("Simple tokenization:")
    print('    cat "sentence to tokenize." | python3 MTUOC_tokenizer_spa.py tokenize')
    print('    python3 MTUOC_tokenizer_spa.py tokenize < file_to_tokenize > tokenized_file')
    print()
    print("Simple detokenization:")
    print('    cat "sentence to tokenize." | python3 MTUOC_tokenizer_spa.py detokenize')
    print('    python3 MTUOC_tokenizer_spa.py detokenize < file_to_detokenize > detokenized_file')
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
        
