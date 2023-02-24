# EEG Noise Tutorial

This repository gives an interactive introduction to sources of noise that can contaminate EEG signals and gives recommendations for troubleshooting.

Types of EEG signal components covered:
* pink (1/f) background spectra
* physiological oscillations
* white noise
* line noise
* Common signs of artifacts
* Recommendations for troubleshooting noisy recordings

# Initial Setup

To start working with any materials contained or linked here, you'll need to
set up tools for writing and running Python code. If you are affiliated with
the Computational Memory Lab and have access to Rhino, our computing cluster,
you can complete just the "Getting started on Rhino section". Otherwise, you
can follow the instructions in the "Getting started on your computer" 
section to set up python on your own computer.

<!-- 
## Command line access

All subsequent stages of these instructions will assume familiarity with and access
to a *NIX command line. If this is unfamiliar to you, please use the resources below
to get yourself oriented.

If you are using Rhino, an apple computer running OSX, or a Linux computer,
you will already have access to a command line. On Windows, we recommend
using Cygwin <https://www.cygwin.com/> or the Ubuntu subsystem
<https://docs.microsoft.com/en-us/windows/wsl/install-win10>.

General Introduction: https://ubuntu.com/tutorials/command-line-for-beginners#1-overview
 -->

## Getting started on Rhino

If you have been provided with an account on the Rhino computing cluster, these instructions will help you access and setup your account to the point where you can follow these workshop notes and perform analyses. If you are using another system, skip ahead to Setting up JupyterLab.

### Setting up your Rhino2 Account

1\. You can log in to Rhino2 in a terminal window by using any ssh client
to ssh into rhino as follows, replacing the "username" with your username:

    ssh username@rhino2.psych.upenn.edu

and then typing your temporary password when prompted. Once successfully
connected, type:

    passwd

to change your password to something only you know. Please do this as soon as
you have the time!


2\. Once you have your password set up, check to be sure you can log in to
JupyterLab, where you'll be completing the tutorial. If you are
connected to the internet on UPenn's campus, you only need to go to
[https://rhino2.psych.upenn.edu:8200](https://rhino2.psych.upenn.edu:8200/) to
access JupyterLab. If you are connecting remotely, follow the rest of this
step. In a terminal where ssh is accessible, replace the "username" with your
username, and open an ssh tunnel by typing:

    ssh -L8000:rhino2.psych.upenn.edu:8200 username@rhino2.psych.upenn.edu

followed by entering your rhino password. In your web browser, navigate to:

[https://127.0.0.1:8000](https://127.0.0.1:8000)

and you should see the JupyterLab interface pop up!  Note that the "s" on https is critical for this to work.  Your browser might warn about this being an insecure connection or invalid certificate, given that 127.0.0.1 (direct to the ssh tunnel on your own computer) is not rhino.  Override this warning and connect anyway, because we are using ssh to provide better security here.  If the connection still fails, go back and make sure that your ssh tunnel was correctly created.

## Setting up your environment (Rhino)
Working on rhino gives you access to a computing environment that already has the right software installed to complete the entire tutorial.

In JupyterLab, open any notebook and then go to Kernel -> Change Kernel... and then select "workshop" from the dropdown! Make sure you use this kernel whenever you're opening a notebook. 

You should be all set! Next time you log in to your JupyterLab account,
choose the option to launch a new notebook with "workshop" as your Python environment.

## Getting started on your computer
To complete this tutorial on your local machine, you will need to install a Python environment with the following dependencies: numpy, pandas, matplotlib, mne (v0.18.0), scipy, ipython, and jupyter. These packages can all be installed through conda and pip. Then run 'jupyter notebook' in the directory containing this notebook file, click the link output to the command line to open up a Jupyter file explorer interface in your browser, and open up this notebook to begin the tutorial.
