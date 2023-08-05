# https代理ip
<p>
<img src='https://img.shields.io/badge/author-%E5%B0%8F%E5%B7%9D-ff69b4.svg'>
<img src='https://img.shields.io/github/license/2239559319/courseDownload.svg?style=flat'>
<img src='https://img.shields.io/badge/python-3.0%2B-blue.svg'>
<img src='https://img.shields.io/badge/python-3.6-blue.svg'>
</p>

-----------
- 运行python3
- 第三方包requests
- 安装
```bash
pip install xiaochuanhttpsproxy
```
- 使用
```python
import xiaochuanhttpsproxy
xiaochuanhttpsproxy.start(2)
print(xiaochuanhttpsproxy.getip())
```
- 每次提取的ip有接近20个,start的参数为2
- 函数解释:start()  开始提取，参数为提取的页面数，一页100个初始ip, getip()获取随机ip

- start(1)的运行时间大概为2分钟，以此类推

---------------
联系

github:[@github][1],pypi:[pypi][2]

mail:w2239559319@outlook.com

[1]:https://github.com/2239559319/xiaochuanhttpsproxy
[2]:https://pypi.org/project/xiaochuanhttpsproxy/