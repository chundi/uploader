# uploader

### 这是一道面试题，题目要求：
#### 背景介绍
用户在其设备上安装某个应用，该应用会向后台上传数据。你的任务是提供一个数据上传接口用来接收数据，并保存。

#### 关于数据
- 每个数据以文本形式存在，大小为 5M 以内。
- 数据按业务分类，分别有 debug log, 用户交易log，分别按天存储在用户端 (例如 debug-20160330, transaction-20160330)。
- 数据按天上传。
- 上传后的数据以文本形式保存在后台服务器的 /var/www/example.com/data/  目录里。

#### 接口要求
- 每个上传设备有一个唯一的设备 ID 。
- 使用签名机制 (HMAC) 替代身份验证机制，签名密钥由设备与后台共享。
- 每次上传都需要传递当前数据类别，设备 ID。
- 每次接口调用都需要上传当前时间，发起 5 分钟内的接口调用为合法调用。

#### 开发要求
- 用你熟悉的语言开发。
- 使用 git 进行版本控制，并可以通过 git log 展示开发过程（包括修复 bug，代码重构等）。
- 请在 github / bitbucket 上创建一个帐号，把开发好的代码上传。

### 安装及运行
先安装框架<a href='http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html'>Installing Pyramid</a>

然后在项目根目录执行 sh run.sh，会在6543端口起来一个服务。

- 接口名：log
- 请求方式：POST
- 参数：
    - sign : 签名
    - device_id : 设备ID
    - log_type : 日志类型
    - ts : 上传时间，需要时间戳，精确到秒
    - log : 日志文件

签名生成方式：

- device_id、log_type、ts按key进行字典升序排列，排序后的参数(key=value)用&拼接起来，如："device_id=abc&log_type=debug&ts=1460361074"。
- 然后将拼好的字符串进行urlencode编码，如："device_id%3Dabc%26log_type%3Ddebug%26ts%3D1460361074"。
- 再用HMAC-SHA1对编码后的字符串加密，hmac(secret_key, query_str, hashmethod)，hashmethod使用sha-1，secret_key为服务端与客户端共享的签名密钥。

成功会返回success，否则为失败。

