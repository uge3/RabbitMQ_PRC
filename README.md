# RabbitMQ_PRC
基于RabbitMQ rpc实现的主机管理

可以对指定机器异步的执行多个命令

例子：

:run "df -h" --hosts 192.168.3.55 10.4.3.4

task id: 45334

: check_task 45334 #查看任务信息

程序结构:

RabbitMQ_PRC/#综合目录

|- - -PRC_CLIENT/#client程序主目录

|       |- - -init.py

|       |- - -bin/#执行程目录

|       |      |- - -init.py

|       |      |- - -clien_start.py #客户端执行文件

|       |

|       |

|       |- - -core #主逻辑程序目录

|       |      |- - -init.py

|       |      |- - -clien_class.py#客户端执行主要逻辑 类

|       |

|       |

|

|

|- - -PRC_SERVER/#服务端程序目录

|       |- - -init.py

|       |- - -bin/#执行目录

|       |     |- - -init.py

|       |     |- - -server_start.py#服务端程序执行文件

|       |

|       |

|       |- - -core/##主逻辑程序目录

|       |     |- - -server_class.py#主逻辑 相关类

|       |

|

|- - -README