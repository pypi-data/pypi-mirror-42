#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  htheatpump - Serial communication module for Heliotherm heat pumps
#  Copyright (C) 2019  Daniel Strigl

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Tests for code in `htheatpump.htparams`. """

import pytest
import re
from htheatpump.htparams import HtDataTypes, HtParam, HtParams
from htheatpump.htheatpump import HtHeatpump


class TestHtDataTypes:
    @pytest.mark.parametrize("str", [
        # -- should raise a 'ValueError':
        "none", "NONE",
        "string", "String",
        "bool", "Bool", "boolean", "Boolean", "BOOLEAN",
        "int", "Int", "integer", "Integer", "INTEGER",
        "float", "Float",
        "123456", "ÄbcDef", "äbcdef", "ab&def", "@bcdef", "aBcde$", "WzßrÖt",
        # ...
    ])
    def test_from_str_raises_ValueError(self, str):
        with pytest.raises(ValueError):
            HtDataTypes.from_str(str)
        #assert 0

    def test_from_str(self):
        assert HtDataTypes.from_str("None") is None
        assert HtDataTypes.from_str("STRING") == HtDataTypes.STRING
        assert HtDataTypes.from_str("BOOL") == HtDataTypes.BOOL
        assert HtDataTypes.from_str("INT") == HtDataTypes.INT
        assert HtDataTypes.from_str("FLOAT") == HtDataTypes.FLOAT
        #assert 0


class TestHtParam:
    @pytest.mark.parametrize("str, data_type, exp_value", [
        ("TestString", HtDataTypes.STRING, "TestString"),
        ("0", HtDataTypes.BOOL, False),
        ("1", HtDataTypes.BOOL, True),
        ("123", HtDataTypes.INT, 123),
        ("-321", HtDataTypes.INT, -321),
        ("123.456", HtDataTypes.FLOAT, 123.456),
        ("-321.456", HtDataTypes.FLOAT, -321.456),
        # -- should raise a 'ValueError':
        ("True", HtDataTypes.BOOL, None),
        ("False", HtDataTypes.BOOL, None),
        ("true", HtDataTypes.BOOL, None),
        ("false", HtDataTypes.BOOL, None),
        ("yes", HtDataTypes.BOOL, None),
        ("no", HtDataTypes.BOOL, None),
        ("y", HtDataTypes.BOOL, None),
        ("n", HtDataTypes.BOOL, None),
        ("TRUE", HtDataTypes.BOOL, None),
        ("FALSE", HtDataTypes.BOOL, None),
        ("YES", HtDataTypes.BOOL, None),
        ("NO", HtDataTypes.BOOL, None),
        ("Y", HtDataTypes.BOOL, None),
        ("N", HtDataTypes.BOOL, None),
        ("abc", HtDataTypes.BOOL, None),
        ("def", HtDataTypes.INT, None),
        ("--99", HtDataTypes.INT, None),
        ("12+55", HtDataTypes.INT, None),
        ("ghi", HtDataTypes.FLOAT, None),
        ("--99.0", HtDataTypes.FLOAT, None),
        ("12.3+55.9", HtDataTypes.FLOAT, None),
        ("789", HtDataTypes.FLOAT, None),
        # ...
    ])
    def test_from_str(self, str, data_type, exp_value):
        if exp_value is None:
            with pytest.raises(ValueError):
                HtParam.from_str(str, data_type)
        else:
            assert HtParam.from_str(str, data_type) == exp_value
        #assert 0

    @pytest.mark.parametrize("val, data_type, exp_str", [
        ("TestString", HtDataTypes.STRING, "TestString"),
        (False, HtDataTypes.BOOL, "0"),
        (True, HtDataTypes.BOOL, "1"),
        (123, HtDataTypes.INT, "123"),
        (-321, HtDataTypes.INT, "-321"),
        (123.456, HtDataTypes.FLOAT, "123.456"),
        (-321.456, HtDataTypes.FLOAT, "-321.456"),
        (789, HtDataTypes.FLOAT, "789.0"),
        (-789, HtDataTypes.FLOAT, "-789.0"),
        (789.0, HtDataTypes.FLOAT, "789.0"),
        (-789.0, HtDataTypes.FLOAT, "-789.0"),
        # ... add some more samples here!
    ])
    def test_to_str(self, val, data_type, exp_str):
        assert HtParam.to_str(val, data_type) == exp_str
        #assert 0

    @pytest.mark.parametrize("name, cmd", [(name, param.cmd()) for name, param in HtParams.items()])
    def test_cmd_format(self, name, cmd):
        m = re.match(r"^[S|M]P,NR=(\d+)$", cmd)
        assert m is not None, "non valid command string for parameter {!r} [{!r}]".format(name, cmd)
        #assert 0


@pytest.fixture(scope="class")
def hthp(cmdopt_device, cmdopt_baudrate):
    hthp = HtHeatpump(device=cmdopt_device, baudrate=cmdopt_baudrate)
    try:
        hthp.open_connection()
        yield hthp  # provide the heat pump instance
    finally:
        hthp.close_connection()


@pytest.fixture()
def reconnect(hthp):
    hthp.reconnect()
    hthp.login()
    yield
    hthp.logout()


class TestHtParams:
    @pytest.mark.parametrize("name, acl", [(name, param.acl) for name, param in HtParams.items()])
    def test_acl(self, name, acl):
        assert acl is not None, "'acl' must not be None"
        m = re.match(r"^(r-|-w|rw)$", acl)
        assert m is not None, "invalid acl definition for parameter {!r} [{!r}]".format(name, acl)
        #assert 0

    @pytest.mark.parametrize("name, min_val, max_val", [(name, param.min_val, param.max_val)
                                                        for name, param in HtParams.items()])
    def test_limits(self, name, min_val, max_val):
        assert min_val is not None, "minimal value for parameter {!r} must not be None".format(name)
        assert max_val is not None, "maximal value for parameter {!r} must not be None".format(name)
        assert min_val <= max_val
        assert max_val >= min_val
        #assert 0

    @pytest.mark.run_if_connected
    @pytest.mark.usefixtures("reconnect")
    @pytest.mark.parametrize("name, param", HtParams.items())
    def test_validate_param(self, hthp, name, param):
        hthp.send_request(param.cmd())
        resp = hthp.read_response()
        m = re.match(r"^{},.*NAME=([^,]+).*VAL=([^,]+).*MAX=([^,]+).*MIN=([^,]+).*$".format(param.cmd()), resp)
        assert m is not None, "invalid response for query of parameter {!r} [{!r}]".format(name, resp)
        dp_name = m.group(1).strip()
        assert dp_name == name,\
            "data point name doesn't match with the parameter name {!r} [{!r}]".format(name, dp_name)
        dp_value = param.from_str(m.group(2))
        assert dp_value is not None, "data point value must not be None [{}]".format(dp_value)
        dp_max = param.from_str(m.group(3))
        assert dp_max == param.max_val,\
            "data point max value doesn't match with the parameter's one {!s} [{!s}]".format(param.max_val, dp_max)
        dp_min = param.from_str(m.group(4))
        assert dp_min == param.min_val,\
            "data point min value doesn't match with the parameter's one {!s} [{!s}]".format(param.min_val, dp_min)
        #assert 0


# TODO: add some more tests here
