# Zench

Linux VPS测评脚本：基于FunctionClub版本来的，没有很多变动。主要变化是增加了很多节点，方便查看全球范围内各测速点到VPS的速度。

## 说明

生成的HTML报告暂时只能保存在/root/report.html。因为FunctionClub的API用法我不熟悉，有时间再去改进。

示例(Demo)：[https://www.zhujiboke.com/zbench-example.html](https://www.zhujiboke.com/zbench-example.html)

## 脚本命令

这里只更新了ZBench.sh和ZPing-CN.py, Generate.py，暂时没有区分中英文版本。

    
英文版：

    wget -N --no-check-certificate https://raw.githubusercontent.com/chenxuzhen/ZBench/master/ZBench.sh && chmod a+rx ZBench.sh && sudo bash ZBench.sh
    
## 效果图

![1.png](1.png)


![2.png](2.png)

## 引用

* Bench.sh ( [https://teddysun.com/444.html](https://teddysun.com/444.html) )
* SuperBench ( [https://www.oldking.net/350.html](https://www.oldking.net/350.html) )
* python实现ping程序 ( [https://www.s0nnet.com/archives/python-icmp](https://www.s0nnet.com/archives/python-icmp) )
* Python 设置颜色 ( [http://www.pythoner.com/357.html](http://www.pythoner.com/357.html) )
* Kirito's Blog ( [https://www.ixh.me](https://www.ixh.me) )


