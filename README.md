# uploader

先安装框架<a href='http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html'>Installing Pyramid</a>

然后在项目根目录执行 sh run.sh，会在6543端口起来一个服务器。

接口名：log
请求方式：POST
参数：

	* sign:签名
	* device_id:设备ID
	* log_type:日志类型
	* ts:上传时间，需要时间戳，精确到秒

签名生成方式：

device_id、log_type、ts按key进行字典升序排列，排序后的参数(key=value)用&拼接起来，如："device_id=abc&log_type=debug&ts=1460361074"。
然后将拼好的字符串进行urlencode编码，如："device_id%3Dabc%26log_type%3Ddebug%26ts%3D1460361074"。
再用HMAC-SHA1对编码后的字符串加密，hmac(secret_key, query_str, hashmethod)，hashmethod使用sha-1，secret_key为服务端与客户端共享的签名密钥。

成功会返回success，否则为失败。

