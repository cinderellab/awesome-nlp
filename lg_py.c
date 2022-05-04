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
  