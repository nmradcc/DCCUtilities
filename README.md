# DCCUtilities v0.0.1

This repository is for maintaining the Saleae High Level Analyzer associated with the DCCAnalayzer Low Level Analyzer for decoding DCC packets.

This is a new repository and is currently under development. Look for noticies of updates on this page.

## Installation

Use the Logic 2 GUI to add the DCCUtilities directory to the user projects. Once you do that, you can add the DCCUtilities HLA to the analyzer along with the DCCAnalyzer LLA to decode packets.

### MacOS

If you're running this on a Mac, you can run the 'install.sh' script to copy the DCSControl.py JMRI Jython script into the /Applications/JMRI/jython directory

To add the DCSControl helper script to your Panel Pro menu as a button, do the following:

1) Open Panel Pro Preferences
2) Click on Start Up
3) Click Add->Add script to button
4) Enter the name, "DCS Testing"
5) Enter the script, browse to DCSControl.py which should now be in your jython path if you ran the install script
6) Click Ok
7) Click Save

Panel Pro will restart and you will now see the "DCS Testing" button.

## Getting Started

To use the JMRI DCSControl along side the DCCUtilities HLA,

1) Open Panel Pro and configure it for the command station you wish to test. You may need to add the DCSControl script to each configuration.
2) Open Logic 2 and make sure the DCCAnalyzer and DCCUtilities logic analzyers are loaded and configured properly
3) Click the "DCS Control" button in Panel Pro and select the test you want to run from the pull down menu
4) At each phase of the test, it will stop and then you can go over to Logic 2 and click the Start button to capture the DCS output



