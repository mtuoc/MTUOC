This directory contains the required tools compiled for macOS (compiled in a macOS Monterey version 12.6.2). If you use macoOS copy these file in the /MTUOC directory replacing the existing files compiled for Linux). Then give the files execution permisions:

```
chmod +x lmplz
chmod +x build_binary
chmod +x fast_align
chmod +x atools
```

Don't forget to give also execution permisions to eflomal-align.py

```
chmod +x eflomal-align.py
```

If you experience problems with these files, you may want to compile the files yourself.

**Installing mac ports**

It's advisable to install mac ports. Follow the instructions in [https://www.macports.org/install.php](https://www.macports.org/install.php). The process is simple and you need to follow the steps in **Quick start**.

**Install cmake**

```
sudo port install cmake
```

**Install boost**

```
sudo port install boost
```

**Compiling and installing kenLM***

```
git clone https://github.com/kpu/kenlm.git
cd kenlm
mkdir -p build
cd build
cmake ..
make -j 4
```

To install the python module do:

```
pip3 install https://github.com/kpu/kenlm/archive/master.zip
```

**Compiling fast_align***

```
git clone https://github.com/clab/fast_align.git
cd fast align
mkdir build
cd build
cmake ..
make
```

**Compiling and installing sentencepiece***

```
git clone https://github.com/google/sentencepiece.git
cd sentencepiece
mkdir build
cd build
cmake ..
make -j $(nproc)
sudo make install
```

And the python module:

```
sudo pip3 install sentencepiece
```

**Installing coreutils**

To have the **shuf** command available we should install **coreutils**, but it will install the **gsuf** command (it is the same as **shuf** but starting with g). We will copy **gshuf** into **shuf** in order the MTUOC scripts to work properly:

```
sudo port install coreutils
sudo cp /opt/local/bin/gshuf /opt/local/bin/shuf
```

 
