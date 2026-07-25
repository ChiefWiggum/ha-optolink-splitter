# Optolink Splitter add-on

Runs [philippoo66/optolink-splitter](https://github.com/philippoo66/optolink-splitter)
inside Home Assistant OS. It talks to a Viessmann heating (Vitocal, Vitodens,
Vitocrossal, ...) through an Optolink USB cable plugged into the machine running
Home Assistant, publishes all datapoints to MQTT, and creates Home Assistant
entities automatically via MQTT discovery.

Built and tested for a Vitocal 300-A with Vitotronic 200 (type WO1C) on a
Raspberry Pi 5, but any VS2/P300 Optolink controller should work.

## Prerequisites

1. The **Mosquitto broker** add-on installed and started, plus the **MQTT
   integration** configured (Settings -> Devices & Services). The add-on
   auto-detects Mosquitto through the Supervisor; no MQTT settings needed.
2. The Optolink USB cable plugged in. Find its stable path under
   Settings -> System -> Hardware -> All Hardware (look for `ttyUSB`), or use
   the `/dev/serial/by-id/...` link so the port survives reboots.
3. Nothing else using the Optolink port (unplug a Vitoconnect unless you wire
   it through the splitter's passthrough, see below).

## Options

| Option | Default | Description |
| --- | --- | --- |
| `optolink_port` | `/dev/ttyUSB0` | Serial port of the Optolink cable. Prefer `/dev/serial/by-id/...`. |
| `vitoconnect_port` | empty | Serial port of an optional Vitoconnect (passthrough / "splitter" mode). Leave empty if none. |
| `mqtt_broker` | empty | `host:port` of an external broker. Leave empty to auto-use the Mosquitto add-on. |
| `mqtt_user` / `mqtt_password` | empty | Broker credentials. Leave empty for auto-detection with Mosquitto. |
| `mqtt_topic` | `vitocal` | Base topic. Values publish to `vitocal/<name>`, commands go to `vitocal/cmnd`, responses to `vitocal/resp`. |
| `mqtt_retain` | `false` | Publish state messages retained. |
| `ha_discovery` | `true` | Publish HA MQTT discovery entities at startup (used with `homeassistant_poll_list.py`). |
| `poll_interval` | `30` | Base poll cycle in seconds. A `poll_interval` set inside your poll list file takes precedence. |
| `wo1c_energy` | `0` | WO1C only: read daily/weekly energy statistics every N-th cycle (0 = off). |
| `tcpip_port` | `0` | TCP interface for tools like Viessdata (0 = off). Also map the port in the add-on network settings. |
| `log_level` | `info` | Splitter log level. |
| `debug_optolink_rx` | `false` | Dump raw Optolink RX data into the add-on log. |
| `write_log_file` | `false` | Also write `optolinkvs2_switch.log` into the config folder (off by default to protect the SD card). |
| `custom_settings` | `[]` | Raw Python lines appended to the generated settings (e.g. `mqtt_no_redundant = True`). |

## The poll list

The set of datapoints lives in the add-on configuration folder, reachable via
the Samba or File editor add-ons at:

    /addon_configs/<repo-hash>_optolink_splitter/

On first start a `homeassistant_poll_list.py` starter template for a
Vitocal 300-A (WO1C) is placed there. It is built from community-tested
air-source WO1C configurations (Vitocal 200-A monobloc and 200-S, see the
[350 Poll Configuration Samples wiki page](https://github.com/philippoo66/optolink-splitter/wiki/350-Poll-Configuration-Samples)).
Both HK1 and HK2 heating-circuit blocks are active - keep the one that shows
real values on your system and delete the other. Edit it, then restart the add-on.
Upstream reference examples are copied alongside as `*.example` files.

Two formats are supported (upstream behavior):

- `homeassistant_poll_list.py` - datapoints enriched with HA entity attributes;
  entities are created automatically via MQTT discovery
  ([wiki 211](https://github.com/philippoo66/optolink-splitter/wiki/211-Alternative-Home-Assistant-Integration)).
- `poll_list.py` - the plain splitter format, MQTT values only
  (you define HA sensors yourself). If both files exist, `poll_list.py` wins.

Address collections for the WO1C and other controllers:
[optolink-splitter wiki](https://github.com/philippoo66/optolink-splitter/wiki)
and the [openv wiki](https://github.com/openv/openv/wiki).

## Reading and writing ad hoc

Publish to `<mqtt_topic>/cmnd` (response arrives on `<mqtt_topic>/resp`):

    read;0x0101;2;0.1          # read outside temperature
    write;0x2000;2;220         # set HK1 normal temp to 22.0 (raw value, scale 1/10)

Every polled datapoint also accepts writes on `<mqtt_topic>/<name>/set` using
the same format it is published in (e.g. payload `21.5`).

## Vitoconnect passthrough

To keep the ViCare app working in parallel, connect the Vitoconnect through a
USB-TTL adapter (CP2102 recommended) and set `vitoconnect_port`. Wiring and
power-up order are described in the
[upstream README](https://github.com/philippoo66/optolink-splitter#readme).

## Troubleshooting

- **`Permission denied` / port not found**: check the Hardware page for the
  real device path; use `/dev/serial/by-id/...`.
- **No entities in HA**: is the MQTT integration set up? Check the add-on log
  for the discovery step; listen to `homeassistant/#` in MQTT settings.
- **Nonsense values / errors on some datapoints**: that address does not exist
  on your unit - remove it from the poll list. Verify individual addresses
  with a `read;...` command first.
- **Updating the wrapped splitter version**: edit `SPLITTER_COMMIT` in the
  Dockerfile, bump `version` in `config.yaml`, push, then update the add-on.
