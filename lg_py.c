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
    int   num_words;
    long   span;
    long   sub_linkages;

    const char *text;
    const char *d_output;

    PyObject *output_list;
    PyObject *word_list;
    PyObject *word2_list;
    PyObject *span_list;
    PyObject *temp;
    PyObject *sublinkage_list;
    PyObject *_diagram;

    output_list = PyList_New(0);
    word_list   = PyList_New(0);
    word2_list  = PyList_New(0);
    sublinkage_list = PyList_New(0);

    span_list = PyList_New(0);

    if (!PyArg_ParseTuple(args, "s", &text))
        return NULL;

    opts = parse_options_create();
    parse_options_set_verbosity(opts, -1);
    parse_options_set_screen_width(opts, 50);

    setlocale(LC_ALL, "");
    dict = dictionary_create_default_lang();

    if (!dict) {
        PyErr_SetString(PyExc_RuntimeError, "Fatal error: Unable to open the dictionary");
        Py_INCREF(Py_None);
        return Py_None;
    }
    
    sent = sentence_create(text, dict);
    sentence_split(sent, opts);
    num_linkages = sentence_parse(sent, opts);

    if (num_linkages > 0) {
        linkage = linkage_create(0, sent, opts);
        /// Get the lengths of everything
        num_words = linkage_get_num_words(linkage);
        links = linkage_get_num_links(linkage);

        for(link_idx=0; link_idx < links; link_idx++){
                PyObject *temp_subLen;

                diagram = linkage_print_diagram(linkage);
                _diagram = PyString_FromString(diagram);

                sub_linkage = linkage_create(link_idx, sent, opts);
                sub_linkages = linkage_get_num_sublinkages(linkage);

                temp_subLen = PyLong_FromLong(sub_linkages);
                linkage_delete(sub_linkage);
                PyList_Append(sublinkage_list, temp_subLen);

                span = linkage_get_link_length(linkage, link_idx);
                PyList_Append(span_list, PyInt_FromLong(span));
                
                PyObject *temp_list;
                temp_list = PyL