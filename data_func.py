import os
import sqlite3
import sys
from decimal import Decimal, ROUND_HALF_UP

attribute_list = ['星', '兽', '岩', '木', '灵', '智']
character_list_x = ['37', '红弩箭', '牙仙', '远旅', '星锑', '金蜜儿', '玛蒂尔达', '夏利', '婴儿蓝', '埃里克', 'TTT',
                    'APPLe', '雾行者', '斯普特尼克', '星之眼', '弄臣']
character_list_s = ['梅兰妮', '百夫长', '鬃毛沙砾', '兔毛手袋', '百夫长', '坦南特', '帕米埃', '玛丽莲', '狼群',
                    '芭妮芭妮', '尼克·波顿', '哒哒达利', '莉拉妮']
character_list_y = ['伽菈波那', '皮克勒斯', '新巴别塔', '温妮弗雷德', '恐怖通', '讣告人', '气球派对', '十四行诗',
                    '莫桑女士', '铅玻璃', '红斗篷', '洋葱头', '贝蒂']
character_list_m = ['洁西卡', '泥鯭的士', '苏芙比', '槲寄生', '坎吉拉', '挖掘艺术', '五色月', '柏林以东', '爱宠', '冬',
                    '小春雀儿', '拉拉泉']
character_list_l = ['未锈铠', '喀嚓喀嚓', '吵闹鬼', '丽莎&路易斯', '无线电小姐']
character_list_z = ['6', 'X', '小梅斯梅尔', '约翰·提托', '门']
character_list = [character_list_x, character_list_s, character_list_y, character_list_m, character_list_l,
                  character_list_z]

resonate_list = {1: 5, 2: 10, 3: 15}
dic_resonate = {
    '大Z形': ['远旅', '6', '槲寄生', '苏芙比', '梅兰妮', '鬃毛沙砾', '温妮弗雷德', '皮克勒斯', '伽菈波那', '未锈铠',
              'X', '柏林以东', '挖掘艺术', '坎吉拉', '帕米埃', '恐怖通', '喀嚓喀嚓', '雾行者', 'TTT', '埃里克',
              '芭妮芭妮', '红斗篷', '莫桑女士', '小梅斯梅尔', '莉拉妮', '贝蒂', '约翰·提托', '门'],
    '大T形': ['星锑', '泥鯭的士', '洁西卡', '夏利', '讣告人', 'APPLe', '冬', '爱宠', '狼群', '拉拉泉'],
    '大U形': ['兔毛手袋', '新巴别塔', '婴儿蓝', '十四行诗', '气球派对', '尼克·波顿', '铅玻璃', '吵闹鬼', '弄臣',
              '星之眼', '丽莎&路易斯', '斯普特尼克', '哒哒达利', '无线电小姐'],
    '大十字形': ['红弩箭', '37', '牙仙', '百夫长', '玛蒂尔达', '金蜜儿', '五色月', '玛丽莲', '坦南特', '小春雀儿',
                 '洋葱头']}
dic_insight2 = {0: ['0.05', 0, 0, 0, 0], 1: [0, '0.1', 0, 0, 0], 2: [0, 0, '0.15', 0, 0], 3: [0, 0, 0, '0.08', 0],
                4: [0, 0, 0, 0, '0.1']}
star_6 = ['37', '红弩箭', '牙仙', '远旅', '星锑', '梅兰妮', '百夫长', '鬃毛沙砾', '兔毛手袋', '百夫长', '伽菈波那',
          '皮克勒斯', '新巴别塔', '温妮弗雷德', '洁西卡', '泥鯭的士', '苏芙比', '槲寄生', '未锈铠', '6']
star_5 = ['金蜜儿', '玛蒂尔达', '夏利', '婴儿蓝', '坦南特', '帕米埃', '玛丽莲', '恐怖通', '讣告人', '气球派对',
          '十四行诗', '坎吉拉', '挖掘艺术', '五色月', '柏林以东', '喀嚓喀嚓', 'X']
star_4 = ['埃里克', 'TTT', 'APPLe', '雾行者', '狼群', '芭妮芭妮', '尼克·波顿', '莫桑女士', '铅玻璃', '红斗篷', '爱宠',
          '冬', '小春雀儿', '吵闹鬼', '小梅斯梅尔']
star_3 = ['斯普特尼克', '星之眼', '弄臣', '哒哒达利', '莉拉妮', '洋葱头', '贝蒂', '拉拉泉', '约翰·提托', '丽莎&路易斯']
star_2 = ['门', '无线电小姐']
star_list = [star_2, star_3, star_4, star_5, star_6]

heart_list = ['美丽新世界', '跳房子游戏', '第二次生命', '夜色亵渎者', '掌声如雷鸣', '好奇心宝贝', '大娱乐至上',
              '必要的记录', '在仙境之外', '沉默与向往', '可度量之心', '请保持平衡', '心驰神往', '明日亦然', '无束无拘',
              '示我以真', '午后小憩', '远大前程', '食足餮满', '荒唐余生', '自由的心', '笑语欢声']
enemy_list = ['凶兆·天蛾人', '深眠平均属性测试怪', '无属性测试怪']
dic_enemy = {0: [553, 513, '0.14', '0.164'], 1: [630, 630, '0.2', '0.25'], 2: [0, 0, '0', '0']}  # 敌人dic，天蛾人，深眠平均，0数据测试怪


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def query_character_db(name, insight, level):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(get_resource_path('db/character.db'))
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT 攻击, 生命, 现实防御, 精神防御, 暴击技巧 FROM '{name}' WHERE 洞悉 ={insight} AND 等级 ={level}")
    results = cursor.fetchall()
    # 获取查询结果
    for result in results:
        value = result

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return value


def query_heart_db(name, level):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(get_resource_path('db/heart.db'))
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT 攻击, 生命, 现实防御, 精神防御, 仪式威力, 术法威力, 攻击百分比, 暴击率, 暴击创伤, 创伤加成, 生命百分比 FROM '{name}' WHERE 等级 ={level}")
    results = cursor.fetchall()
    # 获取查询结果
    for result in results:
        value = result

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return value


def query_resonate_db(c_name, r_level, resonate_name):
    conn = sqlite3.connect(get_resource_path('db/resonate.db'))
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT 生命, 攻击, 现实防御, 精神防御, 暴击率, 暴击创伤, 创伤加成, 生命百分比, 攻击百分比, 现实防御百分比, 精神防御百分比 FROM '{c_name}' WHERE 共鸣等级 ={r_level} and 共鸣块 ='{resonate_name}'")
    # results = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]

    results = cursor.fetchall()

    for result in results:
        value = result

    cursor.close()
    conn.close()

    return value


def choice_attribute(index):
    return character_list[index]


def choice_rare_bg(character_name):
    for i in star_list:
        if character_name in i:
            return star_list.index(i) + 2


def choice_insight(character_name):
    for i in star_list:
        if character_name in i:
            if star_list.index(i) + 2 <= 4:

                return 2
            else:

                return 3


def choice_level(insight):
    if insight == 3:
        return 60
    elif insight == 2:
        return 50
    elif insight == 1:
        return 40
    elif insight == 0:
        return 30


def choice_resonate_level(insight):
    if insight == 3:
        return 15
    elif insight == 2:
        return 10
    elif insight == 1:
        return 5
    elif insight == 0:
        return 0


def choice_main_resonate(name):
    resonate_name = [key for key, value in dic_resonate.items() if name in value][0]
    return resonate_name


def choice_resonate_all_level(name, r_level):
    conn = sqlite3.connect(get_resource_path('db/resonate.db'))

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT 共鸣块, 共鸣块等级, 共鸣块可用数量 FROM '{name}' WHERE 共鸣等级 ={r_level}")
    results = cursor.fetchall()
    # 关闭数据库连接
    cursor.close()
    conn.close()

    return results


def choice_character(name, insight, level):
    value = query_character_db(name, insight, level)

    c_ATK = Decimal(value[0])

    c_HP = Decimal(value[1])
    c_tDEF = Decimal(value[2])
    c_mDEF = Decimal(value[3])

    c_CRT = Decimal(Decimal(str(value[4])) / 3000).quantize(Decimal("0.000"), rounding="ROUND_HALF_UP")
    c_CRT_D = Decimal(Decimal(str(value[4])) / 2000).quantize(Decimal("0.000"), rounding="ROUND_HALF_UP")

    values = [c_ATK, c_HP, c_tDEF, c_mDEF, c_CRT, c_CRT_D]

    return values


def choice_heart(name, level):
    value = query_heart_db(name, level)
    h_ATK = Decimal(value[0])
    h_HP = Decimal(value[1])
    h_tDEF = Decimal(value[2])
    h_mDEF = Decimal(value[3])
    h_rPOW = Decimal(str(value[4]))
    h_mPOW = Decimal(str(value[5]))
    h_ATK_P = Decimal(str(value[6]))
    h_CRT = Decimal(str(value[7]))
    h_CRT_D = Decimal(str(value[8]))
    h_DMG = Decimal(str(value[9]))
    h_HP_P = Decimal(str(value[10]))

    values = [h_ATK, h_HP, h_tDEF, h_mDEF, h_rPOW, h_mPOW, h_ATK_P, h_CRT, h_CRT_D, h_DMG, h_HP_P]

    return values


def choice_resonate(c_name, r_level, number_main, number_L, number_J, number_S, number_Z, number_I, number_O,
                    number_T, number_3, number_2, number_atk, number_def):
    r_HP = r_ATK = r_tDEF = r_mDEF = r_CRT = r_CRT_D = r_DMG = r_HP_P = r_ATK_P = r_tDEF_P = r_mDEF_P = Decimal(0)

    dic = {choice_main_resonate(c_name): number_main, 'L形': number_L,
           'J形': number_J, 'S形': number_S, 'Z形': number_Z, 'I形': number_I,
           'O形': number_O, 'T形': number_T, '三格形': number_3, '双格形': number_2, '增伤单格形': number_atk,
           '减防单格形': number_def}

    for resonate_name in dic.keys():

        number = dic[resonate_name]
        if number != 0:
            value = query_resonate_db(c_name, r_level, resonate_name)

            r_HP += value[0] * number
            r_ATK += value[1] * number
            r_tDEF += value[2] * number
            r_mDEF += value[3] * number
            r_CRT += Decimal(str(value[4])) * number
            r_CRT_D += Decimal(str(value[5])) * number
            r_DMG += Decimal(str(value[6])) * number
            r_HP_P += Decimal(str(value[7])) * number
            r_ATK_P += Decimal(str(value[8])) * number
            r_tDEF_P += Decimal(str(value[9])) * number
            r_mDEF_P += Decimal(str(value[10])) * number

    values = [r_HP, r_ATK, r_tDEF, r_mDEF, r_CRT, r_CRT_D, r_DMG, r_HP_P, r_ATK_P, r_tDEF_P, r_mDEF_P]

    return values


def choice_insight2(insight2):
    ATK_buff = Decimal(dic_insight2[insight2][0])
    CRT = Decimal(dic_insight2[insight2][1])
    CRT_D = Decimal(dic_insight2[insight2][2])
    DMG = Decimal(dic_insight2[insight2][3])
    PTT = Decimal(dic_insight2[insight2][4])
    values = [ATK_buff, CRT, CRT_D, DMG, PTT]

    return values


def choice_enemy(index):
    e_tDEF = Decimal(dic_enemy[index][0])
    e_mDEF = Decimal(dic_enemy[index][1])
    e_rDMG = Decimal(dic_enemy[index][2])
    e_rCRT = Decimal(dic_enemy[index][3])
    values = [e_tDEF, e_mDEF, e_rDMG, e_rCRT]
    return values


def final_damage_calculation(all_zip, i_zip, e_zip):
    ATK, rPOW, mPOW, CRT, CRT_D, DMG = all_zip

    i_ATK_buff, i_CRT, i_CRT_D, i_DMG, i_PTT_buff, match_up, d_type, skill1_ratio, skill2_ratio, skill3_ratio = i_zip

    e_tDEF, e_mDEF, e_rDMG, e_rCRT = e_zip

    if d_type == '现实创伤':
        e_DEF = e_tDEF
    else:
        e_DEF = e_mDEF

    total_ATK = ATK * (1 + i_ATK_buff)

    total_DEF = e_DEF * (1 - i_PTT_buff)

    total_DMG = DMG + i_DMG - e_rDMG

    total_CRT = CRT + i_CRT

    total_CRT_D = CRT_D + i_CRT_D - e_rCRT

    ATK_DEF_Multiplier = total_ATK - total_DEF
    if ATK_DEF_Multiplier < (total_ATK * Decimal(0.1)):
        ATK_DEF_Multiplier = total_ATK * Decimal(0.1)

    DMG_Multiplier = Decimal(1) + total_DMG
    if DMG_Multiplier < Decimal(0.3):
        DMG_Multiplier = Decimal(0.3)

    CRT_D_Multiplier = total_CRT_D
    if CRT_D_Multiplier < Decimal(1.1):
        CRT_D_Multiplier = Decimal(1.1)

    skill1_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill1_ratio * (1 + mPOW) * (1 + match_up)
    skill2_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill2_ratio * (1 + mPOW) * (1 + match_up)
    skill3_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill3_ratio * (1 + rPOW) * (1 + match_up)

    skill1_crit_damage = skill1_normal_damage * CRT_D_Multiplier
    skill2_crit_damage = skill2_normal_damage * CRT_D_Multiplier
    skill3_crit_damage = skill3_normal_damage * CRT_D_Multiplier
    if total_CRT > 1:
        skill1_expectation_damage = skill1_crit_damage
        skill2_expectation_damage = skill2_crit_damage
        skill3_expectation_damage = skill3_crit_damage
    else:
        skill1_expectation_damage = skill1_normal_damage * (1 - total_CRT) + skill1_crit_damage * total_CRT
        skill2_expectation_damage = skill2_normal_damage * (1 - total_CRT) + skill2_crit_damage * total_CRT
        skill3_expectation_damage = skill3_normal_damage * (1 - total_CRT) + skill3_crit_damage * total_CRT

    DPM = (5 * (skill1_expectation_damage + skill2_expectation_damage) + 2 * skill3_expectation_damage) / 12

    results = [round(skill1_normal_damage), round(skill1_crit_damage), round(skill1_expectation_damage),
               round(skill2_normal_damage), round(skill2_crit_damage), round(skill2_expectation_damage),
               round(skill3_normal_damage), round(skill3_crit_damage), round(skill3_expectation_damage),
               round(DPM)]

    results2 = [round(skill1_normal_damage), round(skill1_crit_damage), round(skill1_expectation_damage),
                round(skill2_normal_damage), round(skill2_crit_damage), round(skill2_expectation_damage),
                round(skill3_normal_damage), round(skill3_crit_damage), round(skill3_expectation_damage),
                round(DPM)]

    return results, results2



