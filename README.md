# calculator\_of\_Onmyoji

御魂搭配计算器

## Usage of calculator

```
usage: cal_mitama.py [-h] [-M MITAMA_SUIT] [-P PROP_LIMIT]
                     [-UP UPPER_PROP_LIMIT] [-2P SEC_PROP_VALUE]
                     [-4P FTH_PROP_VALUE] [-6P STH_PROP_VALUE]
                     [-IG IGNORE_SERIAL] [-AS ALL_SUIT] [-DL DAMAGE_LIMIT]
                     [-HL HEALTH_LIMIT] [-AO ATTACK_ONLY]
                     source_data output_file

positional arguments:
  source_data           御魂数据表格，格式参照example/data_Template.xls
  output_file           输出文件位置，格式为pathto/filename.xls

optional arguments:
  -h, --help            show this help message and exit
  -M MITAMA_SUIT, --mitama-suit MITAMA_SUIT
                        期望的御魂x件套类型，多个限制用英文句号.间隔，例如"-M 针女,4"为针女至少4件，"-M
                        针女,4.破势,2"为针女4件+破势2件
  -P PROP_LIMIT, --prop-limit PROP_LIMIT
                        期望限制的属性下限，多个属性条件用英文句号.间隔, 例如"-P
                        暴击,90.暴击伤害,70"为暴击至少90且暴击伤害至少70
  -UP UPPER_PROP_LIMIT, --upper-prop-limit UPPER_PROP_LIMIT
                        期望限制的属性上限，多个属性条件用英文句号.间隔，例如"-UP
                        暴击,95.速度,20"为暴击最多95且速度最多20
  -2P SEC_PROP_VALUE, --sec-prop-value SEC_PROP_VALUE
                        二号位限制的属性类型和数值，多个属性用英文句号.间隔，例如"-2P 攻击加成,55"为二号位攻击加成至少55
  -4P FTH_PROP_VALUE, --fth-prop-value FTH_PROP_VALUE
                        四号位限制的属性类型和数值，多个属性用英文句号.间隔，例如"-4P 攻击加成,55"为四号位攻击加成至少55
  -6P STH_PROP_VALUE, --sth-prop-value STH_PROP_VALUE
                        六号位限制的属性类型和数值，多个属性用英文句号.间隔，例如"-6P
                        暴击,55"为六号位暴击至少55，"-6P
                        暴击,55.暴击伤害,89"为六号位暴击至少55或暴击伤害至少89
  -IG IGNORE_SERIAL, --ignore-serial IGNORE_SERIAL
                        忽略的御魂序号关键字，用逗号,间隔例如"-IG 天狗,鸟"为御魂序号包含天狗或鸟则滤除
  -AS ALL_SUIT, --all-suit ALL_SUIT
                        是否全为套装，默认为True。"-AS False"为允许非套装的组合出现，如5针女1破势
  -DL DAMAGE_LIMIT, --damage-limit DAMAGE_LIMIT
                        基础攻击,基础暴伤,期望的攻击*暴伤，例如"-DL
                        3126,150，20500"，当基础攻击为3126，基础暴伤为150，攻击*暴伤>=20500
  -HL HEALTH_LIMIT, --health-limit HEALTH_LIMIT
                        基础生命,基础暴伤,期望的生命*暴伤，例如"-HL
                        8000,150,60000"，当基础生命为8000，基础暴伤为150，生命*暴伤>=60000
  -AO ATTACK_ONLY, --attack-only ATTACK_ONLY
                        是否只计算输出类御魂，默认为False。"-AO
                        True"为只计算套装属性为攻击加成、暴击和首领御魂的套装组合
  -J  Jipindu, --jipindu_input
                        限定御魂的有效属性和每个位置分别的有效属性条数要求
                        例如"-J 暴击,暴击伤害,速度,攻击加成.5,3,5,3,5,0
                        意味着有效属性定位为暴击、暴击伤害、速度、攻击加成这几类
                        且1~6号位各自的有效条数分别不低于5条、3条、5条、3条、5条、0条
                        有效属性的定义范围可以是1个或者多个甚至超过4个，有效条数不应该超过9

```

## Usage of mitama puller

```
usage: pull_mitama.py [-h] [-O OUTPUT_FILE] acc_id

positional arguments:
  acc_id                藏宝阁id，商品详情页面对应的网址中，格式如201806211901616-3-KJ8J8IQOJTOMD8

optional arguments:
  -h, --help            show this help message and exit
  -O OUTPUT_FILE, --output-file OUTPUT_FILE
                        输出文件位置，格式为pathto/filename.xls
```

## Usage of mitama json converter

```
usage: make sure json files are in the same directory with convert_json2xls.py

python convert_json2xls.py
```

## Usage of result\_combination

```
Cal independent combinations of mitama_results

usage: make sure files(*-result.xls) are in current directory

python calculator_of_Onmyoji/result_combination.py
```

## Test Command
```python calculator_of_Onmyoji/cal_mitama.py example/data_Template.xls result.xls -M 针女,4 -P 暴击,90```

## Cal example
```python calculator_of_Onmyoji/cal_mitama.py example/victor.xls v_result.xls -M 针女,4 -P 暴击,90.暴击伤害,50 -2P 攻击加成,55 -4P 攻击加成,55 -6P 暴击,55 -IG 天狗```

## Make tar
```tar zcf calculator.tar.gz calculator_of_Onmyoji example dist LICENSE README.md requirements.txt setup.* win_compile.txt```
