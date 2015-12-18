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
* [ ] Allow ssh logins via ssh keys.
* [ ] Add my ssh key to user `jrsmith3`.
* [ ] [Update apt and packages](http://elinux.org/Jetson_TK1#Recommended_first_steps_now_that_your_board_has_internet_access).


Change `ubuntu` user password
-----------------------------
I am using the [passwordstore utility]() to generate a difficult-to-guess password for this machine.

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
