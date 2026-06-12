# -*- coding:utf-8 -*-
# Author:银河远征(Agent supported)
# env:py38

import unittest

from src.utils.parseEquipSkill import (
    Condition,
    GroupEntry,
    PythonEntry,
    load_equip_config,
    parse_equip_config,
)
from src.wsgr.phase import AllPhase, AirPhase
from src.wsgr.ship import BM, Ship
from src.wsgr.wsgrTimer import timer


class EquipConfigParserTest(unittest.TestCase):
    def test_effect_and_phase(self):
        entries = parse_equip_config(
            'pierce_coef:0.1;hit_rate:0.05,AirPhase'
        )
        self.assertEqual(entries[0].name, 'pierce_coef')
        self.assertEqual(entries[0].value, 0.1)
        self.assertIsNone(entries[0].phase)
        self.assertEqual(entries[1].phase, 'AirPhase')

    def test_nested_wrappers(self):
        entries = parse_equip_config(
            'Country(C,ShipType(CLT,{crit:0.1;miss_rate:0.05}))'
        )
        self.assertEqual(len(entries), 1)
        self.assertIsInstance(entries[0], GroupEntry)
        self.assertEqual(
            entries[0].entries[0].conditions,
            (Condition('Country', 'C'), Condition('ShipType', 'CLT'))
        )

    def test_side_and_python_directive(self):
        entries = parse_equip_config(
            'Cid(552,Side(0,{hit_rate:-0.05,AirPhase}));@013:0.1'
        )
        self.assertEqual(entries[0].side, 0)
        self.assertIsInstance(entries[1], PythonEntry)
        self.assertEqual(entries[1].values, (0.1,))

    def test_wrapper_can_wrap_single_python_directive(self):
        entries = parse_equip_config('Cid(552,{@013:0.1})')

        self.assertIsInstance(entries[0], PythonEntry)
        self.assertEqual(
            entries[0].conditions,
            (Condition('Cid', ['10552', '11552']),)
        )

    def test_ungrouped_effects_create_separate_skills(self):
        skills = load_equip_config(
            'air_atk_buff:0.05;hit_rate:0.05,ShellingPhase',
            eid='10619'
        )
        master = self.make_master()

        self.assertEqual(len(skills), 2)
        self.assertEqual(len(skills[0](master.timer, master, '').buff), 1)
        self.assertEqual(len(skills[1](master.timer, master, '').buff), 1)

    def test_braced_effects_create_one_skill(self):
        skills = load_equip_config(
            '{air_atk_buff:0.05;hit_rate:0.05,ShellingPhase}',
            eid='10619'
        )
        master = self.make_master()
        buffs = skills[0](master.timer, master, '').buff

        self.assertEqual(len(skills), 1)
        self.assertEqual(
            [(buff.name, str(buff.effect_type)) for buff in buffs],
            [('air_atk_buff', '10619.001'), ('hit_rate', '10619.002')]
        )

    def test_braced_effects_under_wrapper_create_one_skill(self):
        skills = load_equip_config(
            'Country(C,{crit:0.1;miss_rate:0.05})',
            eid='10619'
        )
        master = self.make_master(country='C')

        self.assertEqual(len(skills), 1)
        self.assertEqual(len(skills[0](master.timer, master, '').buff), 2)

    def test_stack_can_participate_in_braced_effect_group(self):
        skills = load_equip_config(
            'ShipType(BM,{pierce_coef:0.1,stack;miss_rate:0.1})',
            eid='10605'
        )
        master = self.make_master(ship_class=BM)
        buffs = skills[0](master.timer, master, '').buff

        self.assertEqual(len(skills), 1)
        self.assertEqual([buff.name for buff in buffs], ['pierce_coef', 'miss_rate'])
        self.assertNotEqual(buffs[0].effect_type, 3)

    def test_braces_cannot_mix_effect_and_context_wrapper(self):
        with self.assertRaisesRegex(ValueError, '不可同时包裹普通词条和包装器'):
            parse_equip_config(
                '{Cid(533,{crit:0.1});miss_rate:0.1}'
            )

    def test_top_level_braces_require_multiple_effects(self):
        with self.assertRaisesRegex(ValueError, '两个或更多普通词条'):
            parse_equip_config('{crit:0.1}')

    def test_short_cid_expands_friend_variants(self):
        entries = parse_equip_config('Cid(["030","552"],{crit:0.1})')
        self.assertEqual(
            entries[0].conditions,
            (Condition('Cid', ['10030', '11030', '10552', '11552']),)
        )

    def test_full_cid_is_used_directly(self):
        friend = parse_equip_config('Cid(10552,{crit:0.1})')
        enemy = parse_equip_config('Cid("00048",{crit:0.1})')
        self.assertEqual(friend[0].conditions, (Condition('Cid', ['10552']),))
        self.assertEqual(enemy[0].conditions, (Condition('Cid', ['00048']),))

    def test_short_and_full_cid_cannot_be_mixed(self):
        with self.assertRaisesRegex(ValueError, '不能混用三位和五位'):
            parse_equip_config('Cid(["552","10552"],{crit:0.1})')

    def test_unknown_effect_rejected(self):
        with self.assertRaisesRegex(ValueError, '未知装备特效词条'):
            parse_equip_config('unknown_effect:0.1')

    def test_load_error_identifies_equipment_and_config(self):
        with self.assertRaises(ValueError) as context:
            load_equip_config('unknown_effect:0.1', eid='10999')
        self.assertIn('装备 10999 的特效配置错误', str(context.exception))
        self.assertIn('配置内容: unknown_effect:0.1', str(context.exception))

    def test_unknown_phase_is_validated_during_load(self):
        with self.assertRaisesRegex(
            ValueError,
            '装备 10999 的特效配置错误: 未知装备特效阶段: UnknownPhase'
        ):
            load_equip_config('crit:0.1,UnknownPhase', eid='10999')

    def test_unknown_ship_type_is_validated_during_load(self):
        with self.assertRaisesRegex(
            ValueError,
            '装备 10999 的特效配置错误: 未知舰种: UnknownType'
        ):
            load_equip_config(
                'ShipType(UnknownType,{crit:0.1})',
                eid='10999'
            )

    def test_python_directive_init_error_identifies_equipment(self):
        skill_class = load_equip_config('@013', eid='10999')[0]
        master = self.make_master()

        with self.assertRaisesRegex(
            ValueError,
            '装备 10999 的特效配置错误'
        ):
            skill_class(master.timer, master, '')

    def test_stack_parameter_under_wrapper(self):
        entries = parse_equip_config(
            'Cid(533,{pierce_coef:0.05,stack})'
        )
        self.assertEqual(
            entries[0].conditions,
            (Condition('Cid', ['10533', '11533']),)
        )
        self.assertTrue(entries[0].stackable)

    def test_wrapper_around_bare_effect_requires_braces(self):
        with self.assertRaisesRegex(ValueError, '普通词条时必须使用大括号'):
            parse_equip_config('Cid(533,pierce_coef:0.05)')

    def test_stack_parameter_makes_unique_effect_stackable(self):
        normal = load_equip_config('pierce_coef:0.1')[0]
        stronger = load_equip_config('pierce_coef:0.2')[0]
        stackable = load_equip_config('pierce_coef:0.05,stack')[0]
        stackable_2 = load_equip_config('pierce_coef:0.1,stack')[0]
        stackable_uplimit = load_equip_config(
            'uplimit_buff:0.1,stack'
        )[0]
        master = self.make_master()
        stack_master = self.make_master()

        normal_buff = normal(master.timer, master, '').buff[0]
        stronger_buff = stronger(master.timer, master, '').buff[0]
        stackable_buff = stackable(master.timer, master, '').buff[0]
        stackable_buff_2 = stackable_2(
            stack_master.timer, stack_master, ''
        ).buff[0]
        stackable_uplimit_buff = stackable_uplimit(
            stack_master.timer, stack_master, ''
        ).buff[0]

        self.assertEqual(normal_buff.effect_type, 3)
        self.assertNotIn(stackable_buff.effect_type, [3, 4])
        self.assertNotIn(stackable_uplimit_buff.effect_type, [3, 4])
        master.add_buff(normal_buff)
        master.add_buff(stronger_buff)
        stack_master.add_buff(stackable_buff)
        stack_master.add_buff(stackable_buff_2)
        self.assertEqual(
            [buff.value for buff in master.temper_buff
             if buff.name == 'pierce_coef'],
            [0.2]
        )
        self.assertEqual(
            sorted(buff.value for buff in stack_master.temper_buff
                   if buff.name == 'pierce_coef'),
            [0.05, 0.1]
        )

    def test_stack_parameter_has_no_effect_on_normal_effects(self):
        normal = load_equip_config('crit:0.1', eid='10619')[0]
        stackable = load_equip_config('crit:0.1,stack', eid='10619')[0]
        master = self.make_master()

        normal_buff = normal(master.timer, master, '').buff[0]
        stackable_buff = stackable(master.timer, master, '').buff[0]

        self.assertEqual(normal_buff.effect_type, stackable_buff.effect_type)
        self.assertEqual(normal_buff.value, stackable_buff.value)

    def test_stack_parameter_must_precede_phase(self):
        with self.assertRaisesRegex(ValueError, '第二个参数必须为 stack'):
            parse_equip_config('pierce_coef:0.1,ShellingPhase,stack')

    def test_stack_parameter_supports_phase(self):
        entry = parse_equip_config(
            'pierce_coef:0.1,stack,ShellingPhase'
        )[0]
        self.assertTrue(entry.stackable)
        self.assertEqual(entry.phase, 'ShellingPhase')

    def test_dynamic_effect_type_identifies_eid_and_entry(self):
        skills = load_equip_config(
            'crit:0.1;pierce_coef:0.05,stack',
            eid='10612'
        )
        master = self.make_master()
        crit_buff = skills[0](master.timer, master, '').buff[0]
        pierce_buff = skills[1](master.timer, master, '').buff[0]

        self.assertEqual(str(crit_buff.effect_type), '10612.001')
        self.assertEqual(str(pierce_buff.effect_type), '10612.002')
        self.assertIn('装备特效10612.002', repr(pierce_buff))
        self.assertGreater(pierce_buff.effect_type, 4)

    def test_condition_wrapper_controls_effect(self):
        skill_class = load_equip_config(
            'Country(C,{final_damage_buff:0.1})'
        )[0]
        master = self.make_master(country='C')
        skill = skill_class(master.timer, master, '')
        self.assertEqual(skill.buff[0].name, 'final_damage_buff')
        self.assertEqual(skill.buff[0].value, 0.1)
        self.assertIs(skill.buff[0].phase, AllPhase)

        master.status['country'] = 'S'
        self.assertEqual(skill_class(master.timer, master, '').buff, [])

    def test_side_wrapper_changes_target(self):
        skill_class = load_equip_config(
            'Side(0,{hit_rate:-0.05,AirPhase})'
        )[0]
        master = self.make_master()
        skill = skill_class(master.timer, master, '')
        self.assertEqual(skill.target.side, 0)
        self.assertIs(skill.buff[0].phase, AirPhase)

    def test_python_directive_uses_configured_values(self):
        skill_class = load_equip_config('@002:0.05')[0]
        master = self.make_master()
        skill = skill_class(master.timer, master, '')
        self.assertEqual(skill.buff[0].effect_type, 2)
        self.assertEqual(skill.buff[0].value, 0.05)

    @staticmethod
    def make_master(country='X', ship_class=Ship):
        battle_timer = timer()
        master = ship_class(battle_timer)
        master.set_cid('99999')
        master.set_status(status={
            'name': 'test',
            'country': country,
            'tag': 'none',
        })
        return master


if __name__ == '__main__':
    unittest.main()
