# SeleniumBase Demo（SeleniumBase + Pytest）

## 准备环境 (python 3.7.4)

### 安装Tesseract

``` s
# Ubuntu
sudo add-apt-repository ppa:alex-p/tesseract-ocr-devel
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev

# MacOS
brew install tesseract
```

[Tesseract Wiki for Windows](https://github.com/UB-Mannheim/tesseract/wiki)

* 下载最新[Tesseract](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200223.exe)
* 添加Tesseract-OCR安装路径（“C:\Program Files\Tesseract-OCR”）到用户系统环境变量Path中并重启对应IDE

## 安装Python依赖库

``` s
pip install -r requirements.txt

# If timeout, use command below
# 
# 清华：https://pypi.tuna.tsinghua.edu.cn/simple
# 阿里云：http://mirrors.aliyun.com/pypi/simple/
# 中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
# 华中理工大学：http://pypi.hustunique.com/
# 山东理工大学：http://pypi.sdutlinux.org/
# 豆瓣：http://pypi.douban.com/simple/
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

## 安装浏览器驱动

``` s
# 在Chrome浏览器地址栏中输入“chrome://version/”进行版本查看
# 脚本编写环境Chrome版本 79.0.3945.130
seleniumbase install chromedriver
# 如果版本更新到最新，可尝试最新chromedriver
seleniumbase install chromedriver latest
seleniumbase install geckodriver
seleniumbase install edgedriver
seleniumbase install iedriver
seleniumbase install operadriver
```

## 目录结构

``` s
├─guard: Guard项目
│  ├─config: 测试服务器相关配置文件
│  ├─data: 测试数据
│  ├─pages: POM页面
│  │  ├─classes: 封装类
│  │  └─components: POM组件
│  ├─tests: 测试用例 
│  │  ├─module: 模块测试
│  │  └─scenario: 场景测试
│  └─tools: 常用工具
└─utils: 基础工具类
```

## 执行用例

``` s
# 执行所有用例
pytest guard/tests/*/test_*.py --html=report/report.html --host=confidence.96 --headless --settings-file=settings.py --username=selenium --password=888888

# Redis无密码登录
pytest guard/tests/*/test_*.py --html=report/report.html --host=confidence.96 --headless --settings-file=settings.py --username=selenium --password=888888 --redis-without-password

# 使用OCR进行验证码识别登录
pytest guard/tests/*/test_*.py --host=confidence.96 --gui --settings-file=settings.py --ocr --username=selenium --password=888888

# 执行指定标记用例
pytest guard/tests/*/test_*.py -v -m "webtest" --html=report/report.html --host=confidence.96 --username=selenium --password=888888

# 执行用例并调试
pytest guard/tests/*/test_*.py -v -m "webtest" --html=report/report.html --host=confidence.96 --pdb -s --username=selenium --password=888888

# 执行用例并并设置重试次数
pytest guard/tests/*/test_*.py -v -m "webtest" --html=report/report.html --host=confidence.96 --maxfail=2 --username=selenium --password=888888

# 最大化窗口执行测试用例
pytest guard/tests/*/test_*.py -v -m "webtest" --html=report/report.html --host=confidence.96 --maximize-window --username=selenium --password=888888

# 执行用例使用指定浏览器
pytest guard/tests/module/test_portrait.py --html=report/report.html --host=confidence.96 --browser=(choose from 'chrome', 'edge', 'firefox', 'ie', 'opera', 'phantomjs', 'safari', 'android', 'iphone', 'ipad', 'remote')
```

