# 短剧故事谱系与首播差异化审议

短剧剧本、审读证据和频道排档。相同 work 的多个 edition 为剪辑或剧本版本。不同渠道的 audience 是去重后的人群量级。对应证据的 known_on 为审读取得的日期。

## 资料格式

样例均为合成记录。CSV 使用 UTF-8，首行为列名。日期或时间采用 ISO 表示，多值字段以竖线分隔，空单元格表示该来源未记录。保留多版记录和部分未匹配的业务事实可供复查。

- editions.csv 的字段为 edition、work、rev、predecessor、submitted、ready_on、kind。
- beats.csv 的字段为 edition、beat、position、character、choice、event、ending。
- readings.csv 的字段为 fact、left_beat、right_beat、property、evidence、known_on。
- lineage.csv 的字段为 record、edition、source、field、authorization、confirmed_on。
- airings.csv 的字段为 broadcast、edition、channel、region、audience、on_day、theme。
- slots.csv 的字段为 slot、channel、region、day、units、limited_kind。
- commitments.csv 的字段为 commitment、work、edition、channel、slot、exclusive_to、state、at。
- program_periods.csv 的字段为 review、start、end、lookback_months、announced_floor、at。

## 查验资料

使用 Python 3.11 及以上版本。资料检查只使用 Python 标准库。请在项目根目录运行。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
