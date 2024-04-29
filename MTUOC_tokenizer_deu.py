#    MTUOC_tokenizer_deu 5.0
#    Copyright (C) 2024  Antoni Oliver
#    14/05/2021
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
#    '\u0027'  # apostrophe (')
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
        self.specialchars=["«","»","—","‘","’","“","”","„",]
        self.subs=["￭'s"]
        self.re_num = re.compile(r'[\d\,\.]+')

    def __init__(self):
        self.specialchars=["«","»","—","‘","’","“","”","„",]
        self.subs=["￭'s"]
        self.re_num = re.compile(r'[\d\,\.]+')
        self.abr=["&c.","0.","1.","10.","2.","3.","4.","5.","6.","7.","8.","9.",".c.",".d.",".v.","A.","a.","a.A.","a.a.","a.a.O.","A.B.","a.c.i.","a.Chr.","a.D.","a.d.","A.D.","a.d.D.","a.d.E.","A.d.Hrsg.","a.d.O.","a.f.","a.G.","a.i.","a.l.i.c.","a.M.","a.n.Chr.","a.n.g.","a.O.","a.o.Prof.","a.Rh.","a.St.","A.T.","a.t.","a.u.c.","a.Z.","a.D.","a.d.D.","Abb.","abchas.","abds.","Abf.","Abfr.","Abg.","abgek.","abh.","Abh.","Abk.","ABl.","Abl.","ABl.EG","Abm.","abn.","Abn.","abr.","Abr.","Abs.","abs.","Abschn.","Abst.","Abt.","abulg.","abw.","abwert.","abzgl.","accel.","a.lib.","Add.","Adj.","adj.","Adr.","adv.","Adv.","adyg.","ae.","aengl.","afghan.","afr.","afranz.","afranzös.","afries.","afrik.","afrk.","afrs.","afrz.","afränk.","ags.","ahd.","Ahd.","aind.","air.","akad.","Akk.","akkad.","akt.","alb.","alban.","alem.","alemann.","all.","allg.","allj.","allm.","alltagsspr.","alphanum.","Alt.","altai.","altengl.","altfranz.","altfranzös.","altfrz.","altgr.","althochdt.","altis.","altisländ.","altpreuß.","altröm.","alttest.","alëut.","am.","amer.","amerik.","amerikan.","amhar.","amt.","amtl.","Amtm.","Amtsbl.","Amtsdt.","Amtsspr.","an.","an.g.","anal.","anat.","Anat.","anatom.","andalus.","ang.","angelsächs.","Angest.","angloamerik.","anglofrz.","angloind.","Anh.","Ank.","Ankl.","Anl.","anl.","Anm.","Ann.","ann.","annamit.","anord.","Anord.","anschl.","Anschl.","Anschr.","antarkt.","Anthrop.","anthrop.","Anw.","aobd.","apl.","Apostr.","App.","Apr.","apreuß.","ar.","arab.","aragon.","aram.","aran.","architekt.","archäol.","arg.","argent.","arkt.","armen.","Art.","Art.-Nr.","as.","aserbaidsch.","aslaw.","assyr.","astron.","asächs.","At.-Gew.","attr.","Attr.","Aufl.","Aug.","Ausg.","Aussch.","ausschl.","Ausspr.","Ausst.","austral.","awar.","awest.","Az.","aztek.","b.","B.","b.R.","b.w.","bab.","babyl.","bair.","Bakt.","balt.","baltoslaw.","Bankw.","bas.","baschk.","bask.","Bat.","bauf.","Bauw.","bay.","bayer.","bayr.","BayVBl.","Bd.","Bde.","Bed.","Begr.","begr.","beif.","beil.","Beil.","Bem.","ben.","berbersprachl.","Bergb.","berlin.","Berufsbez.","bes.","besch.","Beschl.","best.","Best.-Nr.","Betr.","betr.","Betriebswiss.","Bev.","Bez.","bez.","bezw.","Bf.","bfn.","Bg.","Bhf.","bibl.","bildl.","bildungsspr.","Biol.","biol.","Bj.","bl.","Bl.","Blk.","Bln.","Bodenk.","bot.","Bot.","bras.","bret.","breton.","brit.","brn.","Bruchz.","bsd.","Bsp.","bspw.","BT-Drs.","Btl.","btto.","Bttr.","Buchw.","buddh.","bulg.","bulgar.","burjat.","burmes.","Bw.","byzant.","Bz.","bzb.","bzgl.","bzw.","böhm.","Börsenw.","C.","c.b.","c.t.","ca.","Carp.","Cb.","cf.","chakass.","chald.","chant.","chem.","Chem.","chilen.","chin.","Chr.","christl.","chron.","Chron.","Co.","cresc.","D.","d.E.","d.Gr.","d.h.","d.i.","d.J.","d.M.","d.O.","d.Ä.","das.","dass.","Dat.","ders.","des.","Dez.","dgl.","Di.","dial.","dichter.","dies.","dim.","Dim.","Dimin.","dimin.","Dipl.","Dipl.-Ing.","Dipl.-Kff.","Dipl.-Kfm.","Dir.","Diss.","Do.","Do.-Gge.","dominikan.","dor.","Doz.","Dr.","Dr.des.","Dr.h.c.","Dr.rer.nat.","Drchf.","Drcks.","Dres.","Drs.","Drucks.","dt.","Dtl.","dto.","Dtzd.","dz.","Dz.","dän.","E.","e.h.","E.V.","e.V.","ebd.","Ed.","ed.","ehem.","eidg.","eig.","eigtl.","Einf.","einh.","Einl.","einschl.","Einw.","Eisenb.","Elektrot.","elektrotechn.","em.","engl.","entspr.","erb.","erf.","erg.","Erg.","Erl.","erm.","ersch.","erschl.","Erw.","Erzb.","erzg.","erzgeb.","eskim.","estn.","e.al.","etc.","etc.pp.","Etg.","etrusk.","etw.","eur.","europ.","ev.","evang.","evtl.","Ew.","ewen.","ewenk.","exkl.","Expl.","Ez.","f.","F.i.T.","Fa.","fachspr.","Fachspr.","Fag.","Fam.","fam.","fem.","Fet.i.Tr.","ff.","Fig.","fig.","finanzmath.","finn.","finnougr.","Flgh.","fläm.","Fn.","fnhd.","folg.","Forts.","Fortstzg.","Fr.","fr.","fr.H.","fr.Verk.","fragm.","franz.","französ.","Frdf.","frdl.","frdsprlg.","Frfr.","frfr.","Frh.","Frhf.","Frhr.","fries.","friesl.","Frk.","Frl.","Frm.","frnhd.","Frspr.","frstl.","Frt.","frtr.","Frwk.","frz.","fränk.","frühnhd.","Fs.","Fsch.","Fschr.","Fsm.","Ftm.","färö.","förml.","g.","g.e.","g.e.d.","g.g.","Ga.","gall.","galloroman.","Gart.","gaskogn.","Gbf.","geb.","Geb.","Geb.-T.","Geb.-Tag","Gebr.","gebr.","ged.","gef.","geg.","gegr.","geh.","gek.","gel.","geleg.","gem.","gemeingerm.","gen.","Gen.","geod.","geogr.","geograf.","geograph.","geol.","geolog.","geophys.","georg.","gep.","ger.","germ.","Ges.","ges.","ges.gesch.","gesch.","gespr.","gest.","get.","Gew.","gew.","gez.","gez.Bl.","Gfsch.","Gft.","gg.","ggb.","ggbfs.","ggez.","ggf.","ggfls.","ggfs.","Ggs.","ggü.","Ghzg.","Ghzgt.","glchz.","gleichbed.","gleichz.","glz.","got.","gr.","Gr.","Gramm.","grammat.","graph.","grch.","Grchl.","Grdb.","Grdf.","Grdfl.","Grdg.","Grdl.","Grdr.","grds.","Grdst.","griech.","Grz.","grönländ.","Gt.","gyn.","gynäk.","gäl.","h.c.","H.H.","h.M.","H.-I.","H.-Qu.","hait.","Handw.","Hbf.","hd.","hebr.","hess.","hethit.","Hf.","Hg.","hg.","hindust.","hinr.","hins.","Hinw.","hist.","HJber.","Hkl.","hl.","hochd.","hochspr.","Hom.","hor.","hptpl.","hpts.","Hptst.","HQu.","Hr.","Hrn.","Hrsg.","Hs.","Hubbr.","Hubr.","Hw.","Hyaz.","hydr.","hydrol.","Hzm.","i.","i.A.","i.Allg.","i.B.","i.D.","i.d.F.","i.d.R.","i.e.","i.e.F.","i.e.R.","i.e.S.","i.G.","i.H.","i.R.","i.S.d.","i.S.v.","i.V.","i.V.m.","i.w.S.","i.ü.S.","I.E.","i.Tr.","iber.","ibid.","ide.","Ident.","ident.","idg.","ie.","illyr.","Imkerspr.","Ind.","ind.","indef.","indekl.","indian.","indiff.","indir.","indiv.","indog.","indogerm.","indogerman.","indoiran.","indon.","indones.","Inf.","inf.","Ing.","Inh.","inkl.","inn.","insb.","insbes.","int.","intern.","intrans.","ir.","iran.","iron.","isl.","islam.","isländ.","it.","ital.","italien.","j.","J.","j.w.d.","Jahrh.","jakut.","Jan.","jap.","japan.","jav.","jem.","jemen.","Jg.","Jh.","Jhd.","Jhdt.","Jhs.","jidd.","jmd.","jmdm.","jmdn.","jmds.","journ.","jr.","Jt.","Jtsd.","jugendspr.","jugendsprachl.","jugoslaw.","Jul.","jun.","Jun.","jur.","jägersprachl.","jährl.","jüd.","k.A.","K.o.","k.u.","k.u.k.","k.W.","k.u.k.","K.Ö.St.V.","kalm.","kanad.","Kap.","karib.","kastil.","katal.","katalan.","kath.","kaufm.","kaukas.","kelt.","Kgr.","kindersprachl.","kirchenlat.","kirchenslaw.","kirchl.","kirg.","Kl.","klass.","klass.-lat.","klimatol.","kol.","Komm.","Konj.","Konv.","Kop.","kop.","kopt.","korean.","Kr.","kreol.","kret.","Krim.-Ob.-Insp.","krimgot.","kriminaltechn.","kroat.","Krs.","Ks.","Kto.","Kto.-Nr.","kuban.","kurd.","Kurzw.","Kw.","l.","L.A.","L.-Abg.","lab.","LAbg.","ladin.","landsch.","Landw.","langfr.","langj.","langob.","langobard.","lapp.","lat.","latein.","latinis.","lautl.","lautm.","lbd.","lbdg.","Ldkr.","led.","leg.","lett.","lfd.","lfd.J.","lfd.M.","lfd.Nr.","Lfg.","Lfm.","Lfrg.","Lg.","lgfr.","Lgft.","lgj.","lig.","ling.","lit.","LL.M.","lrh.","lt.","ltd.","luth.","luxemb.",".ü.A.",".ü.M.","m.","m.A.n.","m.b.L.","m.B.u.R.","m.Br.","m.d.A.","m.d.B.","m.d.B.u.Ktn.","m.d.B.u.Ü.","m.d.E.","m.d.F.b.","m.d.F.d.G.b.","m.d.L.b.","m.d.L.d.G.b.","M.d.M.","m.d.R.","m.d.T.","m.d.Tit.","M.D.u.H.","m.d.V.b.","m.d.W.","m.d.W.b.","m.d.W.d.G.b.","m.E.","m.N.","m.W.","M.-Schr.","m.a.W.","ma.","MA.","Mag.","Mag.rer.nat.","malai.","marinespr.","marx.","mask.","math.","Math.","max.","Max.","mazedon.","mbl.","Mbl.","MBl.","Mbll.","md.","mdal.","mdj.","mdl.","mdls.","Mdt.","me.","mech.","meckl.","med.","melanes.","mengl.","Merc.","met.","meteorol.","meton.","mex.","mexik.","mfr.","mfranz.","mfrk.","mfrz.","mfränk.","mgl.","Mgl.","mglw.","mhd.","mhdt.","Mi.","mi.","Mia.","milit.","Mill.","min.","Min.","mind.","Mio.","mir.","Mitgl.","mitteld.","mitteldt.","mittelhochdt.","Mittw.","Mitw.","mlat.","mnd.","mndd.","mniederd.","mnl.","Mo.","mod.","mong.","Mrd.","Mrz.","Mschr.","Msgr.","Msp.","mtl.","mundartl.","musik.","MwSt.","Myth.","Mz.","männl.","möbl.","n.","n.Br.","n.Chr.","n.d.","n.d.Z.","N.N.","n.r.","n.R.","n.St.","N.T.","n.u.Z.","n.V.","Nachf.","nachm.","nat.","nationalsoz.","natsoz.","Nbfl.","Nchf.","nd.","ndd.","ndrl.","Nds.SOG","neapolit.","Neub.","neunorweg.","neutest.","neutr.","Nfl.","nhd.","niederd.","niederdt.","niederl.","niederld.","niem.","nl.","nlat.","Nom.","nord.","nordamerik.","nordd.","norddt.","nordgerm.","nordostd.","nordostdt.","nordwestd.","nordwestdt.","norm.","norw.","norweg.","Nov.","Nr.","ntw.","Ntw.","Nutzfl.","nw.","näml.","nö.","nördl.","nördl.Br.","nördl.Breite","o.","o.B.","o.B.d.A.","o.dgl.","o.g.","o.J.","O.K.","o.O.","o.Prof.","o.T.","O.U.","o.V.","o.ä.","o.Ä.","O.K.","Obb.","obb.","obd.","oberlaus.","obers.","obersächs.","obj.","od.","offiz.","Offz.","Okt.","op.","org.","Orig.","orth.","osk.","osman.","ostd.","ostdt.","ostfrz.","ostgerm.","ostmdt.","ostmitteld.","ostniederd.","ostpreuß.","oz.","P.","p.","p.A.","p.a.","p.Adr.","p.Chr.","p.t.","P.S.","pa.","PA6.10","PA6.6","palästin.","Part.","pass.","Pat.","pers.","peruan.","Pet.","Pf.","Pfd.","Pfg.","philos.","Philos.","phonolog.","phryg.","Phys.","phys.","phöniz.","Pi.","pik.","Pkt.","Pl.","Plur.","poet.","Pol.","polit.","poln.","polynes.","port.","portug.","Pos.","pos.","pp.","ppa.","preuß.","Priv.-Doz.","Prof.","prot.","Prot.","prov.","Prov.","prov.-fr.","provenz.","Proz.","Proz.-Bev.","präd.","prähist.","Präs.","Psych.","psych.","Päd.","Q.","Q.b.A.","q.d.","q.e.","Q.E.","q.e.d.","q.e.i.","q.h.","q.i.d.","q.l.","q.n.","q.p.","q.s.","q.v.","q.v.","Qmstr.","Qt.","qu.","Qu.","quadr.","Quadr.","qual.","Qual.","quant.","Quant.","Quar.","Quart.","Quat.","quitt.","Quitt.","Quäst.","r.","R.A.F.","r.-k.","Rab.","rad.","Rak.","rat.","Rat.","rd.","RdErl.","Reg.","Reg.-Bez.","Regt.","Rel.","rel.","relig.","Rep.","resp.","Rg.-Präs.","RGBl.","rglm.","Rgstr.","Rgt.","Rh.","rh.","rhein.","rheinhess.","rhet.","rhfrk.","Rhj.","Rhld.","Rhs.","Ri.","Richtl.","rip.","rk.","roman.","rotw.","Rr.","rrh.","Rspr.","rumän.","russ.","Rvj.","rzp.","rätorom.","röm.","röm.-kath.","S.","s.a.","s.Br.","S.Em.","s.l.","s.l.e.a.","s.o.","s.s.","s.str.","s.t.","s.u.","Sa.","san.","sanskr.","Sat.","sat.","Sbd.","sc.","scherzh.","Schill.","schles.","schott.","schr.","schriftl.","schwed.","schweiz.","schwäb.","Sdp.","sek.","sem.","semit.","sen.","Sep.","Sept.","serb.","serbokroat.","Sg.","sibir.","Sing.","singhal.","Sir.","sizilian.","skand.","slaw.","slow.","slowak.","slowen.","So.","sod.","sof.","sog.","sogen.","sogl.","soldatenspr.","solv.","somal.","sorb.","Sout.","soz.","soziol.","span.","spez.","sportspr.","Spr.","sprachwiss.","Spvg.","Spvgg.","spätahd.","spätgriech.","spätlat.","spätmhd.","Sr.","ssp.","St.","st.Rspr.","staatl.","Std.","stdl.","stellv.","Stellv.","Stk.","Str.","str.","Stud.","stud.","subsp.","Subst.","sumer.","svw.","syn.","Syn.","syr.","sächs.","südafrik.","südd.","süddt.","südl.","südl.Br.","südl.Breite","südostdt.","südwestd.","Süßw.","Tab.","Tabl.","Taf.","tamil.","tatar.","techn.","Tel.","telef.","Temp.","Terr.","tessin.","test.","Tfx.","tgl.","Tgt.","thrak.","thür.","thüring.","Ti.","tib.","tirol.","tochar.","trans.","tsch.","tschech.","tschechoslowak.","Tsd.","tungus.","turkotat.","typogr.","tägl.","türk.","u.","u.a.","u.a.m.","u.A.w.g","u.A.w.g.","u.A.z.n.","u.b.","u.d.M.","u.dgl.","u.dgl.m.","u.M.","u.s.w.","u.U.","u.u.R.","u.V.","u.v.a.","u.V.a.","u.W.","u.Z.","u.zw.","u.ä.","u.Ä.","ugr.","ugs.","ukrain.","umbr.","umg.","unang.","unbefl.","Unf.","unf.","unfol.","unfr.","ung.","ungar.","ungebr.","ungel.","ungen.","unges.","ungl.","Uni-Kl.","Univ.","unzerbr.","urgerm.","urkdl.","urspr.","ursprüngl.","usf.","USt-IdNr.","usw.","uvm.","v.","v.a.","v.Chr.","v.d.","v.J.","v.l.n.r.","v.M.","v.o.n.u.","v.r.n.l.","v.u.Z.","v.s.Dl.a.n.g.","va.","Verf.","Verg.","vergl.","Vergl.","verh.","vert.","Vfg.","vgl.","vh.","viell.","vl.","vlat.","vlt.","volkst.","Vors.","vrt.","vs.","vsl.","vt.","vulg.","vulgärlat.","Vwz.","vzk.","w.","W.","w.L.","Wa.","wal.","weibl.","weißruss.","westd.","westdt.","Westf.","westfäl.","westgerm.","westl.","westmitteld.","westmitteldt.","Wfl.","wg.","wh.","Whg.","winzerspr.","wirtschaftl.","wiss.","wld.","Wtb.","Wwe.","Wz.","Xerogr.","Xerok.","Xyl.","y.","Y.","Y.A.R.","yd.","Yd.","Yds.","yds.","Z.","z.A.","z.B.","z.b.V.","z.F.","z.T.","z.Z.","z.Zt.","z.B.","Zf.","Zi.","Ziff.","Zool.","zool.","Zssg.","Zssgn.","Ztr.","zus.","zw.","Zz.","zz.","zzgl.","zzt.","ägypt.","ö.L.","Ökol.","ökol.","ökon.","ökum.","österr.","Österr.","östl.","ü.M.","ü.W.","übers.","übertr.","überw.","Überw.","übl.","üblw."]
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
    print("MTUOC_tokenizer_deu.py A tokenizer for German, usage:")
    print("Simple tokenization:")
    print('    cat "sentence to tokenize." | python3 MTUOC_tokenizer_deu.py tokenize')
    print('    python3 MTUOC_tokenizer_deu.py tokenize < file_to_tokenize > tokenized_file')
    print()
    print("Simple detokenization:")
    print('    cat "sentence to tokenize." | python3 MTUOC_tokenizer_deu.py detokenize')
    print('    python3 MTUOC_tokenizer_deu.py detokenize < file_to_detokenize > detokenized_file')
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
        

        
