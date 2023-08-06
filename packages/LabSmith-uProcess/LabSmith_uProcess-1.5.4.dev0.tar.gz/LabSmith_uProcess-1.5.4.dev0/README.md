# uProcess
3/3/2019 uProcess Python support V 1.5.4 dev
The python extension uProcess.pyd contains Python (Windows, 3.6, 32-bit) support for controlling LabSmith uDevices.

It contains the following objects:
	CEIB: electrical interface
	C4AM: 4AM 4-channel analog module
	C4PM: 4PM 4-channel power module\
	C4VM: 4VM 4-channel valve driver module
	CSyringe: SPS01 syringe pump module
	CSensor: sensor module
	CLoad: load module
	SRegulate: regulation settings and status
	C4PMChDat: 4PM channel settings and status
	PMCh: enum of 4PM channel indices
	PMMode: enum of 4PM regulation modes
	DigCh: enum of digital channel indices

use help(<object>) for a list of supported methods and variables.
uProcess.help() displays this list of objects
