#!/usr/bin/env python3

roomname = data.get("roomname")
entities_toggle = data.get("entities_toggle",[])
entities_keep = data.get("entities_keep",[])
active_states = data.get("active_states",["on","true","active",True,roomname])
timeout = data.get("timeout",2)
active_devices = []
passive_devices = []

found = False


logger.info("got triggered for room {}".format(roomname))
logger.info("options:\nentities_toggle: {}\nentities_keep: {}\nactive_states: {}".format(entities_toggle, entities_keep, active_states))

def checkStatus(entity):
    logger.info("[checkStatus] got entity {}".format(entity))
    logger.info("[checkStatus] using {}".format(hass.states.get(entity)))
    state = hass.states.get(entity).state
    logger.info("[checkStatus] state is {}".format(state))
    if state in active_states:
        logger.info("[checkStatus] {} IS in {}, returning TRUE".format(state, active_states))
        return True
    else:
        logger.info("[checkStatus] {} IS NOT in {}, returning FALSE".format(state, active_states))
        return False


# when room is occupied, check if it should stay that way
if hass.states.get("timer.{}_timer".format(roomname)).state in active_states:
    logger.info("Room {} is already occupied, timer is in state: {}. checking all entities..".format(roomname,hass.states.get("timer.{}_timer".format(roomname)).state))
    for entity in entities_toggle + entities_keep:
        if checkStatus(entity):
            logger.info("checkStatus returned True for {}".format(entity))
            active_devices.append(entity)
            found = True
        else:
            passive_devices.append(entity)
    if found:
        hass.states.set("input_boolean.{}_occupancy".format(roomname), "on")
        logger.info("found active devices: {}\nsetting input_boolean.{}_occupancy to on".format(active_devices, roomname))
        timeout_formated = "00:0{}:00".format(timeout)
        timer_formated = "timer.{}_timer".format(roomname)
        service_data = {
            "duration": timeout_formated,
            "entity_id": timer_formated
        }
        hass.services.call("timer","start",service_data)
        logger.info("restarted timer. service_data:\n{}".format(service_data))
    else:
        logger.info("haven't found active devices, checked: {}".format(passive_devices))
        logger.info("checkStatus hasn't returned True for any entity, resetting state to off")
        hass.states.set("input_boolean.{}_occupancy".format(roomname), "off")
# if room is not occupied, check only entites that should toggle the status
else:
    logger.info("Room {} is not occupied, timer is in state: {}. checking toggle entities only..".format(roomname,hass.states.get("timer.{}_timer".format(roomname)).state))
    for entity in entities_toggle:
        if checkStatus(entity):
            logger.info("checkStatus returned True for {}".format(entity))
            active_devices.append(entity)
            found = True
        else:
            passive_devices.append(entity)
    if found:
        hass.states.set("input_boolean.{}_occupancy".format(roomname), "on")
        logger.info("found active devices: {}\nsetting input_boolean.{}_occupancy to on".format(active_devices, roomname))
        timeout_formated = "00:0{}:00".format(timeout)
        timer_formated = "timer.{}_timer".format(roomname)
        service_data = {
            "duration": timeout_formated,
            "entity_id": timer_formated
        }
        hass.services.call("timer","start",service_data)
        logger.info("restarted timer. service_data:\n{}".format(service_data))
    else:
        logger.info("haven't found active devices, checked: {}".format(passive_devices))
        logger.info("checkStatus hasn't returned True for any entity, resetting state to off")
        hass.states.set("input_boolean.{}_occupancy".format(roomname), "off")
