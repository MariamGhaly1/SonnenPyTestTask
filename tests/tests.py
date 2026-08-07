import pytest

from DUTmock import DUT


@pytest.fixture(autouse=True)
def dut() -> DUT:
    device = DUT()
    yield device
    device.reset()


def test_surplus_below_max_charge_rate_charges_without_grid_exchange(dut: DUT) -> None:
    assert dut.set("pv.power", 1500.0) is True
    assert dut.set("consumption.power", 500.0) is True

    assert float(dut.get("inverter.power_flow")) == -1000.0
    assert float(dut.get("grid.power")) == 0.0


def test_surplus_above_max_charge_rate_exports_remainder_to_grid(dut: DUT) -> None:
    assert dut.set("pv.power", 5000.0) is True
    assert dut.set("consumption.power", 1000.0) is True

    assert float(dut.get("inverter.power_flow")) == -2000.0
    assert float(dut.get("grid.power")) == -2000.0


def test_deficit_below_max_discharge_rate_discharges_without_grid_import(dut: DUT) -> None:
    assert dut.set("pv.power", 1000.0) is True
    assert dut.set("consumption.power", 3000.0) is True

    assert float(dut.get("inverter.power_flow")) == 2000.0
    assert float(dut.get("grid.power")) == 0.0


def test_deficit_above_max_discharge_rate_imports_remainder_from_grid(dut: DUT) -> None:
    assert dut.set("pv.power", 500.0) is True
    assert dut.set("consumption.power", 3000.0) is True

    assert float(dut.get("inverter.power_flow")) == 2000.0
    assert float(dut.get("grid.power")) == 500.0


def test_balanced_pv_and_consumption_leaves_system_idle(dut: DUT) -> None:
    assert dut.set("pv.power", 2000.0) is True
    assert dut.set("consumption.power", 2000.0) is True

    assert float(dut.get("inverter.power_flow")) == 0.0
    assert float(dut.get("grid.power")) == 0.0
