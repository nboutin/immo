#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.join('..'))

import unittest
import json

from factory import Factory
from rendement import Rendement
from database import Database
from impots.annexe_2044 import Annexe_2044


class TestSimulationA(unittest.TestCase):
    '''
    Source: rendementlocatif.com

    prix net vendeur: 50926
    prix (agence inclus): 55000
    frais agence: 8%
    frais notaire: 4936
    surface: 45
    loyer nu mensuel: 440
    charges total: 1100
    dont charge locataire: 25
    taxe fonciere: 800
    vacance locative:1/24
    revenu: 31400 23000
    part fiscale: 2.5 dont 1 enfant
    tmi: 11%
    apport: 0
    duree emprunt: 20 ans
    taux: 1.15%
    assurance: 0.36%
    frais de dossier: 550
    garantie: 1000
    ---
    rendement brut: 8.59%
    rendement net avec impot annee 2: 3.61%
    rendement net charges: annee1:5.6, annee2:4.85%
    revenu salaire, revenu foncier impossable, deficit imputee, revenu net impossable, tmi, impot sur le revenu, part impot foncier, prelet sociaux, impot total a paye
    annee1: 54400, 1219, 0, 50179, 11%, 2711, 195, 210, 2921
    annee2: 54400, 2335, 0, 51295, 11, 2875, 358, 402, 3276
    Investissement initial: 61486
    net vendeur: 50926
    agence: 4074
    notaire: 10%, 4936
    frais dossier: 500
    frais credit logement: 1000
    Capital a emprunter: 59936
    frais bancaire 1550
    mensualite: 297.65 dont assurance 17.98€
    cout pret: 11501(19%) dont interet 7185(12%)
    '''

    def setUp(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __DATA_TEST_PATHNAME = os.path.join(__location__, 'data', 'input_test_simulationA.json')
        with open(__DATA_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)

        self.achat_data = input_data['achat']
        self.lots_data = input_data['lots']
        self.credit_data = input_data['credit']

        self.bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        self.credit = Factory.make_credit(self.credit_data, self.bi)
        self.rdt = Rendement(self.bi, self.credit)
        database = Database()
#         self.irr = Annexe_2044(database, self.bi, self.credit, 0.11)

    def testInvestissementInitial(self):
        self.assertAlmostEqual(self.bi.agence_montant, 4074.08, 2)
        self.assertAlmostEqual(self.bi.agence_taux, 0.08, 2)
        self.assertAlmostEqual(self.bi.notaire_montant, 4936, 2)
        self.assertAlmostEqual(self.bi.notaire_taux, 0.097, 3)
        self.assertAlmostEqual(self.bi.financement_total, 61486 - 1550, 0)

    def testRendement(self):
        self.assertAlmostEqual(self.rdt.investissement_initial, 61486 - 1550, 0)
        self.assertAlmostEqual(self.rdt.rendement_brut, 0.0881, 4)
#         self.assertAlmostEqual(self.rdt.rendement_net, 0.056, 3)

    def testCredit(self):
        self.assertAlmostEqual(self.credit.get_montant_interet_total(), 7185.22, 2)
        self.assertAlmostEqual(self.credit.get_montant_assurance_total(), 4315.40, 2)
        self.assertAlmostEqual(self.credit.get_montant_interet_total(), 7185, 0)
        self.assertAlmostEqual(self.credit.get_cout_total(), 11501 + 1550, 0)

        start = 1
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start), 297.65, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start), 17.98, 2)
        self.assertAlmostEqual(self.credit.get_interet(start), 57.44, 2)
        self.assertAlmostEqual(self.credit.get_amortissement(start), 222.23, 2)

        start = 12
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start), 297.65, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start), 17.98, 2)
        self.assertAlmostEqual(self.credit.get_interet(start), 55.08, 2)
        self.assertAlmostEqual(self.credit.get_amortissement(start), 224.59, 2)

        start = 230
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start), 297.65, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start), 17.98, 2)
        self.assertAlmostEqual(self.credit.get_interet(start), 2.93, 2)
        self.assertAlmostEqual(self.credit.get_amortissement(start), 276.74, 2)

    @unittest.skip('fixme')
    def testImpot(self):
        self.assertAlmostEqual(self.irr.base_impossable, 1219, 2)


'''
Rang    Date échéance    Echéance globale    Dont assurance    Intérêts    Capital amorti    Capital restant dû
1    05.01.2021    297.65€    17.98€    57.44€    222.23€    59 713.77€
2    05.02.2021    297.65€    17.98€    57.23€    222.44€    59 491.33€
3    05.03.2021    297.65€    17.98€    57.01€    222.66€    59 268.66€
4    05.04.2021    297.65€    17.98€    56.8€    222.87€    59 045.79€
5    05.05.2021    297.65€    17.98€    56.59€    223.08€    58 822.71€
6    05.06.2021    297.65€    17.98€    56.37€    223.3€    58 599.41€
7    05.07.2021    297.65€    17.98€    56.16€    223.51€    58 375.9€
8    05.08.2021    297.65€    17.98€    55.94€    223.73€    58 152.17€
9    05.09.2021    297.65€    17.98€    55.73€    223.94€    57 928.22€
10    05.10.2021    297.65€    17.98€    55.51€    224.16€    57 704.06€
11    05.11.2021    297.65€    17.98€    55.3€    224.37€    57 479.69€
12    05.12.2021    297.65€    17.98€    55.08€    224.59€    57 255.1€
13    05.01.2022    297.65€    17.98€    54.87€    224.8€    57 030.3€
14    05.02.2022    297.65€    17.98€    54.65€    225.02€    56 805.28€
15    05.03.2022    297.65€    17.98€    54.44€    225.23€    56 580.04€
16    05.04.2022    297.65€    17.98€    54.22€    225.45€    56 354.59€
17    05.05.2022    297.65€    17.98€    54.01€    225.66€    56 128.93€
18    05.06.2022    297.65€    17.98€    53.79€    225.88€    55 903.05€
19    05.07.2022    297.65€    17.98€    53.57€    226.1€    55 676.95€
20    05.08.2022    297.65€    17.98€    53.36€    226.31€    55 450.64€
21    05.09.2022    297.65€    17.98€    53.14€    226.53€    55 224.1€
22    05.10.2022    297.65€    17.98€    52.92€    226.75€    54 997.35€
23    05.11.2022    297.65€    17.98€    52.71€    226.96€    54 770.39€
24    05.12.2022    297.65€    17.98€    52.49€    227.18€    54 543.21€
25    05.01.2023    297.65€    17.98€    52.27€    227.4€    54 315.81€
26    05.02.2023    297.65€    17.98€    52.05€    227.62€    54 088.19€
27    05.03.2023    297.65€    17.98€    51.83€    227.84€    53 860.34€
28    05.04.2023    297.65€    17.98€    51.62€    228.05€    53 632.29€
29    05.05.2023    297.65€    17.98€    51.4€    228.27€    53 404.02€
30    05.06.2023    297.65€    17.98€    51.18€    228.49€    53 175.53€
31    05.07.2023    297.65€    17.98€    50.96€    228.71€    52 946.82€
32    05.08.2023    297.65€    17.98€    50.74€    228.93€    52 717.88€
33    05.09.2023    297.65€    17.98€    50.52€    229.15€    52 488.73€
34    05.10.2023    297.65€    17.98€    50.3€    229.37€    52 259.36€
35    05.11.2023    297.65€    17.98€    50.08€    229.59€    52 029.77€
36    05.12.2023    297.65€    17.98€    49.86€    229.81€    51 799.96€
37    05.01.2024    297.65€    17.98€    49.64€    230.03€    51 569.93€
38    05.02.2024    297.65€    17.98€    49.42€    230.25€    51 339.67€
39    05.03.2024    297.65€    17.98€    49.2€    230.47€    51 109.2€
40    05.04.2024    297.65€    17.98€    48.98€    230.69€    50 878.51€
41    05.05.2024    297.65€    17.98€    48.76€    230.91€    50 647.6€
42    05.06.2024    297.65€    17.98€    48.54€    231.13€    50 416.47€
43    05.07.2024    297.65€    17.98€    48.32€    231.35€    50 185.12€
44    05.08.2024    297.65€    17.98€    48.09€    231.58€    49 953.53€
45    05.09.2024    297.65€    17.98€    47.87€    231.8€    49 721.73€
46    05.10.2024    297.65€    17.98€    47.65€    232.02€    49 489.71€
47    05.11.2024    297.65€    17.98€    47.43€    232.24€    49 257.47€
48    05.12.2024    297.65€    17.98€    47.21€    232.46€    49 025.01€
49    05.01.2025    297.65€    17.98€    46.98€    232.69€    48 792.32€
50    05.02.2025    297.65€    17.98€    46.76€    232.91€    48 559.4€
51    05.03.2025    297.65€    17.98€    46.54€    233.13€    48 326.27€
52    05.04.2025    297.65€    17.98€    46.31€    233.36€    48 092.91€
53    05.05.2025    297.65€    17.98€    46.09€    233.58€    47 859.33€
54    05.06.2025    297.65€    17.98€    45.87€    233.8€    47 625.53€
55    05.07.2025    297.65€    17.98€    45.64€    234.03€    47 391.5€
56    05.08.2025    297.65€    17.98€    45.42€    234.25€    47 157.24€
57    05.09.2025    297.65€    17.98€    45.19€    234.48€    46 922.76€
58    05.10.2025    297.65€    17.98€    44.97€    234.7€    46 688.06€
59    05.11.2025    297.65€    17.98€    44.74€    234.93€    46 453.13€
60    05.12.2025    297.65€    17.98€    44.52€    235.15€    46 217.98€
61    05.01.2026    297.65€    17.98€    44.29€    235.38€    45 982.59€
62    05.02.2026    297.65€    17.98€    44.07€    235.6€    45 746.99€
63    05.03.2026    297.65€    17.98€    43.84€    235.83€    45 511.16€
64    05.04.2026    297.65€    17.98€    43.61€    236.06€    45 275.1€
65    05.05.2026    297.65€    17.98€    43.39€    236.28€    45 038.82€
66    05.06.2026    297.65€    17.98€    43.16€    236.51€    44 802.31€
67    05.07.2026    297.65€    17.98€    42.94€    236.73€    44 565.57€
68    05.08.2026    297.65€    17.98€    42.71€    236.96€    44 328.61€
69    05.09.2026    297.65€    17.98€    42.48€    237.19€    44 091.42€
70    05.10.2026    297.65€    17.98€    42.25€    237.42€    43 854€
71    05.11.2026    297.65€    17.98€    42.03€    237.64€    43 616.36€
72    05.12.2026    297.65€    17.98€    41.8€    237.87€    43 378.49€
73    05.01.2027    297.65€    17.98€    41.57€    238.1€    43 140.38€
74    05.02.2027    297.65€    17.98€    41.34€    238.33€    42 902.05€
75    05.03.2027    297.65€    17.98€    41.11€    238.56€    42 663.49€
76    05.04.2027    297.65€    17.98€    40.89€    238.78€    42 424.71€
77    05.05.2027    297.65€    17.98€    40.66€    239.01€    42 185.7€
78    05.06.2027    297.65€    17.98€    40.43€    239.24€    41 946.46€
79    05.07.2027    297.65€    17.98€    40.2€    239.47€    41 706.98€
80    05.08.2027    297.65€    17.98€    39.97€    239.7€    41 467.28€
81    05.09.2027    297.65€    17.98€    39.74€    239.93€    41 227.35€
82    05.10.2027    297.65€    17.98€    39.51€    240.16€    40 987.19€
83    05.11.2027    297.65€    17.98€    39.28€    240.39€    40 746.8€
84    05.12.2027    297.65€    17.98€    39.05€    240.62€    40 506.18€
85    05.01.2028    297.65€    17.98€    38.82€    240.85€    40 265.32€
86    05.02.2028    297.65€    17.98€    38.59€    241.08€    40 024.24€
87    05.03.2028    297.65€    17.98€    38.36€    241.31€    39 782.93€
88    05.04.2028    297.65€    17.98€    38.13€    241.54€    39 541.39€
89    05.05.2028    297.65€    17.98€    37.89€    241.78€    39 299.61€
90    05.06.2028    297.65€    17.98€    37.66€    242.01€    39 057.59€
91    05.07.2028    297.65€    17.98€    37.43€    242.24€    38 815.35€
92    05.08.2028    297.65€    17.98€    37.2€    242.47€    38 572.88€
93    05.09.2028    297.65€    17.98€    36.97€    242.7€    38 330.18€
94    05.10.2028    297.65€    17.98€    36.73€    242.94€    38 087.24€
95    05.11.2028    297.65€    17.98€    36.5€    243.17€    37 844.07€
96    05.12.2028    297.65€    17.98€    36.27€    243.4€    37 600.66€
97    05.01.2029    297.65€    17.98€    36.03€    243.64€    37 357.02€
98    05.02.2029    297.65€    17.98€    35.8€    243.87€    37 113.15€
99    05.03.2029    297.65€    17.98€    35.57€    244.1€    36 869.05€
100    05.04.2029    297.65€    17.98€    35.33€    244.34€    36 624.71€
101    05.05.2029    297.65€    17.98€    35.1€    244.57€    36 380.14€
102    05.06.2029    297.65€    17.98€    34.86€    244.81€    36 135.32€
103    05.07.2029    297.65€    17.98€    34.63€    245.04€    35 890.28€
104    05.08.2029    297.65€    17.98€    34.39€    245.28€    35 645€
105    05.09.2029    297.65€    17.98€    34.16€    245.51€    35 399.49€
106    05.10.2029    297.65€    17.98€    33.92€    245.75€    35 153.74€
107    05.11.2029    297.65€    17.98€    33.69€    245.98€    34 907.76€
108    05.12.2029    297.65€    17.98€    33.45€    246.22€    34 661.53€
109    05.01.2030    297.65€    17.98€    33.22€    246.45€    34 415.08€
110    05.02.2030    297.65€    17.98€    32.98€    246.69€    34 168.39€
111    05.03.2030    297.65€    17.98€    32.74€    246.93€    33 921.46€
112    05.04.2030    297.65€    17.98€    32.51€    247.16€    33 674.3€
113    05.05.2030    297.65€    17.98€    32.27€    247.4€    33 426.9€
114    05.06.2030    297.65€    17.98€    32.03€    247.64€    33 179.25€
115    05.07.2030    297.65€    17.98€    31.8€    247.87€    32 931.38€
116    05.08.2030    297.65€    17.98€    31.56€    248.11€    32 683.27€
117    05.09.2030    297.65€    17.98€    31.32€    248.35€    32 434.92€
118    05.10.2030    297.65€    17.98€    31.08€    248.59€    32 186.33€
119    05.11.2030    297.65€    17.98€    30.85€    248.82€    31 937.5€
120    05.12.2030    297.65€    17.98€    30.61€    249.06€    31 688.44€
121    05.01.2031    297.65€    17.98€    30.37€    249.3€    31 439.14€
122    05.02.2031    297.65€    17.98€    30.13€    249.54€    31 189.6€
123    05.03.2031    297.65€    17.98€    29.89€    249.78€    30 939.82€
124    05.04.2031    297.65€    17.98€    29.65€    250.02€    30 689.8€
125    05.05.2031    297.65€    17.98€    29.41€    250.26€    30 439.53€
126    05.06.2031    297.65€    17.98€    29.17€    250.5€    30 189.03€
127    05.07.2031    297.65€    17.98€    28.93€    250.74€    29 938.29€
128    05.08.2031    297.65€    17.98€    28.69€    250.98€    29 687.31€
129    05.09.2031    297.65€    17.98€    28.45€    251.22€    29 436.09€
130    05.10.2031    297.65€    17.98€    28.21€    251.46€    29 184.63€
131    05.11.2031    297.65€    17.98€    27.97€    251.7€    28 932.92€
132    05.12.2031    297.65€    17.98€    27.73€    251.94€    28 680.98€
133    05.01.2032    297.65€    17.98€    27.49€    252.18€    28 428.8€
134    05.02.2032    297.65€    17.98€    27.24€    252.43€    28 176.37€
135    05.03.2032    297.65€    17.98€    27€    252.67€    27 923.7€
136    05.04.2032    297.65€    17.98€    26.76€    252.91€    27 670.79€
137    05.05.2032    297.65€    17.98€    26.52€    253.15€    27 417.63€
138    05.06.2032    297.65€    17.98€    26.28€    253.39€    27 164.24€
139    05.07.2032    297.65€    17.98€    26.03€    253.64€    26 910.6€
140    05.08.2032    297.65€    17.98€    25.79€    253.88€    26 656.72€
141    05.09.2032    297.65€    17.98€    25.55€    254.12€    26 402.6€
142    05.10.2032    297.65€    17.98€    25.3€    254.37€    26 148.23€
143    05.11.2032    297.65€    17.98€    25.06€    254.61€    25 893.61€
144    05.12.2032    297.65€    17.98€    24.81€    254.86€    25 638.75€
145    05.01.2033    297.65€    17.98€    24.57€    255.1€    25 383.65€
146    05.02.2033    297.65€    17.98€    24.33€    255.34€    25 128.31€
147    05.03.2033    297.65€    17.98€    24.08€    255.59€    24 872.72€
148    05.04.2033    297.65€    17.98€    23.84€    255.83€    24 616.88€
149    05.05.2033    297.65€    17.98€    23.59€    256.08€    24 360.8€
150    05.06.2033    297.65€    17.98€    23.35€    256.32€    24 104.48€
151    05.07.2033    297.65€    17.98€    23.1€    256.57€    23 847.91€
152    05.08.2033    297.65€    17.98€    22.85€    256.82€    23 591.09€
153    05.09.2033    297.65€    17.98€    22.61€    257.06€    23 334.03€
154    05.10.2033    297.65€    17.98€    22.36€    257.31€    23 076.71€
155    05.11.2033    297.65€    17.98€    22.12€    257.55€    22 819.16€
156    05.12.2033    297.65€    17.98€    21.87€    257.8€    22 561.36€
157    05.01.2034    297.65€    17.98€    21.62€    258.05€    22 303.31€
158    05.02.2034    297.65€    17.98€    21.37€    258.3€    22 045.01€
159    05.03.2034    297.65€    17.98€    21.13€    258.54€    21 786.47€
160    05.04.2034    297.65€    17.98€    20.88€    258.79€    21 527.67€
161    05.05.2034    297.65€    17.98€    20.63€    259.04€    21 268.63€
162    05.06.2034    297.65€    17.98€    20.38€    259.29€    21 009.34€
163    05.07.2034    297.65€    17.98€    20.13€    259.54€    20 749.8€
164    05.08.2034    297.65€    17.98€    19.89€    259.78€    20 490.02€
165    05.09.2034    297.65€    17.98€    19.64€    260.03€    20 229.99€
166    05.10.2034    297.65€    17.98€    19.39€    260.28€    19 969.7€
167    05.11.2034    297.65€    17.98€    19.14€    260.53€    19 709.17€
168    05.12.2034    297.65€    17.98€    18.89€    260.78€    19 448.39€
169    05.01.2035    297.65€    17.98€    18.64€    261.03€    19 187.36€
170    05.02.2035    297.65€    17.98€    18.39€    261.28€    18 926.08€
171    05.03.2035    297.65€    17.98€    18.14€    261.53€    18 664.55€
172    05.04.2035    297.65€    17.98€    17.89€    261.78€    18 402.76€
173    05.05.2035    297.65€    17.98€    17.64€    262.03€    18 140.73€
174    05.06.2035    297.65€    17.98€    17.38€    262.29€    17 878.44€
175    05.07.2035    297.65€    17.98€    17.13€    262.54€    17 615.9€
176    05.08.2035    297.65€    17.98€    16.88€    262.79€    17 353.11€
177    05.09.2035    297.65€    17.98€    16.63€    263.04€    17 090.06€
178    05.10.2035    297.65€    17.98€    16.38€    263.29€    16 826.77€
179    05.11.2035    297.65€    17.98€    16.13€    263.54€    16 563.23€
180    05.12.2035    297.65€    17.98€    15.87€    263.8€    16 299.43€
181    05.01.2036    297.65€    17.98€    15.62€    264.05€    16 035.38€
182    05.02.2036    297.65€    17.98€    15.37€    264.3€    15 771.08€
183    05.03.2036    297.65€    17.98€    15.11€    264.56€    15 506.51€
184    05.04.2036    297.65€    17.98€    14.86€    264.81€    15 241.7€
185    05.05.2036    297.65€    17.98€    14.61€    265.06€    14 976.64€
186    05.06.2036    297.65€    17.98€    14.35€    265.32€    14 711.32€
187    05.07.2036    297.65€    17.98€    14.1€    265.57€    14 445.75€
188    05.08.2036    297.65€    17.98€    13.84€    265.83€    14 179.92€
189    05.09.2036    297.65€    17.98€    13.59€    266.08€    13 913.83€
190    05.10.2036    297.65€    17.98€    13.33€    266.34€    13 647.49€
191    05.11.2036    297.65€    17.98€    13.08€    266.59€    13 380.9€
192    05.12.2036    297.65€    17.98€    12.82€    266.85€    13 114.05€
193    05.01.2037    297.65€    17.98€    12.57€    267.1€    12 846.95€
194    05.02.2037    297.65€    17.98€    12.31€    267.36€    12 579.59€
195    05.03.2037    297.65€    17.98€    12.06€    267.61€    12 311.97€
196    05.04.2037    297.65€    17.98€    11.8€    267.87€    12 044.1€
197    05.05.2037    297.65€    17.98€    11.54€    268.13€    11 775.97€
198    05.06.2037    297.65€    17.98€    11.29€    268.38€    11 507.59€
199    05.07.2037    297.65€    17.98€    11.03€    268.64€    11 238.95€
200    05.08.2037    297.65€    17.98€    10.77€    268.9€    10 970.05€
201    05.09.2037    297.65€    17.98€    10.51€    269.16€    10 700.88€
202    05.10.2037    297.65€    17.98€    10.26€    269.41€    10 431.47€
203    05.11.2037    297.65€    17.98€    10€    269.67€    10 161.8€
204    05.12.2037    297.65€    17.98€    9.74€    269.93€    9 891.87€
205    05.01.2038    297.65€    17.98€    9.48€    270.19€    9 621.68€
206    05.02.2038    297.65€    17.98€    9.22€    270.45€    9 351.22€
207    05.03.2038    297.65€    17.98€    8.96€    270.71€    9 080.51€
208    05.04.2038    297.65€    17.98€    8.7€    270.97€    8 809.54€
209    05.05.2038    297.65€    17.98€    8.44€    271.23€    8 538.31€
210    05.06.2038    297.65€    17.98€    8.18€    271.49€    8 266.82€
211    05.07.2038    297.65€    17.98€    7.92€    271.75€    7 995.07€
212    05.08.2038    297.65€    17.98€    7.66€    272.01€    7 723.05€
213    05.09.2038    297.65€    17.98€    7.4€    272.27€    7 450.78€
214    05.10.2038    297.65€    17.98€    7.14€    272.53€    7 178.25€
215    05.11.2038    297.65€    17.98€    6.88€    272.79€    6 905.46€
216    05.12.2038    297.65€    17.98€    6.62€    273.05€    6 632.41€
217    05.01.2039    297.65€    17.98€    6.36€    273.31€    6 359.1€
218    05.02.2039    297.65€    17.98€    6.09€    273.58€    6 085.51€
219    05.03.2039    297.65€    17.98€    5.83€    273.84€    5 811.67€
220    05.04.2039    297.65€    17.98€    5.57€    274.1€    5 537.57€
221    05.05.2039    297.65€    17.98€    5.31€    274.36€    5 263.21€
222    05.06.2039    297.65€    17.98€    5.04€    274.63€    4 988.58€
223    05.07.2039    297.65€    17.98€    4.78€    274.89€    4 713.69€
224    05.08.2039    297.65€    17.98€    4.52€    275.15€    4 438.53€
225    05.09.2039    297.65€    17.98€    4.25€    275.42€    4 163.11€
226    05.10.2039    297.65€    17.98€    3.99€    275.68€    3 887.43€
227    05.11.2039    297.65€    17.98€    3.73€    275.94€    3 611.49€
228    05.12.2039    297.65€    17.98€    3.46€    276.21€    3 335.28€
229    05.01.2040    297.65€    17.98€    3.2€    276.47€    3 058.81€
230    05.02.2040    297.65€    17.98€    2.93€    276.74€    2 782.06€
231    05.03.2040    297.65€    17.98€    2.67€    277€    2 505.06€
232    05.04.2040    297.65€    17.98€    2.4€    277.27€    2 227.79€
233    05.05.2040    297.65€    17.98€    2.14€    277.53€    1 950.26€
234    05.06.2040    297.65€    17.98€    1.87€    277.8€    1 672.46€
235    05.07.2040    297.65€    17.98€    1.6€    278.07€    1 394.38€
236    05.08.2040    297.65€    17.98€    1.34€    278.33€    1 116.05€
237    05.09.2040    297.65€    17.98€    1.07€    278.6€    837.45€
238    05.10.2040    297.65€    17.98€    0.8€    278.87€    558.58€
239    05.11.2040    297.65€    17.98€    0.54€    279.13€    279.45€
240    05.12.2040    297.65€    17.98€    0.27€    279.4€    0.05€
                71 436.61€    4 315.39€    7 185.22€    59 935.95€    -
'''

if __name__ == '__main__':
    unittest.main()
