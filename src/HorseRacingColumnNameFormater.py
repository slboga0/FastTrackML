import pandas as pd

# Redefining data for clarity
raw_data = """
FIELD #,DESCRIPTION
1,Track
2,Date
3,Race #
4,Post Position
5,Entry
6,Distance (in yards)
7,Surface
8,Reserved
9,Race Type
10,Age/Sex Restrictions
11,Today's Race Classification
12,Purse
13,Claiming Price
14,Claiming Price (of horse)
15,Track Record
16,Race Conditions
17,Today's Lasix list (see also field #63)
18,Today's Bute  list
19,Today's Coupled list
20,Today's Mutuel list
21,Simulcast host track code
22,Simulcast host track race #
23,Breed Type (if available)
24,Today's Nasal Strip Change
25,Today's All-Weather Surface flag
26-27,Reserved for future use
28,Today's Trainer
29,Trainer Sts     Current Meet
30,Trainer Wins    Current Meet
31,Trainer Places  Current Meet
32,Trainer Shows   Cureent Meet
33,Today's Jockey
34,Apprentice wgt allow.(if any)
35,Jockey  Sts     Current Meet
36,Jockey  Wins    Current Meet
37,Jockey  Places  Current Meet
38,Jockey  Shows   Current Meet
39,Today's Owner
40,Owner's Silks
41,Main Track Only/AE Indicator
42,Reserved for possible future expansion
43,Program Number (if available)
44,Morn. Line Odds(if available)
45,Horse Name
46,Year of Birth
47,Horse's Foaling Month
48,Reserved
49,Sex
50,Horse's color
51,Weight
52,Sire
53,Sire's sire
54,Dam
55,Dam's sire
56,Breeder
57,State/Country abrv. where bred
58,Program Post Position (if avail
59-61,Blank fields reserved for possi
62,Today's Medication w/1st time Lasix info see also fields #17 & #18
63,Today's Medication w/o 1st time Lasix info
64,Horse's Lifetime Record @ Today's Distance Equipment Change
65,Horse's Lifetime Record @ Today's Distance Starts
66,Horse's Lifetime Record @ Today's Distance Wins
67,Horse's Lifetime Record @ Today's Distance Places
68,Horse's Lifetime Record @ Today's Distance Shows
69,Horse's Lifetime Record @ Today's Distance Earnings
70,Horse's Lifetime Record @ Today's track Starts
71,Horse's Lifetime Record @ Today's track Wins
72,Horse's Lifetime Record @ Today's track Places
73,Horse's Lifetime Record @ Today's track Shows
74,Horse's Lifetime Record @ Today's track Earnings
75,Horse's Lifetime Turf Record Starts
76,Horse's Lifetime Turf Record Wins
77,Horse's Lifetime Turf Record Places
78,Horse's Lifetime Turf Record Shows
79,Horse's Lifetime Turf Record Earnings
80,Horse's Lifetime Wet Record Starts
81,Horse's Lifetime Wet Record Wins
82,Horse's Lifetime Wet Record Places
83,Horse's Lifetime Wet Record Shows
84,Horse's Lifetime Wet Record Earnings
85,Horse's Current Year Record Year
86,Horse's Current Year Record Starts
87,Horse's Current Year Record Wins
88,Horse's Current Year Record Places
89,Horse's Current Year Record Shows
90,Horse's Current Year Record Earnings
91,Horse's Previous Year Record Year
92,Horse's Previous Year Record Starts
93,Horse's Previous Year Record Wins
94,Horse's Previous Year Record Places
95,Horse's Previous Year Record Shows
96,Horse's Previous Year Record Earnings
97,Horse's Lifetime Record Starts
98,Horse's Lifetime Record Wins
99,Horse's Lifetime Record Places
100,Horse's Lifetime Record Shows
101,Horse's Lifetime Record Earnings
102,Date of Workout            #1
103,Date of Workout            #2
104,Date of Workout            #3
105,Date of Workout            #4
106,Date of Workout            #5
107,Date of Workout            #6
108,Date of Workout            #7
109,Date of Workout            #8
110,Date of Workout            #9
111,Date of Workout            #10
112,Date of Workout            #11
113,Date of Workout            #12
114,Time of Workout            #1
115,Time of Workout            #2
116,Time of Workout            #3
117,Time of Workout            #4
118,Time of Workout            #5
119,Time of Workout            #6
120,Time of Workout            #7
121,Time of Workout            #8
122,Time of Workout            #9
123,Time of Workout            #10
124,Time of Workout            #11
125,Time of Workout            #12
126,Track of Workout           #1
127,Track of Workout           #2
128,Track of Workout           #3
129,Track of Workout           #4
130,Track of Workout           #5
131,Track of Workout           #6
132,Track of Workout           #7
133,Track of Workout           #8
134,Track of Workout           #9
135,Track of Workout           #10
136,Track of Workout           #11
137,Track of Workout           #12
138,Distance of Workout        #1
139,Distance of Workout        #2
140,Distance of Workout        #3
141,Distance of Workout        #4
142,Distance of Workout        #5
143,Distance of Workout        #6
144,Distance of Workout        #7
145,Distance of Workout        #8
146,Distance of Workout        #9
147,Distance of Workout        #10
148,Distance of Workout        #11
149,Distance of Workout        #12
150,Track Condition of Workout #1
151,Track Condition of Workout #2
152,Track Condition of Workout #3
153,Track Condition of Workout #4
154,Track Condition of Workout #5
155,Track Condition of Workout #6
156,Track Condition of Workout #7
157,Track Condition of Workout #8
158,Track Condition of Workout #9
159,Track Condition of Workout #10
160,Track Condition of Workout #11
161,Track Condition of Workout #12
162,Description of Workout     #1
163,Description of Workout     #2
164,Description of Workout     #3
165,Description of Workout     #4
166,Description of Workout     #5
167,Description of Workout     #6
168,Description of Workout     #7
169,Description of Workout     #8
170,Description of Workout     #9
171,Description of Workout     #10
172,Description of Workout     #11
173,Description of Workout     #12
174,Main/Inner track indicator #1
175,Main/Inner track indicator #2
176,Main/Inner track indicator #3
177,Main/Inner track indicator #4
178,Main/Inner track indicator #5
179,Main/Inner track indicator #6
180,Main/Inner track indicator #7
181,Main/Inner track indicator #8
182,Main/Inner track indicator #9
183,Main/Inner track indicator #10
184,Main/Inner track indicator #11
185,Main/Inner track indicator #12
186,day/distance           #1
187,day/distance           #2
188,day/distance           #3
189,day/distance           #4
190,day/distance           #5
191,day/distance           #6
192,day/distance           #7
193,day/distance           #8
194,day/distance           #9
195,day/distance           #10
196,day/distance           #11
197,day/distance           #12
198,other works that day/dist #1
199,other works that day/dist #2
200,other works that day/dist #3
201,other works that day/dist #4
202,other works that day/dist #5
203,other works that day/dist #6
204,other works that day/dist #7
205,other works that day/dist #8
206,other works that day/dist #9
207,other works that day/dist #10
208,other works that day/dist #11
209,other works that day/dist #12
210,BRIS Run Style designation
211,Quirin style Speed Points
212,Reserved
213,Reserved
214,2F BRIS Pace Par for level
215,4F BRIS Pace Par for level
216,6F BRIS Pace Par for level
217,BRIS Speed Par for class level
218,BRIS Late Pace Par for level
219,T/J Combo # Starts (365D)
220,T/J Combo # Wins (365D)
221,T/J Combo # Places (365D)
222,T/J Combo # Shows (365D)
223,T/J Combo $2 ROI (365D)
224,# of days since last race
225-230,complete race condition lines
231,Lifetime Starts - All Weather Surface
232,Lifetime Wins - All Weather Surface
233,Lifetime Places - All Weather Surface
234,Lifetime Shows - All Weather Surface
235,Lifetime Earnings - All Weather Surface
236,Best BRIS Speed - All Weather Surface
237,Reserved
238, Low Claiming Price (for today's race)"
239,Statebred Flag s (for today's race)"
240-248,Wager Types for this race
249,Reserved
250,Reserved
251,BRIS Prime Power Rating
252-255,Reserved fields for future use
256-265,265 Race Date
266-274,# of days since previous rac
275,Reserved (# days since prev. rac
276-285,Track Code
286-295,BRIS Track Code
296-305,Race #
306-315,Track Condition
316-325,Distance (in yards)
326-335,Surface
336-345,Special Chute indicator
346-355,# of entrants
356-365,Post Position
366-375,Equipment
376-385,Racename of previous races
386-395,Medication see also field #62
396-405,Trip Comment
406-415,Winner's Name
416-425,2nd Place finishers Name
426-435,3rd Place finishers Name
436-445,Winner's Weight carried
446-455,2nd Place Weight carried
456-65,3rd Place Weight carried
466-475,Winner's Margin
476-485,2nd Place Margin
486-495,3rd Place Margin
496-405,Alternate/Extra Comment line
506-515,Weight
516-525,Odds
526-535,Entry
536-545,Race Classification
546-555,Claiming Price (of horse)
556-565,Purse
566-575,Start Call Position
576-585,1st Call Position(if any)
586-595,2nd Call Position(if any)
596-605,Gate Call Position(if any)
606-615,Stretch Position (if any)
616-625,Finish Position
626-635,Money Position
636-645,Start Call BtnLngths/Ldr mar
646-655,Start Call BtnLngths only
656-665,1st Call BtnLngths/Ldr margi
666-675,1st Call BtnLngths only
676-685,2nd Call BtnLngths/Ldr margi
686-695,2nd Call BtnLngths only
696-75,BRIS Race Shape - 1st Call
706-715,Reserved
716-725,Stretch  BtnLngths/Ldr margi
726-735,Stretch  BtnLngths only
736-745,Finish   BtnLngths/Wnrs marg
746-755,Finish   BtnLngths only
756-765,BRIS Race Shape - 2nd Call
766-775,BRIS 2f Pace Fig
776-785,BRIS 4f Pace Fig
786-795,BRIS 6f Pace Fig
796-85,BRIS 8f Pace Fig
806-815,BRIS 10f Pace Fig
816-825,BRIS Late Pace Fig
826-835,Reserved
836-845,Reserved
846-855,BRIS Speed Rating
856-865,Speed Rating
866-875,Track Variant
876-885,2f  Fraction (if any)
886-895,3f  Fraction (if any)
896-95,4f  Fraction (if any)
906-915,5f  Fraction (if any)
916-925,6f  Fraction (if any)
926-935,7f  Fraction (if any)
936-945,8f  Fraction (if any)
946-955,10f Fraction (if any)
956-965,12f Fraction (if any)
966-975,14f Fraction (if any)
976-985,16f Fraction (if any)
986-995,Fraction #1
996-105,Fraction #2
1006-1015,Fraction #3
1016-1025,Reserved
1026-1035,Reserved
1036-1045,Final Time
1046-1055,Claimed code
1056-1065,Trainer (when available)
1066-1075,Jockey
1076-1085,Apprentice Wt allow (if any)
1086-1095,Race Type
1096-1105,Age and Sex Restrictions
1106-1115,Statebred flag
1116-1125,Restricted/Qualifier flag
1126-1135,Favorite indicator
1136-1145,Front Bandages indicator
1146,Reserved
1147,Trainer      Sts     Current Year
1148,Trainer      Win     Current Year
1149,Trainer      Place     Current Year
1150,Trainer      Shows Current Year
1151,Trainer      ROI     Current Year
1152,Trainer      Sts     Previous Year
1153,Trainer      Win Previous Year
1154,Trainer      Place Previous Year
1155,Trainer      Show Previous Year
1156,Trainer      ROI Previous Year
1157,Jockey       Sts     Current Year
1158,Jockey       Win Current Year
1159,Jockey       Place Current Year
1160,Jockey       Show Current Year
1161,Jockey       ROI Current Year
1162,Jockey       Sts     Previous Year
1163,Jockey       Win     Previous Year
1164,Jockey       Place Previous Year
1165,Jockey       Show Previous Year
1166,Jockey       ROI Previous Year
1167-1176,BRIS Speed Par for class lev
1177,Sire Stud Fee (current)
1178,Best BRIS Speed - Fast track
1179,Best BRIS Speed - Turf
1180,Best BRIS Speed - Off track
1181,Best BRIS Speed - Distance
1182-1191,Bar shoe
1192-1201,Company Line Codes
1202-1211, Low Claiming Price of race
1212-1212, High Claiming Price of race
1222,Auction Price
1223,Where/When Sold at Auction
1224-1253,Reserved for future use
1254-1263,Code for prior 10 starts
1264,BRIS Dirt Pedigree Rating
1265,BRIS Mud Pedigree Rating
1266,BRIS Turf Pedigree Rating
1267,BRIS Dist Pedigree Rating
1268-1277,Claimed from and trainer switches
1278-1287,Claimed from and trainer switches
1288-1297,Claimed from and trainer switches
1298-1307,Claimed from and trainer switches
1308-1317,Claimed from and trainer switches
1318-1327,Claimed from and trainer switches
1328,Best BRIS Speed: Life
1329,Best BRIS Speed: Most Recent
1330,Best BRIS Speed: 2nd Most Re
1331,Best BRIS Speed: Today's Tra
1332,# Starts (FAST Dirt)
1333,# Wins   (FAST Dirt)
1334,# Places (FAST Dirt)
1335,# Shows  (FAST Dirt)
1336,Earnings (FAST Dirt)
1337,Key Trnr Stat Category #1
1338,# of starts            #1
1339,Win%                   #1
1340,in-the-money (itm) %   #1
1341,$2ReturnOnInvestment   #1
1342,Key Trnr Stat Category #2
1343,# of starts            #2
1344,Win%                   #2
1345,in-the-money (itm) %   #2
1346,$2ReturnOnInvestment   #2
1347,Key Trnr Stat Category #3
1348,# of starts            #3
1349,Win%                   #3
1350,in-the-money (itm) %   #3
1351,$2ReturnOnInvestment   #3
1352,Key Trnr Stat Category #4
1353,# of starts            #4
1354,Win%                   #4
1355,in-the-money (itm) %   #4
1356,$2ReturnOnInvestment   #4
1357,Key Trnr Stat Category #5
1358,# of starts            #5
1359,Win%                   #5
1360,in-the-money (itm) %   #5
1361,$2ReturnOnInvestment   #5
1362,Key Trnr Stat Category #6
1363,# of starts            #6
1364,Win%                   #6
1365,in-the-money (itm) %   #6
1366,$2ReturnOnInvestment   #6
1367,JKY@Dis/JkyonTurf Label
1368,JKY@Dis/JkyonTurf Starts
1369,JKY@Dis/JkyonTurf Wins
1370,JKY@Dis/JkyonTurf Places
1371,JKY@Dis/JkyonTurf Shows
1372,JKY@Dis/JkyonTurf ROI
1373,JKY@Dis/JkyonTurf Earnings
1374,Post Times (by region)
1375-1382,Reserved
1383-1392,Extended Start Comment
1393-1402,Sealed track indicator
1403-1412,Prev. All-Weather Surface flag
1413,T/J Combo # Starts (meet)
1414,T/J Combo #Wins (meet)
1415,T/J Combo #Places (meet)
1416,T/J Combo # Shows (meet)
1417,T/J Combo $2 ROI (meet)
1418,Post Time (Pacific military
1419-1428,Equibase Abbrev. Race Condit
1429,Today's EQB Abbrev. Race Con
1430-1435,Reserved
"""

# Helper function to expand ranges and normalize names
def expand_and_normalize(data):
    expanded_data = []
    for field, description in data:
        # Replace '@' with 'at', remove single quotes, replace '#' with 'no'
        description = (description.replace("@", "at").replace("'", "").replace("%", "percent")
                                  .replace("#", "no").replace("/", " Or ").replace(".", "")
                                  .replace("(", "").replace(")", ""))
        if '-' in field:
            start, end = map(int, field.split('-'))
            base_name = "_".join(description.lower().split())
            for i in range(start, end + 1):
                expanded_data.append((i, f"{base_name}_{i}"))
        else:
            normalized_name = "_".join(description.lower().split())
            expanded_data.append((int(field), normalized_name))

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(expanded_data, columns=["field_position", "field_name"])
    df.to_csv("fields_mapping.csv", index=False)

    return expanded_data


# Split data into lines and process
lines = raw_data.strip().split("\n")[1:]
data = [line.split(",", 1) for line in lines]

# Expand and normalize the data
expanded_data = expand_and_normalize(data)

# Create a DataFrame
df = pd.DataFrame(expanded_data, columns=["field_number", "description"])

# Display the DataFrame for the user
import matplotlib.pyplot as plt

# Show the head of the DataFrame to the user
print(df.head)
