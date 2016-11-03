#! /bin/sh
RUN_INFO=".run_info"
echo "Google Apps installer for Nathan"
# Check if nathan is running
if ! [ -e "nathan_x86/$RUN_INFO" ] || ! [ -e "nathan_arm/$RUN_INFO" ]
then
    echo "Please start Nathan emulator."
    exit
fi
# Check for adb
if  which "adb" >/dev/null || ! [ -e "sdk/platform-tools/adb" ]
then
    echo "adb command is missing."
    exit
fi
mkdir gapps
echo "Downloading gapps..."
wget -qO- https://github.com/cgapps/vendor_google/raw/builds/x86/gapps-5.1-x86-2015-07-17-15-08.zip | tar -xvf- --exclude vendor --exclude addon.d --exclude META-INF -C gapps
echo "Pushing files to Nathan..."
./nathan.py push -f gapps/common/ -p system/
./nathan.py push -f gapps/arch/ -p system/
echo "Freezing system image..."
./nathan.py freeze -y
echo "Removing files"
rm -rf gapps
echo "Restarting Nathan..."
adb shell killall -9 zygote
echo "Gapps installation complete!"