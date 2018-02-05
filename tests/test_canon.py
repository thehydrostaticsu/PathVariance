import unittest

from pathvariance.canon import (
    CanonOptions,
    canonicalise,
    label_paths,
    signature_id,
)
from pathvariance.runs import Run, Step


def _run(tools, args=None):
    steps = []
    for i, t in enumerate(tools):
