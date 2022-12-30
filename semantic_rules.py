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
          'match': ['<F_R head-word ref> != %']},
 'ADV2_HEADLESS': {'set': ['<F_R BACKGROUND-FLAG> = T',
                                '<F_R ref links _advmod> += <F_L ref>'],
                   'regex': ['= E\.*|EA\.*', '!= EA[my]\.*'],
                   'match': ['<F_R head-word ref> = %']},
 'ADV3': {'set': ['<F_R BACKGROUND-FLAG> = T',
                       '<F_R ref links _advmod> += <F_L ref>'],
          'regex': ['= EE\.* | EA'],
          'match': []},
 'ADV4': {'set': ['<F_L POS> = adv',
                       '<F_R head-word BACKGROUND-FLAG> = T',
                       '<F_R head-word ref links _advmod> += <F_L ref>'],
          'regex': ['= CO\.*'],
          'match': ['<F_L obj> = %', '<F_L head-word> = %']},
 'APPO_LEFT': {'set': ['<F_R ref links _nn> += <F_L ref>'],
               'regex': ['= GN\.*'],
               'match': []},
 'APPO_RIGHT': {'set': ['<F_L ref links _appo> += <F_R ref>'],
                'regex': ['= MX|MXs|MXp'],
                'match': []},
 'CLEAN_UP_BAD_REFS1': {'set': ['<GOOD-REF-FLAG> = T'],
                        'regex': [],
                        'match': ['<ref name> != %']},
 'CLEAN_UP_BAD_REFS2': {'set': ['<ref> = %'],
                        'regex': [],
                        'match': ['<GOOD-REF-FLAG> != T', '<ref> != %']},
 'COMPARATIVE_OBJ1': {'set': ['<F_L comparative-obj-word> = <F_R>'],
                      'regex': ['=  U\.c\.*| O\.c\.*'],
                      'match': ['<F_L str> = than|as']},
 'COMPARATIVE_OBJ2': {'set': ['<F_L comparative-obj-word> = <F_R comparative-obj-word>'],
                      'regex': ['=  MV[tz]\.*'],
                      'match': ['<F_R comparative-obj-word> != % ']},
 'COMPARATIVE_OBJ3A': {'set': ['<F_R comparative-cvar name> = _$cVar',
                                    '<F_R comparative-cvar links _$crVar> = <F_L comparative-obj-word ref>'],
                       'regex': ['=  O\.*'],
                       'match': ['<F_R COMP-SUBJ-FLAG> = T']},
 'COMPARATIVE_OBJECT_FINAL': {'set': [],
                              'regex': [],
                              'match': ['<COMP-SUBJ-FLAG> = T',
                                      '<this> = $modified',
                                      '<comparative-relation-word ref name> = $prep',
                                      '<comparative-relation-word> = $prep_source',
                                      '<comparative-cvar> = $prep_obj']},
 'COMPARATIVE_RELATION1': {'set': ['<F_R comparative-relation-word> = <F_L>',
                                        '<F_R COMP-SUBJ-FLAG> = T'],
                           'regex': ['=  D\.\.[my]\.*'],
                           'match': []},
 'COPULA_QUESTION1': {'set': ['<head> = %',
                                   '<head> = $O',
                                   '<head COPULA-QUESTION-FLAG> = T'],
                      'regex': [],
                      'match': ['<head name> = be',
                              '<head links _subj name> = _$qVar',
                              '<head links _obj> = $O']},
 'COPY_POS_TO_REF': {'set': ['<ref pos> = <POS>'],
                     'regex': [],
                     'match': ['<POS> != %']},
 'DECLARATIVE_QUESTION1': {'set': ['<F_L punc> = <F_R str>'],
                           'regex': ['=  Xp\.*'],
                           'match': []},
 'DECLARATIVE_QUESTION2': {'set': ['<F_R head-word ref TRUTH-QUERY-FLAG> = T',
                                        '<F_R head-word ref HYP> = T',
                                        '<F_L wall sentence_type> = QUERY'],
                           'regex': ['=  Wd\.*'],
                           'match': ['<F_L punc> =  [  ?]',
                                   '<F_L head-word> != %']},
 'DIR_OBJ1': {'set': ['<F_L OBJ-LINK-TAG> = O',
                           '<F_L obj> += <F_R ref>'],
              'regex': ['=  O\.*| OD\.*| OT\.*',
                        '!=  O\.n\.*',
                        '!=  O\.i\.*'],
              'match': ['<F_L OBJ-LINK-TAG> = O|UNMATCH']},
 'DIR_OBJ2': {'set': ['<F_L OBJ-LINK-TAG> = O-n',
                           '<F_L obj> += <F_R ref>',
                           '<F_L iobj> += <F_R ref>'],
              'regex': ['=  O\.n\.*',
                        '!=  O\.i\.*',
                        '=  O\.n\.*',
                        '!=  O\.i\.*'],
              'match': ['<F_L OBJ-LINK-TAG> = O-n|UNMATCH',
                      '<F_L OBJ-LINK-TAG> != O-n|UNMATCH']},
 'DO_QUESTION1': {'set': ['<F_R obj> = %',
                               '<F_R ref name> = %',
                               '<F_R ref name> = _$qVar',
                               '<F_R ref QUERY-FLAG> = T'],
                  'regex': ['=  B.w'],
                  'match': ['<F_R str> = do']},
 'DROP_REF': {'set': ['<ref> = %'],
              'regex': [],
              'match': ['<ref DROP-REF-FLAG> = T']},
 'FILLER_FIX': {'set': ['<F_R subj> = <F_R obj>', '<F_R obj> = %'],
                'regex': ['=  Ix\.*| PPf\.*'],
                'match': ['<F_R subj> = %', '<F_R obj> != %']},
 'GER_OBJ': {'set': ['<F_R OBJ-LINK-TAG> = Mv',
                          '<F_R obj> += <F_L ref>'],
             'regex': ['=  Mv\.*'],
             'match': []},
 'HEAD-QUESTION-WHICH': {'set': ['<F_L head-question-word> += <F_R head-question-word>',
                                      '<F_L head-question-word> += <F_R head-word>'],
                         'regex': ['=  D\.\.w\.*', '=  D\.\.w\.*'],
                         'match': ['<F_R head-question-word> != %',
                                 '<F_R head-question-word> = %']},
 'HEAD-QUESTION-WORD': {'set': ['<F_L head-question-word> += <F_R head-word>'],
                        'regex': ['=  Rw\.*|Q'],
                        'match': []},
 'HEAD-QUESTION-WORD2': {'set': ['<F_L head-word> += <F_R head-question-word>'],
                         'regex': ['=  W[qs]\.*'],
                         'match': ['<F_R head-question-word> != %']},
 'HEAD-QUESTION-WORD2NULL': {'set': ['<F_L head-word> += <F_R head-word>'],
                             'regex': ['=  W[qs]\.*'],
                             'match': ['<F_R head-question-word> = %']},
 'HEAD-WORD_GROUP0': {'set': ['<head-word ref> += $R', '<head> += $R'],
                      'regex': [],
                      'match': ['<head-word member0 ref> = $R',
                              '<head-word member0 ref> = $R']},
 'HEAD-WORD_GROUP1': {'set': ['<head-word ref> += $R', '<head> += $R'],
                      'regex': [],
                      'match': ['<head-word member1 ref> = $R',
                              '<head-word member1 ref> = $R']},
 'HEAD-WORD_GROUP2': {'set': ['<head-word ref> += $R', '<head> += $R'],
                      'regex': [],
                      'match': ['<head-word member2 ref> = $R',
                              '<head-word member2 ref> = $R']},
 'HEAD-WORD_GROUP3': {'set': ['<head-word ref> += $R', '<head> += $R'],
                      'regex': [],
                      'match': ['<head-word member3 ref> = $R',
                              '<head-word member3 ref> = $R']},
 'HEAD-WORD_GROUP4': {'set': ['<head-word ref> += $R', '<head> += $R'],
                      'regex': [],
                      'match': ['<head-word member4 ref> = $R',
                              '<head-word member4 ref> = $R']},
 'HEAD-WORD_GROUP5': {'set': ['<head-word ref> += $R', '<head> += $R'],
                      'regex': [],
                      'match': ['<head-word member5 ref> = $R',
                              '<head-word member5 ref> = $R']},
 'HEAD-WORD_GROUP6': {'set': ['<head-word ref> += $R', '<head> += $R'],
                      'regex': [],
                      'match': ['<head-word member6 ref> = $R',
                              '<head-word member6 ref> = $R']},
 'HEAD_IDENTIFY': {'set': ['<HEAD-FLAG> = T'],
                   'regex': [],
                   'match': ['<tense> != %', '<tense MODAL-FLAG> = %']},
 'HEAD_INIT': {'set': ['<ref tense> = <tense name>'],
               'regex': [],
               'match': ['<HEAD-FLAG> = T']},
 'HEAD_TO_CLAUSE_AND_WALL': {'set': ['<F_L head-word> += <F_R head-word>'],
                             'regex': ['=  W\.*| C\.*| RS\.*| Qd\.*',
                                       '!=  C[ie]| Ct\.*',
                                       '!=  W[qs]\.*'],
                             'match': []},
 'HEAD_TO_FIRST_VERB': {'set': ['<tense first_verb head-word> += <this>'],
                        'regex': [],
                        'match': ['<HEAD-FLAG> = T']},
 'HEAD_TO_SUBJ_AND_OBJ1': {'set': ['<F_L head-word> += <F_R head-word>'],
                           'regex': ['=  S\.*| SX\.*| B.w\.*| SF\.*'],
                           'match': []},
 'HEAD_TO_SUBJ_AND_OBJ2': {'set': ['<F_L head-word> += <F_R head-word>'],
                           'regex': ['=  S\.*| SX\.*'],
                           'match': []},
 'HEAD_WORD_REF_TO_HEAD': {'set': ['<head> = $R']