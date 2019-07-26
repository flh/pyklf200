# -*- coding: utf-8 -*-

"""
List of commands understood or sent by the KLF-200 gateway
"""

# Provides information on what triggered the error
GW_ERROR_NTF = 0x0000

# Request gateway to reboot
GW_REBOOT_REQ = 0x0001

# Acknowledge to GW_REBOOT_REQ command
GW_REBOOT_CFM = 0x0002

# Request the state of the gateway
GW_GET_STATE_REQ = 0x000C

# Acknowledge to GW_GET_STATE_REQ
GW_GET_STATE_CFM = 0x000D

# Request extended information of all nodes
GW_GET_ALL_NODES_INFORMATION_REQ = 0x0202

# Acknowledge to GW_GET_ALL_NODES_INFORMATION_REQ
GW_GET_ALL_NODES_INFORMATION_CFM = 0x0203

# Acknowledge to GW_GET_ALL_NODES_INFORMATION_REQ. Holds node information
GW_GET_ALL_NODES_INFORMATION_NTF = 0x0204

# Acknowledge to GW_GET_ALL_NODES_INFORMATION_REQ. No more nodes
GW_GET_ALL_NODES_INFORMATION_FINISHED_NTF = 0x0205

# Enter password to authenticate request
GW_PASSWORD_ENTER_REQ = 0x3000

# Acknowledge to GW_PASSWORD_ENTER_REQ
GW_PASSWORD_ENTER_CFM = 0x3001

# Request password change
GW_PASSWORD_CHANGE_REQ = 0x3002

# Acknowledge to GW_PASSWORD_CHANGE_REQ
GW_PASSWORD_ENTER_CFM = 0x3003

# Acknowledge to GW_PASSWORD_CHANGE_REQ. Broadcasted to all connected
# clients.
GW_PASSWORD_ENTER_NTF = 0x3004
