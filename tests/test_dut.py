import pytest

from DUT import DUT
from devices.Meter import PV_Meter 
from devices.Meter import Consumption_Meter
from devices.StorageSys import StorageSystem
from devices.Inverter import Inverter
from devices.BMS import BMS


@pytest.fixture
def make_dut():
    dut = None

    def create(modules_num):
        nonlocal dut

        pv_meter = PV_Meter()
        consumption_meter = Consumption_Meter()
        inverter = Inverter()
        bms = BMS()
        storage_system = StorageSystem(inverter, bms, modules_num)

        dut = DUT(pv_meter, consumption_meter, storage_system)
        return dut

    yield create

    if dut is not None:
        dut.reset()
    

def _get_float(dut: DUT, key: str) -> float:
    return float(dut.get(key))


def test_dut_initial_state_for_basic_config(make_dut) -> None:
    dut = make_dut(1)
    # assert dut.get("system.setup") == "basic"

    assert _get_float(dut, "grid.power") == 0.0
    assert _get_float(dut, "inverter.active_power") == 0.0


def test_dut_charges_battery_from_surplus_without_grid_import_for_basic(make_dut) -> None:
    dut = make_dut(1)
    assert dut.set("pv.power", 3000.0) is True
    assert dut.set("consumption.power", 1000.0) is True

    assert _get_float(dut, "inverter.active_power") == -2000.0
    assert _get_float(dut, "grid.power") == 0.0


# def test_dut_exports_surplus_to_grid_when_battery_is_full_for_standard(make_dut) -> None:
#     dut = make_dut(3)
#     assert dut.get("system.setup") == "standard"

#     assert dut.set("pv.power", 5000.0) is True
#     assert dut.set("consumption.power", 1000.0) is True

#     assert _get_float(dut, "inverter.active_power") == -6000.0
#     assert _get_float(dut, "grid.power") == -2000.0


def test_dut_discharges_battery_to_cover_deficit_without_grid_import_for_standard(make_dut) -> None:
    dut = make_dut(3)
    # assert dut.get("system.setup") == "standard"
    assert dut.set("pv.power", 1000.0) is True
    assert dut.set("consumption.power", 6000.0) is True

    assert _get_float(dut, "inverter.active_power") == 5000.0
    assert _get_float(dut, "grid.power") == 0.0
    # assert bms active power (single module) = 5000.0/3


def test_dut_imports_grid_power_when_deficit_exceeds_battery_capacity_for_pro(make_dut) -> None:
    dut = make_dut(5)
    # assert dut.get("system.setup") == "pro"
    assert dut.set("pv.power", 500.0) is True
    assert dut.set("consumption.power", 10000.0) is True

    assert _get_float(dut, "inverter.active_power") == 9000.0
    assert _get_float(dut, "grid.power") == 500.0


# def test_dut_updates_module_count_when_config_changes(make_dut) -> None:
#     dut = make_dut(1)
#     assert dut.set("system.config", "standard") is True
#     assert dut.get("system.config") == "standard"
#     assert dut.get("system.modules") == "3"


# def test_dut_rejects_invalid_config_and_grid_writes(make_dut) -> None:
#     dut = make_dut(1)
#     assert dut.set("system.config", "enterprise") is False
#     assert dut.get("system.modules") == "1"

#     assert dut.set("grid.power", 42.0) is False
#     assert _get_float(dut, "grid.power") == 0.0


# def test_dut_reset_restores_initial_state(make_dut) -> None:
#     dut = make_dut(1)
#     dut.set("pv.power", 2500.0)
#     dut.set("consumption.power", 1000.0)
#     dut.set("system.config", "standard")

#     dut.reset()

#     assert dut.get("system.config") == "basic"
#     assert dut.get("system.modules") == "1"
#     assert _get_float(dut, "grid.power") == 0.0
#     assert _get_float(dut, "inverter.active_power") == 0.0
