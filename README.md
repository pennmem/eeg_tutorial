# EEG Noise Tutorial

This repository gives an interactive introduction to sources of noise that can contaminate EEG signals and gives recommendations for troubleshooting.

Types of EEG signal components covered:
* pink (1/f) background spectra
* physiological oscillations
* white noise
* line noise
* Common signs of artifacts
* Recommendations for troubleshooting noisy recordings

We recommend walking through all sections of the notebook, making sure to take
the line noise recognition quiz at the end of the document until you receive a passing score.

# Initial Setup

To start working with any materials contained or linked here, you'll need to
set up tools for writing and running Python code. If you are affiliated with
the Computational Memory Lab and have access to Rhino, our computing cluster,
you can complete the "Getting started on Rhino section". Otherwise, you
can follow the instructions in the "Getting started on your computer" 
section to set up python on your own computer.

## Command line access

All subsequent stages of these instructions will assume familiarity with and access
to a *NIX command line. If this is unfamiliar to you, please use the resources below
to get yourself oriented.

If you are using Rhino, an apple computer running OSX, or a Linux computer,
you will already have access to a command line. On Windows, we recommend
using Cygwin <https://www.cygwin.com/> or the Ubuntu subsystem
<https://docs.microsoft.com/en-us/windows/wsl/install-win10>.

General Introduction: https://ubuntu.com/tutorials/command-line-for-beginners#1-overview

## Getting started on Rhino

If you have been provided with an account on the Rhino computing cluster, these instructions will help you access and setup your account to the point where you can follow these workshop notes and perform analyses. If you are using another system, skip ahead to the section "Getting started on your computer".

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

You should be all set! Next time you log in to your JupyterLab account, choose the option to launch a new notebook with "workshop" as your Python environment.

## Getting started on your computer
To complete this tutorial on your local machine, you will need Python 3.7 or higher along with a few dependencies. You can install Python from <https://www.python.org/downloads/> for Mac. Again, for Windows users we recommend using the Windows Subsystem for Linux described above, which will provide you with an Ubuntu Linux distribution which comes installed with Python 3. You can confirm that you have python installed by running the command "python" from your terminal. This will open up an interactive Python command line, in which you can execute Python code as commands (try typing '1 + 1'). Type "exit()" to leave this Python command line interface. Once you have access to Python, navigate in your terminal to the tutorial folder created when you cloned the repository and run the command 'pip install -r requirements.txt'. Once these dependencies have been installed, run the command 'jupyter lab' in the directory containing the tutorial notebook. A couple links will be displayed on the command line. Copy and paste either one of these links in your browser to open up the Jupyter Lab interface from which you will access the tutorial.

## Using Jupyter Notebooks

A Jupyter notebook is a file which can include both executable code and formatted (Markdown) text in isolated blocks or "cells". These code cells can be executed one by one, which is convenient for prototyping code as well as for displaying results near the code that produced those results. If you'd like a tutorial on Jupyter notebooks (in the Jupyter Lab interface), you can access one here:
<https://jupyter.org/try-jupyter/lab/?path=notebooks%2FIntro.ipynb>. Once the Jupyter Lab interface loads, click the "Try the Welcome Tour" in the bottom right corner of the page to get acquainted with the Jupyter Lab interface. Open up the Jupyter Lab tutorial again (at the same link) and instead click the "Try the Notebook Tour" option in the bottom right corner of the webpage to see notebooks in action! To open up the EEG noise tutorial notebook, click on the eeg_tutorial.ipynb file in the file explorer on the left side of the Jupyter Lab webpage as shown on the tutorial.
