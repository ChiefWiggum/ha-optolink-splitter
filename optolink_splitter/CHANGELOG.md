# Changelog

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
