# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""Checker for Python and msticpy versions."""
import os
import sys
from IPython.display import display, HTML


MISSING_PKG_ERR = """
    <h3><font color='orange'>The package '<b>{package}</b>' is not
    installed or has an incorrect version</font></h3>
    <h4>Please install this now</h4>
    """
MIN_PYTHON_VER_DEF = (3, 6)
MSTICPY_REQ_VERSION = (0, 5, 2)


def check_python_ver(min_py_ver=MIN_PYTHON_VER_DEF):
    """
    Check the current version of the Python kernel.

    Parameters
    ----------
    min_py_ver : Tuple[int, int]
        Minimum Python version

    Raises
    ------
    RuntimeError
        If the Python version does not support the notebook.

    """
    display(HTML("Checking Python kernel version..."))
    if sys.version_info < min_py_ver:
        display(
            HTML(
                """
            <h3><font color='red'>This notebook requires a different notebook
            (Python) kernel version.</h3></font>
            From the Notebook menu (above), choose <b>Kernel</b> then
            <b>Change Kernel...</b> from the menu.<br>
            Select a <b>Python %s.%s</b> (or later) version kernel and then re-run
            this cell.<br><br>
            """
                % min_py_ver
            )
        )
        display(
            HTML(
                """
            Please see the <b><a href="./TroubleShootingNotebooks.ipynb">
            TroubleShootingNotebooks</a></b>
            in this folder for more information<br><br><hr>
            """
            )
        )
        raise RuntimeError("Python %s.%s or later kernel is required." % min_py_ver)

    display(
        HTML(
            "Python kernel version %s.%s.%s OK"
            % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
        )
    )

    _check_nteract()


# pylint: disable=import-outside-toplevel
def check_mp_ver(min_msticpy_ver=MSTICPY_REQ_VERSION):
    """
    Check and optionally update the current version of msticpy.

    Parameters
    ----------
    min_py_ver : Tuple[int, int]
        Minimum Python version

    Raises
    ------
    RuntimeError
        If the Python version does not support the notebook.

    """
    display(HTML("Checking msticpy version..."))
    try:
        import msticpy
        wrong_ver_err = "msticpy %s.%s.%s or later is needed." % min_msticpy_ver
        mp_version = tuple([int(v) for v in msticpy.__version__.split(".")])
        if mp_version < min_msticpy_ver:
            raise ImportError(wrong_ver_err)

    except ImportError:
        display(HTML(MISSING_PKG_ERR.format(package="msticpy")))
        resp = input("Install? (y/n)")  # nosec
        if resp.casefold().startswith("y"):
            raise ImportError("Install msticpy")

        display(
            HTML(
                """
            <h3><font color='red'>The notebook cannot be run without
            the correct version of '<b>%s</b>' (%s.%s.%s or later)
            </font></h3>
            Please see the <b><a href="./TroubleShootingNotebooks.ipynb">
            TroubleShootingNotebooks</a></b>
            in this folder for more information<br><br><hr>
            """
                % ("msticpy", *min_msticpy_ver)
            )
        )
        raise RuntimeError(wrong_ver_err)

    display(HTML("msticpy version %s.%s.%s OK" % mp_version))


_NTERACT_MSSG = """
<b>Azure ML detected</b><br>
It looks like this notebook is running in an Azure Machine Learning workspace.
If you using the AzureML native notebook interface
(i.e. not Jupyter or Jupyter lab) we need to adjust a
setting for the UI to behave properly.
Ignoring or answering "n" will not affect the functionality of the notebook
but you may see some extraneous UI elements being displayed.
"""


def _check_nteract():
    if os.environ.get("USER", "").casefold() == "azureuser":
        display(HTML(_NTERACT_MSSG))
        set_app = input("Configure for Azure ML Notebooks? (y/n)")  # nosec
        if set_app.casefold().startswith("y"):
            os.environ["KQLMAGIC_NOTEBOOK_APP"] = "nteract"
