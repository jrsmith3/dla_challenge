I don't really know how I'm going to structure these notes, but I need to capture them during this process.


Hardware setup
==============
The first order of business is to fire this board up and get it on the network. I expect to do all of the coding on this thing over the network via ssh.

It doesn't look like this board has wifi capabilities, so I will have to eventually plug it into the router if I want to access it over the network.

To get started, I should probably just plug in a monitor, keyboard, and mouse and see what happens.

There's no VGA or DVI connector on this thing, just an HDMI. I don't have an HDMI cable handy, so I will probably actually have to put this thing on the network and ssh into it (assuming sshd is on by default). Otherwise I'm going to have to pick up an HDMI cable.

I'm checking out the [TK1 site](http://www.nvidia.com/object/jetson-tk1-embedded-dev-kit.html) to see if this thing ships with sshd started.

There are [setup instructions on the TK1 wiki](http://elinux.org/Jetson_TK1#Basic_setup_steps_to_access_the_board_and_access_internet) that I'm following with a few modifications.

Here's what I'm going to do. The instructions say [to execute a command so that `apt` doesn't clobber `libglx.so`](http://elinux.org/Jetson_TK1#An_important_step_before_connecting_the_Jetson_to_Internet) **before** connecting the board to the internet. I will just unplug my router from the cable modem before plugging the TK1 into the router and powering it on.

I disconnected the router from the cable modem, plugged the TK1 into the router, then plugged the TK1 into power. The fan spun up and lights came on. According to the router config site, the TK1 has the following ID:

hostname: tegra-ubuntu
IP address: 192.168.1.108

I can ping the system:

```
$ ping tegra-ubuntu.local
PING tegra-ubuntu.local (192.168.11.108): 56 data bytes
64 bytes from 192.168.11.108: icmp_seq=0 ttl=64 time=4.872 ms
64 bytes from 192.168.11.108: icmp_seq=1 ttl=64 time=4.437 ms
^C
--- tegra-ubuntu.local ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 4.437/4.655/4.872/0.217 ms
```

Can I ssh into this thing? Yes.

```
$ ssh -l ubuntu tegra-ubuntu
ubuntu@tegra-ubuntu's password: 
Welcome to Ubuntu 14.04 LTS (GNU/Linux 3.10.24-g6a2d13a armv7l)

 * Documentation:  https://help.ubuntu.com/

0 packages can be updated.
0 updates are security updates.

Last login: Tue Feb  1 00:00:17 2000
```

Now that I'm in, I need to do a few sysadmin things.

* [x] Change the `ubuntu` user password.
* [x] Prevent `apt` from clobbering `libglx.so`.
* [x] Create a user `jrsmith3`.
* [x] Give user `jrsmith3` sudo access.
* [x] Allow ssh logins via ssh keys.
* [x] Add my ssh key to user `jrsmith3`.
* [x] [Update apt and packages](http://elinux.org/Jetson_TK1#Recommended_first_steps_now_that_your_board_has_internet_access).


Change `ubuntu` user password
-----------------------------
I am using the [passwordstore utility](http://www.passwordstore.org/) to generate a difficult-to-guess password for this machine.

password: U33HzPE-(.vIQJ\:3kj_


Prevent `apt` from clobbering `libglx.so`
-----------------------------------------
I just [followed the instructions](http://elinux.org/Jetson_TK1#An_important_step_before_connecting_the_Jetson_to_Internet). I also plugged the router back into the cable modem and I'm back on the internet.


Create a user `jrsmith3`
------------------------
Pretty simple.

```
$ sudo adduser jrsmith3
Adding user `jrsmith3' ...
Adding new group `jrsmith3' (1001) ...
Adding new user `jrsmith3' (1001) with group `jrsmith3' ...
Creating home directory `/home/jrsmith3' ...
Copying files from `/etc/skel' ...
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
Changing the user information for jrsmith3
Enter the new value, or press ENTER for the default
    Full Name []: Joshua Ryan Smith
    Room Number []: 
    Work Phone []: 
    Home Phone []: 
    Other []: joshua.r.smith@gmail.com
Is the information correct? [Y/n] y
Adding new user `jrsmith3' to extra groups ...
Adding user `jrsmith3' to group `video' ...
```


Give user `jrsmith3` sudo access
--------------------------------
Also pretty simple.

```
ubuntu@tegra-ubuntu:~/NVIDIA-INSTALLER$ sudo usermod -a -G sudo jrsmith3
```

At this point, I've logged out of the TK1 as user `ubuntu` and logged back in as `jrsmith3`.


Allow ssh logins via ssh keys
-----------------------------
Maybe this feature is already set up. I will try to copy my public ssh key from gamma over to the TX1. First, I had to create an `.ssh` directory on the TX1.

```
jrsmith3@tegra-ubuntu:~$ mkdir .ssh
```

Then I use scp to copy my ssh key to the TX1.

```
gamma:$ scp -rCp ~/.ssh/id_rsa.pub jrsmith3@tegra-ubuntu:.ssh
jrsmith3@tegra-ubuntu's password: 
id_rsa.pub                                    100%  396     0.4KB/s   00:00
```

The ssh key is on the TX1, but logging out and logging back in I still had to enter my password.

At this point I'm going to have to modify files in `/etc` and so I should probably set up `etckeeper`. To do that, I should also probably update the packages.


Update apt and packages
-----------------------
Simple.

```
sudo apt-add-repository universe
sudo apt-get update
```

I will also install `bash-completion` and `command-not-found` as suggested in the instructions.


Install `etckeeper`, `git`, and other utils
-------------------------------------------
I need to modify some things in `~etc`, so I will [install `etckeeper`](https://help.ubuntu.com/lts/serverguide/etckeeper.html) as well.

```
sudo apt-get install etckeeper
```

I'm pretty sure the above pulled in `bzr` and set up `/etc` as a `bzr` repo. [I want git instead](http://evilrouters.net/2011/02/18/using-etckeeper-with-git-on-ubuntu/).

```
sudo apt-get install -y git-core
```

Configure git

```
$ git config --global user.name "Joshua Ryan Smith"
$ git config --global user.email joshua.r.smith@gmail.com
```

After the above commands, I modified `/etc/etckeeper/etckeeper.conf` to use git. I had to unintialize `etckeeper` so that it would remove the bzr repo and use git instead.

```
$ sudo etckeeper uninit
[sudo] password for jrsmith3: 
** Warning: This will DESTROY all recorded history for /etc,
** including the bzr repository.

Are you sure you want to do this? [yN] y
Proceeding..
```

Next, I initialize `etckeeper`.

```
$ sudo etckeeper init
Initialized empty Git repository in /etc/.git/
$ sudo etckeeper commit "Initial commit."
```

Now everything looks right.


Allow ssh logins via ssh keys, revisited
----------------------------------------
[Derp](http://askubuntu.com/questions/54670/passwordless-ssh-not-working). I copied `id_rsa.pub` to the TK1, but I didn't add it to the `~/.ssh/authorized_keys` file.


Upgrade packages
----------------
Simple.

```
sudo apt-get upgrade
```


Project
=======
At this point I think I've done enough systems administration and devops. I need to select a project that won't take more than about 10 hours or so.

The obvious project is handwriting recognition. Frankly, I should start with that kind of project because there are enough examples documented on the internet and in some of the books I have.

The downside is that I don't have a good sense of which projects are easy and which are difficult.

Here are a few ideas:

* Follow the handwriting example from [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/).
* Read the rest of NNADL.
* How hard is it to create a cat identifier?

At this point I think I should create a handwriting recognition system because its sufficiently documented online. It may turn out that training this thing takes 20-100h and so I should take the path of least resistance.


Ideas
-----
* Predict temperature using photos along with weather data.
* Use a physics simulator to teach the neural net to catch a ball or something similar: http://spectrum.ieee.org/view-from-the-valley/transportation/self-driving/autonomous-vehicles-learn-by-playing-video-games


Toy Project from NNADL
======================
After some reflection and re-reading the letter DLA sent me, I don't think there should be much of a problem just implemeting the program from NNADL. There's a chance this approach won't be acceptable to DLA. Even in that event, implementing NNADL's example is a good exercise.

Here's the plan:

* [ ] Email DLA and ask if implementing the example from NNADL is acceptable.
* [ ] Implement the example from NNADL.

I'm going to implement this project in the `jobapp-2015-12_deep_learning_analytics` repo as a subdirectory so that I can split it out as a subtree later.

After re-reading NNADL, I can pretty much just add [the repo](https://github.com/mnielsen/neural-networks-and-deep-learning) as a submodule and execute all of the code according to the example in Ch. 1.


Results
-------
I've downloaded the code and I'm now executing it on gamma. I am getting results kind of slowly. It finished in around 5 minutes I think.

I think the point of this exercise is that its nearly trivial to run on gamma. Can I get it to run on the TK1? To do so, I should attempt to install Continuum's Anaconda.

Apparently there's a [linux installer](https://www.continuum.io/downloads#_unix).

It also looks like [someone recently asked about installing Anaconda for the TK1](https://devtalk.nvidia.com/default/topic/901150/jetson-tx1/python-anaconda-on-tx1/).

At this point I've downloaded the linux installer script on the TK1. I'm pretty sure there's no cost to installing this thing because everything will go into `/home/jrsmith3`. If things don't work, I think I can just delete the `~/anaconda` directory and perhaps `.bashrc` or something.

To mitigate any problems, I copied `.bashrc` to `bashrc.old` and `.profile` to `profile.old`. I will now attempt to install anaconda on the TK1.

```
$ bash Anaconda2-2.4.1-Linux-x86_64.sh
WARNING:
    Your operating system appears not to be 64-bit, but you are trying to
    install a 64-bit version of Anaconda2.
    Are sure you want to continue the installation? [yes|no]
[no] >>> 
Aborting installation
```

So am I running a 64bit OS?

I'm pretty sure this board is an [ARM Cortex-A15](https://en.wikipedia.org/wiki/ARM_Cortex-A15) which is a 32-bit processor. I think that the TK1 is this ARM Cortex-A15 because that's what the spec sheet included with the board says.


32-bit anaconda
---------------
I will try again with the [most recent release of the 32-bit version of linux anaconda](https://repo.continuum.io/archive/Anaconda2-2.4.1-Linux-x86.sh). There doesn't appear to be an ARM version.

Package downloaded; now to install:

```
$ bash Anaconda2-2.4.1-Linux-x86.sh
```

I had to review and agree to a license. It now looks like things are uncompressing.

It looks like I get an error:

```
Anaconda2-2.4.1-Linux-x86.sh: line 445: /home/jrsmith3/anaconda2/pkgs/python-2.7.11-0/bin/python: cannot execute binary file: Exec format error
ERROR:
cannot execute native linux-32 binary, output from 'uname -a' is:
Linux tegra-ubuntu 3.10.24-g6a2d13a #1 SMP PREEMPT Fri Apr 18 15:56:45 PDT 2014 armv7l armv7l armv7l GNU/Linux
```

I suspect because this anaconda is built for x86 architecture instead of arm.

It looks like Continuum has an [anaconda for armv7l](https://www.continuum.io/content/conda-support-raspberry-pi-2-and-power8-le) which is also what the TK1 is:

```
$ uname -m
armv7l
```

I will need to install miniconda, but `numpy`, `scipy`, and a few other packages have been built. I'm using the [latest armv7l](http://repo.continuum.io/miniconda/Miniconda-latest-Linux-armv7l.sh). 

The md5sum matches, next to install:

```
$ bash Miniconda-latest-Linux-armv7l.sh
```

Again with the license. Miniconda will be installed at `/home/jrsmith3/miniconda`. Some unpacking. I'd expect less than anaconda. Already done. Next message:

```
installation finished.
Do you wish the installer to prepend the Miniconda install location
to PATH in your /home/jrsmith3/.bashrc ? [yes|no]
[no] >>> yes

Prepending PATH=/home/jrsmith3/miniconda/bin to PATH in /home/jrsmith3/.bashrc
A backup will be made to: /home/jrsmith3/.bashrc-miniconda.bak


For this change to become active, you have to open a new terminal.

Thank you for installing Miniconda!
```

So I think its done. The installer even backed up my old `.bashrc` file. I logged out and rebooted because ubuntu said I should.

Now that I have (mini)conda installed, I will attempt the NNADL example on the TK1.


Toy project from NNADL on the TK1
=================================
Clone the repo
--------------

```
$ git clone https://github.com/mnielsen/neural-networks-and-deep-learning.git
```

I had to clone over HTTPS instead of SSH because I don't have a private SSH key on this machine associated with github.


Set up conda virtual env
------------------------
In the root of the cloned repo:

```
$ conda create -yp ./env python
```

Next I will install some packages into it.

```
$ conda install numpy ipython scipy -p ./env/
```

Next I will activate the environment and see what's been installed.

```
$ conda list
# packages in environment at /home/jrsmith3/miniconda:
#
conda                     3.16.0                   py27_0  
conda-env                 2.4.2                    py27_0  
openssl                   1.0.1k                        1  
pycosat                   0.6.1                    py27_0  
pycrypto                  2.6.1                    py27_0  
python                    2.7.10                        0  
pyyaml                    3.11                     py27_1  
requests                  2.7.0                    py27_0  
sqlite                    3.8.4.1                       1  
yaml                      0.1.6                         0  
zlib                      1.2.8                         0

$ source activate ./env
discarding /home/jrsmith3/miniconda/bin from PATH
prepending /home/jrsmith3/Documents/neural-networks-and-deep-learning/env/bin to PATH

$ conda list
# packages in environment at /home/jrsmith3/Documents/neural-networks-and-deep-learning/env:
#
decorator                 4.0.2                    py27_0  
ipython                   4.0.0                    py27_0  
ipython-genutils          0.1.0                     <pip>
ipython_genutils          0.1.0                    py27_0  
libgfortran               1.0                           0  
numpy                     1.9.2                    py27_1  
openblas                  0.2.14                        1  
openssl                   1.0.2d                        0  
path.py                   7.6.1                    py27_0  
pexpect                   3.3                      py27_0  
pickleshare               0.5                      py27_0  
pip                       7.1.2                    py27_0  
python                    2.7.10                        2  
readline                  6.2                           2  
scipy                     0.16.0               np19py27_1  
setuptools                18.4                     py27_0  
simplegeneric             0.8.1                    py27_0  
sqlite                    3.8.4.1                       1  
traitlets                 4.0.0                    py27_0  
wheel                     0.26.0                   py27_1  
zlib                      1.2.8                         0
```

So it looks like I have the appropriate packages.


Running the example
-------------------
I've executed the commands like I did above and now I'm calling the `net.SGD` method. This TK1 computer is significantly slower than gamma. I'm sure I could speed things along if I could use the system's GPU.


Next actions
============
I've now demonstrated that I can get this problem running on both gamma and the TK1. I'm pretty sure I can use the code from NNADL but I need to ask. In fact, I need to ask a few questions:

* [ ] Can I use the code from NNADL?
* [ ] Do they want me to leverage the GPU of the TK1 board?

The real issue is: I need to work through an example. I now have the environment and I've worked through a canned example from NNADL.


Example problem: predicting result of Langmuir model
====================================================
Yesterday I decided to try to train a NN to predict the maximum motive for the Langmuir model. In order to do this calculation, I have to:

* [ ] Install `tec` in a conda environment.
* [ ] Write some code to generate the training data.
* [ ] Train and test the NN.

I don't really know how this is going to work out, so I need to get through these steps as quickly as possible.


Installing `tec` in conda env
-----------------------------
I've installed `tec` in the past, but I don't remember how to do it.

First, does `tec` pass its tests?

```
gamma:tec jrsmith3$ source activate ./env/
discarding /Users/jrsmith3/anaconda/bin from PATH
prepending /Users/jrsmith3/Documents/work/tec/env/bin to PATH
(/Users/jrsmith3/Documents/work/tec/env)gamma:tec jrsmith3$ nosetests
.....................................................................................................................
----------------------------------------------------------------------
Ran 117 tests in 11.345s

OK
```

Looks like it.

Next, can I install this package in a conda environment? The dependencies are:

* [x] python
* [x] numpy
* [x] scipy >=0.15.0
* [ ] matplotlib
* [x] astropy
* [ ] physicalproperty

Check marks in the list above indicate that the package can be installed on the TK1.

I should be able to easily modify the `tec` codebase so that it doesn't depend on matplotlib. I can probably also bring `physicalproperty` in as well.

Before I get too far along building this package for the TK1, I should just attempt to install `tec` in a conda env. I'm pretty sure I'm going to use the `conda build` and `conda install` commands.

Instead of building `tec`, I'm going to attempt to build/install `ibei` because it has fewer dependencies and should be easier. It turns out that `ibei` still depends on `physicalproperty`.

The best approach here is to build `physicalproperty` and upload it to anaconda.org with the `noarch` flag (or whatever its called).

To test the build, I've upgraded `conda` and `conda-build` to their most recent versions. I'm also on branch i11 of the `physicalproperty` repo (commit fd90fb0b3c80e9b98551e2f1a7cc88981bc368c6). I should be able to build this thing locally. According to `README.rst` in the repo I simply:

```
conda build path/to/physicalproperty/conda.recipe
```

Before installing, I should search for this package in the locally build packages.

That command seemed to work. It also created a directory `/Users/jrsmith3/anaconda/conda-bld/noarch`. So maybe the update fixed the problems I was having previously.

Next, I installed `anaconda-client` and executed the following command to upload to anaconda.org:

```
$ anaconda upload /Users/jrsmith3/anaconda/conda-bld/noarch/physicalproperty-1.0.1-py_0.tar.bz2
Using Anaconda Cloud api site https://api.anaconda.org
The action you are performing requires authentication, please sign in:
Using Anaconda Cloud api site https://api.anaconda.org
Username: jrsmith3
jrsmith3's Password: 
login successful
Using Anaconda Cloud api site https://api.anaconda.org
detecting package type ...
conda
extracting package attributes for upload ...
done

Uploading file jrsmith3/physicalproperty/1.0.1/noarch/physicalproperty-1.0.1-py_0.tar.bz2 ... 
 uploaded 9 of 9Kb: 100.00% ETA: 0.0 minutes


Upload(s) Complete

Package located at:
https://anaconda.org/jrsmith3/physicalproperty
```

The package now appears on anaconda.org. 


Can I install this thing in an environment on the TK1?
------------------------------------------------------
First, I ssh into the TK1. Then I create a dummy environment.

```
$mkdir tmp/jnk
$cd jnk

$ conda create -yp ./env python 
Fetching package metadata: ....
Solving package specifications: .
Package plan for installation in environment /home/jrsmith3/tmp/jnk/env:

The following NEW packages will be INSTALLED:

    openssl:    1.0.2d-0     
    pip:        7.1.2-py27_0 
    python:     2.7.10-2     
    readline:   6.2-2        
    setuptools: 18.4-py27_0  
    sqlite:     3.8.4.1-1    
    wheel:      0.26.0-py27_1
    zlib:       1.2.8-0      

Linking packages ...
[      COMPLETE      ]|###################################################| 100%
#
# To activate this environment, use:
# $ source activate /home/jrsmith3/tmp/jnk/env
#
# To deactivate this environment, use:
# $ source deactivate
#

$ source activate ./env
```

The activation step was probably unnecessary. Next, I need to attempt to install `physicalproperty` from anaconda.org. According to `physicalproperty`' s `README.rst`:

```
$ conda install -c jrsmith3 physicalproperty
Fetching package metadata: ......
Solving package specifications: .
Package plan for installation in environment /home/jrsmith3/tmp/jnk/env:

The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    astropy-1.0.4              |       np19py27_0         7.0 MB
    physicalproperty-1.0.1     |             py_0           7 KB
    ------------------------------------------------------------
                                           Total:         7.0 MB

The following NEW packages will be INSTALLED:

    astropy:          1.0.4-np19py27_0
    libgfortran:      1.0-0           
    numpy:            1.9.2-py27_1    
    openblas:         0.2.14-1        
    physicalproperty: 1.0.1-py_0      

Proceed ([y]/n)? 

Fetching packages ...
astropy-1.0.4- 100% |################################| Time: 0:00:02   3.13 MB/s
physicalproper 100% |################################| Time: 0:00:00   1.07 MB/s
Extracting packages ...
[      COMPLETE      ]|###################################################| 100%
Linking packages ...
[      COMPLETE      ]|###################################################| 100%
```

Sweet. It looks like it worked!


Closing some issues on `physicalproperty`
-----------------------------------------
Before moving on, I will clean up and close some issues with `physicalproperty`. As a matter of fact, I'm having some trouble with the build string and the noarch flag.

Here's how I'm going to unwind this problem. I need to release version 1.0.2 of `physicalproperty`. I think I should push the `master` branch back to the `1.0.1` commit.


`physicalproperty` 1.0.2 released
---------------------------------
At this point, I've released [`physicalproperty` version 1.0.2](https://github.com/jrsmith3/physicalproperty/releases/tag/1.0.2) and [posted the noarch version on anaconda.org](https://anaconda.org/jrsmith3/physicalproperty/files?version=1.0.2). I should be able to install this version on the TK1.

```
# Executed on the TK1 after creating a dummy environment 
# similar to the example above:
$ $ conda install -c jrsmith3 physicalproperty -p ./env 
Fetching package metadata: ......
Solving package specifications: .
Package plan for installation in environment /home/jrsmith3/tmp/jnk/env:

The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    physicalproperty-1.0.2     |             py_0           7 KB

The following NEW packages will be INSTALLED:

    astropy:          1.0.4-np19py27_0
    libgfortran:      1.0-0           
    numpy:            1.9.2-py27_1    
    openblas:         0.2.14-1        
    physicalproperty: 1.0.2-py_0      

Proceed ([y]/n)? y

Fetching packages ...
physicalproper 100% |################################| Time: 0:00:00 342.70 kB/s
Extracting packages ...
[      COMPLETE      ]|###################################################| 100%
Linking packages ...
[      COMPLETE      ]|###################################################| 100%
```

It works!


`ibei`
======
I will update this package as well to be installable from anaconda.org since `tec` depends on it.

I modified a few things in the repo and the package built properly. However, I'm concerned that the install worked because there's a local copy of `physicalproperty`.

I executed `conda clean -t` to remove the tarballs from the local cache. Lets see if I can still `conda build` this thing.

It seems to work. I will attempt to upload to anaconda.org to the `test` channel.

```
$ anaconda upload -c test /Users/jrsmith3/anaconda/conda-bld/noarch/ibei-1.0.6-py_0.tar.bz2
Using Anaconda Cloud api site https://api.anaconda.org
detecting package type ...
conda
extracting package attributes for upload ...
done

Uploading file jrsmith3/ibei/1.0.6/noarch/ibei-1.0.6-py_0.tar.bz2 ... 
 uploaded 14 of 14Kb: 100.00% ETA: 0.0 minutes


Upload(s) Complete

Package located at:
https://anaconda.org/jrsmith3/ibei
```

Seems to work. Now I will see if I can install this package on the TK1.

Before attempting to install `ibei`, I want to see if I can find it since I uploaded it to my "test" channel.

```
$ conda search -c jrsmith3/channel/test ibei
Fetching package metadata: ......
ibei                         1.0.6                      py_0  jrsmith3
```

It looks like its up there.        

I installed the barebones conda environment again. Next, attempt to install `ibei`.

```
$ conda install -c jrsmith3/channel/test ibei -p ./env 
Fetching package metadata: ......
Solving package specifications: .
Package plan for installation in environment /home/jrsmith3/tmp/jnk/env:

The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    fastcache-1.0.2            |           py27_0          39 KB
    sympy-0.7.6                |           py27_0         6.2 MB
    ibei-1.0.6                 |             py_0          12 KB
    ------------------------------------------------------------
                                           Total:         6.2 MB

The following NEW packages will be INSTALLED:

    astropy:          1.0.4-np19py27_0
    fastcache:        1.0.2-py27_0    
    ibei:             1.0.6-py_0      
    libgfortran:      1.0-0           
    numpy:            1.9.2-py27_1    
    openblas:         0.2.14-1        
    physicalproperty: 1.0.1-py_0      
    sympy:            0.7.6-py27_0    

Proceed ([y]/n)? 

Fetching packages ...
fastcache-1.0. 100% |################################| Time: 0:00:00 947.01 kB/s
sympy-0.7.6-py 100% |################################| Time: 0:00:01   3.32 MB/s
ibei-1.0.6-py_ 100% |################################| Time: 0:00:00 703.21 kB/s
Extracting packages ...
[      COMPLETE      ]|###################################################| 100%
Linking packages ...
[      COMPLETE      ]|###################################################| 100%
```

So it looks like it managed to grab everything, including `physicalproperty`, but it got the wrong version of physicalproperty.

I'm rebuilding `ibei` to see if that fixes the problem. It doesn't. Somehow I'm still installing the 1.0.1 version of physicalproperty.


`tec`
=====
Now I think I can install the `tec` package. I will probably have to modify it a little bit.

At this point I think I need to rip out the matplotlib functionality. Its not strictly necessary and I won't be able to install matplotlib on the TK1 since its not in the arm conda distribution.

In fact, I don't think I need to rip out the matplotlib functionality, I just need to make it optional.

I'm pretty sure I've modified this thing appropriately. Nope. I'm getting some errors with the `conda build` command.

I think I fixed the bug. Now the tests pass during `conda build`. I will upload this thing to anaconda.org in the "test" channel and try to install it on the TK1.

```
# Upload to anaconda.org
$ anaconda upload -c test /Users/jrsmith3/anaconda/conda-bld/noarch/tec-1.0.0.dev2-py_0.tar.bz2

Using Anaconda Cloud api site https://api.anaconda.org
detecting package type ...
conda
extracting package attributes for upload ...
done

Uploading file jrsmith3/tec/1.0.0.dev2/noarch/tec-1.0.0.dev2-py_0.tar.bz2 ... 
 uploaded 24 of 24Kb: 100.00% ETA: 0.0 minutes


Upload(s) Complete

Package located at:
https://anaconda.org/jrsmith3/tec
```

Looks good. Now to install on the TK1.

```
$ conda install -y -c jrsmith3/channel/test tec -p ./env 
Fetching package metadata: ......
Solving package specifications: 
Error: Could not find some dependencies for tec: ibei

You can search for this package on anaconda.org with

    anaconda search -t conda ibei

You may need to install the anaconda-client command line client with

    conda install anaconda-client
```

For some reason it can't find `ibei`. I can probably manually install `ibei` first and then pick up `tec`. The `ibei` install worked. The `tec` install still doesn't work. It gives the same error as above.

I don't understand why `ibei` will install even though it depends on `physicalproperty`, but `tec` won't install.

I uploaded the package to my "main" channel instead of the "test" channel on anaconda.org, and now it works on the TK1 somehow.


Generating the test data
========================
At this point, I can generate the test data I need. I don't think I really have the energy to do much of anything else on this project, but I'm going to try to calculate at least one output for a set of inputs and build a data structure out of the result.

I just found out that there's no models in this revision of the `tec` package. In order to do the project I've been trying to do, I will need to hack on the `tec` class to get the Langmuir model working again.


Time tracking
=============
2015-12-18: 1.5h
2015-12-19: 2h
2015-12-21: 2h
2015-12-22: 2h
2015-12-23: 5h

Running total: 12.5h
