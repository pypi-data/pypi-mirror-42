#ifndef OCCA_PY_DEFINES_HEADER
#define OCCA_PY_DEFINES_HEADER

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <structmember.h>
#include <numpy/arrayobject.h>
#include <numpy/arrayscalars.h>
#include <numpy/npy_common.h>

#include <occa.hpp>


#if PY_MAJOR_VERSION == 3
#  define OCCA_PY3 1
#  define OCCA_PY2 0
#elif PY_MAJOR_VERSION == 2
#  define OCCA_PY3 0
#  define OCCA_PY2 1
#endif


#define OCCA_PY_METHOD(NAME, FUNC, TYPE)        \
  { NAME, (PyCFunction) FUNC, TYPE, NULL }

#define OCCA_PY_METHOD_NO_ARGS(NAME, FUNC)      \
  OCCA_PY_METHOD(NAME, FUNC, METH_NOARGS)

#define OCCA_PY_METHOD_WITH_ARGS(NAME, FUNC)    \
  OCCA_PY_METHOD(NAME, FUNC, METH_VARARGS)

#define OCCA_PY_METHOD_WITH_KWARGS(NAME, FUNC)              \
  OCCA_PY_METHOD(NAME, FUNC, METH_VARARGS | METH_KEYWORDS)


#define OCCA_PY_NO_METHODS                      \
  {NULL, NULL, 0, NULL}


#define OCCA_PY_METHODS(METHODS, ...)           \
  static PyMethodDef METHODS[] = {              \
    __VA_ARGS__,                                \
    {NULL, NULL, 0, NULL}                       \
  }


// Python 3.X
#if OCCA_PY3
#  define OCCA_PY_MODULE(MODULE, ...)                               \
  OCCA_PY_METHODS(occa_c_##MODULE##_methods,                        \
                  __VA_ARGS__);                                     \
                                                                    \
  static PyModuleDef occa_c_##MODULE##_module = {                   \
    PyModuleDef_HEAD_INIT,                                          \
    "occa.c." #MODULE,                                              \
    "Wrappers for " #MODULE " methods",                             \
    -1,                                                             \
    occa_c_##MODULE##_methods                                       \
  };                                                                \
                                                                    \
  OCCA_START_EXTERN_C                                               \
  PyMODINIT_FUNC PyInit_##MODULE() {                                \
    import_array();                                                 \
    if (!MODULE##_has_valid_module()) {                             \
      return NULL;                                                  \
    }                                                               \
    PyObject *module = PyModule_Create(&occa_c_##MODULE##_module);  \
    if (!module) {                                                  \
      return NULL;                                                  \
    }                                                               \
    MODULE##_init_module(module);                                   \
    return module;                                                  \
  }                                                                 \
  OCCA_END_EXTERN_C
// Python 2.X
#elif OCCA_PY2
#  define OCCA_PY_MODULE(MODULE, ...)                                   \
  OCCA_PY_METHODS(occa_c_##MODULE##_methods,                            \
                  __VA_ARGS__);                                         \
                                                                        \
  OCCA_START_EXTERN_C                                                   \
  PyMODINIT_FUNC init##MODULE() {                                       \
    import_array();                                                     \
    if (!MODULE##_has_valid_module()) {                                 \
      return;                                                           \
    }                                                                   \
    PyObject *module = Py_InitModule("occa.c." #MODULE,                 \
                                     occa_c_##MODULE##_methods);        \
    if (module) {                                                       \
      MODULE##_init_module(module);                                     \
    }                                                                   \
  }                                                                     \
  OCCA_END_EXTERN_C
// Python ?.X
#else
#  error "Unsupported Python major version: " #PY_MAJOR_VERSION
#endif

#endif
