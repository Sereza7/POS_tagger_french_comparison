# coding: utf8
Data="admirent : admettre / admirer;affiliez : affiler / affilieraille : ailler / aller;alliez : aller / allier;assène : assener / asséner;brouillasse : brouillasser / brouiller;bruissaient : bruire / bruisser;chevrette : chevreter / chevretter;choie : choir / choyer;clamecer : clamecer / clamser;coloriez : colorer / colorier;comparais : comparaître / comparer;convient : convenir / convier;crevasse : crevasser / crever;crûmes : croire / croître;cuite : cuire / cuiter;damasse : damasser / damer;distanciez : distancer / distancier;durent : devoir / durer;débarrasse : débarrasser / débarrer;découd : découdre / en découdre;décrue : décroître / décruer;dégueulasse : dégueulasser / dégueuler;dépariez : déparer / déparier;dépeignaient : dépeigner / dépeindre;déprise : déprendre / dépriser;embarrasse : embarrasser / embarrer;encrasse : encrasser / encrer;enliasse : enliasser / enlier;entasse : entasser / enter;faille : faillir / falloir;feinte : feindre / feinter;ficha : fiche / ficher;fondaient : fondre / fonder;frimasse : frimasser / frimer;frisaient : frire / friser;galèrent : galer / galérer;gangrène : gangrener / gangréner;lacèrent : lacer / lacérer;lisère : liserer / lisérer;manièrent : manier / maniérer;mirent : mettre / mirer;mise : mettre / miser;mouillasse : mouillasser / mouiller;moulaient : moudre / mouler;moulurent : moudre / moulurer;murent : mouvoir / murer;musse : mouvoir / musser;médisaient : médire / médiser;médite : médire / méditer;mégissaient : mégir / mégisser;méprise : mépriser / méprendre;obvient : obvenir / obvier;officiez : officer / officier;ouvraient : ouvrir / ouvrer;parais : paraître / parer;pariez : parer / parier;peignaient : peigner / peindre;plu : plaire / pleuvoir;pointe : poindre / pointer;pressent : pressentir / presser;prise : prendre / priser;pâtissaient : pâtir / pâtisser;radiez : rader / radier;raille : railler / raller;ralliez : raller / rallier;ramasse : ramasser / ramer;rassis : rassir / rasseoir;recouvraient : recouvrer / recouvrir;recèle : receler / recéler;recèpe : receper / recéper;refondaient : refonder / refondre;remise : remettre / remiser;remoulaient : remoudre / remouler;rengrène : rengrener / rengréner;rentraient : rentraire / rentrer;reprise : reprendre / repriser;revirent : revirer / revoir;revis : revivre / revoir;revisse : revisser / revoir;rira : raller / rire;rêvasse : rêvasser / rêver;saura : saurer / savoir;sommes : sommer / être;sue : savoir / suer;suis : suivre / être;surfais : surfaire / surfer;tapissaient : tapir / tapisser;tarifiez : tarifer / tarifier;teinte : teinter / teindre;terrasse : terrer / terrasser;traite : traire / traiter;traînasse : traîner / traînasser;tue : taire / tuer;vermoulaient : vermoudre / vermouler;vernissaient : vernir / vernisser;virent : virer / voir;vis : vivre / voir;visse : visser / voir;étaient : étayer / être;"


tags=[]
estunvb=0
tag=""
for charactere in Data:

    if charactere==":" or charactere=="/":
        estunvb=1
    elif estunvb==1:
        estunvb=2
    elif estunvb==2:
        if charactere!=" " and charactere!=";":
            tag+=charactere
        else:
            estunvb=0
            tags.append("V"+tag)
            tag=""
print(len(list(set(tags))))
#print(list(set(tags)))
tags.remove("Vassener")
tags.remove("Vasséner")
tags.remove("Vchevreter")
tags.remove("Vchevretter")
tags.remove("Vclamecer")
tags.remove("Vclamser")
tags.remove("Vdécoudre")
tags.remove("Ven")
tags.remove("Vfrire")
tags.remove("Vfriser")
tags.remove("Vgangrener")
tags.remove("Vgangréner")
tags.remove("Vliserer")
tags.remove("Vlisérer")
tags.remove("Vmégir")
tags.remove("Vmégisser")
tags.remove("Vrailler")
tags.remove("Vreceler")
tags.remove("Vrecéler")
tags.remove("Vreceper")
tags.remove("Vrecéper")
tags.remove("Vrengrener")
tags.remove("Vrengréner")
tags.remove("Vrire")
tags.remove("Vtarifer")
tags.remove("Vtarifier")
#print(list(set(tags)))
tags=sorted(list(set(tags)))
print(tags)
print(len(tags))