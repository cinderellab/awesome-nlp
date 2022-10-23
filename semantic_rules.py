# -*- coding: utf-8 -*-

## LAB [string]
## F_L[node] the word on the left side of the link 
## F_R[node] the word on the right side of the link
## name: points to a string value for the name of the refent.
## tense: if the referent is a verb/event, points to a string value representing a tense
## HYP: if the referent is a verb/event, points to a string with value “T” iff the event is hypothetical.
## TRUTH-QUERY-FLAG: if the referent is a verb/event, points to a string with value “T” iff the event a question (i.e., 'eat' in “Did John eat the cake?”).
## COPULA-QUERY-FLAG: Points to the string “T” for particular entities involved in particular forms of copula questions (i.e., 'John' in “Who is john?”).
## noun_number: if the referent is a noun/thing, points to a string value representing a noun number
## links: points to a a feature node, with features representing the dependency relations in which this referent is the first argument.
## memberN: if the referent represents a group of things, it will contain only memberN features where N is an integer, and the memberN feature points to the Nth member in the group. 

semantic_rules = {
 'ADJ1': {'set': ['<F_R BACKGROUND-FLAG> = T',
                  '<F_R ref links _amod> += <F_L ref>'],
          'regex': ['= A\.*|DT\.*'],
          'match': []},
 'ADJ2': {'set': ['<F_L BACKGROUND-FLAG> = T',
                       '<F_L ref links _amod> += <F_R ref>'],
          'regex': ['=  Mp\.*| MVp\.*| Ma\.*'],
          'match': ['<F_R PREP-OBJ> = %']},
 'ADV1': {'set': ['<F_L head-word BACKGROUND-FLAG> = T',
                       '<F_L head-word ref links _advmod> += <F_R ref>'],
          'regex': ['= MVa\.*|EB\.*', '!= EBx\.*'],
          'match': ['<F_R str> != not', '<F_L head-word> != %']},
 'ADV2': {'set': ['<F_R head-word BACKGROUND-FLAG> = T',
                       '<F_R head-word ref links _advmod> += <F_L ref>'],
          'regex': ['= E\.*|EA\.*', '!= EA[my]\.*'],
          'match': ['<F_R head-word ref> != 