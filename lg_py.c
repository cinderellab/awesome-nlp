#include "Python.h"
#include <locale.h>
#include "link-includes.h"
/*
typedef struct {
    PyObject_HEAD
    PyObject *word_list;
    PyObject *span_list;
    PyObject *links_list;
    PyObject *tag_list;
    PyObject *tag_pair_list;
    
    
    
} Sentence;

static PyTypeObject linkgrammar_SentenceType = {
    PyObject_HEAD_INIT(NULL)
    0,                         
    "linkgrammar.Sentence",    
    sizeof(Sentence),          
    0,             