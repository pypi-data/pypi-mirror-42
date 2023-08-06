#include <Python.h>
#include <driveline/dl_video_sdk.h>

typedef struct {
  PyObject_HEAD
  /* Type-specific fields go here. */
  struct pablo_video_decoder* decoder;
} video_decoder_t;

static PyObject* vd_new(PyTypeObject* type, PyObject* args, PyObject* kwargs) {
  video_decoder_t* self = (video_decoder_t*) type->tp_alloc(type, 0);
  if (self == NULL) {
    return NULL;
  }
  self->decoder = pablo_sdk_init_decoder();
  if (self->decoder == NULL) {
    type->tp_free((PyObject*) self);
    return NULL;
  }
  return (PyObject*) self;
};

static void vd_dealloc(video_decoder_t* self) {
  if (self != NULL) {
    if (self->decoder != NULL) {
      pablo_sdk_free_decoder(self->decoder);
    }
    Py_TYPE(self)->tp_free((PyObject*) self);
  }
}

static PyObject* vd_decode(video_decoder_t* self, PyObject* args) {
  const char* data = NULL;
  int length = 0;

  if (PyArg_ParseTuple(args, "y#", &data, &length) == 0) {
    PyErr_SetString(PyExc_ValueError, "byte string expected");
    return NULL;
  }

  if (length == 0) {
    Py_RETURN_NONE;
  }

  if (!pablo_sdk_decode(self->decoder, data, (size_t) length)) {
    PyErr_SetString(PyExc_BufferError, "decoding error");
    return NULL;
  }

  Py_RETURN_NONE;
}

static PyObject* vd_convert_frame(struct pablo_video_frame* frame) {
  PyObject* data = NULL;
  PyObject* stride = NULL;

  data = Py_BuildValue("[y#, y#, y#, y#, y#, y#, y#, y#]",
    (const char*) frame->data[0], frame->data[0] == NULL ? 0 : frame->stride[0] * frame ->height,
    (const char*) frame->data[1], frame->data[1] == NULL ? 0 : frame->stride[1] * frame ->height,
    (const char*) frame->data[2], frame->data[2] == NULL ? 0 : frame->stride[2] * frame ->height,
    (const char*) frame->data[3], frame->data[3] == NULL ? 0 : frame->stride[3] * frame ->height,
    (const char*) frame->data[4], frame->data[4] == NULL ? 0 : frame->stride[4] * frame ->height,
    (const char*) frame->data[5], frame->data[5] == NULL ? 0 : frame->stride[5] * frame ->height,
    (const char*) frame->data[6], frame->data[6] == NULL ? 0 : frame->stride[6] * frame ->height,
    (const char*) frame->data[7], frame->data[7] == NULL ? 0 : frame->stride[7] * frame ->height
  );

  if (data == NULL) {
    goto exit_failure;
  }

  stride = Py_BuildValue("[i, i, i, i, i, i, i, i]",
      frame->stride[0], frame->stride[1], frame->stride[2], frame->stride[3],
      frame->stride[4], frame->stride[5], frame->stride[6], frame->stride[7]) ;

  if (stride == NULL) {
    goto exit_failure;
  }

  PyObject* result = Py_BuildValue("{s:i, s:i, s:N, s:N}",
    "width", frame->width,
    "height", frame->height,
    "data", data,
    "stride", stride
  );

  if (result == NULL) {
    goto exit_failure;
  }
  return result;

exit_failure:
  Py_XDECREF(data);
  Py_XDECREF(stride);
  return NULL;
}

static PyObject* vd_next_frame(video_decoder_t* self, PyObject* args) {
  struct pablo_video_frame frame;
  int rc = pablo_sdk_next_frame(self->decoder, &frame);
  if (rc == 0) {
    Py_RETURN_NONE;
  }
  PyObject* pyFrame = vd_convert_frame(&frame);
  if (PyErr_Occurred()) {
    return NULL;
  }
  return pyFrame;
}

static PyMethodDef video_decoder_methods[] = {
  {"decode",     (PyCFunction) vd_decode,     METH_VARARGS, "decode a chunk of binary data"},
  {"next_frame", (PyCFunction) vd_next_frame, METH_NOARGS,  "get a frame from the decoder"},
  {NULL, NULL, 0, NULL}
};

static PyTypeObject VideoDecoderType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  .tp_name = "driveline.video.VideoDecoder",
  .tp_doc = "Video decoder",

  .tp_basicsize = sizeof(video_decoder_t),
  .tp_itemsize = 0,

  .tp_flags = Py_TPFLAGS_DEFAULT,
  .tp_methods = video_decoder_methods,
  .tp_new = vd_new,
  .tp_dealloc=  (destructor) vd_dealloc,
};

static struct PyModuleDef module = {
  .m_base = PyModuleDef_HEAD_INIT,
  .m_name= "_driveline_video",
  .m_doc = NULL,
  .m_size =  0,
};

PyMODINIT_FUNC PyInit__driveline_video(void) {
  if (PyType_Ready(&VideoDecoderType) < 0) {
    return NULL;
  }

  PyObject* m = PyModule_Create(&module);
  if (m == NULL) {
    return NULL;
  }
  Py_INCREF(&VideoDecoderType);
  PyModule_AddObject(m, "VideoDecoder", (PyObject*) &VideoDecoderType);
  return m;
}
