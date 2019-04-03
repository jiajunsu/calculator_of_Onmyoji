# calculator\_of\_Onmyoji

御魂搭配计算器

## Setup

Python version >= 3.6.*

```
pip install -r requirements.txt
pip install .
```


## Usage of calculator

```
usage: cal_mitama.py [-h] [-M MITAMA_SUIT] [-P PROP_LIMIT]
                     [-UP UPPER_PROP_LIMIT] [-2P SEC_PROP_VALUE]
                     [-4P FTH_PROP_VALUE] [-6P STH_PROP_VALUE]
                     [-IG IGNORE_SERIAL] [-AS ALL_SUIT] [-DL DAMAGE_LIMIT]
                     [-HL HEALTH_LIMIT] [-AO ATTACK_ONLY]
                     [-ESP EFFECTIVE_SECONDARY_PROP]
                     [-ESPN EFFECTIVE_SECONDARY_PROP_NUM]
                     source_data output_file

positional arguments:
  source_data           御魂数据，格式参照example/data_Template.xls
  output_file           输出文件位置，格式为pathto/filename.xls

optional arguments:
  -h, --help            show this help message and exit
  -M MITAMA_SUIT, --mitama-suit MITAMA_SUIT
                        期望的x件套御魂类型或者加成类型，多个限制用英文符号#间隔，例如"-M 针女,4"为针女至少4件，"-M
                        针女,4#破势,2"为针女4件+破势2件，"-M 生命加成,2#生命加成,2#生命加成,2"为3个生命两件套
  -P PROP_LIMIT, --prop-limit PROP_LIMIT
                        期望限制的属性下限，多个属性条件用英文符号#间隔, 例如"-P
                        暴击,90#暴击伤害,70"为暴击至少90且暴击伤害至少70
  -UP UPPER_PROP_LIMIT, --upper-prop-limit UPPER_PROP_LIMIT
                        期望限制的属性上限，多个属性条件用英文符号#间隔，例如"-UP
                        暴击,95#速度,20"为暴击最多95且速度最多20
  -2P SEC_PROP_VALUE, --sec-prop-value SEC_PROP_VALUE
                        二号位限制的属性类型和数值，多个属性用英文符号#间隔，例如"-2P 攻击加成,55"为二号位攻击加成至少55
  -4P FTH_PROP_VALUE, --fth-prop-value FTH_PROP_VALUE
                        四号位限制的属性类型和数值，多个属性用英文符号#间隔，例如"-4P 攻击加成,55"为四号位攻击加成至少55
  -6P STH_PROP_VALUE, --sth-prop-value STH_PROP_VALUE
                        六号位限制的属性类型和数值，多个属性用英文符号#间隔，例如"-6P
                        暴击,55"为六号位暴击至少55，"-6P
                        暴击,55#暴击伤害,89"为六号位暴击至少55或暴击伤害至少89
  -IG IGNORE_SERIAL, --ignore-serial IGNORE_SERIAL
                        忽略的御魂序号关键字，用逗号,间隔例如"-IG 天狗,鸟"为御魂序号包含天狗或鸟则滤除
  -AS ALL_SUIT, --all-suit ALL_SUIT
                        是否全为套装，默认为True。"-AS False"为允许非套装的组合出现，如5针女1破势
  -DL DAMAGE_LIMIT, --damage-limit DAMAGE_LIMIT
                        基础攻击,基础暴伤,期望的攻击*暴伤，例如"-DL
                        3126,150,20500"，当基础攻击为3126，基础暴伤为150，攻击*暴伤>=20500
  -HL HEALTH_LIMIT, --health-limit HEALTH_LIMIT
                        基础生命,基础暴伤,期望的生命*暴伤，例如"-HL
                        8000,150,60000"，当基础生命为8000，基础暴伤为150，生命*暴伤>=60000
  -AO ATTACK_ONLY, --attack-only ATTACK_ONLY
                        是否只计算输出类御魂，默认为False。"-AO
                        True"为只计算套装属性为攻击加成、暴击和首领御魂的套装组合
  -ESP EFFECTIVE_SECONDARY_PROP, --effective-secondary-prop 
                        设定御魂的有效副属性，用逗号,间隔
                        例如"-ESP 暴击,暴击伤害,速度,攻击加成"意味着有效副属性定位为暴击、暴击伤害、速度、攻击加成
  -ESPN EFFECTIVE_SECONDARY_PROP_NUM, --effective-secondary-prop-num 
                        与-ESP配合使用,限定1-6号位御魂的有效副属性加成次数（含初始次数）用逗号,间隔
                        例如"-ESP 暴击,暴击伤害 -ESPN 3,3,5,3,5,0"
                        意味着1、2、3、4、5、6号位御魂以暴击和暴击伤害为集合的有效属性集合，出现的总次数不低于3、3、5、3、5、0次
                        以一号位举例，暴击、暴击伤害的加成次数（含初始次数）为3次的分布可能有如下情况：
                        组合一：暴击*3、暴击伤害*0，即暴击+7.2、暴击伤害+0
                        组合二：暴击*2、暴击伤害*1，即暴击+4.8、暴击伤害+3.2
                        组合三：暴击*1、暴击伤害*2，即暴击+2.4、暴击伤害+6.4
                        组合四：暴击*0、暴击伤害*3，即暴击+0  、暴击伤害+9.6
```

## Usage of cm server

```
python ./calculator_of_Onmyoji/cm_server.py
```

Then open http://127.0.0.1:2019 in web browser, Chrome etc. The ip and port could support to be modified in future.

Request example:
```
curl http://127.0.0.1:2019/calculate -X POST -H "Content-Type: application/json" -d '{"src_filename":"data_Template.xls", "mitama_suit":"针女,4", "prop_limit":"暴击,90", "upper_prop_limit":",0", "sec_prop_value":",0", "fth_prop_value":",0", "sth_prop_value":",0", "ignore_serial":"","all_suit":"True","damage_limit":"0,0,0", "health_limit":"0,0,0","attack_only":"False","effective_secondary_prop":"","effective_secondary_prop_num":""}'

Note:
src_filename: source file must be in current directroy
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

or

python convert_json2xls.py -ESPS True
```

```
在转换成的excel中的“输出类有效条数”、“奶盾类有效条数”、“命中类有效条数”、“双堆类有效条数”、“混合类有效条数”下面的值为该类包含有效属性的有效条数，
其中:
“输出类”为包含 攻击加成、速度、暴击、暴击伤害的有效条数'
“奶盾类”为包含 生命加成、速度、暴击、暴击伤害的有效条数'
“命中类”为包含 效果命中、速度的有效条数'
“双堆类”为包含 效果命中、效果抵抗、速度的有效条数'
“混合类”为包含 攻击加成、速度、暴击、暴击伤害、生命加成、效果命中、效果抵抗的有效条数
“说明：首领御魂的固有属性也加入计算，因此最大可能达到12分以上”
```

## Usage of result\_combination

```
Cal independent combinations of mitama_results

usage: make sure files(*-result.xls) are in current directory

python calculator_of_Onmyoji/result_combination.py
```

## Test Command
```python calculator_of_Onmyoji/cal_mitama.py example/data_Template.xls result.xls -M 针女,4 -P 暴击,90```

## Calculate examples
```python calculator_of_Onmyoji/cal_mitama.py example/victor.xls v_result.xls -M 针女,4 -P 暴击,90.暴击伤害,50 -2P 攻击加成,55 -4P 攻击加成,55 -6P 暴击,55 -IG 天狗```

* 超星破势荒骷髅茨木
```python calculator_of_Onmyoji/cal_mitama.py example/victor.xls v_result.xls -M 破势,4.荒骷髅,2 -P 暴击,90.速度,16 -2P 攻击加成,55 -4P 攻击加成,55 -6P 暴击,55 -DL 3216,150,17120 -AO True -ESP 暴击,暴击伤害,攻击加成,速度 -ESPN 3,3,3,3,3,0```

* 190速150命中招财凤凰火
```python calculator_of_Onmyoji/cal_mitama.py example/victor.xls v_result.xls -M 招财猫,4 -P 速度,84,效果命中,150 -2P 速度,57 -4P 效果命中,55  -AS False -ESP 速度,效果命中 -ESPN 3,3,3,0,3,3```

* 辉夜姬蚌精盾
```python calculator_of_Onmyoji/cal_mitama.py example/victor.xls v_result.xls -M 蚌精,4 -P 暴击,95 -2P 生命加成,55 -4P 生命加成,55 -6P 暴击,55  -HL 13785,150,40000 -AS False -ESP 暴击,暴击伤害,生命加成,速度 -ESPN 5,3,5,3,5,0```

* 散件爆伤面灵气
```python calculator_of_Onmyoji/cal_mitama.py example/victor.xls v_result.xls -M 暴击,2.暴击,2.暴击,2 -P 暴击,92 -2P 攻击加成,54 -4P 攻击加成,54 -6P 暴击伤害,89 -ESP 暴击,暴击伤害,攻击加成,速度 -ESPN 3,3,3,3,3,0```

* 散件生生暴蜃气楼书翁
```python calculator_of_Onmyoji/cal_mitama.py example/victor.xls v_result.xls -M 蜃气楼,2 -P 暴击,92 -2P 生命加成,55 -4P 生命加成,55 -6P 暴击,55 -ESP 暴击,暴击伤害,生命加成,速度 -ESPN 3,3,3,3,3,0```

## Make tar for release
```tar zcf calculator.tar.gz calculator_of_Onmyoji example dist doc LICENSE README.md requirements.txt setup.* win_compile.txt```

## Related projects
* web-UI https://github.com/yinxin630/yys-yuhun-calculator-ui
