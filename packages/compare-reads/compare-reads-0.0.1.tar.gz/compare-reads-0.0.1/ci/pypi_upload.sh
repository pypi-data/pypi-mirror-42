#!/bin/bash
if [ "$WHEEL" == "1" ]; then
    python -m pip install twine
    python -m twine upload wheelhouse/*.whl
fi
