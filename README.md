# httpscan

[Forked版本]

httpscan是一个扫描指定CIDR网段的Web主机的小工具。和端口扫描器不一样，httpscan是以爬虫的方式进行Web主机发现，因此相对来说不容易被防火墙拦截。

httpscan会返回IP http状态码 Web容器版本 以及网站标题。

**Usage**：`python2 httpscan IP/CIDR –t threads`

Example:


```
(venv) ❯❯❯❯ python2 httpscan.py 192.168.31.0/24 -t 16                                                                                                   ~/w/httpscan master
+----------------+------+--------------------+------------------------------+
|     IP         |Status|       Server       |            Title             |
+----------------+------+--------------------+------------------------------+
|192.168.31.1    |200   |nginx               |小米路由器               
+----------------+------+--------------------+------------------------------+
(venv) ❯❯❯❯    
```


NOTE: 后续准备用python3重新一遍