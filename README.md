# PT-Generator
Generates standard CFN PT Files ([Spec Here](http://www.cfnnet.com/OpManual/appendix/ptlayout112.html)) from TSC sales file logs.

## Requirements
1. Python 3.6 and up. No extra packages needed.
2. A windows machine. OS and file operations are exclusively written for windows.
___

## Configuration
Configuration of the program can be done through the config.yaml file. 
#### Value Explanation
1. **file_name:** list that includes values for the file name output 
   * **custom:** Allows for a custom string at the beginning of the file name, like a company name.
    * **custom_beginning** *bool*, Sets whether or not the custom beginning is on or not.
