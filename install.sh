#!/bin/bash

script="DCSControl.py";
jmri="/Applications/JMRI";
dest="${jmri}/jython";

if [[ -L "${jmri}" && -d "${jmri}" ]]; then
    echo "${jmri} is a symbolic link";
    link=`readlink ${jmri}`;
    echo "Version is ${link}";
fi;

echo "copying ${script} to ${dest}";
cp ${script} ${dest}

