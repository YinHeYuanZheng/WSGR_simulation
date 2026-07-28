# -*- coding:utf-8 -*-

from types import SimpleNamespace
import unittest
from unittest.mock import patch

import src.utils.envBuffUtil as env_buff_util
from src.utils.envBuffUtil import _build_environment_target


def ship(cid, country='X'):
    return SimpleNamespace(cid=cid, status={'country': country})


class EnvironmentTargetTest(unittest.TestCase):
    def test_short_cid_targets_friend_variants(self):
        target = _build_environment_target({
            'name': '指定舰船',
            'country': '',
            'shiptype': 'Cid(533)',
        })
        friend = [ship('10533'), ship('11533'), ship('10552')]
        enemy = [ship('10533')]

        self.assertEqual(
            [item.cid for item in target.get_target(friend, enemy)],
            ['10533', '11533'],
        )

    def test_cid_array_uses_equipment_expansion_rules(self):
        target = _build_environment_target({
            'name': '多舰增益',
            'country': '',
            'shiptype': 'Cid(["030","552"])',
        })
        friend = [
            ship('10030'), ship('11030'), ship('10552'), ship('11552'),
            ship('10533'),
        ]

        self.assertEqual(
            [item.cid for item in target.get_target(friend, [])],
            ['10030', '11030', '10552', '11552'],
        )

    def test_full_cid_is_used_directly(self):
        target = _build_environment_target({
            'name': '完整编号',
            'country': '',
            'shiptype': 'Cid(10552)',
        })

        self.assertEqual(
            [item.cid for item in target.get_target(
                [ship('10552'), ship('11552')], [],
            )],
            ['10552'],
        )

    def test_country_and_cid_are_both_required(self):
        target = _build_environment_target({
            'name': '国籍限定',
            'country': 'U',
            'shiptype': 'Cid(533)',
        })
        friend = [ship('10533', 'U'), ship('11533', 'C')]

        self.assertEqual(
            [item.cid for item in target.get_target(friend, [])],
            ['10533'],
        )

    def test_mixed_short_and_full_cid_is_rejected(self):
        with self.assertRaisesRegex(ValueError, '不能混用三位和五位'):
            _build_environment_target({
                'name': '错误编号',
                'country': '',
                'shiptype': 'Cid(["533","10552"])',
            })

    def test_malformed_cid_has_environment_context(self):
        with self.assertRaisesRegex(
            ValueError, '错误语法: 舰种列 Cid 语法错误'
        ):
            _build_environment_target({
                'name': '错误语法',
                'country': '',
                'shiptype': 'Cid[533]',
            })

    def test_reload_updates_in_place_and_preserves_additional_env(self):
        original_configured = env_buff_util._configured_env[:]
        original_env = env_buff_util.env[:]
        existing_reference = env_buff_util.env
        additional_skill = object()
        refreshed_skill = object()
        try:
            env_buff_util.env.append(additional_skill)
            with patch.object(
                env_buff_util,
                'load_env_buffs',
                return_value=[refreshed_skill],
            ):
                result = env_buff_util.reload_env_buffs()

            self.assertIs(result, existing_reference)
            self.assertEqual(result, [refreshed_skill, additional_skill])
        finally:
            env_buff_util._configured_env[:] = original_configured
            env_buff_util.env[:] = original_env


if __name__ == '__main__':
    unittest.main()
