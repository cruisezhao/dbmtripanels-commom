from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from .forms import *
from copy import deepcopy
from .models.network import (DeviceRacks, DevicePowers, DeviceDrives, DeviceKVMs,
                             DeviceRouters, DeviceSwitches, DeviceFirewalls, DeviceBares)








