# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Utilities for IBM Q provider."""


import json

from numpy import ndarray

from qiskit.qobj import QobjConfig


class NumpyJSONEncoder(json.JSONEncoder):
    """JSON encoder for NumPy arrays and complex numbers.

    This functions as the standard JSON Encoder but adds support
    for encoding:
        * complex numbers z as lists [z.real, z.imag]
        * ndarrays as nested lists.
    """

    # pylint: disable=method-hidden,arguments-differ
    def default(self, obj):
        if isinstance(obj, ndarray):
            return obj.tolist()
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        if hasattr(obj, "as_dict"):
            return obj.as_dict()
        return super().default(obj)


def update_qobj(qobj, backend_options=None, noise_model=None):
    """Update a Qobj appending backend options and noise model.

    Args:
        qobj (Qobj): qobj.
        backend_options (dict): dictionary of backend options.
        noise_model (NoiseModel): noise model.
    """
    original_config = qobj.config
    config = original_config.as_dict()

    if backend_options:
        for key, val in backend_options:
            config[key] = val

    if noise_model:
        a = json.dumps(noise_model, cls=NumpyJSONEncoder)
        b = json.loads(a)
        config['noise_model'] = b

    qobj.config = QobjConfig.from_dict(config)
