# PT-Generator

Generates back office accounting transaction files from TSC VB6 and .NET fuel controller sales files.  
Supports the following back office formats: 
* CFN 1.1.2 Fixed length PT files ([Spec Here](http://www.cfnnet.com/OpManual/appendix/ptlayout112.html))
* CFN CSV PT files
* Gasboy controller format
* Merchant Ag
* VDP
* AGTRAX
* JC Doyle
* FuelMaster

## Requirements
1. Python 3.6 and up.
2. pyYaml
3. pySFTP
4. A windows machine. OS and file operations are exclusively written for windows.
