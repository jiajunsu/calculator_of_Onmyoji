# calculator\_of\_Onmyoji

御魂搭配计算器

## Usage

```python calculator_of_Onmyoji/cal_mitama.py -h```

```
usage: cal_mitama.py [-h] [-M MITAMA_SUIT] [-P PROP_LIMIT]
                     [-2P SEC_PROP_VALUE] [-4P FTH_PROP_VALUE]
                     [-6P STH_PROP_VALUE] [-IG IGNORE_SERIAL] [-AS ALL_SUIT]
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
                        期望限制的属性类型，多个属性条件用英文句号.间隔, 例如"-P
                        暴击,90.暴击伤害,70"为暴击至少90且暴击伤害至少70
  -2P SEC_PROP_VALUE, --sec-prop-value SEC_PROP_VALUE
                        二号位限制的属性类型和数值，例如"-2P 攻击加成,55"为二号位攻击加成至少55
  -4P FTH_PROP_VALUE, --fth-prop-value FTH_PROP_VALUE
                        四号位限制的属性类型和数值，例如"-4P 攻击加成,55"为四号位攻击加成至少55
  -6P STH_PROP_VALUE, --sth-prop-value STH_PROP_VALUE
                        六号位限制的属性类型和数值，例如"-6P 暴击,55"为六号位暴击至少55
  -IG IGNORE_SERIAL, --ignore-serial IGNORE_SERIAL
                        忽略的御魂序号关键字，用逗号,间隔例如"-IG 天狗,鸟"为御魂序号包含天狗或鸟则滤除
  -AS ALL_SUIT, --all-suit ALL_SUIT
                        是否全为套装，默认为True。"-AS False"为允许非套装的组合出现，如5针女1破势
```

## Test Command
```python calculator_of_Onmyoji/cal_mitama.py example/data_Template.xls data/result.xls -M 针女,4 -P 暴击,90```

## Cal example
```python calculator_of_Onmyoji/cal_mitama.py example/victor.xls data/v_result.xls -M 针女,4 -P 暴击,90.暴击伤害,50 -2P 攻击加成,55 -4P 攻击加成,55 -6P 暴击,55 -IG 天狗```

## Make tar
```tar zcf calculator.tar.gz calculator_of_Onmyoji example dist LICENSE README.md requirements.txt setup.* win_compile.txt```
