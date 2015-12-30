Predicting behavior of a complicated physical system
====================================================

Neural networks (NNs) have been employed to great effect in recent years as a result of improvements in deep learning algorithms.
NNs are typically employed in computer vision applications such as image classification (i.e. finding pictures of dogs or cats) and handwriting recognition \cite{}.

NNs can be constructed in a number of configurations, but before a NN can be deployed, it must be "trained".
Training involves adjusting the weights of the neurons comprising the net such that the net properly categorizes a set of training data.

Although NNs seem to mostly be used for image processing applications, there are some reports of applying NNs to problems in physics.
For example, Grzeszczuk et.al. \cite{} used a NN to generate physically plausible computer animations.
After training, their NN was able to produce physically realistic motion faster than the approach of solving the system's equations of motion.

The upshot of modeling physical systems with a NN is as follows.
Consider the task fo developing control software for an autonomous vehicle (e.g. drone aircraft, driverless car, etc.) or for a robot.
At some point during development a prototype machine must be constructed and deployed in a test envorinment. 
For example, consider a driverless car whos task is to navigate a street with pedestrian crossing.
If the task is to navigate the street without hitting pedestrians, then the two outcomes are clear: hit pedestrian or didn't hit pedestrian.
Thus, a navigation strategy can be input into the NN and tested.

Another important aspect of this problem is that its easily simulated.
Instead of building a prototype vehicle and organizing a training course, the vehicle and course can be simulated in software.
This approach should speed training since the computer can parallelize training simulations.
Additionally, this approach is presumably less expensive \cite{IEEE Spectrum}.

Given the limited amount of time to work on this project, I chose a much simpler problem to solve which is based on a physical simulation.
Specifically the task is to determine the value of the maximum motive for a thermoelectron engine given the operating parameters of the device.
This problem is good because it is not trivial but it is not as complicated as the examples listed above.
Moreover, I've written code to perform this simulation and so it is suited for the problem of generating training data for the NN.


Background on thermoelectron engine
===================================
A thermoelectron engine, also known as a thermoelectron energy converter or TEC, is a thermodynamic heat engine consisting of two electrodes enclosed in an evacuated container.
The electrodes are separated by a distance named the interelectrode spacing.
The emitter electrode is held at a higher temperature than the collector electrode, and electrons are emitted via the phenomenon of thermoelectron emission.
These thermoelectrons travel across the interelectrode space and arrive at the collector where they are absorbed. 
The electrons then travel through a lead, through an external load where work is done, and back to the emitter to complete the circuit.

The interesting output parameters of this device, such as the output power density and efficiency, are fully determined by the electron transport across the device.
Specifically, the output parameters are determined by a quantity known as the maximum motive of the device.
This quantity is essentially the highest barrier electrons encounter as they traverse the device.
There is a difficulty in calculating the maximum motive because the electron transport cannot be expressed by a closed-form equation.
Instead, a set of coupled differential equations must be self-consistently solved.

The `tec` python module I wrote implements a numerical solution to the electron transport problem described above and is used as the simulator to generate the training and validation data for the NN.


TK1 configuraiton and devops
============================
The TK1 ships with an installation of ubuntu; there's a user named ubuntu with password ubuntu.
I plugged the TK1 into the power supply and connected it via an ethernet cable to the network; all communication with the TK1 was performed via SSH.
According to the setup instructions, I must [execute a command so that `apt` doesn't clobber `libglx.so`](http://elinux.org/Jetson_TK1#An_important_step_before_connecting_the_Jetson_to_Internet) **before** connecting the board to the internet.

For the sake of convenience and good systems administration, I wanted to configure the TK1 so that I could log in without a password using an SSH key.
I also wanted a user named "jrsmith3" to match the username on my notebook in which I will install all of the code and administer the machine.
Finally, I wanted to change the default password for the "ubuntu" user for the sake of security.

Change `ubuntu` user password
-----------------------------
First, I logged into the TK1 via the user "ubuntu."
I used the [passwordstore utility](http://www.passwordstore.org/) on my notebook to generate a difficult-to-guess password for this machine.

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
For sysadmin purposes.

```
ubuntu@tegra-ubuntu:~$ sudo usermod -a -G sudo jrsmith3
```


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


Install Continuum.io's anaconda
-------------------------------
