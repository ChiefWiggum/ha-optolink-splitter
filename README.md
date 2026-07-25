# Home Assistant app (add-on): Optolink Splitter

A Home Assistant OS app wrapping
[philippoo66/optolink-splitter](https://github.com/philippoo66/optolink-splitter):
a local Viessmann Optolink <-> MQTT bridge with Home Assistant MQTT discovery.

> Since Home Assistant 2026.2, add-ons are called **apps** in the UI
> (Settings -> Apps). Technically nothing changed - this repository works the
> same way as before, and the developer docs still use the term "add-on".

Target setup: Optolink USB cable plugged directly into the machine running
HAOS (e.g. Raspberry Pi 5), Viessmann heat pump / boiler with a VS2/P300
controller such as the **Vitotronic 200 WO1C** (Vitocal 300-A and friends).

## Install in Home Assistant

1. Install the **Mosquitto broker** app and set up the **MQTT integration**.
2. Settings -> Apps -> **App Store** -> (three-dot menu) -> **Repositories**
   -> add `https://github.com/ChiefWiggum/ha-optolink-splitter`.
3. Install **Optolink Splitter** (the image is built on your machine;
   a few minutes on a Pi 5).
4. In the app's Configuration tab set `optolink_port` to your cable
   (Settings -> System -> Hardware; prefer `/dev/serial/by-id/...`).
   Leave the MQTT options empty - Mosquitto is auto-detected.
5. Start the app and watch the log. A Vitocal 300-A (WO1C) starter poll
   list is placed in `/addon_configs/..._optolink_splitter/` on first start,
   discovery entities are published, and a **Vitocal 300-A** device appears
   under the MQTT integration.
6. Tune the datapoints by editing `homeassistant_poll_list.py` in that folder
   (File editor / Samba app), then restart the app.

Full documentation: [`optolink_splitter/DOCS.md`](optolink_splitter/DOCS.md)
(also shown in the app's Documentation tab).

> Alternative without GitHub: copy the `optolink_splitter/` folder into the
> `/addons` share of your HAOS machine (Samba app) and it appears in the
> store under the local section.

## Layout

```
repository.yaml                     add-on repository manifest
optolink_splitter/
  config.yaml                       add-on manifest (options, schema, uart, mqtt)
  build.yaml                        base images per architecture
  Dockerfile                        installs Python deps + pinned splitter checkout
  run.sh                            generates settings from options, seeds poll
                                    list, publishes HA discovery, starts splitter
  templates/
    homeassistant_poll_list.py      Vitocal 300-A / WO1C starter datapoints
  DOCS.md                           user documentation
  CHANGELOG.md
  translations/                     option labels for the HA UI (en, de)
```

## Credits

All heavy lifting by [philippoo66/optolink-splitter](https://github.com/philippoo66/optolink-splitter)
(GPL-3.0). WO1C datapoint addresses from the upstream examples and the
[openv wiki](https://github.com/openv/openv/wiki). This wrapper is
unaffiliated with Viessmann.

Licensed under the [GPL-3.0](LICENSE), same as the upstream project.
