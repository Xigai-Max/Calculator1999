# 仅做攻防区内取整
import math

from decimal import Decimal
import openpyxl as op


# 完全不取整
def start_damage_calculation(all_zip, i_zip, e_zip, b_zip):
    # 数据解包
    ATK, rPOW, mPOW, CRT, CRT_D, DMG = all_zip

    i_ATK_buff, i_CRT, i_CRT_D, i_DMG, i_PTT_buff, match_up, d_type, skill1_ratio, skill2_ratio, skill3_ratio = i_zip

    e_tDEF, e_mDEF, e_rDMG, e_rCRT = e_zip

    b_rDEF, b_DMG ,b_PT= b_zip

    # 入战数据
    if d_type == '现实创伤':
        e_DEF = e_tDEF
    else:
        e_DEF = e_mDEF

    # 总属性计算
    total_ATK = ATK * (1 + i_ATK_buff)

    total_DEF = e_DEF * (1 - i_PTT_buff- b_PT ) * (1 - b_rDEF)

    total_DMG = DMG + i_DMG - e_rDMG + b_DMG

    total_CRT_D = CRT_D + i_CRT_D - e_rCRT

    # 分乘区计算
    ATK_DEF_Multiplier = total_ATK - total_DEF
    if ATK_DEF_Multiplier < (total_ATK * Decimal(0.1)):
        ATK_DEF_Multiplier = total_ATK * Decimal(0.1)

    DMG_Multiplier = Decimal(1) + total_DMG
    if DMG_Multiplier < Decimal(0.3):
        DMG_Multiplier = Decimal(0.3)

    CRT_D_Multiplier = total_CRT_D
    if CRT_D_Multiplier < Decimal(1.1):
        CRT_D_Multiplier = Decimal(1.1)

    # 未暴击伤害计算
    skill1_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill1_ratio * (1 + mPOW) * (1 + match_up)
    skill2_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill2_ratio * (1 + mPOW) * (1 + match_up)
    skill3_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill3_ratio * (1 + rPOW) * (1 + match_up)

    # 暴击伤害计算
    skill1_crit_damage = skill1_normal_damage * CRT_D_Multiplier
    skill2_crit_damage = skill2_normal_damage * CRT_D_Multiplier
    skill3_crit_damage = skill3_normal_damage * CRT_D_Multiplier

    # 结果打包
    results = [skill1_normal_damage, skill1_crit_damage,
               skill2_normal_damage, skill2_crit_damage,
               skill3_normal_damage, skill3_crit_damage]
    return results


# 仅做攻防区内取整
def final_damage_calculation(all_zip, i_zip, e_zip, b_zip):
    # 数据解包
    ATK, rPOW, mPOW, CRT, CRT_D, DMG = all_zip

    i_ATK_buff, i_CRT, i_CRT_D, i_DMG, i_PTT_buff, match_up, d_type, skill1_ratio, skill2_ratio, skill3_ratio = i_zip

    e_tDEF, e_mDEF, e_rDMG, e_rCRT = e_zip

    b_rDEF, b_DMG ,b_PT= b_zip

    # 入战数据
    if d_type == '现实创伤':
        e_DEF = e_tDEF
    else:
        e_DEF = e_mDEF

    # 总属性计算
    total_ATK = ATK * (1 + i_ATK_buff)

    total_DEF = e_DEF * (1 - i_PTT_buff- b_PT ) * (1 - b_rDEF)

    total_DMG = DMG + i_DMG - e_rDMG + b_DMG

    total_CRT_D = CRT_D + i_CRT_D - e_rCRT

    # 分乘区计算
    ATK_DEF_Multiplier = math.floor(total_ATK - total_DEF)
    if ATK_DEF_Multiplier < (total_ATK * Decimal(0.1)):
        ATK_DEF_Multiplier = total_ATK * Decimal(0.1)

    DMG_Multiplier = Decimal(1) + total_DMG
    if DMG_Multiplier < Decimal(0.3):
        DMG_Multiplier = Decimal(0.3)

    CRT_D_Multiplier = total_CRT_D
    if CRT_D_Multiplier < Decimal(1.1):
        CRT_D_Multiplier = Decimal(1.1)

    # 未暴击伤害计算
    skill1_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill1_ratio * (1 + mPOW) * (1 + match_up)
    skill2_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill2_ratio * (1 + mPOW) * (1 + match_up)
    skill3_normal_damage = ATK_DEF_Multiplier * DMG_Multiplier * skill3_ratio * (1 + rPOW) * (1 + match_up)

    # 暴击伤害计算
    skill1_crit_damage = skill1_normal_damage * CRT_D_Multiplier
    skill2_crit_damage = skill2_normal_damage * CRT_D_Multiplier
    skill3_crit_damage = skill3_normal_damage * CRT_D_Multiplier

    # 结果打包
    results = [skill1_normal_damage, skill1_crit_damage,
               skill2_normal_damage, skill2_crit_damage,
               skill3_normal_damage, skill3_crit_damage]
    return results


# 攻防区内取整，先计算攻防乘创伤取整，再乘倍率威力克制取整，最后暴击取整
def test_damage_calculation(all_zip, i_zip, e_zip, b_zip):
    # 数据解包
    ATK, rPOW, mPOW, CRT, CRT_D, DMG = all_zip

    i_ATK_buff, i_CRT, i_CRT_D, i_DMG, i_PTT_buff, match_up, d_type, skill1_ratio, skill2_ratio, skill3_ratio = i_zip

    e_tDEF, e_mDEF, e_rDMG, e_rCRT = e_zip

    b_rDEF, b_DMG ,b_PT= b_zip

    # 入战数据
    if d_type == '现实创伤':
        e_DEF = e_tDEF
    else:
        e_DEF = e_mDEF

    # 总属性计算
    total_ATK = ATK * (1 + i_ATK_buff)

    total_DEF = e_DEF * (1 - i_PTT_buff- b_PT ) * (1 - b_rDEF)

    total_DMG = DMG + i_DMG - e_rDMG + b_DMG

    total_CRT = CRT + i_CRT

    total_CRT_D = CRT_D + i_CRT_D - e_rCRT

    # 分乘区计算
    ATK_DEF_Multiplier = math.floor(total_ATK - total_DEF)
    if ATK_DEF_Multiplier < (total_ATK * Decimal(0.1)):
        ATK_DEF_Multiplier = total_ATK * Decimal(0.1)

    DMG_Multiplier = Decimal(1) + total_DMG
    if DMG_Multiplier < Decimal(0.3):
        DMG_Multiplier = Decimal(0.3)

    CRT_D_Multiplier = total_CRT_D
    if CRT_D_Multiplier < Decimal(1.1):
        CRT_D_Multiplier = Decimal(1.1)

    # 未暴击伤害计算
    skill1_normal_damage = math.floor(ATK_DEF_Multiplier * DMG_Multiplier) * skill1_ratio * (1 + mPOW) * (1 + match_up)
    skill2_normal_damage = math.floor(
        math.floor(ATK_DEF_Multiplier * DMG_Multiplier) * skill2_ratio * (1 + mPOW) * (1 + match_up))
    skill3_normal_damage = math.floor(
        math.floor(ATK_DEF_Multiplier * DMG_Multiplier) * skill3_ratio * (1 + rPOW) * (1 + match_up))

    # 暴击伤害计算
    skill1_crit_damage = math.floor(skill1_normal_damage * CRT_D_Multiplier)
    skill2_crit_damage = math.floor(skill2_normal_damage * CRT_D_Multiplier)
    skill3_crit_damage = math.floor(skill3_normal_damage * CRT_D_Multiplier)

    # 结果打包
    results = [skill1_normal_damage, skill1_crit_damage,
               skill2_normal_damage, skill2_crit_damage,
               skill3_normal_damage, skill3_crit_damage]
    return results


# 攻防区内取整后 每乘区相乘时取整
def test2_damage_calculation(all_zip, i_zip, e_zip, b_zip):
    # 数据解包
    ATK, rPOW, mPOW, CRT, CRT_D, DMG = all_zip

    i_ATK_buff, i_CRT, i_CRT_D, i_DMG, i_PTT_buff, match_up, d_type, skill1_ratio, skill2_ratio, skill3_ratio = i_zip

    e_tDEF, e_mDEF, e_rDMG, e_rCRT = e_zip

    b_rDEF, b_DMG ,b_PT= b_zip

    # 入战数据
    if d_type == '现实创伤':
        e_DEF = e_tDEF
    else:
        e_DEF = e_mDEF

    # 总属性计算
    total_ATK = ATK * (1 + i_ATK_buff)

    total_DEF = e_DEF * (1 - i_PTT_buff- b_PT ) * (1 - b_rDEF)

    total_DMG = DMG + i_DMG - e_rDMG + b_DMG

    total_CRT = CRT + i_CRT

    total_CRT_D = CRT_D + i_CRT_D - e_rCRT

    # 分乘区计算
    ATK_DEF_Multiplier = math.floor(total_ATK - total_DEF)
    if ATK_DEF_Multiplier < (total_ATK * Decimal(0.1)):
        ATK_DEF_Multiplier = total_ATK * Decimal(0.1)

    DMG_Multiplier = Decimal(1) + total_DMG
    if DMG_Multiplier < Decimal(0.3):
        DMG_Multiplier = Decimal(0.3)

    CRT_D_Multiplier = total_CRT_D
    if CRT_D_Multiplier < Decimal(1.1):
        CRT_D_Multiplier = Decimal(1.1)

    def step_m_calcultor(ratio):
        step1 = math.floor(ATK_DEF_Multiplier * DMG_Multiplier)
        step2 = math.floor(step1 * (1 + mPOW))
        step3 = math.floor(step2 * ratio)
        step4 = math.floor(step3 * (1 + match_up))
        return step4

    def step_r_calcultor(ratio):
        step1 = math.floor(ATK_DEF_Multiplier * DMG_Multiplier)
        step2 = math.floor(step1 * ratio)
        step3 = math.floor(step2 * (1 + rPOW))
        step4 = math.floor(step3 * (1 + match_up))
        return step4

    # 未暴击伤害计算
    skill1_normal_damage = step_m_calcultor(skill1_ratio)
    skill2_normal_damage = step_m_calcultor(skill2_ratio)
    skill3_normal_damage = step_r_calcultor(skill3_ratio)

    # 暴击伤害计算
    skill1_crit_damage = math.floor(skill1_normal_damage * CRT_D_Multiplier)
    skill2_crit_damage = math.floor(skill2_normal_damage * CRT_D_Multiplier)
    skill3_crit_damage = math.floor(skill3_normal_damage * CRT_D_Multiplier)

    # 结果打包
    results = [skill1_normal_damage, skill1_crit_damage,
               skill2_normal_damage, skill2_crit_damage,
               skill3_normal_damage, skill3_crit_damage]
    return results


# 攻防区内取整，先计算攻防乘创伤取整，再乘倍率威力克制取整，最后暴击取整(测试穿透率问题)
def test3_damage_calculation(all_zip, i_zip, e_zip, b_zip):
    # 数据解包
    ATK, rPOW, mPOW, CRT, CRT_D, DMG = all_zip

    i_ATK_buff, i_CRT, i_CRT_D, i_DMG, i_PTT_buff, match_up, d_type, skill1_ratio, skill2_ratio, skill3_ratio = i_zip

    e_tDEF, e_mDEF, e_rDMG, e_rCRT = e_zip

    b_rDEF, b_DMG ,b_PT= b_zip

    # 入战数据
    if d_type == '现实创伤':
        e_DEF = e_tDEF
    else:
        e_DEF = e_mDEF

    # 总属性计算
    total_ATK = ATK * (1 + i_ATK_buff)

    total_DEF = e_DEF * (1 - i_PTT_buff - b_PT) * (1 - b_rDEF)

    total_DMG = DMG + i_DMG - e_rDMG + b_DMG

    total_CRT = CRT + i_CRT

    total_CRT_D = CRT_D + i_CRT_D - e_rCRT

    # 分乘区计算
    ATK_DEF_Multiplier = math.floor(total_ATK - total_DEF)
    if ATK_DEF_Multiplier < (total_ATK * Decimal(0.1)):
        ATK_DEF_Multiplier = total_ATK * Decimal(0.1)

    DMG_Multiplier = Decimal(1) + total_DMG
    if DMG_Multiplier < Decimal(0.3):
        DMG_Multiplier = Decimal(0.3)

    CRT_D_Multiplier = total_CRT_D
    if CRT_D_Multiplier < Decimal(1.1):
        CRT_D_Multiplier = Decimal(1.1)

    # 未暴击伤害计算
    skill1_normal_damage = math.floor(ATK_DEF_Multiplier * DMG_Multiplier) * skill1_ratio * (1 + mPOW) * (1 + match_up)
    skill2_normal_damage = math.floor(
        math.floor(ATK_DEF_Multiplier * DMG_Multiplier) * skill2_ratio * (1 + mPOW) * (1 + match_up))
    skill3_normal_damage = math.floor(
        math.floor(ATK_DEF_Multiplier * DMG_Multiplier) * skill3_ratio * (1 + rPOW) * (1 + match_up))

    # 暴击伤害计算
    skill1_crit_damage = math.floor(skill1_normal_damage * CRT_D_Multiplier)
    skill2_crit_damage = math.floor(skill2_normal_damage * CRT_D_Multiplier)
    skill3_crit_damage = math.floor(skill3_normal_damage * CRT_D_Multiplier)

    # 结果打包
    results = [skill1_normal_damage, skill1_crit_damage,
               skill2_normal_damage, skill2_crit_damage,
               skill3_normal_damage, skill3_crit_damage]
    return results


# 14 3关关底ex
ATK = Decimal(1177)  # 角色攻击力
CRT = Decimal('0')  # 角色暴击率
CRT_D = Decimal('1.412')  # 角色暴击创伤
rPOW = Decimal('0')  # 角色仪式威力
mPOW = Decimal('0.16')  # 角色术法威力
DMG = Decimal('0.015')  # 角色创伤加成

i_ATK_buff = Decimal(0)  # 洞悉2攻击加成效果
i_CRT = Decimal(0)  # 洞悉2暴击率效果
i_CRT_D = Decimal('0')  # 洞悉2暴击创伤效果
i_DMG = Decimal(0)  # 洞悉2创伤加成效果
i_PTT_buff = Decimal(0)  # 洞悉2穿透效果

match_up = 0  # 是否克制 0/1
d_type = '现实创伤'  # 创伤类型，字符串即可
skill1_ratio = Decimal('2.2')  # 一技能倍率
skill2_ratio = Decimal('0')  # 二技能倍率
skill3_ratio = Decimal('3')  # 仪式倍率

b_rDEF = Decimal('0.15')  # buff减防效果
b_DMG = Decimal('0.15')+Decimal('0.15')+Decimal('0.1')  # buff创伤加成&受创提升&受创减免效果
b_ATK = Decimal(0)  # buff攻击力效果
b_PT = Decimal('0.15')

e_tDEF = Decimal(383)  # 敌方现实防御
e_mDEF = Decimal(383)  # 敌方精神防御
e_rDMG = Decimal('0.116')  # 敌方受创减免
e_rCRT = Decimal('0.036')  # 敌方暴击防御

# 数据打包
all_zip = [ATK, rPOW, mPOW, CRT, CRT_D, DMG]
i_zip = [i_ATK_buff, i_CRT, i_CRT_D, i_DMG, i_PTT_buff, match_up, d_type, skill1_ratio, skill2_ratio, skill3_ratio]
b_zip = [b_rDEF, b_DMG, b_PT]
e_zip = [e_tDEF, e_mDEF, e_rDMG, e_rCRT]

result = start_damage_calculation(all_zip, i_zip, e_zip, b_zip)
final_result = final_damage_calculation(all_zip, i_zip, e_zip, b_zip)
test_result = test_damage_calculation(all_zip, i_zip, e_zip, b_zip)
test2_result = test2_damage_calculation(all_zip, i_zip, e_zip, b_zip)
print('1.完全不取整')
print(f'{result[0]}\n')

print('2.仅做攻防区内取整')
print(f'{final_result[0]}\n')

print('3.攻防区内取整，先计算攻防乘创伤取整，再乘倍率威力克制取整，最后暴击取整')
print(f'{test_result[0]}\n')

print('4.攻防区内取整后 每乘区相乘时取整')
print(f'{test2_result[0]}\n')
