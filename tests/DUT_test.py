import pytest

from DUT import DUT
from devices.Meter import PV_Meter 
from devices.Meter import Consumption_Meter
from devices.StorageSys import StorageSystem
from devices.Inverter import Inverter
from devices.BMS import BMS


##----------assumptions----------

MODULE_MAX_POWER : float = 2000.0
INVERTER_MAX_POWER: float = 9000.0


@pytest.fixture
def make_dut():
    dut = None

    def create(modules_num, module_max_power, inverter_max_power):
        nonlocal dut

        pv_meter = PV_Meter()
        consumption_meter = Consumption_Meter()
        inverter = Inverter(inverter_max_power)
        bms = BMS(module_max_power)
        storage_system = StorageSystem(inverter, bms, modules_num)

        dut = DUT(pv_meter, consumption_meter, storage_system)
        return dut

    yield create

    if dut is not None:
        dut.reset()


CONFIG_MODULES = [
    ("basic", 2),
    ("standard", 3),
    ("pro", 5),
]


@pytest.fixture(params=CONFIG_MODULES)
def system_config(request):
    return request.param


def test_surplus_below_max_charge_rate_charges_without_grid_exchange(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)

    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 1500.0) is True
    assert dut.set("consumption.power", 500.0) is True

    assert float(dut.get("inverter.active_power")) == -1000.0
    assert float(dut.get("grid.power")) == 0.0



def test_surplus_above_max_charge_rate_exports_remainder_to_grid(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)

    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 15000.0) is True
    assert dut.set("consumption.power", 1000.0) is True

    assert float(dut.get("inverter.active_power")) == -min(14000.0, 2000.0 * modules)
    assert float(dut.get("grid.power")) == -(14000.0 - min(14000.0, 2000.0 * modules))


def test_deficit_below_max_discharge_rate_discharges_without_grid_import(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)
    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 1000.0) is True
    assert dut.set("consumption.power", 3000.0) is True

    assert float(dut.get("inverter.active_power")) == 2000.0
    assert float(dut.get("grid.power")) == 0.0



def test_deficit_above_max_discharge_rate_imports_remainder_from_grid(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)
    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 500.0) is True
    assert dut.set("consumption.power", 15000.0) is True

    expected_discharge = min(14500.0, 2000.0 * modules)
    expected_grid = 14500.0 - expected_discharge

    assert float(dut.get("inverter.active_power")) == expected_discharge
    assert float(dut.get("grid.power")) == expected_grid



def test_balanced_pv_and_consumption_leaves_system_idle(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)

    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 2000.0) is True
    assert dut.set("consumption.power", 2000.0) is True

    assert float(dut.get("inverter.active_power")) == 0.0
    assert float(dut.get("grid.power")) == 0.0



def test_power_command_discharging_to_grid_when_balanced_consumption(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)
    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 2000.0) is True
    assert dut.set("consumption.power", 2000.0) is True
    assert dut.set("storage.power_command", 1200.0) is True

    assert float(dut.get("grid.power")) == -1200.0


def test_power_command_discharging_to_grid_plus_surplus(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)
    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 4000.0) is True
    assert dut.set("consumption.power", 1000.0) is True
    assert dut.set("storage.power_command", 1200.0) is True

    expected_grid = -(3000.0 + 1200.0)
    assert float(dut.get("grid.power")) == expected_grid



def test_power_command_charging_from_grid_when_balanced_consumption(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)
    
    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 2000.0) is True
    assert dut.set("consumption.power", 2000.0) is True
    assert dut.set("storage.power_command", -1200.0) is True

    assert float(dut.get("grid.power")) == 1200.0
    


def test_power_command_charging_from_grid_and_surplus_when_surplus_is_low(make_dut, system_config) -> None:
    config, modules = system_config
    dut = make_dut(modules, MODULE_MAX_POWER, INVERTER_MAX_POWER)
    assert dut.get("system.setup") == config

    assert dut.set("pv.power", 1500.0) is True
    assert dut.set("consumption.power", 1000.0) is True
    assert dut.set("storage.power_command", -1200.0) is True

    assert float(dut.get("grid.power")) == 700.0








