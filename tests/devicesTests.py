"""
Unit tests for the individual device mocks in devices.py, in isolation
from the energy-management algorithm. These validate that each mini-mock
faithfully exposes the parameters listed for that component in the task
doc, and rejects anything it shouldn't know about.
"""
 
import pytest
 
from devices.PVmock import PV
from devices.Consumptionmock import Consumption
from devices.StorageSysmock import StorageSystem
from devices.Invertermock import Inverter
from devices.BMSmock import BMS
 
# ---------------------------------------------------------------------------
# Production / Consumption meters
# ---------------------------------------------------------------------------
 
def test_production_meter_defaults():
    meter = PV()
    assert meter.get("power") == 0.0
    assert meter.get("voltage") == 220.0
    assert meter.get("current") == 0.0
    assert meter.get("frequency") == 50.0
 
 
def test_production_meter_set_and_get_power():
    meter = PV()
    assert meter.set("power", 4200) is True
    assert meter.get("power") == 4200
 
 
def test_production_meter_rejects_unknown_param():
    meter = PV()
    with pytest.raises(KeyError):
        meter.set("bogus", 1)
 
 
def test_consumption_meter_defaults():
    meter = Consumption()
    assert meter.get("power") == 0.0
    assert meter.get("voltage") == 220.0
    assert meter.get("frequency") == 50.0
    assert meter.get("current") == 0.0
 
 
# ---------------------------------------------------------------------------
# Inverter
# ---------------------------------------------------------------------------
 
def test_inverter_defaults():
    inverter = Inverter(modules=2, module_power_w=2000)
    assert inverter.get("power_flow") == 0.0
    assert inverter.get("battery_voltage") == 48.0
    assert inverter.get("battery_current") == 0.0
    assert inverter.get("grid_frequency") == 50.0
    assert inverter.get("grid_voltage") == 220.0
 
 
def test_inverter_max_power_scales_with_module_count():
    inverter = Inverter(modules=3, module_power_w=2000)
    assert inverter.get("max_power") == 6000
 
    inverter.modules = 5
    assert inverter.get("max_power") == 10000
 
 
def test_inverter_max_power_is_read_only():
    inverter = Inverter(modules=1)
    assert inverter.set("max_power", 999) is False
    # value is unaffected by the rejected write
    assert inverter.get("max_power") == 2000
 
 
def test_inverter_power_flow_sign_convention_is_settable():
    inverter = Inverter(modules=1)
    inverter.set("power_flow", -1500)  # charging
    assert inverter.get("power_flow") == -1500
    inverter.set("power_flow", 800)  # discharging
    assert inverter.get("power_flow") == 800
 
 
# ---------------------------------------------------------------------------
# BMS (all battery modules assumed identical)
# ---------------------------------------------------------------------------
 
def test_bms_defaults():
    bms = BMS(num_modules=3, module_power_w=2000)
    assert bms.get("temp") == 25.0
    assert bms.get("voltage") == 48.0
    assert bms.get("current") == 0.0
    assert bms.get("soc") == 60.0
 
 
def test_bms_set_and_get_reading():
    bms = BMS(num_modules=2)
    assert bms.set("soc", 87.5) is True
    assert bms.get("soc") == 87.5
 
 
def test_bms_max_power_scales_with_module_count():
    bms = BMS(num_modules=4, module_power_w=2000)
    assert bms.get("max_power") == 8000
 
 
def test_bms_num_modules_and_max_power_are_read_only():
    bms = BMS(num_modules=3, module_power_w=2000)
    assert bms.set("num_modules", 99) is False
    assert bms.set("max_power", 99) is False
    # values unaffected by the rejected writes
    assert bms.get("num_modules") == 3
    assert bms.get("max_power") == 6000
 
 
def test_bms_rejects_unknown_param():
    bms = BMS(num_modules=1)
    with pytest.raises(KeyError):
        bms.set("bogus", 1)
 
 
# ---------------------------------------------------------------------------
# Storage system
# ---------------------------------------------------------------------------
 
def test_storage_system_power_command_default_and_set():
    inverter = Inverter(modules=1)
    bms = BMS(num_modules=1)
    storage = StorageSystem(inverter, bms)
 
    assert storage.get("storage_power_command") == 0.0
    assert storage.set("storage_power_command", -1200) is True  # charge command
    assert storage.get("storage_power_command") == -1200.0
 
 
def test_storage_system_rejects_unknown_param():
    storage = StorageSystem(Inverter(modules=1), BMS(num_modules=1))
    assert storage.set("bogus", 1) is False
    with pytest.raises(KeyError):
        storage.get("bogus")