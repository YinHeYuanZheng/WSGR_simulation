# WSGR WebUI

The browser interface is a first-class application entry point.  UI assets live
under `src/webui/static`, while `src/webui/service.py` adapts the existing
dataset/configuration loaders and battle engine into JSON-friendly operations.
Battle rules remain in `src/wsgr` and `src/utils`.

## Run

From the project root:

```bash
python webui.py
```

Then open `http://127.0.0.1:8765`.  To open the default browser automatically:

```bash
python webui.py --open
```

The server listens on the loopback interface by default, so it is not exposed
to other devices on the network.

## Structure

```text
WSGR/
├── main.py                 # command-line simulation entry
├── webui.py                # browser UI and local API server entry
└── src/
    ├── wsgr/               # domain model and battle rules
    ├── utils/
    │   └── gui.py          # legacy Tkinter entry during migration
    └── webui/
        ├── service.py      # dataset/config/simulation adapter
        └── static/         # HTML, CSS, JavaScript, fonts and images
```

The WebUI currently supports real database-backed fleet editing, YAML/XML
configuration import, YAML export, actual start/stop simulation control, and
result aggregation for all four analysis tabs.

