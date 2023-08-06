# DSS Python: Unofficial bindings for EPRI's OpenDSS

Python bindings and misc tools for using OpenDSS (EPRI Distribution System Simulator). Based on CFFI and DSS C-API, aiming for full COM compatibility on Windows, Linux and MacOS.

See also the other projects from [DSS-Extensions.org](https://dss-extensions.org/):

- [DSS C-API library](http://github.com/dss-extensions/dss_capi/): the base library that exposes a slightly modified version of EPRI's OpenDSS through a more traditional C interface, built with the open-source Free Pascal compiler instead of Delphi.
- [OpenDSSDirect.py](http://github.com/dss-extensions/OpenDSSDirect.py/): if you don't need COM compatibility, or just would like to check its extra funcionalities. You can mix DSS Python and OpenDSSDirect.py -- for example, if you have old code using the official COM objects, you could quickly switch to DSS Python with very few code changes, and then use [`opendssdirect.utils`](https://dss-extensions.org/OpenDSSDirect.py/opendssdirect.html#module-opendssdirect.utils) to generate some DataFrames.
- [OpenDSSDirect.jl](http://github.com/dss-extensions/OpenDSSDirect.jl/): a Julia module, created by Tom Short (@tshort), recently migrated with the help of Dheepak Krishnamurthy (@kdheepak) to DSS C-API instead of the DDLL.
- [DSS Sharp](http://github.com/dss-extensions/dss_sharp/): available for .NET/C#, also mimics the COM classes, but Windows-only at the moment. Soon it will be possible to use it via COM too.
- [DSS MATLAB](http://github.com/dss-extensions/dss_matlab/): presents multi-platform integration (Windows, Linux, MacOS) with DSS C-API and is also very compatible with the COM classes.

Version 0.10.2, based on OpenDSS revision 2504. While we plan to add a lot more funcionality into DSS Python, the main goal of creating a COM-compatible API has been reached. If you find an unexpected missing feature, please report it!

This module mimics the COM structure (as exposed via `win32com` or `comtypes`), effectively enabling multi-platform compatibility at Python level.
Most of the COM documentation can be used as-is, but instead of returning tuples or lists, this modules returns/accepts NumPy arrays for numeric data exchange. 

The module depends on CFFI, NumPy and, optionally, SciPy.Sparse for reading the sparse system admittance matrix.

## Recent changes

Check the [changelog](docs/changelog.md#0101) document for a more detailed list.

- **2019-02-28 / version 0.10.2: Some small fixes, adds the missing `CtrlQueue.Push`, faster LoadShapes and new property `DSS.AllowEditor` to toggle editor calls.**
- 2019-02-17 / version 0.10.1: Integrate DSS C-API changes/fix, some small fixes, and more error-checking. 
- 2018-11-17 / version 0.10.0: Lots of changes, fixes and new features. Check the new [changelog](docs/changelog.md#0100) document for a list.
- 2018-08-12 / version 0.9.8: Reorganize modules (v7 and v8), adds 8 missing methods and new backend methods for OpenDSSDirect.py v0.3+. Integrates many fixes from DSS_CAPI and the upstream OpenDSS.
- 2018-04-30 / version 0.9.7: Fix some of the setters that used array data.
- 2018-04-05 / version 0.9.6: Adds missing `ActiveCircuit.CktElements[index]` (or `...CktElements(index)`) and `ActiveCircuit.Buses[index]` (or `...Buses(index)`).
- 2018-03-07 / version 0.9.4: Allows using `len` on several classes, fixes DSSProperty, and includes COM helpstrings as docstrings. Contains changes up to OpenDSS revision 2152.
- 2018-02-16 / version 0.9.3: Integrates COM interface fixes from revision 2136 (`First` `Next` iteration on some elements)
- 2018-02-12 / version 0.9.2: Experimental support for OpenDSS-PM (at the moment, a custom patch is provided for FreePascal support) and port COM interface fixes (OpenDSS revision 2134)
- 2018-02-08 / version 0.9.1: First public release (OpenDSS revision 2123)


## Missing features and limitations

Most limitations are inherited from `dss_capi`, i.e., these are not implemented:

- `DSSEvents` from `DLL/ImplEvents.pas`: seems too dependent on COM.
- `DSSProgress` from `DLL/ImplDSSProgress.pas`: would need a reimplementation depending on the target UI (GUI, text, headless, etc.).

In general, the DLL from `dss_capi` provides more features than both the official Direct DLL and the COM object.

## Extra features

Besides most of the COM methods, some of the unique DDLL methods are also exposed in adapted forms, namely the methods from `DYMatrix.pas`, especially `GetCompressedYMatrix` (check the source files for more information).

Since no GUI components are used in the FreePascal DLL, we are experimenting with different ways of handling OpenDSS errors. Currently, the `DSS.Text.Command` call checks for OpenDSS errors (through the `DSS.Error` interface) and converts those to Python exceptions. Ideally every error should be converted to Python exceptions, but that could negatively impact performance. You can manually trigger an error check by calling the function `CheckForError()` from the main module.


## Installing

On all major platforms, you can install directly from pip:

```
    pip install dss_python
```

Or, if you're using the Anaconda distribution, you can use:

```
    conda install -c pmeira dss_python
```

Binary wheels are provided for all major platforms (Windows, Linux and MacOS) and many combinations of Python versions (2.7, 3.4 to 3.7). If you have issues with a specific version, please open an issue about it. Conda packages support at least Python 2.7, 3.5, 3.6 and 3.7.

After a successful installation, you can then import the `dss` module from your Python interpreter.

## Building

Get this repository:

```
    git clone https://github.com/dss-extensions/dss_python.git
```    

Assuming you successfully built or downloaded the DSS C-API DLLs (check [its repository](http://github.com/dss-extensions/dss_capi/) for instructions), keep the folder organization as follows:

```
dss_capi/
dss_python/
electricdss-src/
```

Open a command prompt in the `dss_python` subfolder and run the build process:

```
python setup.py build
python setup.py install
```

If you are familiar with `conda-build`, there is a complete recipe to build DSS C-API, KLUSolve and DSS Python in the `conda` subfolder.

Example usage
=============

If you were using `win32com` in code like:

```python
import win32com.client 
dss_engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
```

or `comtypes`:

```python
import comtypes.client
dss_engine = comtypes.client.CreateObject("OpenDSSEngine.DSS")
```

you can replace that fragment with:
```python
import dss
dss.use_com_compat()
dss_engine = dss.DSS
```

Assuming you have a DSS script named `master.dss`, you should be able to run it as shown below:

```python
import dss
dss.use_com_compat()
dss_engine = dss.DSS

dss_engine.Text.Command = "compile c:/dss_files/master.dss"
dss_engine.ActiveCircuit.Solution.Solve()
voltages = dss_engine.ActiveCircuit.AllBusVolts

for i in range(len(voltages) // 2):
    print('node %d: %f + j%f' % (i, voltages[2*i], voltages[2*i + 1]))
```

If you do not need the mixed-cased handling, omit the call to `use_com_compat()` and use the casing used in this project, which should use most of the COM instance conventions.

If you want to play with the experimental OpenDSS-PM interface (from OpenDSS v8), it is installed side-by-side and you can import it as:

```python
import dss.v8
dss_engine = dss.v8.DSS
```

Although it is experimental, most of its funcionality is working. Depending on your use-case, the parallel interface can be an easy way of better using your machine resources. Otherwise, you can always use general distributed computing resources via Python.


Testing
=======
Since the DLL is built using the Free Pascal compiler, which is not officially supported by EPRI, the results are validated running sample networks provided in the official OpenDSS distribution. The only modifications are done directly by the script, removing interactive features and some other minor issues.

The validation scripts is `tests/validation.py` and requires the same folder structure as the building process. You need `win32com` to run it.

Currently, at least the following sample files from the official OpenDSS repository are used:

```
    Distrib/EPRITestCircuits/ckt5/Master_ckt5.dss
    Distrib/EPRITestCircuits/ckt7/Master_ckt7.dss
    Distrib/EPRITestCircuits/ckt24/Master_ckt24.dss
    Distrib/IEEETestCases/8500-Node/Master-unbal.dss
    Distrib/IEEETestCases/IEEE 30 Bus/Master.dss
    Distrib/IEEETestCases/NEVTestCase/NEVMASTER.DSS
    Distrib/IEEETestCases/37Bus/ieee37.dss
    Distrib/IEEETestCases/4Bus-DY-Bal/4Bus-DY-Bal.DSS
    Distrib/IEEETestCases/4Bus-GrdYD-Bal/4Bus-GrdYD-Bal.DSS
    Distrib/IEEETestCases/4Bus-OYOD-Bal/4Bus-OYOD-Bal.DSS
    Distrib/IEEETestCases/4Bus-OYOD-UnBal/4Bus-OYOD-UnBal.DSS
    Distrib/IEEETestCases/4Bus-YD-Bal/4Bus-YD-Bal.DSS
    Distrib/IEEETestCases/4Bus-YY-Bal/4Bus-YY-Bal.DSS
    Distrib/IEEETestCases/123Bus/IEEE123Master.dss
    Distrib/IEEETestCases/123Bus/SolarRamp.DSS
    Distrib/IEEETestCases/13Bus/IEEE13Nodeckt.dss
    Test/IEEE13_LineSpacing.dss
    Test/IEEE13_LineGeometry.dss
    Test/IEEE13_LineAndCableSpacing.dss
    Test/IEEE13_Assets.dss
    Test/CableParameters.dss
    Test/Cable_constants.DSS
    Test/BundleDemo.DSS
    Test/IEEE13_SpacingGeometry.dss
    Test/TextTsCable750MCM.dss
    Test/TestDDRegulator.dss
    Test/XYCurvetest.dss
    Test/PVSystemTestHarm.dss
    Test/TestAuto.dss
    Test/Stevenson.dss
    Test/YgD-Test.dss 
    Test/Master_TestCapInterface.DSS  
    Test/LoadTest.DSS
    Test/IEEELineGeometry.dss
    Test/ODRegTest.dss
    Test/MultiCircuitTest.DSS
    Test/TriplexLineCodeCalc.DSS
    Test/PVSystemTest-Duty.dss
    Test/PVSystemTest.dss 
    Test/REACTORTest.DSS
```

On Windows 10, remember to set the compatibility layer to Windows 7 (set the environment variable `__COMPAT_LAYER=WIN7RTM`), otherwise you may encounter issues with COM due to [ASLR](https://en.wikipedia.org/wiki/Address_space_layout_randomization) on Python 3.6+.

There is no full validation on Linux yet since we cannot run the COM module there. There is an ongoing effort on pickling the data on Windows and loading on Linux for comparison (for the full test suite, it results in 8+GB of data and can be time-consuming).

Roadmap
=======
Besides bug fixes, the main funcionality of this library is mostly done. Notable desirable features that may be implemented are:

- More and better documentation
- Plotting and reports integrated in Python

Questions?
==========
If you have any question, feel free to open a ticket on GitHub, or contact directly me through email (pmeira at ieee.org). Please allow me a few days to respond.


Credits / Acknowlegement
========================
DSS Python is based on EPRI's OpenDSS via the [`dss_capi`](http://github.com/dss-extensions/dss_capi/) project, check its licensing information.

This project is licensed under the (new) BSD, available in the `LICENSE` file. It's the same license OpenDSS uses (`OPENDSS_LICENSE`). OpenDSS itself uses KLUSolve and SuiteSparse, licensed under the GNU LGPL 2.1.

I thank my colleagues at the University of Campinas, Brazil, for providing feedback and helping me test this module.


