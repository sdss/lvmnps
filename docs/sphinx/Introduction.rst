.. _Introduction:

Introduction
=================

An NPS (Network Power Switch) is a device that can control multiple power switches through a network. By connecting the power of the LVM-I Spectroograph Box and subsystem through this device, the power of each device can be controlled through the network. 

LVM-I selected two models for NPS. 
In the LVM-I SCP, we decide to use “web power switch pro” by digital loggers(dli) for NPS. More details can be found through `here <https://dlidirect.com/products/new-pro-switch>`_ 
In the LVM-I TCP, we're using iboot web power switch in dataprobe Co.(iboot). More details can be found through `here <https://dataprobe.com/iboot/>`_ 
We updated *switch* moduel for the nps control library applicable to both models. The powerswitch class is created for the basic modules of dli and iboot and used in the actor command.

dli
------

The digital loggers provides a library made to control the power switch for the above models. Based on this module, the KHU team redefines and asynchronously changes the functions required for the command in SCP. This module plays a role in web crawling from the index web page that provides information about the power switch and controlling the power. For asynchronous web crawling, the asynchronous class provided by httpx was used instead of the default requests library. We also overridden the rest of the functions asynchronously. A new module for controlling power switch is defined as *lvmpower.py*.

.. image:: _static/dlinps.png
    :align: center

iboot
-------

.. image:: _static/ibootnps.png
    :align: center