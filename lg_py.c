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
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    0,                         
    Py_TPFLAGS_DEFAULT,        
    "linkgrammar objects",     
};
static void Sentence_dealloc(Noddy* self){
    Py_XDECREF(self->word_list);
    Py_XDECREF(self->span_list);
    Py_XDECREF(self->links_list);
    Py_XDECREF(self->tag_list);
    Py_XDECREF(self->tag_pair_list);

    self->ob_type->tp_free((PyObject*)self);
}

static PyObject *Sentence_new(PyTypeObject *type, PyObject *args, PyObject *kwds){
    Sentence *self;

    self = (Sentence *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->word_list = PyList_New(0);
        if (self->word_list == NULL){
            Py_DECREF(self);
            return NULL;
        }
        
        self->span_list = PyList_New(0);
        if (self->span_list == NULL){
            Py_DECREF(self);
            return NULL;
        }

        self->links_list = PyList_New(0);
        if (self->links_list == NULL){
            Py_DECREF(self);
            return NULL;
        }
        self->tag_list = PyList_New(0);
        if (self->tag_list == NULL){
            Py_DECREF(self);
            return NULL;
        }
        self->tag_pair_list = PyList_New(0);
        if (self->tag_pair_list == NULL){
            Py_DECREF(self);
            return NULL;
        }

        self->number = 0;
    }

    return (PyObject *)self;
}


static int Sentence_init(Sentence *self, PyObject *args, PyObject *kwds){
    PyObject *word_list = NULL;
    PyObject *span_list = NULL;
    PyObject *links_list = NULL;
    PyObject *tag_list = NULL;
    PyObject *tag_pair_list = NULL;
    
    static char *kwlist[] = {"word_list", "span_list",
     "links_list", "tag_list", "tag_pair_list", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOOOO", kwlist, 
                                      &first, &last, 
                                      &self->number))
        return -1; 

    if (first) {
        tmp = self->first;
        Py_INCREF(first);
        self->first = first;
        Py_XDECREF(tmp);
    }

    if (last) {
        tmp = self->last;
        Py_INCREF(last);
        self->last = last;
        Py_XDECREF(tmp);
    }

    return 0;
}

*/


/// This is the basic sentence dissection
static PyObject *sentence(PyObject *self, PyObject *args){
    Dictionary    dict;
    Parse_Options opts;
    Sentence      sent;
    Linkage       linkage;
    Linkage       sub_linkage;
    char *        diagram;

    /// Link counts
    int   num_linkages;
    int   links;

    ///  Index's for the iterators
    int   link_idx;
    int   word_idx;
