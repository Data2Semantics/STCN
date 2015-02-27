#!/usr/bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
import re
import sys, traceback


g = {
"A": 1,
"B": 2,
"C": 3,
"D": 4,
"E": 5,
"F": 6,
"G": 7,
"H": 8,
"I": 9,
"K": 10,
"L": 11,
"M": 12,
"N": 13,
"O": 14,
"P": 15,
"Q": 16,
"R": 17,
"S": 18,
"T": 19,
"U": 20,
"V": 21,
"X": 22,
"Y": 23,
"Z": 24,
"a": 1,
"b": 2,
"c": 3,
"d": 4,
"e": 5,
"f": 6,
"g": 7,
"h": 8,
"i": 9,
"k": 10,
"l": 11,
"m": 12,
"n": 13,
"o": 14,
"p": 15,
"q": 16,
"r": 17,
"s": 18,
"t": 19,
"u": 20,
"v": 21,
"x": 22,
"y": 23,
"z": 24
}

sparql = SPARQLWrapper("http://ops.few.vu.nl:8890/sparql")
sparql.setQuery("""
PREFIX vocab: <http://stcn.data2semantics.org/vocab/resource/>

SELECT ?f
FROM <http://stcn.data2semantics.org>
WHERE {
?p rdf:type vocab:Publicatie;
   vocab:publications_kmc4060 ?f ;
   vocab:drukker ?drukker .
   FILTER (?drukker IN (<http://stcn.data2semantics.org/drukker/304650463>, <http://stcn.data2semantics.org/drukker/207234116>, <http://stcn.data2semantics.org/drukker/16196141x>, <http://stcn.data2semantics.org/drukker/111952999>, <http://stcn.data2semantics.org/drukker/075573539>, <http://stcn.data2semantics.org/drukker/075573520>, <http://stcn.data2semantics.org/drukker/075570882>, <http://stcn.data2semantics.org/drukker/075553422>, <http://stcn.data2semantics.org/drukker/075547740>, <http://stcn.data2semantics.org/drukker/332485722>, <http://stcn.data2semantics.org/drukker/328745081>, <http://stcn.data2semantics.org/drukker/186624611>, <http://stcn.data2semantics.org/drukker/143840789>))
}
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

#results = ["A-G`SUP`12`LO` H`SUP`6`LO` (lacks H6, blank?)", "`SUP`8`LO` (*1+Û1) A-2C`SUP`8`LO` 2D`SUP`4`LO`", "`SUP`8`LO` A-L`SUP`8`LO` M`SUP`6`LO`"]

#Statistics
formulas = 0
parseErrors = 0
badFormulaErrors = 0

for r in results["results"]["bindings"]:
#for r in results:
    f = r["f"]["value"]
    #f = r
    print "Formula:", f.encode('utf8')
    prog = re.compile('''
                      (.(?P<cover_sheet>>[0-9]))?                                  # Cover sheet
                      (\`SUP\`(?P<pren>[0-9]+)\`LO\`\s*(?P<pre>(\(.*\)\s*))?)?     # Preface sheets
                      (?P<start_sheet>[A-Za-z])(-(?P<end_sheet_n>[0-9]*)(?P<end_sheet>[A-Za-z]))?\`SUP\`(?P<sheet_count>[0-9]+)(\/[0-9])?\`LO\`                                                          # Main block
                        (\(.(?P<missing>[A-Za-z][0-9]*)\))?                        # Missing sheets
                        \s*                                                        # Spaces
                      ((?P<remain_start>[0-9]*[A-Za-z])(-(?P<remain_end>[0-9]*[A-Za-z]))?\`SUP\`(?P<remain_n>[0-9]+)\`LO\`)?                                                                             # Remaining sheets
                      (\[(?P<remain_start_a>[A-Za-z])\](?P<remain_n_a>[0-9]))?     # Alternative remaining sheets
                      .*                                                           # Trail
                      '''
                      , re.VERBOSE)
    matches = prog.search(f)
    if matches:
        if matches.group("cover_sheet"):
            cover_sheet = int(matches.group("cover_sheet"))
        else:
            cover_sheet = 0
        start_sheet = matches.group("start_sheet")
        end_sheet = matches.group("end_sheet")
        if not matches.group("end_sheet") and matches.group("remain_end"):
            end_sheet = matches.group("remain_end")
        elif not matches.group("end_sheet") and not matches.group("remain_end"):
            if matches.group("remain_start"):
                end_sheet = matches.group("remain_start")
            else:
                end_sheet = matches.group("remain_start_a")
        if not end_sheet:
            end_sheet = start_sheet
        if matches.group("end_sheet_n"):
            end_sheet_n = int(matches.group("end_sheet_n"))
        else:
            end_sheet_n = 1
        sheet_count = int(matches.group("sheet_count"))
        remain_start = matches.group("remain_start")
        remain_end = matches.group("remain_end")
        if matches.group("remain_n"):
            remain_n = int(matches.group("remain_n"))
        else:
            if matches.group("remain_n_a"):
                remain_n = int(matches.group("remain_n_a"))
            else:
                remain_n = 0
        if matches.group("pren"):
            pren = int(matches.group("pren"))
        else:
            pren = 0
        if not matches.group("pre"):
            pre = "None"
        if not matches.group("remain_start") and not matches.group("remain_start_a"):
            remain_start = "None"
        elif matches.group("remain_start_a"):
            remain_start = matches.group("remain_start_a")
        if not matches.group("remain_end"):
            remain_end = "None"
        if matches.group("missing"):
            missing = matches.group("missing")
        else:
            missing = "None"

    else:
        print "I do not recognise this formula!"
        badFormulaErrors += 1
        formulas += 1
        print
        continue
    print "cover_sheet", cover_sheet
    print "pren", pren
    print "pre", pre
    print "start_sheet", start_sheet
    print "end_sheet_n", end_sheet_n
    print "end_sheet", end_sheet
    print "sheet_count", sheet_count
    print "missing", missing
    print "remain_start", remain_start
    print "remain_end", remain_end
    print "remain_n", remain_n
    try:
        sheets = pren + ((end_sheet_n - 1) * len(g) + g[end_sheet] - g[start_sheet] + 1) * sheet_count + remain_n
        pages = sheets * 2
    except KeyError:
        traceback.print_exc(file=sys.stdout)
        parseErrors += 1
        pass
    #print pren, " + ((", end_sheet_n, "- 1 ) * ", len(g)," + ", g[end_sheet], " - ", g[start_sheet], " + 1) *", sheet_count, " + ", remain_n
    print "Sheets:", sheets
    print "Pages:", pages
    print
    formulas += 1

print "Stats"
print "-----"
print "Parsed formulas: ", formulas
print "Parsing errors: ", parseErrors
print "Bad formulas: ", badFormulaErrors
