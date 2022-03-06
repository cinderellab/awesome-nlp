Overview
========
An interface to link grammar to build and extend the idea

Semantic Matching
=================
For the semantic matching i have a set rules, the input tags are run through 
a non-deterministic finite state machine that keeps left and right registers.
The rule sets are as follows, each rule has a regular expression to match to,
it also has a set of registers to match to and then set if they match.

Semantic rule tokenizing
========================
I have another non-deterministic finite state machine(read: regex finite state
machine) to parse the rules that were taken from RelEx into something that is
manageable.

Pre-requisites
==============
- Python 2.5+
- Link Grammar (newest)

File Overview
=============
- debug.py          -- for the pretty print debug function
- grammar_fsm.py    -- contains the FSM for the semantics
- help.py           -- will contain help in the f