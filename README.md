# SonnenPyTask

Mock implementation and test suite for a Sonnen battery Device Under Test (DUT).

## Project Summary

This repository models a simplified solar energy system with:

- `DUT.py`: main device class that connects PV and consumption meters to a storage system.
- `devices/`: supporting component classes for meters, inverter, BMS, and storage.
- `tests/`: pytest-based tests validating power flow behavior across different system configurations.

The DUT uses the following design assumptions:

- Each battery module supports up to 2000 W charge/discharge power, by default, but it can be setted up with a different value inside each test setup.
- System configurations are based on module counts:
  - `basic` = 2 modules
  - `standard` = 3 modules
  - `pro` = 5 modules
- Inverter sign convention: `inverter.power_flow` is positive for discharge and negative for charge.
- Grid sign convention: `grid.power` is positive for import and negative for export.

## Repository Structure

- `DUT.py`: DUT wrapper exposing `get`, `set`, and `reset` methods.
- `devices/Meter.py`: generic meter class plus PV and consumption meter subclasses.
- `devices/Inverter.py`: inverter state with active power, battery voltage, and grid interface values.
- `devices/BMS.py`: battery management system state and active power tracking.
- `devices/StorageSys.py`: storage logic for calculating grid power and inverter/BMS responses.
- `tests/DUT_test.py`: parameterized DUT tests for system configs and storage behavior.
- `requirements.txt`: project dependency list.

## Setup

Recommended: create a virtual environment and install dependencies.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

Run the test suite with pytest:

```bash
python -m pytest tests/DUT_test.py -v
```

## Notes

- The repository currently contains a mock DUT implementation intended for testing charge/discharge logic and grid interaction rules.
- The `reset()` method restores meters and storage state to zero after test execution.
