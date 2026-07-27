# Changelog

## 1.0.5

- Poll list template now polls only heating circuit HK2 - the HK1 datapoints
  are removed (all known real WO1C air-source systems, including a verified
  Vitocal 300-A, run their circuit as HK2). The HK1 address mapping stays
  documented in the template header for the rare HK1 system.
- Docs updated accordingly; ad-hoc write example now uses the HK2 address.

## 1.0.4

First field feedback from a real Vitocal 300-A (thanks!):

- Poll list template: `compressor_running` (0x0480) and `dhw_loading_pump`
  (0x0496) never respond on a real 300-A - both are now commented out with
  probe instructions (`read;0x0480;1` via the cmnd entity) so they can be
  re-enabled on units that do answer.
- Dashboard examples: the heat-pump-card now derives "compressor running"
  from `compressor_power > 0` and "DHW charging" from `dhw_pump_speed > 0`
  via two new template helpers.

NOTE: the template is only copied to /addon_configs/ on first start - apply
the change to an existing homeassistant_poll_list.py manually (or delete it
and restart). Existing helper users: re-copy heat_pump_card_helpers.yaml.

## 1.0.3

- Fix: HA discovery entities were never published. homeassistant_publish.py
  waits for the splitter's MQTT LWT to be 'online', but the add-on ran it
  before starting the splitter. Discovery now runs in the background (up to
  3 attempts, 15 s apart) after the splitter has started.

## 1.0.2

Poll list template fixes:

- Removed invalid `state_class` from the writable number entities - Home
  Assistant's MQTT discovery rejects number configs with this key, which
  could prevent all setpoint / heating-curve sliders from being created.
- Heating-curve level sliders now allow negative values (min -13, was 0).
- DHW setpoint slider range aligned with the water_heater entity (30-60 C).

NOTE: the template is only copied to /addon_configs/ on first start. If a
homeassistant_poll_list.py already exists there, apply these changes
manually (or delete the file and restart the app to re-seed it).

## 1.0.1

- German translation of the app options.
- Graphical dashboard example: mapping of the app's entities to the
  [lovelace-heat-pump-card](https://github.com/ManfredTremmel/lovelace-heat-pump-card),
  including the required template helpers (`examples/` folder in the
  repository, see README).

## 1.0.0

Initial release.

- Wraps [philippoo66/optolink-splitter](https://github.com/philippoo66/optolink-splitter)
  (pinned commit) with settings generated from the app options; Mosquitto
  broker auto-detection via the Supervisor MQTT service.
- Vitocal 300-A / Vitotronic 200 WO1C starter poll list, built from
  community-tested air-source WO1C configurations (wiki "350 Poll
  Configuration Samples"): temperatures, pressures, fan/pump/compressor
  modulation, defrost, compressor phase, thermal/electrical power, energy
  counters split heating/DHW, COP/SCOP, runtimes, fault buffers.
- Ready-made HA entities via MQTT discovery: climate (HK2 thermostat incl.
  presets), water_heater, one-time DHW charge button, e-heater switch,
  writable heating-curve and setpoint numbers, ad-hoc command console.
- HK1 and HK2 heating-circuit blocks both included - delete the circuit your
  system doesn't use.
- Optional Vitoconnect passthrough, TCP interface (Viessdata), raw
  custom_settings escape hatch.
