
# -*- coding: utf-8 -*-

u'''Test UTM function with the C(TMcoords.dat} from
U{C.F.F. Karney, "Test data for the transverse Mercator projection (2009)"
<http://GeographicLib.SourceForge.io/html/transversemercator.html>},
also available U{here<http://Zenodo.org/record/32470>}, file C{TMcoords.dat}.
'''

__all__ = ('Tests',)
__version__ = '18.09.16'

from base import TestsBase

from pygeodesy import Ellipsoids, RangeError, toUtm, utm


class Tests(TestsBase):

    def testUtmTMcoord(self, coord, line, fmt='%.4f', eps=1.5e-4):
        # format: lat lon easting northing convergence scale
        lat, lon, e1, n1, c1, s1 = map(float, coord.split())
        # skip tests with "out of range" lon
        if lon > 70.0:
            self.skip(line + repr(coord))
        else:
            try:
                _, e2, n2, _, c2, s2 = toUtm(lat, lon, cmoff=False)
                self.test(line + 'easting',     e2, e1, fmt=fmt, known=abs(e2 - e1) < eps)
                self.test(line + 'northing',    n2, n1, fmt=fmt, known=abs(e2 - e1) < eps)
                self.test(line + 'convergence', c2, c1, fmt=fmt)
                self.test(line + 'scale',       s2, s1, fmt=fmt)
            except RangeError as x:
                self.test(line + 'RangeError', x, None, known=True)


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:  # get "TMcoords.dat" file
        coords = open(sys.argv[1], 'rb')
        v = False

    else:
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO
        v = True

        # first 258 of 258,000 lines in file "TMcoords.dat"
        coords = StringIO('''
70.579277094557 45.599419731762 1548706.7916191491794 8451449.1987722350778 43.922790121040067192 1.02906022837807180952
10.018893710119 23.313323816796 2624150.74092867098 1204434.0416046227631 4.292619330037266837 1.08605124643084949596
19.479895588178 75.662049225092 9855841.2329353332058 6145496.1151551160577 53.348315487088028046 2.44509802490834298722
21.072464821428 29.82868439326 3206390.6919962592145 2650745.4004060203847 11.666949788578689434 1.12935868700276526857
5.458957393183 36.385237374895 4328154.0835012728645 749647.6236903529367 4.024317088431326062 1.24082851823154139331
70.175453699652 22.865350231728 847598.2665137468857 7947180.9624403351564 21.639091006346664631 1.00839909846273441335
61.965604972549 58.931370849824 2727657.3379737519243 8283916.696409868168 55.690908843041317298 1.09194224601298976532
11.11604988045 20.901069188458 2331001.7518903972451 1313608.2247509045811 4.214689849139200616 1.067599217405929328
32.210543147532 60.705849110026 6035557.2394798919255 5791770.7918786862854 43.698170496647401371 1.48126008977138889627
79.187450900634 61.532382486867 1064553.1258517419121 9417273.7372082489829 61.100379706055074729 1.01347470196600136158
77.103758907396 74.899104969954 1400137.116164341178 9616907.0176860890621 74.527086843388856251 1.02363990993625301115
21.889514024862 80.019885892785 9860691.0166261508479 7433039.1433282732643 65.357693372142649007 2.43897318400097845293
30.53629567699 82.186177919416 8076501.8336948099169 8561614.1747819103782 75.073393190238557702 1.90620203595203984732
49.990484734989 48.203178547341 3335099.8666228919764 6740519.0840148855017 40.611821429856773932 1.13902138155931159626
14.486311853451 80.905136710227 12051574.9284996192629 6587213.0519512810474 59.033236797073779959 3.3574686117030164354
25.936823898765 49.913597662516 5387578.7352981155567 4111216.907168232907 27.574337077887971363 1.37935729177176469738
64.402196051067 64.091394847023 2622214.3802330300654 8678923.9845665762 61.697275181170245505 1.08480957578496618881
48.451353594584 84.856197560189 5068474.169632778036 9492066.9937094951003 83.156739839119105102 1.3299901985118008373
27.203894742072 7.440229319956 738062.0477794809553 3031007.0741158638797 3.416801681625375868 1.00633168074600267019
72.509000485409 78.982283482292 1944413.834565346853 9613299.2244925100134 78.462831057851165665 1.04613441222572206659
41.824953736899 25.39274385366 2114521.4184058719787 4954077.4400978378572 17.571877886939805077 1.05509329051878698199
42.701376407719 7.572738186139 620365.9050898417601 4755542.0265620241836 5.152021939103753522 1.00433819291969569998
40.552052236608 3.10605643618 263004.7709889716198 4493669.7624508701848 2.020523080004668331 1.00045152537558245158
3.501241735308 27.806507229666 3217221.7394620754606 437776.1191609587993 1.848169127986085672 1.13055811977484279446
10.148714782203 85.373767569431 14661142.4449607145297 7476100.8241849819567 68.376669038799719822 4.89664968310721668858
58.582623413754 16.755557927357 967777.1585538550834 6615684.2665918122107 14.410044184805568143 1.01110049967174710461
19.793004266049 61.746763253022 7558840.7284607307613 4144728.1307639004491 32.557263709306064222 1.79148974312616264707
78.666776295717 56.365355032529 1056008.3141606622993 9290799.6926694787804 55.843278085670068777 1.01325308986429560329
11.99878827065 17.597873384909 1943965.1346867432457 1389972.228689978338 3.774868749144232083 1.04672441163442516954
32.540378157921 58.764613204285 5803077.0729023443587 5649957.9436588808605 41.717942799520694469 1.44257204179252015685
45.160355715851 37.465284907696 2928716.9860089971354 5731835.0583167290719 28.538550438111537283 1.10677992098177181933
79.584190378868 16.367006094695 326141.9757557496954 8881325.164542603823 16.111414681359673051 1.00089993942341181312
52.470664133515 64.125580446166 3933015.2674496992268 7932373.9095122782833 58.577423527128429231 1.19481101723429277124
23.702672650774 72.630363287434 8598926.9832129798489 6214135.1675031200387 52.612877781738863878 2.05136696382462895237
32.603520070077 67.280123028581 6620553.3337715800496 6540527.1229476324152 52.3501400177981775 1.58661390145658678613
33.776224430873 16.280993301103 1515136.7582917435602 3858996.0875369629012 9.225127467948732285 1.02802878359903348214
79.932747307768 25.363621893141 479854.3734451901139 8980501.3898956884036 25.021222386954738067 1.00241454728029893439
.935055560116 42.53882371151 5243446.5649397923937 140657.2139601745984 .862816875528843911 1.36035750366692273797
13.490862440668 83.178380075606 12806457.9232176809509 7170118.6846750266674 64.708921319446620085 3.7405880916836789809
48.979056611144 16.474541916245 1202993.4591584864223 5557316.0535990491813 12.579061086594141623 1.01742642054231242781
65.03601551382 38.72909058624 1729088.7101955880128 7770874.2899540818008 36.021783497671091455 1.03639655778420600386
45.510091059252 31.303728868569 2437301.5174252324938 5539327.7483181566592 23.461878886124479373 1.07345865279937953966
16.058009627762 32.520026226815 3647186.1350656452881 2086412.3309827435192 10.023991299493014563 1.16870736569005615013
36.84520033941 20.282283332283 1818497.2435558675661 4275471.7450572589369 12.499655874401409124 1.04060375620579838882
37.865481186501 41.990401524014 3751304.1137831969124 5130454.0015917055942 28.959706974035481776 1.17768130761447297485
3.28727188791 22.917603895056 2616733.138544322417 394644.4638147892681 1.390425099091137669 1.08559457351075303955
47.813685905876 23.545092456754 1756506.5739421266743 5570393.9863943798503 17.89789444055791977 1.03773249943759836051
22.836853045404 72.604384975988 8752461.8947109875583 6087728.1522842465577 51.628464534451266003 2.09546464339560774477
.527262488978 11.684209132768 1309272.2164321123566 59520.0288993871333 .109069182167531056 1.02089660980397436268
20.166741997072 3.143947731274 328652.2771294843991 2233043.9588736710395 1.084863297347176706 1.00093521803437134364
28.604629015528 85.988721094779 8637959.7164470998207 9190635.1560309800028 81.802562643198123218 2.05432863342852874819
28.984047991106 85.833447775172 8548521.4551470334531 9172410.9432821880799 81.583928102890161419 2.02964145862183583179
68.071020468737 19.392822879186 796987.2811043724991 7677446.3576754183788 18.084471771162892811 1.00738114483985271123
61.416576191872 81.981611413918 3291036.4967623295988 9513199.6006662170596 80.890253980644739593 1.13482563910814382209
35.074753204279 79.496002969799 7087225.3309060931216 8382823.8558221762359 72.25375612182016949 1.67806984242534083556
28.078789930145 48.684349570647 5090358.1257235686008 4318294.1334886064437 28.266280188302695739 1.33626407173290792824
84.986930137199 2.067177857261 20163.0752214330146 9438635.9888499043815 2.059277291707588222 .99960496589466017622
28.473948268025 34.12730567449 3447670.5507847334006 3680238.888222715322 17.934947982475010676 1.14983099536013499926
56.629353655336 62.196473719193 3396522.9067977887178 8093659.6875928252142 57.747116822698645359 1.1440063909987750803
4.747761773803 70.932554556127 11249894.1007840611758 1619226.5062987145353 14.210358187648878999 3.04834698412044976957
35.882112501618 76.741848750875 6808805.23095023548 8044779.7773693533498 68.242008178358314082 1.62146359128641854174
6.42070482504 20.416028355525 2306021.5565059955892 757191.5928659006169 2.385685550799879322 1.06615932703313059382
52.335248167422 22.879293778793 1547406.3138615646706 6048712.7518236823564 18.474372076286182044 1.0291226350124929634
59.846390709402 46.262536374951 2430467.6503829496158 7557167.6139715559925 42.110020812285922144 1.07275901175575821842
16.461790285243 21.433269186661 2334053.9058301522643 1948076.9665824793916 6.353185129915976783 1.06773282981445423028
11.707905244928 45.827075179052 5564175.1867374906587 1836851.6604118701417 11.870682401525300151 1.40826542507146242973
38.519075230481 71.935917931082 6118505.5903586656687 7631684.5524210322411 62.477323370615224648 1.49341988810791699
34.264007222954 82.647878110272 7365359.2946646287171 8818194.4515306837741 77.207042218974141605 1.73763853091849729372
19.376879758731 .344604702538 36187.3424147238117 2142565.3248023055831 .114334366652574163 .99961618629427946552
65.075805475982 57.653438169334 2380328.5468508919474 8440109.8723841409767 55.076066661701381469 1.06965834492909651546
78.691869858364 27.591736411927 582511.6088260822781 8876047.2170705300021 27.133299634302376408 1.00374884070881342847
40.893022388204 10.668803645636 899441.3504769787009 4582046.4305161929187 7.031211200325183102 1.00957251523499968837
48.914278679322 87.35926802682 5022485.1243369246483 9741774.9337207800497 86.505947369926030588 1.32369954850478170836
16.208377106594 54.494282151347 6701004.5872038334316 2954368.2582310730947 21.560152646875578 1.60855373936651177994
43.977935890852 5.672541129169 454986.2188972515956 4885087.8878842827264 3.945648021963556589 1.00214702964307690511
26.850860749352 82.834479937822 8903956.1403106503714 8470608.5774824981183 74.723116471645531699 2.13131124920824155268
52.234164942694 22.827654621252 1547627.5947405022567 6036584.5383472499045 18.407628762946557814 1.0291318457152898605
11.674645926334 43.500147485032 5221488.7785972672924 1762592.0443920618937 10.927880117548569099 1.35672143999466385616
22.49275252749 44.179153244168 4880570.2971608056244 3325433.9888672882599 20.469862411706803346 1.3084757212046467219
.910999463005 88.548822916123 23930680.0826936110445 7491462.0990379651261 75.937628056628715446 15.55636485152285563369
33.028801664026 .765842683855 71519.4504575306802 3654740.4448518867014 .417448360256695198 .9996630662116279997
50.649194793146 64.389075825035 4152797.7952199466443 7823098.5027514052623 58.238900518140347763 1.21805179919494488513
58.820639878533 55.841047796984 2926725.7076386952317 7904918.0728436936236 51.592748230544387725 1.10620560258341567775
77.86576233957 76.414618233373 1325509.1138687410279 9675214.9482134019947 76.116212990328245516 1.02113632957426301409
4.389639152193 26.458976490586 3045296.4489264779145 542153.443280018004 2.185095458409962455 1.11666391460268667495
13.924448317313 79.017873037038 11843870.8875184068712 5912803.073342800756 52.814259465980122311 3.26725623456589470495
.679713299722 62.036791960028 8891099.7049355983737 162160.1422267625235 1.312094322525505534 2.15736251126013465557
20.478280678952 42.678233741598 4784814.2144494965077 2984497.432579909692 17.946544510697015083 1.29611569101488809107
73.695702778891 74.259097009997 1772074.6821540221529 9491552.5601429632962 73.634829544651613543 1.03820223054775212902
58.569370243141 33.777549098621 1907649.7821061786815 6994232.4293791756103 29.718928505880864701 1.04450291519041301412
18.933880535395 19.492695056232 2084423.8189620029383 2211816.0356192490603 6.556448180639453111 1.05379306456956292405
68.317934453741 26.515687019151 1064373.6717288683288 7812482.547460769636 24.874124026895538133 1.01348961758472755197
50.641941364984 87.111556505544 4770385.4792965339274 9734318.9029801439364 86.27311877223132818 1.29055338238288419467
24.411297840798 56.88182311078 6398096.6772973600439 4410894.7521038311977 32.558023304777286275 1.54800368213678933224
24.571871102264 30.073097169764 3138623.3004145471641 3082960.6007977759991 13.557671585295237223 1.12372399807947897752
34.20257557563 29.383165969835 2748325.7946509686296 4202811.912667864605 17.578705709567679327 1.09410195730734136777
27.756284848275 61.881904854712 6677830.6303670122334 5350071.837395327614 41.306641371021023125 1.59977445641749126253
19.74226995492 50.957821039519 5941536.6674313585796 3293112.1751404267828 22.752845451823778194 1.46847293646826714846
45.453581601033 40.659833471976 3152481.7925671135891 5903048.8379780052155 31.494605530298385784 1.12408455578287267344
8.322143510836 69.488157190493 10460475.8977297807162 2553463.624390859904 21.965868544314762363 2.70029645950992131633
47.749830606963 26.322001579253 1964010.7780209841382 5634042.9230556657743 20.117800254064358466 1.04734380074617176454
18.297492825554 19.244669003371 2065306.4249344182821 2135008.4686507365035 6.258980787330580674 1.05280028635971539682
40.834540746347 61.650750017598 5127738.1329756395441 6793804.3044111353216 50.557914709602202724 1.33941150728477513513
26.27324746762 74.926694319674 8385525.1481661815737 6924932.3443060878421 59.087561176849211121 1.9903641945426514594
23.698347493871 22.155656995693 2297510.7919089474927 2805666.9628340797276 9.30155297617018372 1.06550832603200218621
12.364112546807 86.348578425071 13749544.9176345767153 8288728.3846500523233 75.033969786420407131 4.27058754359004466627
9.916090592983 2.895277339837 317518.4555464869534 1097517.5837454216348 .499003720919636014 1.00084775964536943313
56.553876228037 78.215077042034 3856035.1848884240006 9141364.4502903059687 75.972762873607038529 1.18678624695045238303
75.957630588142 67.407382685044 1457484.9428227196297 9385297.1019733464598 66.784661729241963706 1.02566019553942792804
31.826530823362 13.731050162682 1304934.9018412828799 3604655.155715481906 7.343988561535999759 1.02067230331888663326
70.542985267281 40.282054589142 1399093.4917923557236 8314607.120342236932 38.630161278888698433 1.0236249515019550137
38.617487254111 4.099838486616 356983.618539634654 4282309.0489941972154 2.561484750887838159 1.00116967656345686077
5.389446869748 66.729612162904 9952911.3250914975731 1510288.2122287705261 12.752154123386704553 2.51135680697119678551
6.995168275875 50.014762673612 6367592.5040067391371 1200437.0776723467399 8.338041363617584015 1.5462097188295546001
42.32189384152 53.784040052344 4391263.6764595202809 6325455.989407695451 42.653540961791053971 1.24556015758625337757
12.698514957503 50.242046782422 6209880.5275270171723 2154754.4497471950918 14.919512494122454149 1.5165601290898930918
54.207636072355 23.325730771441 1507053.6887724474652 6261383.5132798271265 19.280372700853517863 1.02758396387063827962
13.224786669751 62.426697605612 8332725.0037766352019 3002712.3297530032296 24.059211770061643256 1.99044967828556833824
25.650281524787 37.710390879145 3958910.0852347261854 3462284.9261024711771 18.546398104130172202 1.19935066297013315842
20.684773383075 82.849734261238 10452892.2820830090734 8000059.6051139389546 71.07524025411428855 2.6501109339363854772
57.367533447896 8.260865981663 496148.2537306291007 6388503.3650426645438 6.970955082495557851 1.00261965657610768433
25.958756519165 65.760477206515 7375792.0858501333485 5544624.072155191546 44.510851262372117173 1.74589815151284094781
41.395847513261 33.661790413276 2826258.0419787338802 5167759.8169594580007 23.783897043835053021 1.09941471776423452703
54.266617122219 70.602199344259 3958563.3788510011838 8499923.2312431065963 66.570944905261286671 1.19729647829139513622
49.840392952501 68.036727864486 4408189.5334624673805 8046312.0036419493641 62.216958843252958235 1.24674966630032523203
46.306035173144 48.085828071782 3629225.6275122633607 6371258.4546454462175 38.881674764054976478 1.16551075937682077929
43.570988154502 7.46449391571 602838.450710449767 4851370.6372051615015 5.160395241581517306 1.00407312998832083041
19.427290417638 7.268247299591 764616.6650506681717 2164299.3379453227242 2.429300399613599967 1.00683508317252458097
12.713793748691 42.507018471253 5048953.0219314851332 1885974.0573976666868 11.459803714497619668 1.33220663200426135551
20.238782471807 21.566067847502 2293996.6011553478844 2392408.6442210939576 7.791837899898628743 1.06534808910887717165
62.367847456811 30.43884908056 1530603.839417656944 7287841.4598977046908 27.502921059804991696 1.02841626834792068661
41.891568633612 31.959547272043 2660000.0931521348398 5161982.2132484260178 22.629836281156892582 1.08785143983905682151
47.664247649433 77.630061639566 5037478.3294144716228 8768172.3799078950489 73.511182499373789255 1.32591926229798518833
67.2595593736 62.71529258458 2289650.95779913061 8784328.5936072402413 60.786067001346348057 1.06434628696322565557
60.295380699684 11.763096536191 647913.8897442235616 6742382.2282168677249 10.252667402382069508 1.00474800452158321223
76.878914074271 49.685772707959 1118372.6985656095089 9040627.9422628652853 48.936802955632901532 1.01491963932848643155
49.495348846691 6.087551111735 440696.5100700030027 5500355.8262971466109 4.636103927615996534 1.00198639702101890472
80.297265209749 33.816371631992 601728.1497271233657 9095352.0481485300158 33.435771182948412959 1.00402665627010237281
2.286436766954 29.855148933378 3481444.7778274356602 291665.7087491972233 1.314726047860802375 1.15353417379878877774
11.264456523809 30.743906888841 3515304.9015238188873 1443981.8829184631458 6.641637995051852051 1.15650928833492118964
35.434073450488 1.762794707137 160012.1869587518858 3922609.2532306700222 1.022225124144958262 .99991553289064298164
6.923694525049 35.289455784944 4163744.2456224223412 936884.6748035344939 4.89255872378144431 1.22216428398585218853
36.129671646557 67.533176237312 6155200.0179262357161 6926306.6283897454627 55.103257728863139942 1.5005557389379217801
4.406528980638 81.965734206053 16263383.2854400911299 3591296.7313406507021 36.040254103487111035 6.58928781751888396522
8.474589009114 81.129945130597 14220995.5153984992101 5100587.4575033509156 47.314258427760984573 4.69320221531225352172
53.9072758977 51.252904494063 3173034.8023721438908 7263421.9429571994497 45.215808095130154586 1.1254103499728070173
22.120544817855 85.756781608119 10253274.0922039670098 8867574.2997916978265 79.198250285604314115 2.57237240666878171579
66.444099685789 64.532959623888 2415561.4832300277853 8813225.2170972443615 62.548978471128893639 1.07174792673045743011
6.670965383497 65.660407658138 9589179.2932946116388 1777680.7841433564398 14.838482736502380244 2.38071598202088822511
33.054056916574 7.787458413753 727939.4383912861907 3684363.2368099898959 4.266227267489998418 1.00614020225651810072
7.03552544447 11.253707285756 1250765.991085162047 792869.242718733336 1.396497323452689659 1.01902556917615578856
44.971340061426 9.009304223525 710421.7058868297322 5019406.0759277693493 6.39394902348355911 1.00581176650310200228
30.821397273114 45.970576586721 4600995.0746431898409 4505712.0845933605189 27.997457530594202466 1.27184146679060042739
62.763886473774 10.960144152175 557642.6277821351813 7006911.2516444447618 9.769902837537033542 1.00341081628731571164
18.888610683787 41.009871020315 4635062.294290666664 2702556.1533113415592 15.779546941050109522 1.27717838268611630498
7.524119461376 81.050715469439 14554962.2559189870471 4716639.9085720199214 44.192751352918149954 4.96001986321419027847
70.063902088267 23.705255280431 882126.661735638301 7947612.3695055354723 22.429486595349178622 1.0091317513017451276
3.556525834215 88.363529198819 20262021.6459832969292 8113827.8207957955275 76.936057264555500879 10.34909168211805703369
34.551256940467 69.111090740792 6500508.3998499190022 6956476.3423679842735 56.237115700755496095 1.56316164401685017241
47.929051428655 54.103418434236 3884036.6413140485904 6890167.4117333333762 45.760130455073278298 1.19016705049074162293
55.753535712331 3.471798114123 217855.5460780085389 6184108.1225681774287 2.870992737838008847 1.00018219161553870971
18.530847071862 86.555312055898 11384139.290401676268 8893889.9495562311576 79.77485364572019046 3.02467156922968230025
54.51012548939 58.556056134661 3469855.989804779935 7723193.799228055759 53.114700483137237471 1.15054018967525499602
42.864161881687 84.866325602975 5926165.994939154109 9385463.7327467371322 82.506981261616342016 1.45975761947329382411
30.911943481323 57.114101855719 5798639.6622244850132 5305387.6409164746931 38.617257368242120557 1.44226267698891684426
58.542492989325 .162592684741 9464.9343875445955 6489121.6249442771542 .138696123095078659 .9996010981636145684
15.022689088683 85.792615487152 12575834.2756139069875 8356610.8954857643175 75.235223160840771295 3.59944161831319404851
65.692275101448 77.241377062715 2719653.543469453487 9362389.163494812678 76.049669860936597376 1.09131485659964876498
48.806211025007 76.486364889518 4845341.924698123028 8710522.3269010880979 72.320942261938292347 1.30038173928117133974
56.436024794624 82.61156798689 3935261.5227628794258 9454271.6490618694486 81.162334302626197333 1.19476734082123451158
8.766053048623 54.367539445614 7074299.8229999322031 1648736.0650554142139 12.145925189190523145 1.68755130286482068464
17.095494987028 33.059128480797 3689072.5793081136744 2230802.665210606288 10.856247689039007266 1.172689254381165737
22.142861155811 67.200684381182 8102565.8855870031253 5167396.6175796945199 42.324885914448306908 1.9219274646958517469
19.222622658932 65.180784834064 8181271.3535636852753 4425436.5471854103601 35.900845441172145359 1.94501710140275939189
33.182473524247 8.216951902375 767067.394002692496 3701745.8572961374759 4.51920087574012941 1.00686283543265220857
11.417962794215 52.808690576538 6688114.1685717468661 2052857.2996385244734 14.766190785695058024 1.60720037033586573011
23.836687975833 50.500179576009 5608408.7737612426501 3859055.6591101537216 26.244150765445430928 1.41346329021445609204
45.550019860279 50.14803591077 3836942.7652752247224 6415467.6343256756272 40.575884932620234329 1.18561510259200656239
52.74607907826 19.343926388799 1298730.3660248456423 6021453.0007924546626 15.61331972872290951 1.02036705756269413871
65.513347930022 9.039528600078 416934.2892077992663 7295683.4517048496437 8.238231681111888838 1.00172869465579164901
48.709795163906 63.554005498623 4336076.8508893208355 7617975.7227786210095 56.53708844224499691 1.23858191461628412453
19.753508884702 1.603846135125 168047.3369803282036 2185000.046530304967 .542186563040675395 .99994905785319155467
1.20281563245 59.377275851199 8276281.3287903988364 263444.3505446412864 2.071435348100689305 1.98031420974262704294
42.564974643093 59.356947122688 4772573.8107103474239 6765710.3360024941148 48.857561258189057019 1.29191121145283131016
10.090572450083 44.604132315642 5427755.0746387213808 1556055.8209236854074 9.862177972083542442 1.38739359283613734884
14.133028449482 78.097533396115 11588458.6160411409115 5707993.9226125151612 50.784827016461182713 3.14956744637764457506
4.031123274 54.048782203105 7152433.8026883113497 761390.6958441980795 5.607350212971261226 1.70526145367652322678
62.746603094236 79.968640698878 3105651.3909011889729 9426026.169064495616 78.750206331373698422 1.1197368650353186846
60.626429309951 61.851551200568 2959009.6390219621423 8339242.2692824755336 58.460864592396548599 1.10855399347957011951
23.600626307178 72.811633889695 8640472.2671449642382 6230320.4179312077616 52.816810016658736762 2.06297336227917101194
82.572235784013 77.402323331121 811352.1089323540173 9816129.813480900982 77.299183800337734488 1.00765089959951951668
6.030050581949 50.783504648331 6521874.9734575493479 1053612.4797442143876 7.407328325531892571 1.57552927490754724882
42.411522802341 42.258009167689 3477983.9978745138452 5651613.3259470101084 31.530672987296576972 1.15187476329973936765
29.526119573162 6.49306920517 629892.8222431609312 3283914.9104510948801 3.210482004553411381 1.00449937658081974569
39.021852555506 38.64177900453 3381879.6872268223164 5103629.3256646459488 26.748108324630378211 1.14355942712754379458
64.971849693 78.151893481622 2815986.5341766402522 9387029.1207183539003 76.967261983821977885 1.0980320958404978263
59.961819383357 76.473421916083 3398195.8896027542059 9138936.0314903480334 74.477498798722526602 1.1440087531530389723
41.374039662563 28.848343380399 2421734.7546371300191 5002372.094990707966 20.017081678810957981 1.07259228948474384177
68.946086784215 79.574522659006 2360869.8955247775101 9553298.4495364430773 78.848204601472288619 1.06845342678358744205
79.275096210569 83.551272329394 1196539.9721941076965 9861920.8362302532842 83.437668440198132309 1.01713723718699411107
21.00025216114 12.697444145976 1327758.7047952488776 2375509.2416830163028 4.617571985370999766 1.02146477826651065683
68.015226658605 56.732418805889 2070860.3276435193044 8604500.7195812988461 54.722761328920499997 1.05246941876679550946
37.423674968963 76.947359213963 6564776.6548642858201 8171207.1773792722081 69.237522745576966155 1.57389402814129411208
54.922706739174 9.260818037311 592653.5538208670326 6125529.8100517279554 7.600784978354020046 1.00391174097748520221
61.982810332428 13.299659317104 693459.6718213818294 6943779.9910315244271 11.787586852381879951 1.00549585710526849984
30.324214164174 18.95976913715 1838956.1876248715618 3511959.6123814068572 9.844313438294355647 1.04160310725478373473
37.629667084297 49.649130811064 4460690.8845966838252 5541873.2354029792273 35.768612643971450111 1.25417856143495034578
69.225574124261 77.656135038343 2311168.9989410427594 9480561.8691194226305 76.828257327042052528 1.06555550830984186384
44.698477679082 52.979304033315 4111775.1144506591286 6509014.34879221625 43.052129903922234176 1.21412520026532777805
69.499593633291 1.928335626092 75358.2619616238705 7711258.6622510055509 1.806297402204658786 .99966947406657274597
27.981363604998 86.061112755721 8781885.2291162503299 9184776.4522114918448 81.795538514711932534 2.09490761781464961377
65.699838958157 21.104724677749 954378.415174206079 7449110.6698066379025 19.380657249577556028 1.01076790612075854417
47.143647786825 9.512189225272 720971.7937060109688 5265195.1215547760107 7.002994879368465904 1.00599450857948113857
8.920166746304 5.101512904759 561561.4939374572189 989910.2362210683617 .793118092514896753 1.00350496287174529381
59.778971443417 78.080321923984 3446829.6344680763077 9232868.1556635258258 76.279074811621407782 1.14826328124958159164
55.865310107291 87.384288430943 4048307.5459092527942 9800416.4229977935137 86.843918034217523739 1.20649504624906774925
24.310972620263 76.823776927159 8973188.4802934670189 7042230.0870214786274 60.872455730741034486 2.15609754083154148987
3.58204121273 1.137286307295 126314.1916179008865 396006.6879211498981 .071064512019013209 .99979750106848045799
46.124232899607 77.313118243239 5247652.3456465087758 8670513.3597516003913 72.700498211859798231 1.35527175380864724565
31.17139056295 87.104503768139 8103656.8381187232079 9469794.014736839373 84.490673011906282841 1.91216400164486142107
.553170847481 49.117104423642 6300112.7582358087614 93835.917364330774 .644804518587009776 1.53407289319208408993
35.361587058134 41.860599406739 3894813.5937815908838 4833832.3410270198018 27.453297917146541997 1.19213517510824943619
31.750313985725 4.2481669819 402511.3467124300447 3520621.5619106356485 2.238473873171145824 1.0015987516192805961
17.924336382444 46.096401879115 5357378.5031484014897 2772997.6022343006705 17.823560123150715559 1.3760313482865829253
60.93148826873 58.221214091933 2807553.985865849925 8177847.9802750533299 54.680044767243502309 1.09753087110632478314
5.358150979521 87.556213284144 18289045.16650076146 7792942.3396035398889 73.216494415207315628 8.09800850850277481729
28.616673489124 80.452426461437 8376822.4595378634541 8128174.6238782329989 70.920116640676321501 1.98487312027093768388
11.709762713844 76.76029473875 11898068.3532717452677 4772439.493697450272 42.613968390266890749 3.31441188528359472753
12.009497822309 71.782350911974 10550946.9390504663061 3851968.8152950466266 33.383025340643754993 2.72475395098346736944
37.62978386356 85.795687334213 6828299.1236065501034 9394803.2274626281036 83.181386462369626591 1.62435875189611017521
7.721127951451 71.662730825344 11162550.3340223216379 2640267.2795929572988 23.145403728553680897 2.9984080097281902618
34.295025633828 46.442191339458 4411584.4479407645043 4956173.6944069178108 30.713918710252302272 1.24873566005930301271
42.622496157528 8.193605260546 672108.8979047416191 4751554.6570537128986 5.569178495150195348 1.00516237476077590859
41.667779769016 61.518287698071 5022964.2905788176273 6860418.1995022955836 50.862229638446081312 1.32492457134934124443
36.060369077115 18.444112270623 1669655.5952065894204 4152086.5370207665606 11.110236960128259085 1.03413776443206420354
27.948090550481 56.816429243836 6055876.7296551104864 4896837.5526193317564 35.799747003161249681 1.48596684753865910284
63.386029820146 24.662716065038 1209214.164379140446 7266409.8591775283149 22.319632705363371281 1.01755357711026002199
4.68092204293 42.114426024981 5154564.5595835170479 698118.3499747117951 4.242359757630121766 1.34748098807212642544
61.826624569709 57.525095752371 2695149.8065425071908 8208197.765605494917 54.178615016022205573 1.08972999788265824831
25.104353060784 32.528660477914 3394792.3278196264635 3217583.4155517515191 15.165863193990857289 1.14528478584558078423
69.678351026027 39.275512777413 1429160.9669848868208 8212685.3620316119996 37.484903790606035469 1.02467583111433290394
29.671383681805 84.19659549085 8343387.9980651104898 8885196.9545780118644 78.561937382568633298 1.97473261886829061763
62.300207596594 40.474050846282 1990722.9286056967338 7569202.0651622239222 37.075276428875924023 1.04848569035674592378
12.721775625713 14.19000340868 1554980.0995591305952 1449423.9195855762854 3.188328226050696487 1.02966384266140977388
49.811296434482 10.925010729071 785205.4501960671258 5575158.4230962316151 8.388417204407732086 1.00718127027442280511
45.132680485087 42.478624119594 3310405.9883131323503 5955022.2338814200249 33.007586777459435385 1.13714097985385542068
.904279361648 39.078411665769 4733460.9606659335466 129034.8898158858145 .737551493227957266 1.2904394895705916755
30.163605012904 33.577996163511 3322708.343909214722 3864738.0787416917819 18.472565938696923191 1.13883761185498551135
27.643243707755 81.892859091432 8672864.4172042475623 8333465.9834441061554 73.206272638168122883 2.06544053870286774312
18.201207657521 82.434617649311 11126818.23119627031 7618712.1749910723126 67.88717347393512063 2.92241673495261070414
28.804576432117 89.886072420251 8650100.9817967479337 9975084.1689971279206 89.767446308690086924 2.05728879562910108817
5.542997543365 19.589578015412 2212701.1801922521748 650348.1002291364067 1.970441347893608046 1.06082971035302853684
34.237147232655 73.678164431851 6890222.3266181808204 7506813.4995466613258 62.684825342605895137 1.63848831967028469855
22.704949386668 57.877009924539 6692260.0673245543216 4244174.0081103084813 31.81292024414934456 1.60464028065919297249
42.192424494362 14.828195694778 1225564.1371902108879 4778923.9241444004467 10.08341913141319719 1.01813429638637496502
11.481151181645 78.189236347565 12341116.1549503000916 5081855.5219659557156 45.712545623618863671 3.53517039848850746171
6.609625778315 51.735782590089 6673845.0217707773023 1177587.1905652433534 8.389140750220349367 1.60517112128624127574
19.059369023131 57.52643949087 6966354.6904170428304 3641802.0050929558396 27.409635588911986928 1.66146945739340651918
'''.strip())

    t = Tests(__file__, __version__, utm, verbose=v)

    for n, coord in enumerate(coords.readlines()):
        t.testUtmTMcoord(coord.rstrip(), 'line %d ' % (n + 1,))

    # XXX Pythonista run_path doesn't reload modules
    E = Ellipsoids.WGS84
    t.test(E.name + '.KsOrder', E.KsOrder, 8)

    coords.close()

    t.results()
