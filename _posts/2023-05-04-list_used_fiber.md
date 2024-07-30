---
layout:     post
title:      "PowerCLI Scirpt: list_used_fiber.ps"
subtitle:   "PowerCLI Scirpt: list_used_fiber"
date:       2023-05-04
author:     "Gavin Wang"
catalog:    true
categories:
    - [VCenter]
tags:
    - VCenter
    - PowerCLI
---


# Overview

This script is used to find fibre card for each VM on vCenter.

Usage:

```pwsh list_used_fiber.ps -server 10.1.2.3 -user user1 -pwd password -fibre_name *Fibre* ```


# Scripts of list_used_fiber.ps

```shell
# This script is used to find fibre card for each VM on vCenter.
# Usage: pwsh list_used_fiber.ps -server 10.1.2.3 -user user1 -pwd password -fibre_name *Fibre*

param (
    [string] $server = "",
    [string] $user = "",
    [string] $pwd = "",
    [string] $fibre_name= "*Fibre*"
)

If (-Not ($server -and $user -and $pwd)) {
    Write-Host "Please input vCenter IP, user name and password to conect to vCenter:$server"
    Write-Host "Usage: pwsh list_used_fiber.ps -server 10.1.14.3 -user user1 -pwd password -fibre_name *Fibre*" -ForegroundColor green
    exit
}

$output = ""

Connect-VIServer -Server $server -Protocol https -force -User $user -Password $pwd
$vm_name = Get-VM

Write-Host    "`n`nStart to search which VM used fibre card...`n"
#Write-Host "VM | PCI Device"
$output += "VM | PCI Device`n"
foreach($vm in $vm_name)
{
    $device=Get-PassthroughDevice -Type pci -VM $vm -name $fibre_name
    If ($device) {
	    #Write-Host "$($vm) | $($device)"
	    $output += "$($vm) | $($device)`n"
    }
}

Write-Host $output

```
