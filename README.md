# room-occupancy
## why
because I needed an propper way to manage the occupancy of my home. I tried a lot of other projects, but none of them really fits my needs.
## concepts
There are a few components to this script:
- the room that gets controlled (timer)
- entities_toggle: devices that can mark a room as occupied (motion sensors)
- entities_keep: devices that are only allowed to keep a room occupied (room-assistant, input booleans,..)
- active_states: a list of states that should be used to determin the state of a room (depending on your devices, e.g. active, on, True, roomname,..)
- automations to control lights/music (could be extended for hvac for example)

The flow goes like this:
- automation triggers the python script every 10 seconds or if the motion sensor for that room gets triggered (the configuration is placed in that automation, see EXAMPLE)
- the script then checks if the room is occupied already (timer is running)
- if yes, it checks every entity for its status and marks the room as occupied
- if not, it only checks entities defined in entities_toggle
- if it finds an active entity, it (re)starts the corresponding timer

## stuff you should create
For my setup I use the following helpers and entities:
- timer for each room
- overwrite toggle (input boolean) for each room
- room-assistant with a Pi in every room, measuring distances to our watches via bluetooth
- one or more motion sensors in each room
- automation for each room to run this script
- followup automations which are checking for the timer state (see EXAMPLES) and toggle lights/music/whatever you like
