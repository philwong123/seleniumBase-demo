#!/usr/bin/env python3

import pytest
import re
from guard.pages.timezone import TimezonePage


@pytest.mark.positive
def test_add_timezone(sb, timezone):
    TimezonePage.add_timezone_name(sb, timezone["name"])
    assert timezone["name"] in TimezonePage.assert_result_by_name(sb, timezone["name"])


@pytest.mark.positive
def test_add_timezone_section(sb, timezone_section):
    TimezonePage.add_timezone_section_by_timezone_name(sb, timezone_section["name"])
    result = TimezonePage.assert_timezone_section(sb)
    assert re.match(r'\d+:\d+-\d+:\d', result)


@pytest.mark.positive
def test_create_holidays(sb, holidays):
    TimezonePage.create_holidays(sb, "添加假期", holidays["name"], num=1)
    assert holidays["name"] in TimezonePage.assert_result_by_name(sb, holidays["name"])


@pytest.mark.positive
def test_create_workday(sb, workday):
    TimezonePage.create_workday(sb, "添加特殊工作日", workday["name"], num=1)
    assert workday["name"] in TimezonePage.assert_result_by_name(sb, workday["name"])


@pytest.mark.negative
def test_add_timezone_and_beyond(sb, negative_te):
    TimezonePage.add_timezone_name(sb, negative_te["name"])
    result = TimezonePage.judge_alert_info(sb)
    assert "请输入最多40个字符的时间条件名称" in result


@pytest.mark.negative
def test_add_holidays_negative_conflict(sb, negative_te):
    TimezonePage.create_holidays(sb, "添加假期", negative_te["name"])
    result = TimezonePage.judge_alert_info(sb)
    assert "创建的假期与已有的假期有冲突，请检查后重新设置" in result


@pytest.mark.negative
def test_add_workday_negative_conflict(sb, negative_te):
    TimezonePage.create_workday(sb, "添加特殊工作日", negative_te["name"])
    result = TimezonePage.judge_alert_info(sb)
    assert "创建的特殊工作日与已有的特殊工作日有冲突，请检查后重新设置" in result
