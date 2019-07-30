# -*- coding: utf-8 -*-

"""
List of commands understood or sent by the KLF-200 gateway
"""

# Provides information on what triggered the error.
GW_ERROR_NTF = 0x0000

# Request gateway to reboot.
GW_REBOOT_REQ = 0x0001

# Acknowledge to GW_REBOOT_REQ command.
GW_REBOOT_CFM = 0x0002

# Request gateway to clear system table, scene table and set Ethernet settings to factory default. Gateway will reboot.
GW_SET_FACTORY_DEFAULT_REQ = 0x0003

# Acknowledge to GW_SET_FACTORY_DEFAULT_REQ command.
GW_SET_FACTORY_DEFAULT_CFM = 0x0004

# Request version information.
GW_GET_VERSION_REQ = 0x0008

# Acknowledge to GW_GET_VERSION_REQ command.
GW_GET_VERSION_CFM = 0x0009

# Request KLF
GW_GET_PROTOCOL_VERSION_REQ = 0x000A

# Acknowledge to GW_GET_PROTOCOL_VERSION_REQ command.
GW_GET_PROTOCOL_VERSION_CFM = 0x000B

# Request the state of the gateway
GW_GET_STATE_REQ = 0x000C

# Acknowledge to GW_GET_STATE_REQ command.
GW_GET_STATE_CFM = 0x000D

# Request gateway to leave learn state.
GW_LEAVE_LEARN_STATE_REQ = 0x000E

# Acknowledge to GW_LEAVE_LEARN_STATE_REQ command.
GW_LEAVE_LEARN_STATE_CFM = 0x000F

# Request network parameters.
GW_GET_NETWORK_SETUP_REQ = 0x00E0

# Acknowledge to GW_GET_NETWORK_SETUP_REQ.
GW_GET_NETWORK_SETUP_CFM = 0x00E1

# Set network parameters.
GW_SET_NETWORK_SETUP_REQ = 0x00E2

# Acknowledge to GW_SET_NETWORK_SETUP_REQ.
GW_SET_NETWORK_SETUP_CFM = 0x00E3

# Request a list of nodes in the gateways system table.
GW_CS_GET_SYSTEMTABLE_DATA_REQ = 0x0100

# Acknowledge to GW_CS_GET_SYSTEMTABLE_DATA_REQ
GW_CS_GET_SYSTEMTABLE_DATA_CFM = 0x0101

# Acknowledge to GW_CS_GET_SYSTEM_TABLE_DATA_REQList of nodes in the gateways systemtable.
GW_CS_GET_SYSTEMTABLE_DATA_NTF = 0x0102

# Start CS DiscoverNodes macro in
GW_CS_DISCOVER_NODES_REQ = 0x0103

# Acknowledge to GW_CS_DISCOVER_NODES_REQ command.
GW_CS_DISCOVER_NODES_CFM = 0x0104

# Acknowledge to GW_CS_DISCOVER_NODES_REQ command.
GW_CS_DISCOVER_NODES_NTF = 0x0105

# Remove one or more nodes in the systemtable.
GW_CS_REMOVE_NODES_REQ = 0x0106

# Acknowledge to GW_CS_REMOVE_NODES_REQ.
GW_CS_REMOVE_NODES_CFM = 0x0107

# Clear systemtable and delete system key.
GW_CS_VIRGIN_STATE_REQ = 0x0108

# Acknowledge to GW_CS_VIRGIN_STATE_REQ.
GW_CS_VIRGIN_STATE_CFM = 0x0109

# Setup
GW_CS_CONTROLLER_COPY_REQ = 0x010A

# Acknowledge to GW_CS_CONTROLLER_COPY_REQ.
GW_CS_CONTROLLER_COPY_CFM = 0x010B

# Acknowledge to GW_CS_CONTROLLER_COPY_REQ.
GW_CS_CONTROLLER_COPY_NTF = 0x010C

# Cancellation of system copy to other controllers.
GW_CS_CONTROLLER_COPY_CANCEL_NTF = 0x010D

# Receive system key from another controller.
GW_CS_RECEIVE_KEY_REQ = 0x010E

# Acknowledge to GW_CS_RECEIVE_KEY_REQ.
GW_CS_RECEIVE_KEY_CFM = 0x010F

# Acknowledge to GW_CS_RECEIVE_KEY_REQ with status.
GW_CS_RECEIVE_KEY_NTF = 0x0110

# Information on Product Generic Configuration job initiated by press on PGC button.
GW_CS_PGC_JOB_NTF = 0x0111

# Broadcasted to all clients and gives information about added and removed actuator nodes in system table.
GW_CS_SYSTEM_TABLE_UPDATE_NTF = 0x0112

# Generate new system key and update actuators in systemtable.
GW_CS_GENERATE_NEW_KEY_REQ = 0x0113

# Acknowledge to GW_CS_GENERATE_NEW_KEY_REQ.
GW_CS_GENERATE_NEW_KEY_CFM = 0x0114

# Acknowledge to GW_CS_GENERATE_NEW_KEY_REQ with status.
GW_CS_GENERATE_NEW_KEY_NTF = 0x0115

# Update key in actuators holding an old key.
GW_CS_REPAIR_KEY_REQ = 0x0116

# Acknowledge to GW_CS_REPAIR_KEY_REQ.
GW_CS_REPAIR_KEY_CFM = 0x0117

# Acknowledge to GW_CS_REPAIR_KEY_REQ with status.
GW_CS_REPAIR_KEY_NTF = 0x0118

# Request one or more actuator to open for configuration.
GW_CS_ACTIVATE_CONFIGURATION_MODE_REQ = 0x0119

# Acknowledge to GW_CS_ACTIVATE_CONFIGURATION_MODE_REQ.
GW_CS_ACTIVATE_CONFIGURATION_MODE_CFM = 0x011A

# Request extended information of one specific actuator node.
GW_GET_NODE_INFORMATION_REQ = 0x0200

# Acknowledge to GW_GET_NODE_INFORMATION_REQ.
GW_GET_NODE_INFORMATION_CFM = 0x0201

# Request extended information of all nodes.
GW_GET_ALL_NODES_INFORMATION_REQ = 0x0202

# Acknowledge to GW_GET_ALL_NODES_INFORMATION_REQ
GW_GET_ALL_NODES_INFORMATION_CFM = 0x0203

# Acknowledge to GW_GET_ALL_NODES_INFORMATION_REQ. Holds node information
GW_GET_ALL_NODES_INFORMATION_NTF = 0x0204

# Acknowledge to GW_GET_ALL_NODES_INFORMATION_REQ. No more nodes.
GW_GET_ALL_NODES_INFORMATION_FINISHED_NTF = 0x0205

# Set node variation.
GW_SET_NODE_VARIATION_REQ = 0x0206

# Acknowledge to GW_SET_NODE_VARIATION_REQ.
GW_SET_NODE_VARIATION_CFM = 0x0207

# Set node name.
GW_SET_NODE_NAME_REQ = 0x0208

# Acknowledge to GW_SET_NODE_NAME_REQ.
GW_SET_NODE_NAME_CFM = 0x0209

# Set node velocity.
GW_SET_NODE_VELOCITY_REQ = 0x020A

# Acknowledge to GW_SET_NODE_VELOCITY_REQ.
GW_SET_NODE_VELOCITY_CFM = 0x020B

# Information has been updated.
GW_NODE_INFORMATION_CHANGED_NTF = 0x020C

# Information has been updated.
GW_NODE_STATE_POSITION_CHANGED_NTF = 0x0211

# Set search order and room placement.
GW_SET_NODE_ORDER_AND_PLACEMENT_REQ = 0x020D

# Acknowledge to GW_SET_NODE_ORDER_AND_PLACEMENT_REQ.
GW_SET_NODE_ORDER_AND_PLACEMENT_CFM = 0x020E

# Request information about all defined groups.
GW_GET_GROUP_INFORMATION_REQ = 0x0220

# Acknowledge to GW_GET_GROUP_INFORMATION_REQ.
GW_GET_GROUP_INFORMATION_CFM = 0x0221

# Acknowledge to GW_GET_NODE_INFORMATION_REQ.
GW_GET_GROUP_INFORMATION_NTF = 0x0230

# Change an existing group.
GW_SET_GROUP_INFORMATION_REQ = 0x0222

# Acknowledge to GW_SET_GROUP_INFORMATION_REQ.
GW_SET_GROUP_INFORMATION_CFM = 0x0223

# Broadcast to all, about group information of a group has been changed.
GW_GROUP_INFORMATION_CHANGED_NTF = 0x0224

# Delete a group.
GW_DELETE_GROUP_REQ = 0x0225

# Acknowledge to GW_DELETE_GROUP_INFORMATION_REQ.
GW_DELETE_GROUP_CFM = 0x0226

# Request new group to be created.
GW_NEW_GROUP_REQ = 0x0227

# Request information about all defined groups.
GW_GET_ALL_GROUPS_INFORMATION_REQ = 0x0229

# Acknowledge to GW_GET_ALL_GROUPS_INFORMATION_REQ.
GW_GET_ALL_GROUPS_INFORMATION_CFM = 0x022A

# Acknowledge to GW_GET_ALL_GROUPS_INFORMATION_REQ.
GW_GET_ALL_GROUPS_INFORMATION_NTF = 0x022B

# Acknowledge to GW_GET_ALL_GROUPS_INFORMATION_REQ.
GW_GET_ALL_GROUPS_INFORMATION_FINISHED_NTF = 0x022C

# GW_GROUP_DELETED_NTF is broadcasted to all, when a group has been removed.
GW_GROUP_DELETED_NTF = 0x022D

# Enable house status monitor.
GW_HOUSE_STATUS_MONITOR_ENABLE_REQ = 0x0240

# Acknowledge to GW_HOUSE_STATUS_MONITOR_ENABLE_REQ.
GW_HOUSE_STATUS_MONITOR_ENABLE_CFM = 0x0241

# Disable house status monitor.
GW_HOUSE_STATUS_MONITOR_DISABLE_REQ = 0x0242

# Acknowledge to GW_HOUSE_STATUS_MONITOR_DISABLE_REQ.
GW_HOUSE_STATUS_MONITOR_DISABLE_CFM = 0x0243

# Send activating command direct to one or more io-homecontrol nodes.
GW_COMMAND_SEND_REQ = 0x0300

# Acknowledge to GW_COMMAND_SEND_REQ.
GW_COMMAND_SEND_CFM = 0x0301

# Gives run status for io-homecontrol
GW_COMMAND_RUN_STATUS_NTF = 0x0302

# Gives remaining time before io-homecontrol node enter target position.
GW_COMMAND_REMAINING_TIME_NTF = 0x0303

# Command send, Status request, Wink, Mode or Stop session is finished.
GW_SESSION_FINISHED_NTF = 0x0304

# Acknowledge to GW_STATUS_REQUEST_REQ.
GW_STATUS_REQUEST_CFM = 0x0306

# Acknowledge to GW_STATUS_REQUEST_REQ. Status request from one or more io-homecontrol nodes.
GW_STATUS_REQUEST_NTF = 0x0307

# Request from one or more io-homecontrol nodes to Wink.
GW_WINK_SEND_REQ = 0x0308

# Acknowledge to GW_WINK_SEND_REQ
GW_WINK_SEND_CFM = 0x0309

# Status info for performed wink request.
GW_WINK_SEND_NTF = 0x030A

# Set a parameter limitation in an actuator.
GW_SET_LIMITATION_REQ = 0x0310

# Acknowledge to GW_SET_LIMITATION_REQ.
GW_SET_LIMITATION_CFM = 0x0311

# Get parameter limitation in an actuator.
GW_GET_LIMITATION_STATUS_REQ = 0x0312

# Acknowledge to GW_GET_LIMITATION_STATUS_REQ.
GW_GET_LIMITATION_STATUS_CFM = 0x0313

# Hold information about limitation.
GW_LIMITATION_STATUS_NTF = 0x0314

# Send Activate Mode to one or more io-homecontrol nodes.
GW_MODE_SEND_REQ = 0x0320

# Acknowledge to GW_MODE_SEND_REQ
GW_MODE_SEND_CFM = 0x0321

# Notify with Mode activation info.
GW_MODE_SEND_NTF = 0x0322

# Prepare gateway to record a scene.
GW_INITIALIZE_SCENE_REQ = 0x0400

# Acknowledge to GW_INITIALIZE_SCENE_REQ.
GW_INITIALIZE_SCENE_CFM = 0x0401

# Acknowledge to GW_INITIALIZE_SCENE_REQ.
GW_INITIALIZE_SCENE_NTF = 0x0402

# Cancel record scene process.
GW_INITIALIZE_SCENE_CANCEL_REQ = 0x0403

# Acknowledge to GW_INITIALIZE_SCENE_CANCEL_REQ command.
GW_INITIALIZE_SCENE_CANCEL_CFM = 0x0404

# Store actuator positions changes since GW_INITIALIZE_SCENE, as a scene.
GW_RECORD_SCENE_REQ = 0x0405

# Acknowledge to GW_RECORD_SCENE_REQ.
GW_RECORD_SCENE_CFM = 0x0406

# Acknowledge to GW_RECORD_SCENE_REQ.
GW_RECORD_SCENE_NTF = 0x0407

# Delete a recorded scene.
GW_DELETE_SCENE_REQ = 0x0408

# Acknowledge to GW_DELETE_SCENE_REQ.
GW_DELETE_SCENE_CFM = 0x0409

# Request a scene to be renamed.
GW_RENAME_SCENE_REQ = 0x040A

# Acknowledge to GW_RENAME_SCENE_REQ.
GW_RENAME_SCENE_CFM = 0x040B

# Request a list of scenes.
GW_GET_SCENE_LIST_REQ = 0x040C

# Acknowledge to GW_GET_SCENE_LIST.
GW_GET_SCENE_LIST_CFM = 0x040D

# Acknowledge to GW_GET_SCENE_LIST.
GW_GET_SCENE_LIST_NTF = 0x040E

# Request extended information for one given scene.
GW_GET_SCENE_INFOAMATION_REQ = 0x040F

# Acknowledge to GW_GET_SCENE_INFOAMATION_REQ.
GW_GET_SCENE_INFOAMATION_CFM = 0x0410

# Acknowledge to GW_GET_SCENE_INFOAMATION_REQ.
GW_GET_SCENE_INFOAMATION_NTF = 0x0411

# Request gateway to enter a scene.
GW_ACTIVATE_SCENE_REQ = 0x0412

# Acknowledge to GW_ACTIVATE_SCENE_REQ.
GW_ACTIVATE_SCENE_CFM = 0x0413

# Request all nodes in a given scene to stop at their current position.
GW_STOP_SCENE_REQ = 0x0415

# Acknowledge to GW_STOP_SCENE_REQ.
GW_STOP_SCENE_CFM = 0x0416

# A scene has either been changed or removed.
GW_SCENE_INFORMATION_CHANGED_NTF = 0x0419

# Activate a product group in a given direction.
GW_ACTIVATE_PRODUCTGROUP_REQ = 0x0447

# Acknowledge to GW_ACTIVATE_PRODUCTGROUP_REQ.
GW_ACTIVATE_PRODUCTGROUP_NTF = 0x0449

# Get list of assignments to all Contact Input to scene or product group.
GW_GET_CONTACT_INPUT_LINK_LIST_REQ = 0x0460

# Acknowledge to GW_GET_CONTACT_INPUT_LINK_LIST_REQ.
GW_GET_CONTACT_INPUT_LINK_LIST_CFM = 0x0461

# Set a link from a Contact Input to a scene or product group.
GW_SET_CONTACT_INPUT_LINK_REQ = 0x0462

# Acknowledge to GW_SET_CONTACT_INPUT_LINK_REQ.
GW_SET_CONTACT_INPUT_LINK_CFM = 0x0463

# Remove a link from a Contact Input to a scene.
GW_REMOVE_CONTACT_INPUT_LINK_REQ = 0x0464

# Acknowledge to GW_REMOVE_CONTACT_INPUT_LINK_REQ.
GW_REMOVE_CONTACT_INPUT_LINK_CFM = 0x0465

# Request header from activation
GW_GET_ACTIVATION_LOG_HEADER_REQ = 0x0500

# Confirm header from activation log.
GW_GET_ACTIVATION_LOG_HEADER_CFM = 0x0501

# Request clear all data in activation log.
GW_CLEAR_ACTIVATION_LOG_REQ = 0x0502

# Confirm clear all data in activation log.
GW_CLEAR_ACTIVATION_LOG_CFM = 0x0503

# Request line from activation log.
GW_GET_ACTIVATION_LOG_LINE_REQ = 0x0504

# Confirm line from activation log.
GW_GET_ACTIVATION_LOG_LINE_CFM = 0x0505

# Confirm line from activation log.
GW_ACTIVATION_LOG_UPDATED_NTF = 0x0506

# Request lines from activation log.
GW_GET_MULTIPLE_ACTIVATION_LOG_LINES_REQ = 0x0507

# Error log data from activation log.
GW_GET_MULTIPLE_ACTIVATION_LOG_LINES_NTF = 0x0508

# Confirm lines from activation log.
GW_GET_MULTIPLE_ACTIVATION_LOG_LINES_CFM = 0x0509

# Request to set UTC time.
GW_SET_UTC_REQ = 0x2000

# Acknowledge to GW_SET_UTC_REQ.
GW_SET_UTC_CFM = 0x2001

# Set time zone and daylight savings rules.
GW_RTC_SET_TIME_ZONE_REQ = 0x2002

# Acknowledge to GW_RTC_SET_TIME_ZONE_REQ.
GW_RTC_SET_TIME_ZONE_CFM = 0x2003

# Request the local time based on current time zone and daylight savings rules.
GW_GET_LOCAL_TIME_REQ = 0x2004

# Acknowledge to GW_RTC_SET_TIME_ZONE_REQ.
GW_GET_LOCAL_TIME_CFM = 0x2005

# Enter password to authenticate request
GW_PASSWORD_ENTER_REQ = 0x3000

# Acknowledge to GW_PASSWORD_ENTER_REQ
GW_PASSWORD_ENTER_CFM = 0x3001

# Request password change.
GW_PASSWORD_CHANGE_REQ = 0x3002

# Acknowledge to GW_PASSWORD_CHANGE_REQ.
GW_PASSWORD_CHANGE_CFM = 0x3003

# Acknowledge to GW_PASSWORD_CHANGE_REQ. Broadcasted to all connected clients.
GW_PASSWORD_CHANGE_NTF = 0x3004
