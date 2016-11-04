<pre>
  _   _       _   _
 | \ | |     | | | |
 |  \| | __ _| |_| |__   __ _ _ __
 | . ` |/ _` | __| '_ \ / _` | '_ \
 | |\  | (_| | |_| | | | (_| | | | |
 |_| \_|\__,_|\__|_| |_|\__,_|_| |_|

Nathan Emulator - Mobile Security Lab 2016
</pre>

# Introduction
Nathan is a 5.1.1 SDK 22 AOSP Android emulator customized to perform mobile security assessment.  

Supported architectures:
* x86
* arm (soon)

The emulator is equipped with the [Xposed Framework](http://forum.xda-developers.com/xposed) and the following pre-installed modules:
* [SSLUnpinning] (https://github.com/ac-pm/SSLUnpinning_Xposed), to bypass SSL Certificate pinning.
* [Inspeckage] (https://github.com/ac-pm/Inspeckage), to perform the dynamic analysis of an application.
* [RootCloak] (https://github.com/devadvance/rootcloak), to bypass root detection.  

The following tools are already installed:
* [#SuperSU] (http://www.supersu.com/): Superuser access management tool
* [Drozer] (https://labs.mwrinfosecurity.com/tools/drozer): Comprehensive security and attack framework for Android 
 
# Features
* Only python 2.7.x required
* Hooking ready with Xposed
* Pre-installed tools for application analysis
* Fully customizable
* Snapshot and restore of user data

# Installation
Download Nathan core scripts from git:
```
$ git clone https://github.com/mseclab/nathan/
$ cd nathan
```
Init Nathan for the first time (for downloading firmware files)
``` 
$ ./nathan.py init 
``` 
If a proxy is required to download files, the parameter **-dp** is available :
``` 
$ ./nathan.py init -dp 127.0.0.1:3128
``` 
The **init** command downloads all the files required to run use Nathan Emulator.
  
  
# Usage
To start Nathan:
 ``` 
$ ./nathan.py start
 ```

To redirect the traffic through a proxy (es. http://127.0.0.1:3128),  the parameter **-p** can be used:
 ``` 
$ ./nathan.py start -p http://127.0.0.1:3128
 ```

To create a snapshot of current user image data with a label (*current* in this case):
 ``` 
$ ./nathan.py snapshot -sl current 
 ```

To restore the emulator to the snapshot with label *current*:
 ``` 
$ ./nathan.py restore --rl current
 ```

To get a list of available snapshots to restore:
 ``` 
$ ./nathan.py restore --ll  
 ```

Every time the emulator is started,  a temporary copy of system image is created and each changes made to system data is lost when the emulator is powered off.  
To keep permanent the changes, the command **freeze** is available:
 ``` 
$ ./nathan.py freeze  
 ```

To push files from a folder to a running Nathan emulator, the command **push** is available:
 ``` 
$ ./nathan.py push -f folder   
 ```
  
The complete list of command is:
```
usage: nathan.py [-h] [-v] [-a ARCH]
                 {init,start,snapshot,restore,freeze,push} ...

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show emulator/kernel logs
  -a ARCH, --arch ARCH  Select architecture (arm/x86) - Default = x86

Command to run:
  {init,start,snapshot,restore,freeze,push}
    init                Download and init Nathan emulator
    start               Start Nathan emulator
    snapshot            Create userdata image snapshot
    restore             Restore userdata image snapshot
    freeze              Freeze temporary system image
    push                Push files to Nathan emulator 
```
The parameter **-h** for each command shows specific options.

# Nathan Customization
The emulator can be easily customized by pushing files in system partition and freezing it.  
The example script ``` ./install-gapps.sh```  shows how to customize the emulator with Google Apps.

# Unknown issue
Please run ``` ./nathan.py -v start```  or look at ***nathan.log*** to show the log messages.

# Know Issue
## libstdc++.so on Kali Linux Rolling 2016.1 
```
libGL error: unable to load driver: i965_dri.so
libGL error: driver pointer missing
libGL error: failed to load driver: i965
libGL error: unable to load driver: i965_dri.so
libGL error: driver pointer missing
libGL error: failed to load driver: i965
libGL error: unable to load driver: swrast_dri.so
libGL error: failed to load driver: swrast
```
The issue is related to libstdc++.so.6  in  **PATH_NATHAN/sdk/tools/lib64/** and can be resolved with the following command:

```{r, engine='bash', count_lines}
cd ~/nathan/sdk/tools/lib64/libstdc++
mv libstdc++.so.6 libstdc++.so.6_OLD
ln -sf /usr/lib/x86_64-linux-gnu/libstdc++.so.6 libstdc++.so.6 
```
 
