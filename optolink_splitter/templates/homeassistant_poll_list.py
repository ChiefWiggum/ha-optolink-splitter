"""
Poll list for a Viessmann Vitocal 300-A with Vitotronic 200 (type WO1C),
"Alternative Home Assistant Integration" format of optolink-splitter:
    https://github.com/philippoo66/optolink-splitter/wiki/211-Alternative-Home-Assistant-Integration

SOURCES (community-tested WO1C air-source configurations):
  [A] Vitocal 200-A AWO-E-AC 201.A16 (monobloc air-source, WO1C / CU401B_A -
      the same controller family as the Vitocal 300-A), poll list by @lellem:
      "Tabelle fuer Vitocalxxx-A mit Vitotronic 200 (Typ WO1C) (ab 04/2012)"
  [S] Vitocal 200-S AWB-E-AC 201.D16 (split air-source, WO1C / CU401B_S),
      HA poll list by @EarlSneedSinclair with Vitosoft-verified datapoint names
  Both from: https://github.com/philippoo66/optolink-splitter/wiki/350-Poll-Configuration-Samples
  Cross-checked against https://github.com/openv/openv/wiki (WO1C address pages).

HEATING CIRCUIT NOTE:
  All known real WO1C air-source systems (both reference systems and a
  verified Vitocal 300-A) run their heating circuit as HK2, so this template
  only polls HK2. In the unlikely case your system uses HK1 (HK2 values stay
  at 0 / implausible), replace the HK2 addresses with their HK1 counterparts:
    HK2: 0xB001 mode, 0x3xxx setpoints, 0x0114/0x1801 supply, 0x048E pump
    HK1: 0xB000 mode, 0x2xxx setpoints, 0x010A/0x1800 supply, 0x048D pump

After editing: restart the add-on. Probe single addresses any time via MQTT:
    publish to <mqtt_topic>/cmnd:  read;0x01cd;3;0.1   (answer on .../resp)
"""

poll_list = {
    "device": {
        "identifiers": ["Vitotronic_WO1C"],
        "name": "Vitocal 300-A",
        "model": "Vitocal 300-A (Vitotronic 200 WO1C)",
        "manufacturer": "Viessmann",
    },
    "node_id": "vitocal",
    "dp_prefix": "vitocal_",
    "beautifier": {
        "fixed": ["COP", "SCOP", "HK1", "HK2", "DHW", "WP"],
    },
    # "poll_interval": 30,   # if set here, it overrides the add-on option
    "poll_groups": {
        "ONCEONLY":  0,
        "ALWAYS":    1,
        "FAST":      2,
        "MEDIUM":    30,
        "SLOW":      120,
        "HOURLY":    3600,   # with poll_interval=30 more like "every 30h"; tune to taste
        "DEBUG":     -1,
    },
    "mqtt_delay": 0.05,

    "domains": [
        # ======================================================================
        # Temperatures  [A][S]
        # ======================================================================
        {
            "domain": "sensor",
            "unit_of_measurement": "\u00b0C",
            "device_class": "temperature",
            "state_class": "measurement",
            "suggested_display_precision": 1,
            "poll": [
                ("MEDIUM", "outside_temperature",             0x0101, 2, 0.1, True),           # [A][S]
                ("FAST",   "buffer_temperature",              0x010B, 2, 0.1, False),          # [A][S] buffer top
                ("FAST",   "dhw_temperature",                 0x01CD, 3, 'b:0:1', 0.1, True),  # [A][S] DHW storage top

                ("FAST",   "hk2_supply_temperature",          0x0114, 2, 0.1, False),          # [A][S]
                ("FAST",   "hk2_supply_target_temperature",   0x1801, 2, 0.1, False),          # [A][S]

                # Refrigerant / hydraulic circuit (3-byte: bytes 0-1 value,
                # byte 2 sensor status: 0 = OK, 6 = sensor not present)
                ("FAST",   "primary_supply_temperature",      0xB400, 3, 'b:0:1', 0.1, True),  # [A][S] air inlet side
                ("FAST",   "secondary_supply_temperature",    0xB402, 3, 'b:0:1', 0.1, True),  # [A][S]
                ("FAST",   "secondary_return_temperature",    0xB403, 3, 'b:0:1', 0.1, True),  # [A][S]
                ("MEDIUM", "liquid_gas_temperature",          0xB404, 3, 'b:0:1', 0.1, True),  # [A][S]
                ("MEDIUM", "evaporation_temperature",         0xB407, 3, 'b:0:1', 0.1, True),  # [A][S]
                ("MEDIUM", "condensation_temperature",        0xB408, 3, 'b:0:1', 0.1, True),  # [A][S]
                ("MEDIUM", "suction_gas_temperature",         0xB409, 3, 'b:0:1', 0.1, True),  # [A][S]
                ("MEDIUM", "hot_gas_temperature",             0xB40A, 3, 'b:0:1', 0.1, True),  # [A][S]
                ("MEDIUM", "superheating_target",             0xB40B, 3, 'b:0:1', 0.1, True),  # [S]
                ("MEDIUM", "superheating",                    0xB40D, 3, 'b:0:1', 0.1, True),
                # ("FAST", "primary_return_temperature",      0xB401, 3, 'b:0:1', 0.1, True),  # ground-source only, usually n/a on -A
            ],
        },

        # ======================================================================
        # Pressures  [A][S]
        # ======================================================================
        {
            "domain": "sensor",
            "unit_of_measurement": "bar",
            "device_class": "pressure",
            "state_class": "measurement",
            "suggested_display_precision": 1,
            "poll": [
                ("MEDIUM", "suction_gas_pressure", 0xB410, 3, 'b:0:1', 0.1, True),
                ("MEDIUM", "hot_gas_pressure",     0xB411, 3, 'b:0:1', 0.1, True),
            ],
        },

        # ======================================================================
        # Fan / pumps / compressor modulation (percent)  [A][S]
        # ======================================================================
        {
            "domain": "sensor",
            "unit_of_measurement": "%",
            "state_class": "measurement",
            "units": [
                {
                    "icon": "mdi:fan",
                    "poll": [
                        # air-source: "primary source speed" = the fan  [S: WPR3_B420_Drehzahl_Primaerquelle]
                        ("FAST", "fan_speed", 0xB420, 2, 1, False),
                    ],
                },
                {
                    "icon": "mdi:heat-pump-outline",
                    "poll": [
                        ("FAST", "compressor_power", 0xB423, 2, 1, False),   # [A][S]
                    ],
                },
                {
                    "icon": "mdi:pump",
                    "poll": [
                        ("FAST",   "secondary_pump_speed", 0xB421, 2, 1, False),  # [A][S]
                        ("MEDIUM", "dhw_pump_speed",       0xB422, 2, 1, False),  # [A][S]
                        # ("MEDIUM", "expansion_valve",    0xB424, 2, 1, False),
                    ],
                },
            ],
        },

        # ======================================================================
        # Binary states  [S: relay states, Vitosoft-verified]
        # ======================================================================
        {
            "domain": "binary_sensor",
            "payload_on": "1",
            "payload_off": "0",
            "units": [
                # 0x0480 compressor_running [S] did NOT respond on a real
                # Vitocal 300-A (never publishes). Probe with 'read;0x0480;1'
                # and re-enable if your unit answers; otherwise derive the
                # state from compressor_power > 0 (see examples/ in the repo).
                # {
                #     "device_class": "power",
                #     "icon": "mdi:heat-pump-outline",
                #     "poll": [
                #         ("ALWAYS", "compressor_running", 0x0480, 1, 1, False),   # [S]
                #     ],
                # },
                {
                    "icon": "mdi:snowflake-melt",
                    "poll": [
                        ("ALWAYS", "defrost_active", 0xB446, 1, 1, False),       # [A][S] air-source defrost
                    ],
                },
                {
                    "device_class": "running",
                    "icon": "mdi:pump",
                    "poll": [
                        ("FAST", "hk2_pump",             0x048E, 1, 1, False),   # [A][S]
                        ("FAST", "secondary_pump_relay", 0x0484, 1, 1, False),   # [S]
                        # 0x0496 dhw_loading_pump [S] did NOT respond on a real
                        # Vitocal 300-A - probe with 'read;0x0496;1' before
                        # re-enabling; or derive from dhw_pump_speed (0xB422).
                        # ("FAST", "dhw_loading_pump",   0x0496, 1, 1, False),   # [S]
                        ("FAST", "dhw_circulation_pump", 0x0490, 1, 1, False),   # [S]
                    ],
                },
                {
                    "device_class": "problem",
                    "entity_category": "diagnostic",
                    "icon": "mdi:alert-circle",
                    "poll": [
                        ("MEDIUM", "error", 0x0491, 1, 1, False),                # [S] common fault relay
                    ],
                },
            ],
        },

        # ======================================================================
        # Compressor phase (ViCare-style state)  [S]
        # 0=off, 1=preparing/start, 2=heating, 3=pause, 6=defrost
        # ======================================================================
        {
            "domain": "sensor",
            "icon": "mdi:state-machine",
            "value_template": "{% if value=='0' %}Off{% elif value=='1' %}Start"
                              "{% elif value=='2' %}Heating{% elif value=='3' %}Pause"
                              "{% elif value=='6' %}Defrost{% else %}{{ value|trim }}{% endif %}",
            "poll": [
                ("ALWAYS", "compressor_phase", 0x130B, 1, 1, False),
            ],
        },

        # ======================================================================
        # Operating modes (raw; the climate entity below decodes/writes HK2)
        # values: 0=off/standby, 2=auto(heating+DHW), 4=perm. reduced,
        #         5=perm. normal, 6=eco, 66=party 8h, 130=save -5K   [S]
        # ======================================================================
        {
            "domain": "sensor",
            "entity_category": "diagnostic",
            "icon": "mdi:cog",
            "poll": [
                ("FAST", "hk2_mode", 0xB001, 1, 1, False),
            ],
        },

        # ======================================================================
        # Writable setpoints (HA number entities)  [A][S]
        # ======================================================================
        {
            "domain": "number",
            "command_topic": "%mqtt_listen%",
            "command_template": "{{ \"w;%DpAddr%;%Length%;\"~(value*10)|int }}",
            "units": [
                {
                    "unit_of_measurement": "\u00b0C", "min": "10", "max": "30",
                    "step": "0.5", "mode": "slider", "icon": "mdi:thermometer",
                    "poll": [
                        ("MEDIUM", "hk2_normal_temperature",  0x3000, 2, 0.1, False),   # [A][S]
                        ("MEDIUM", "hk2_reduced_temperature", 0x3001, 2, 0.1, False),   # [A][S]
                        ("MEDIUM", "hk2_party_temperature",   0x3022, 2, 0.1, False),   # [A][S]
                    ],
                },
                {
                    "unit_of_measurement": "\u00b0C", "min": "30", "max": "60",
                    "step": "1", "icon": "mdi:water-thermometer",
                    "entity_category": "config",
                    "poll": [
                        ("MEDIUM", "dhw_normal_temperature", 0x6000, 2, 0.1, False),  # [A][S]
                        ("MEDIUM", "dhw_temperature_2",      0x600C, 2, 0.1, False),  # [A][S]
                    ],
                },
                {
                    "min": "-13", "max": "40", "step": "1",
                    "entity_category": "config", "icon": "mdi:plus-minus-variant",
                    "poll": [
                        ("SLOW", "hk2_heating_curve_level", 0x3006, 2, 0.1, True),   # [A][S]
                    ],
                },
                {
                    "min": "0", "max": "3.5", "step": "0.1",
                    "entity_category": "config", "icon": "mdi:slope-uphill",
                    "poll": [
                        ("SLOW", "hk2_heating_curve_inclination", 0x3007, 2, 0.1, True),  # [A][S]
                    ],
                },
            ],
        },

        # ======================================================================
        # Power  [A][S]
        # ======================================================================
        {
            "domain": "sensor",
            "unit_of_measurement": "W",
            "device_class": "power",
            "state_class": "measurement",
            "poll": [
                ("FAST", "thermal_power",    0x16A0, 4, 1, False),      # [A][S] WPR3_Heizleistung_1
                ("FAST", "electrical_power", 0x16A4, 4, 1, False),      # [A][S] WPR3_Leistungsaufnahme_1
                ("FAST", "eheater_power",    0x1909, 1, 3000, False),   # [A][S] booster stages 0/3/6/9 kW
            ],
        },

        # ======================================================================
        # Energy counters, split heating vs DHW  [A]; 0x1650 confirmed by openv
        # ======================================================================
        {
            "domain": "sensor",
            "unit_of_measurement": "kWh",
            "device_class": "energy",
            "state_class": "total_increasing",
            "suggested_display_precision": 1,
            "poll": [
                ("SLOW", "thermal_energy_heating",    0x1640, 4, 0.1, False),
                ("SLOW", "thermal_energy_dhw",        0x1650, 4, 0.1, False),
                ("SLOW", "electrical_energy_heating", 0x1660, 4, 0.1, False),
                ("SLOW", "electrical_energy_dhw",     0x1670, 4, 0.1, False),
            ],
        },

        # ======================================================================
        # Efficiency  [A][S]
        # ======================================================================
        {
            "domain": "sensor",
            "state_class": "measurement",
            "icon": "mdi:multiplication",
            "suggested_display_precision": 1,
            "poll": [
                ("FAST",   "cop",          0x1690, 1, 0.1, False),   # current COP
                ("HOURLY", "scop",         0x1680, 1, 0.1, False),   # seasonal (JAZ) total
                ("HOURLY", "scop_heating", 0x1681, 1, 0.1, False),
                ("HOURLY", "scop_dhw",     0x1682, 1, 0.1, False),
            ],
        },

        # ======================================================================
        # Runtimes & counters (diagnostic)  [A][S]
        # ======================================================================
        {
            "domain": "sensor",
            "entity_category": "diagnostic",
            "state_class": "total_increasing",
            "icon": "mdi:counter",
            "units": [
                {
                    "unit_of_measurement": "h",
                    "device_class": "duration",
                    "poll": [
                        ("SLOW", "compressor_runtime",     0x0580, 4, 2.7777778e-4, False),  # [A][S]
                        ("SLOW", "secondary_pump_runtime", 0x0584, 4, 2.7777778e-4, False),  # [A]
                        ("SLOW", "hk2_pump_runtime",       0x058E, 4, 2.7777778e-4, False),  # [A][S]
                        ("SLOW", "eheater_stage1_runtime", 0x0588, 4, 0.0008333, False),     # [S]
                        ("SLOW", "eheater_stage2_runtime", 0x0589, 4, 0.0016667, False),     # [S]
                    ],
                },
                {
                    "poll": [
                        ("SLOW", "compressor_starts", 0x0500, 4, 'b:0:1', 1, False),         # [A][S]
                    ],
                },
            ],
        },

        # ======================================================================
        # E-heater enable (HA switch, writes 0x7902)  [S]
        # ======================================================================
        {
            "domain": "switch",
            "command_topic": "%mqtt_listen%",
            "optimistic": False,
            "state_topic": "eheater_enabled",
            "payload_on": "w;0x7902;1;1",
            "payload_off": "w;0x7902;1;0",
            "state_on": "1",
            "state_off": "0",
            "icon": "mdi:heating-coil",
            "poll": [
                ("MEDIUM", "eheater_enabled", 0x7902, 1, 1, False),
            ],
        },

        # ======================================================================
        # One-time DHW charge (HA button, writes 0xB020 = 2)  [A][S]
        # ======================================================================
        {
            "domain": "button",
            "entity_name": "dhw_one_time_charge",
            "command_topic": "%mqtt_listen%",
            "payload_press": "w;0xB020;1;2",
            "icon": "mdi:shower-head",
        },

        # ======================================================================
        # DHW as HA water_heater entity  [S]
        # ======================================================================
        {
            "domain": "water_heater",
            "entity_name": "Warmwasser",
            "current_temperature_topic": "dhw_temperature",
            "temperature_state_topic": "dhw_normal_temperature",
            "temperature_command_topic": "%mqtt_listen%",
            "temperature_command_template":
                "{{ \"w;%dhw_normal_temperature:DpAddr%;%dhw_normal_temperature:Length%;\" ~ ((value|float*10)|int) }}",
            "min_temp": 30,
            "max_temp": 60,
        },

        # ======================================================================
        # Heating circuit as HA climate entity - HK2 variant  [S]
        # (For HK1: duplicate this block, replace 0xB001 -> 0xB000 and the
        #  hk2_* topics with hk1_*.)
        # ======================================================================
        {
            "domain": "climate",
            "entity_name": "HK2_Thermostat",
            "modes": ["off", "auto", "heat"],
            "mode_command_topic": "%mqtt_listen%",
            "mode_command_template":
                "{% if value==\"off\" %} w;0xB001;1;0 {% elif value==\"auto\" %} w;0xB001;1;2 "
                "{% elif value==\"heat\" %} w;0xB001;1;5 {% endif %}",
            "mode_state_topic": "hk2_mode",
            "mode_state_template":
                "{% if value==\"0\" %} off {% elif value==\"2\" %} auto "
                "{% elif value in [\"4\",\"5\",\"6\",\"66\",\"130\"] %} heat {% endif %}",
            "preset_modes": ["Normal", "Reduced", "Eco", "Party (8h)", "Save (-5K)"],
            "preset_mode_command_topic": "%mqtt_listen%",
            "preset_mode_command_template":
                "{% if value==\"Normal\" %} w;0xB001;1;5 {% elif value==\"Reduced\" %} w;0xB001;1;4 "
                "{% elif value==\"Eco\" %} w;0xB001;1;6 {% elif value==\"Party (8h)\" %} w;0xB001;1;66 "
                "{% elif value==\"Save (-5K)\" %} w;0xB001;1;130 {% endif %}",
            "preset_mode_state_topic": "hk2_mode",
            "preset_mode_value_template":
                "{% if value==\"5\" %} Normal {% elif value==\"4\" %} Reduced {% elif value==\"6\" %} Eco "
                "{% elif value==\"66\" %} Party (8h) {% elif value==\"130\" %} Save (-5K) "
                "{% elif value==\"2\" %} None {% endif %}",
            "current_temperature_topic": "hk2_supply_temperature",
            "temperature_state_topic": "hk2_normal_temperature",
            "temperature_command_topic": "%mqtt_listen%",
            "temperature_command_template":
                "{{ \"w;%hk2_normal_temperature:DpAddr%;%hk2_normal_temperature:Length%;\" ~ ((value|float*10)|int) }}",
            "precision": 0.1,
            "min_temp": 10,
            "max_temp": 30,
        },

        # ======================================================================
        # Diagnostics: fault message buffers (raw hex)  [S]
        # ======================================================================
        {
            "domain": "sensor",
            "entity_category": "diagnostic",
            "icon": "mdi:message-alert",
            "poll": [
                ("SLOW", "messages_heatpump",   0x0700, 32),
                ("SLOW", "messages_compressor", 0x0704, 32),
            ],
        },

        # ======================================================================
        # Ad-hoc command console entities  [S]
        # ======================================================================
        {
            "domain": "text",
            "entity_name": "cmnd",
            "command_topic": "%mqtt_listen%",
            "command_template": "{{ value }}",
            "entity_category": "config",
            "icon": "mdi:gesture-tap-button",
        },
        {
            "domain": "sensor",
            "entity_name": "resp",
            "entity_category": "diagnostic",
            "icon": "mdi:responsive",
        },
    ],
}
