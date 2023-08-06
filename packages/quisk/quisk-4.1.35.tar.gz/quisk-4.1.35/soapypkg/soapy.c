#include <Python.h>
#include <complex.h>
#include <SoapySDR/Device.h>
#include <SoapySDR/Formats.h>

#define IMPORT_QUISK_API
#include "quisk.h"

// This module was written by James Ahlstrom, N2ADR.

// This module uses the Python interface to import symbols from the parent _quisk
// extension module.  It must be linked with import_quisk_api.c.  See the documentation
// at the start of import_quisk_api.c.

#define DEBUG		0

#define RX_BUF_SIZE	(SAMP_BUFFER_SIZE / 2)
static SoapySDRDevice * soapy_sample_device;		// device for the sample stream
static SoapySDRDevice * soapy_config_device;		// device for configuration, not samples
static SoapySDRStream * rxStream;
static double rx_sample_rate = 48000;
static complex float stream_buffer[RX_BUF_SIZE];
static void * stream_buffs[] = {stream_buffer};
static int shutdown_sample_device;
static int data_poll_usec = 10000;

// Start sample capture; called from the sound thread.
static void quisk_start_samples(void)
{
	//setup a stream (complex floats)
	if (SoapySDRDevice_setupStream(soapy_sample_device, &rxStream, SOAPY_SDR_RX, SOAPY_SDR_CF32, NULL, 0, NULL) != 0) {
		printf("Soapy setupStream fail: %s\n", SoapySDRDevice_lastError());
	}
	else {
		SoapySDRDevice_activateStream(soapy_sample_device, rxStream, 0, 0, 0); //start streaming
	}
}

// Stop sample capture; called from the sound thread.
static void quisk_stop_samples(void)
{
	shutdown_sample_device = 1;
	if (rxStream) {
		SoapySDRDevice_deactivateStream(soapy_sample_device, rxStream, 0, 0); //stop streaming
		SoapySDRDevice_closeStream(soapy_sample_device, rxStream);
		rxStream = NULL;
	}
}

// Called in a loop to read samples; called from the sound thread.
static int quisk_read_samples(complex double * cSamples)
{
	int i, flags; //flags set by receive operation
	long long timeNs; //timestamp for receive buffer
	int ret;
	int num_samp;

	num_samp = (int)(rx_sample_rate * (data_poll_usec * 1E-6));
	num_samp = ((num_samp + 255) / 256) * 256;
	if (num_samp > RX_BUF_SIZE)
		num_samp = RX_BUF_SIZE;
	if (shutdown_sample_device) {
		if (rxStream) {
			quisk_stop_samples();
		}
		if (soapy_sample_device) {
			SoapySDRDevice_unmake(soapy_sample_device);
			soapy_sample_device = NULL;
		}
		ret = num_samp;
		for (i = 0; i < ret; i++)
			cSamples[i] = 0;
	}
	else if (rxStream) {
		ret = SoapySDRDevice_readStream(soapy_sample_device, rxStream, stream_buffs, num_samp, &flags, &timeNs, data_poll_usec * 2);
		if (ret < 0) {
			pt_quisk_sound_state->read_error++;
			ret = 0;
		}
		pt_quisk_sound_state->latencyCapt = 0;
		for (i = 0; i < ret; i++)
			cSamples[i] = stream_buffer[i] * CLIP32;
	}
	else {
		ret = num_samp;
		for (i = 0; i < ret; i++)
			cSamples[i] = 0;
	}
	return ret;	// return number of samples
}

// Called to close the sample source; called from the GUI thread.
static PyObject * close_device(PyObject * self, PyObject * args)
{
	int sample_device;

	if (!PyArg_ParseTuple (args, "i", &sample_device))
		return NULL;
	if (sample_device) {
		shutdown_sample_device = 1;
	}
	else {
		if (soapy_config_device) {
			SoapySDRDevice_unmake(soapy_config_device);
			soapy_config_device = NULL;
		}
	}
	Py_INCREF (Py_None);
	return Py_None;
}

// Called to open the SoapySDR device, and perhaps start samples; called from the GUI thread.
static PyObject * open_device(PyObject * self, PyObject * args)
{
	int sample_device, poll;
	const char * name;
	char buf128[128];
	SoapySDRDevice * sdev;

	if (!PyArg_ParseTuple (args, "sii", &name, &sample_device, &poll))
		return NULL;
	sdev = SoapySDRDevice_makeStrArgs(name);
	if(sdev) {
		snprintf(buf128, 128, "Capture from %s", name);
		if (sample_device) {
			shutdown_sample_device = 0;
			soapy_sample_device = sdev;
			data_poll_usec = poll;
			// Record our C-language Start/Stop/Read functions for use by sound.c.
			quisk_sample_source(&quisk_start_samples, &quisk_stop_samples, &quisk_read_samples);
		}
		else {
			soapy_config_device = sdev;
		}
	}
	else {
		snprintf(buf128, 128, "SoapySDRDevice_make fail: %s", SoapySDRDevice_lastError());
	}
	return PyString_FromString(buf128);
}

static void get_direc_len(const char * name, int * direction, int * length)
{  // return the direction (Rx or Tx) and length of name to compare
	*length = strlen(name);
	*direction = SOAPY_SDR_RX;
	if (*length < 4)
		return;
	if (name[*length - 1] == 'x' && name[*length - 3] == '_') {	// ends in "_rx" or "_tx"
		if (name[*length - 2] == 't')
			*direction = SOAPY_SDR_TX;
		*length -= 3;
	}
}

// Get a list of SoapySDR devices
static PyObject * get_device_list(PyObject * self, PyObject * args)	// Called from GUI thread
{
	PyObject * devices;
	PyObject * dict;
	size_t length, i, j;
	SoapySDRKwargs * results;

	if (!PyArg_ParseTuple (args, ""))
		return NULL;
	devices = PyList_New(0);
	results = SoapySDRDevice_enumerate(NULL, &length);
	for (i = 0; i < length; i++) {
		dict = PyDict_New();
		for (j = 0; j < results[i].size; j++)
			PyDict_SetItemString(dict, results[i].keys[j], PyString_FromString(results[i].vals[j]));
		PyList_Append(devices, dict);
		Py_DECREF(dict);
	}
	SoapySDRKwargsList_clear(results, length);
	return devices;
}

// Set a float parameter
static PyObject * set_parameterD(PyObject * self, PyObject * args)
{
	int direction, length;
	char * name;
	double datum;

	if (!PyArg_ParseTuple (args, "sd", &name, &datum))
		return NULL;
	printf ("Set %s to %lf\n", name, datum);
	get_direc_len(name, &direction, &length);
	if (soapy_sample_device) {
		if ( ! strncmp(name, "soapy_freq", length)) {
			if (SoapySDRDevice_setFrequency(soapy_sample_device, direction, 0, datum, NULL) != 0) {
				printf("Soapy setFrequency fail: %s\n", SoapySDRDevice_lastError());
			}
		}
		else if ( ! strncmp(name, "soapy_sample_rate", length)) {
			if (direction == SOAPY_SDR_RX)
				rx_sample_rate = datum;
			if (soapy_sample_device && SoapySDRDevice_setSampleRate(soapy_sample_device, direction, 0, datum) != 0)
				printf("Soapy setSampleRate fail: %s\n", SoapySDRDevice_lastError());
		}
		else if ( ! strncmp(name, "soapy_gain", length)) {
			if (soapy_sample_device && SoapySDRDevice_setGain(soapy_sample_device, direction, 0, datum) != 0)
				printf("Soapy setGain fail: %s\n", SoapySDRDevice_lastError());
		}
		else {
			printf("Soapy set_parameterD() for unknown name %s\n", name);
		}
	}
	Py_INCREF (Py_None);
	return Py_None;
}

// Set a string parameter
static PyObject * set_parameterS(PyObject * self, PyObject * args)
{
	int direction, length;
	char * name;
	char * datum;

	if (!PyArg_ParseTuple (args, "ss", &name, &datum))
		return NULL;
	printf("Set %s to %s\n", name, datum);
	get_direc_len(name, &direction, &length);
	if (soapy_sample_device && datum[0]) {		// do not set zero length datum
		if ( ! strncmp(name, "soapy_antenna", length)) {
			if (SoapySDRDevice_setAntenna(soapy_sample_device, direction, 0, datum) != 0)
				printf("Soapy setAntenna fail: %s\n", SoapySDRDevice_lastError());
		}
		else {
			printf("Soapy set_parameterS() for unknown name %s\n", name);
		}
	}
	Py_INCREF (Py_None);
	return Py_None;
}

static PyObject * get_parameter(PyObject * self, PyObject * args)	// Called from GUI thread
{ // Return a Python list of string names or string [min, m2, m3, ..., max] for a parameter name.
  // Parameter name can end in "_rx" or "_tx" to specify direction.
	int sample_device, direction, length;
	double step, dd;
	char buf32[32];
	char * name;
	char ** names;
	size_t i, len_list;
	PyObject * pylist, * pyobj;
	SoapySDRDevice * sdev;
	SoapySDRRange range;

	if (!PyArg_ParseTuple (args, "si", &name, &sample_device))
		return NULL;
	if (sample_device)
		sdev = soapy_sample_device;
	else
		sdev = soapy_config_device;
	get_direc_len(name, &direction, &length);
	pylist = PyList_New(0);
	if ( ! sdev) {
		;
	}
	else if ( ! strncmp(name, "soapy_antenna", length)) {		// _rx or _tx
		names = SoapySDRDevice_listAntennas(sdev, direction, 0, &len_list);
		for (i = 0; i < len_list; i++) {
			pyobj = PyString_FromString(names[i]);
			PyList_Append(pylist, pyobj);
			Py_DECREF(pyobj);
		}
		SoapySDRStrings_clear(&names, len_list);
	}
	else if ( ! strncmp(name, "soapy_gain", length)) {		// _rx or _tx
		range = SoapySDRDevice_getGainRange(sdev, direction, 0);
		step = range.step;
		if (range.maximum - range.minimum < 1E-4) {
			snprintf(buf32, 32, "%.3lf", range.minimum);
			pyobj = PyString_FromString(buf32);
			PyList_Append(pylist, pyobj);
			Py_DECREF(pyobj);
		}
		else if (step < 1E-4) {
			step = (range.maximum - range.minimum) / 4.0;
			dd = range.minimum;
			for (i = 0; i < 5; i++) {
				snprintf(buf32, 32, "%.3lf", dd);
				pyobj = PyString_FromString(buf32);
				PyList_Append(pylist, pyobj);
				Py_DECREF(pyobj);
				dd += step;
			}
		}
		else {
			dd = range.minimum;
			for (i = 0; i < 5; i++) {
				snprintf(buf32, 32, "%.3lf", dd);
				pyobj = pylist, PyString_FromString(buf32);
				PyList_Append(pylist, pyobj);
				Py_DECREF(pyobj);
				dd += step;
				if (dd > range.maximum - 1E-4)
					break;
			}
			snprintf(buf32, 32, "%.3lf", range.maximum);
			pyobj = PyString_FromString(buf32);
			PyList_Append(pylist, pyobj);
			Py_DECREF(pyobj);
		}
	}
	else {
		printf("Soapy get_parameter() for unknown name %s\n", name);
	}
	return pylist;
}

// Functions callable from Python are listed here:
static PyMethodDef QuiskMethods[] = {
	{"open_device", open_device, METH_VARARGS, "Open the hardware."},
	{"close_device", close_device, METH_VARARGS, "Close the hardware"},
	{"get_device_list", get_device_list, METH_VARARGS, "Return a list of SoapySDR devices"},
	{"get_parameter", get_parameter, METH_VARARGS, "Return a list of choices for a SoapySDR parameter"},
	{"set_parameterD", set_parameterD, METH_VARARGS, "Set float parameter"},
	{"set_parameterS", set_parameterS, METH_VARARGS, "Set string parameter"},
	{NULL, NULL, 0, NULL}		/* Sentinel */
};

// Initialization, and registration of public symbol "initsoapy":
PyMODINIT_FUNC initsoapy (void)
{
	if (Py_InitModule ("soapy", QuiskMethods) == NULL) {
		printf("Py_InitModule failed!\n");
		return;
	}
	// Import pointers to functions and variables from module _quisk
	if (import_quisk_api()) {
		printf("Failure to import pointers from _quisk\n");
		return;		//Error
	}
}
