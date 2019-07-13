#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import urllib2


def change_to_list(filename):
    content = open(filename,"r").read().strip()
    return list(content.split("\n"))


def traceroute_to_dict(filename):

    txtfile = open(filename,"r")
    content = txtfile.read().strip().split("\n")[1:]
    d=dict()

    for i in range(len(content)):

        line = content[i]
        if line[1].isdigit():
            if line[4] != "*" :
                ip = line.strip().split("  ")[1]
                asn = line.strip().split("  ")[3]
                iptest = ip.strip().split(" ")[0]
                url = "http://ip-api.com/csv/" + iptest
                req = urllib2.Request(url)
                res_data = urllib2.urlopen(req)
                res = res_data.read()
                if res.strip().split(",")[0] == "success" :
					isp=res.strip().split(",")[11]
					asn=res.strip().split(",")[12]
                else:
					isp= "*"
                latency=line.strip().split("  ")[2]
                route = line.strip().split("  ")[4]
                step = line[0:2]
            else:
                latency="*"
                asn = "*"
                route = "*"
                ip = "*"
                isp= "*"
                step = line[0:2]

            d[int(step)]=dict()
            d[int(step)]["ip"]=ip
            if int(step) < 3:
                d[int(step)]["ip"]="*.*.*.*(已隐藏)"
            d[int(step)]["latency"]=latency
            d[int(step)]["asn"]=asn
            d[int(step)]["route"]=route
            d[int(step)]["isp"]=isp

    return dict(d)

def traceroute_to_table(filename):
  d = traceroute_to_dict(filename)
  string = ""
  for i in sorted(d.keys()):
    x = d[i]
    template = """
  <tr>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  </tr>
  """
    string = string + template.format(i,x["ip"],x["route"],x["isp"],x["asn"],x["latency"]) + "\n"
    
    writefile = open(filename + "_table","w")
    writefile.write(string)
    writefile.close()


def dict_to_table(d,tab):

    table_class = "ui bottom attached tab segment"
    if tab == "first":
        table_class = table_class + " active"
    
    table_html = """
    
    <div class="{0}" data-tab="{1}">
<table class="ui very compact striped table">
  <thead>
    <tr><th>跳数</th>
    <th>IP</th>
    <th>路由</th>
	<th>ISP</th>
    <th>AS Number</th>
    <th>延迟</th>
  </tr></thead>
  <tbody>
    """.format(table_class,tab)

    for step in sorted(d.keys()):
        table_html = table_html + """
        
        <tr>
      <td>{0}</td>
      <td>{1}</td>
      <td>{2}</td>
      <td>{3}</td>
      <td>{4}</td>
	  <td>{5}</td>
    </tr>
        
        """.format(step,d[step]["ip"],d[step]["route"],d[step]["isp"],d[step]["asn"],d[step]["latency"])
    table_html = table_html + """
      </tbody>
</table>
</div>
    """
    return table_html

html = """

<html>
<head>
    <meta charset="UTF-8" id="home">
    <meta name="keywords" content="Zbench,Function Club,Bench Mark,VPS,主机博客,测评,测试脚本">
    <title>Zbench v1.0 HTML Output</title>
<link rel="stylesheet" type="text/css" href="https://cdn.bootcss.com/semantic-ui/2.2.13/semantic.min.css">
<script src="https://cdn.bootcss.com/jquery/3.1.1/jquery.min.js"></script>
<script src="https://cdn.bootcss.com/semantic-ui/2.2.13/semantic.min.js"></script>
</head>
<body>

<div class="ui attached stackable menu">
  <div class="ui container">
    <a class="item" onclick="javascript:scroller('home', 100);">
      <i class="home icon"></i> 主页
    </a>
    <a class="item" onclick="javascript:scroller('system', 300);">
      <i class="grid layout icon"></i> 系统信息
    </a>
    <a class="item" onclick="javascript:scroller('hdd', 600);">
      <i class="desktop icon"></i> 硬盘 I/O
    </a>
    <a class="item" onclick="javascript:scroller('net', 900);">
      <i class="sitemap icon"></i> 网络测试
    </a>
    <a class="item" onclick="javascript:scroller('route', 1600);">
      <i class="plug icon"></i> 路由追踪
    </a>
    <div class="ui simple dropdown item">
      更多
      <i class="dropdown icon"></i>
      <div class="menu">
        <a class="item" href="https://www.github.com/FunctionClub"><i class="edit icon"></i> 关于我们</a>
        <a class="item" href="https://github.com/FunctionClub/ZBench/"><i class="github icon"></i>Github </a>
      </div>
    </div>
    <div class="right item">
      <div class="ui">    
            <a href="https://github.com/FunctionClub/ZBench/">ZBench v1.0-Beta</a>
      </div>
    </div>
  </div>
</div>

<div class="ui hidden divider"></div>
<div class="ui container">
<div class="ui message red">
<i class="close icon"></i>
  <div class="header">
    您正在使用的是开发中的项目。
  </div>
  <p>此程序正处于开发版, 我们无法保证在运行过程中不会出错. 我们将在近期测试后放出正式版，敬请期待.</p>
</div>
</div>
<div class="ui hidden divider"></div>
<div class="ui container">
<div class="ui message">
  <div class="header">
    测试数据准确性说明
  </div>
  <p>请注意，所有的测试数据为测试时的实时数据. 我们不保证您的服务商会在日后一直使用保持完全相同的服务。数据仅供参考.</p>
</p>
</div>
</div>
<div class="ui hidden divider" id="system"></div>

<h2 class="ui center aligned icon header">
  <i class="circular Laptop icon"></i>
  系统信息
</h2>
<div class="ui hidden divider"></div>
<div class="ui container">
<table class="ui celled striped table">
  <thead>
    <tr> 
      <th>项目</th>
      <th>数据</th>
  </tr></thead>
  <tbody>
    <tr>
      <td class="collapsing">
        <i class="Microchip icon"></i> CPU 型号
      </td>
      <td>{0}</td>
    </tr>
    <tr>
      <td>
        <i class="Microchip icon"></i> CPU 核心数
      </td>
      <td>{1}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Microchip icon"></i> CPU 主频
      </td>
      <td>{2}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Archive icon"></i> 硬盘大小
      </td>
      <td>{3}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Lightning icon"></i> 内存大小
      </td>
      <td>{4}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Database icon"></i> SWAP 交换空间大小
      </td>
      <td>{5}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Bar Chart icon"></i> 在线时长
      </td>
      <td>{6}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Pie Chart icon"></i> 系统负载
      </td>
      <td>{7}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Windows icon"></i> 系统
      </td>
      <td>{8}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Columns icon"></i> 架构
      </td>
      <td>{9}</td>
      
    </tr>
    <tr>
      <td>
        <i class="File Code Outline icon"></i> 核心
      </td>
      <td>{10}</td>
      
    </tr>
    <tr>
      <td>
        <i class="Group Object icon"></i> 虚拟化技术
      </td>
      <td>{11}</td>
      
    </tr>
  </tbody>
</table>
</div>



<div class="ui hidden divider" id="hdd"></div>

<h2 class="ui center aligned icon header">
  <i class="circular Clone icon"></i>
  硬盘 I/O
</h2>
<div class="ui hidden divider"></div>
<div class="ui container">
<table class="ui celled striped table">
  <thead>
    <tr>
    <th>次数</th>
      <th>速度</th>
  </tr></thead>
  <tbody>
    <tr>
      <td class="collapsing">
        <i class="folder icon"></i> 第一次测试
      </td>
      <td>{12}</td>
    </tr>
    <tr>
      <td>
        <i class="folder icon"></i> 第二次测试
      </td>
      <td>{13}</td>
    </tr>
    <tr>
      <td>
        <i class="folder icon"></i> 第三次测试
      </td>
      <td>{14}</td>
    </tr>

  </tbody>
</table>
</div>






<div class="ui hidden divider" id="net"></div>
<h2 class="ui center aligned icon header">
  <i class="circular Internet Explorer icon"></i>
  网络测试
</h2>
<div class="ui hidden divider"></div>
<div class="ui container">
<table class="ui compact striped table">
  <thead>
    <tr>
      <th>节点</th>
      <th>IP 地址</th>
      <th>下载速度</th>
      <th>延迟</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CacheFly</td>
      <td>{15}</td>
      <td>{16}</td>
      <td>{17}</td>
    </tr>
    <tr>
      <td>Linode 日本</td>
      <td>{18}</td>
      <td>{19}</td>
      <td>{20}</td>
    </tr>
    <tr>
      <td>Linode 新加坡</td>
      <td>{21}</td>
      <td>{22}</td>
      <td>{23}</td>
    </tr>
    <tr>
      <td>Linode 英国</td>
      <td>{24}</td>
      <td>{25}</td>
      <td>{26}</td>
    </tr>
    <tr>
      <td>Linode 法兰克福</td>
      <td>{27}</td>
      <td>{28}</td>
      <td>{29}</td>
    </tr>
    <tr>
      <td>Linode 加拿大</td>
      <td>{30}</td>
      <td>{31}</td>
      <td>{32}</td>
    </tr>
    <tr>
      <td>Softlayer 达拉斯</td>
      <td>{33}</td>
      <td>{34}</td>
      <td>{35}</td>
    </tr>
    <tr>
      <td>Softlayer 西雅图</td>
      <td>{36}</td>
      <td>{37}</td>
      <td>{38}</td>
    </tr>
    <tr>
      <td>Softlayer 法兰克福</td>
      <td>{39}</td>
      <td>{40}</td>
      <td>{41}</td>
    </tr>
    <tr>
      <td>Softlayer 新加坡</td>
      <td>{42}</td>
      <td>{43}</td><td>{44}</td>
    </tr>
    <tr>
      <td>Softlayer 香港</td>
      <td>{45}</td>
      <td>{46}</td>
      <td>{47}</td>
    </tr>
    
    <tr>
      <td>Softlayer Vultr, Frankfurt, DE</td>
      <td>{48}</td>
      <td>{49}</td>
      <td>{50}</td>
    </tr>    
    
    <tr>
      <td>Softlayer Vultr, Paris, France</td>
      <td>{51}</td>
      <td>{52}</td>
      <td>{53}</td>
    </tr>       

    <tr>
      <td>Softlayer Vultr, London, UK</td>
      <td>{54}</td>
      <td>{55}</td>
      <td>{56}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Singapore</td>
      <td>{57}</td>
      <td>{58}</td>
      <td>{59}</td>
    </tr>    
    
    <tr>
      <td>Softlayer Vultr, New York (New Jersey)</td>
      <td>{60}</td>
      <td>{61}</td>
      <td>{62}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Tokyo, Japan</td>
      <td>{63}</td>
      <td>{64}</td>
      <td>{65}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Chicago, Illinois</td>
      <td>{66}</td>
      <td>{67}</td>
      <td>{68}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Atlanta, Georgia</td>
      <td>{69}</td>
      <td>{70}</td>
      <td>{71}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Miami, Florida</td>
      <td>{72}</td>
      <td>{73}</td>
      <td>{74}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Seattle, Washington</td>
      <td>{75}</td>
      <td>{76}</td>
      <td>{77}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Dallas, Texas/td>
      <td>{78}</td>
      <td>{79}</td>
      <td>{80}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Los Angeles, California</td>
      <td>{81}</td>
      <td>{82}</td>
      <td>{83}</td>
    </tr>    

    <tr>
      <td>Softlayer Vultr, Vultr, Sydney, Australia</td>
      <td>{84}</td>
      <td>{85}</td>
      <td>{86}</td>
    </tr>    

    <tr>
      <td>Softlayer Digital Ocean, NYC1(New York)</td>
      <td>{87}</td>
      <td>{88}</td>
      <td>{89}</td>
    </tr>    

    <tr>
      <td>Softlayer Digital Ocean, NYC2(New York)</td>
      <td>{90}</td>
      <td>{91}</td>
      <td>{92}</td>
    </tr>    
   
    <tr>
      <td>Softlayer Digital Ocean, AMS2(Amsterdam)</td>
      <td>{93}</td>
      <td>{94}</td>
      <td>{95}</td>
    </tr>    

    <tr>
      <td>Softlayer Digital Ocean, SFO1(San Francisco)</td>
      <td>{96}</td>
      <td>{97}</td>
      <td>{98}</td>
    </tr>    

    <tr>
      <td>Softlayer Digital Ocean, SGP1(Singapore)</td>
      <td>{99}</td>
      <td>{100}</td>
      <td>{101}</td>
    </tr>    

    <tr>
      <td>Softlayer Digital Ocean, LON1(London)</td>
      <td>{102}</td>
      <td>{103}</td>
      <td>{104}</td>
    </tr>    

    <tr>
      <td>Softlayer Digital Ocean, FRA1(Frankfurt)</td>
      <td>{105}</td>
      <td>{106}</td>
      <td>{107}</td>
    </tr>    
    
    <tr>
      <td>Softlayer Digital Ocean, TOR1(Toronto)</td>
      <td>{108}</td>
      <td>{119}</td>
      <td>{120}</td>
    </tr>    

    <tr>
      <td>Softlayer Digital Ocean, BLR1(Bangalore)</td>
      <td>{121}</td>
      <td>{122}</td>
      <td>{123}</td>
    </tr>    
  </tbody>
</table>
</dev>

<div class="ui hidden divider"></div>
<div class="ui container">
<table class="ui compact striped table">
  <thead>
    <tr>
      <th>节点</th>
      <th>上传速度</th>
      <th>下载速度</th>
      <th>延迟</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>上海电信</td>
      <td>{124}</td>
      <td>{125}</td>
      <td>{126}</td>
    </tr>
    <tr>
      <td>成都电信</td>
      <td>{127}</td>
      <td>{128}</td>
      <td>{129}</td>
    </tr>
    <tr>
      <td>西安电信</td>
      <td>{130}</td>
      <td>{131}</td>
      <td>{132}</td>
    </tr>
    <tr>
      <td>上海联通</td>
      <td>{133}</td>
      <td>{134}</td>
      <td>{135}</td>
    </tr>
    <tr>
      <td>重庆联通</td>
      <td>{136}</td>
      <td>{137}</td>
      <td>{138}</td>
    </tr>
    <tr>
      <td>北京电信</td>
      <td>{139}</td>
      <td>{140}</td>
      <td>{141}</td>
    </tr>
    <tr>
      <td>北京联通</td>
      <td>{142}</td>
      <td>{143}</td>
      <td>{144}</td>
    </tr>
    <tr>
      <td>湖南电信</td>
      <td>{145}</td>
      <td>{146}</td>
      <td>{147}</td>
    </tr>
  </tbody>
</table>
</div>

<div class="ui hidden divider" id="route"></div>
<h2 class="ui center aligned icon header">
  <i class="circular Blind icon"></i>
  路由追踪
</h2>

<div class="ui hidden divider"></div>
<div class="ui container">
<div class="ui top attached tabular menu">
  <a class="item active" data-tab="first">上海移动</a>
  <a class="item" data-tab="second">上海电信</a>
  <a class="item" data-tab="third">上海联通</a>
  <a class="item" data-tab="fourth">广东移动</a>
  <a class="item" data-tab="fifth">广东电信</a>
  <a class="item" data-tab="sixth">广东联通</a>
  <a class="item" data-tab="seventh">所在地IP</a>
</div>

"""


footer = """
</div>
</div>
<div class="ui hidden divider"></div>
<div class="ui visible message">
  <p>CopyRight 2016-2018 <a href="https://www.github.com/FunctionClub">Function Club</a>. All Right Reserved.   Published By <a href="https://www.geoseis.cn">Geoseis</a></p>
</div>

</body>
<footer>
<script type="text/javascript"> 
//平滑滚动支持
// 转换为数字
function intval(v)
{
    v = parseInt(v);
    return isNaN(v) ? 0 : v;
}
 
// 获取元素信息
function getPos(e)
{
    var l = 0;
    var t  = 0;
    var w = intval(e.style.width);
    var h = intval(e.style.height);
    var wb = e.offsetWidth;
    var hb = e.offsetHeight;
    while (e.offsetParent){
        l += e.offsetLeft + (e.currentStyle?intval(e.currentStyle.borderLeftWidth):0);
        t += e.offsetTop  + (e.currentStyle?intval(e.currentStyle.borderTopWidth):0);
        e = e.offsetParent;
    }
    l += e.offsetLeft + (e.currentStyle?intval(e.currentStyle.borderLeftWidth):0);
    t  += e.offsetTop  + (e.currentStyle?intval(e.currentStyle.borderTopWidth):0);
    return {x:l, y:t, w:w, h:h, wb:wb, hb:hb};
}
 
// 获取滚动条信息
function getScroll() 
{
    var t, l, w, h;
    
    if (document.documentElement && document.documentElement.scrollTop) {
        t = document.documentElement.scrollTop;
        l = document.documentElement.scrollLeft;
        w = document.documentElement.scrollWidth;
        h = document.documentElement.scrollHeight;
    } else if (document.body) {
        t = document.body.scrollTop;
        l = document.body.scrollLeft;
        w = document.body.scrollWidth;
        h = document.body.scrollHeight;
    }
    return { t: t, l: l, w: w, h: h };
}
 
// 锚点(Anchor)间平滑跳转
function scroller(el, duration)
{
    if(typeof el != 'object') { el = document.getElementById(el); }
 
    if(!el) return;
 
    var z = this;
    z.el = el;
    z.p = getPos(el);
    z.s = getScroll();
    z.clear = function(){window.clearInterval(z.timer);z.timer=null};
    z.t=(new Date).getTime();
 
    z.step = function(){
        var t = (new Date).getTime();
        var p = (t - z.t) / duration;
        if (t >= duration + z.t) {
            z.clear();
            window.setTimeout(function(){z.scroll(z.p.y, z.p.x)},13);
        } else {
            st = ((-Math.cos(p*Math.PI)/2) + 0.5) * (z.p.y-z.s.t) + z.s.t;
            sl = ((-Math.cos(p*Math.PI)/2) + 0.5) * (z.p.x-z.s.l) + z.s.l;
            z.scroll(st, sl);
        }
    };
    z.scroll = function (t, l){window.scrollTo(l, t)};
    z.timer = window.setInterval(function(){z.step();},13);
}
</script>
<script type="text/javascript">
//Tab功能支持
    $('.menu .item')
    .tab()
    ;
//Message工具
$('.message .close')
  .on('click', function() {
    $(this)
      .closest('.message')
      .transition('fade')
    ;
  })
;
//Model
$('.ui.basic.modal')
  .modal('show')
  .closable('false')
;
</script>
</footer>
</html>


"""

info = change_to_list("/tmp/info.txt")

speed = change_to_list("/tmp/speed.txt")

speed_cn = change_to_list("/tmp/speed_cn.txt")

shm = traceroute_to_dict("/tmp/shm.txt")
traceroute_to_table("/tmp/shm.txt")
shm_html = dict_to_table(shm,"first")

sht = traceroute_to_dict("/tmp/sht.txt")
traceroute_to_table("/tmp/sht.txt")
sht_html = dict_to_table(sht,"second")

shu = traceroute_to_dict("/tmp/shu.txt")
traceroute_to_table("/tmp/shu.txt")
shu_html = dict_to_table(shu,"third")

gdm = traceroute_to_dict("/tmp/gdm.txt")
traceroute_to_table("/tmp/gdm.txt")
gdm_html = dict_to_table(gdm,"fourth")

gdt = traceroute_to_dict("/tmp/gdt.txt")
traceroute_to_table("/tmp/gdt.txt")
gdt_html = dict_to_table(gdt,"fifth")

gdu = traceroute_to_dict("/tmp/gdu.txt")
traceroute_to_table("/tmp/gdu.txt")
gdu_html = dict_to_table(gdu,"sixth")

own = traceroute_to_dict("/tmp/own.txt")
traceroute_to_table("/tmp/own.txt")
own_html = dict_to_table(own,"seventh")

html = html.format(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10],info[11],info[12],info[13],info[14], \

speed[0],speed[1],speed[2],speed[3],speed[4],speed[5],speed[6],speed[7],speed[8],speed[9],speed[10],speed[11],speed[12],\

speed[13],speed[14],speed[15],speed[16],speed[17],speed[18],speed[19],speed[20],speed[21],speed[22],speed[23],\
speed[24],speed[25],speed[26],speed[27],speed[28],speed[29],speed[30],speed[31],speed[32],speed[33],speed[34],speed[35],speed[36],\
speed[37],speed[38],speed[39],speed[40],speed[41],speed[42],speed[43],speed[44],speed[45],speed[46],speed[47],speed[48],speed[49],\

speed[50],	speed[51],	speed[52],	speed[53],	speed[54],	speed[55],	speed[56],	speed[57],	speed[58],	speed[59],\
speed[60],	speed[61],	speed[62],	speed[63],	speed[64],	speed[65],	speed[66],	speed[67],	speed[68],	speed[69],\
speed[70],	speed[71],	speed[72],	speed[73],	speed[74],	speed[75],	speed[76],	speed[77],	speed[78],	speed[79],\
speed[80],	speed[81],	speed[82],	speed[83],	speed[84],	speed[85],	speed[86],	speed[87],	speed[88],	speed[89],\

speed_cn[0],speed_cn[1],speed_cn[2],speed_cn[3],speed_cn[4],speed_cn[5],speed_cn[6],speed_cn[7],speed_cn[8],speed_cn[9],speed_cn[10],speed_cn[11],speed_cn[12],\
speed_cn[13],speed_cn[14],speed_cn[15],speed_cn[16],speed_cn[17],speed_cn[18],speed_cn[19],speed_cn[20],speed_cn[21],speed_cn[22],speed_cn[23],\
speed_cn[24],speed_cn[25],speed_cn[26],speed_cn[27],speed_cn[28],speed_cn[29],speed_cn[30],speed_cn[31],speed_cn[32],speed_cn[33],speed_cn[34],speed_cn[35],speed_cn[36],\
speed_cn[37],speed_cn[38],speed_cn[39],speed_cn[40],speed_cn[41],speed_cn[42],speed_cn[43],speed_cn[44],speed_cn[45],speed_cn[46],speed_cn[47],speed_cn[48],speed_cn[49],\
speed_cn[50],	speed_cn[51],	speed_cn[52],	speed_cn[53],	speed_cn[54],	speed_cn[55],	speed_cn[56],	speed_cn[57],	speed_cn[58],	speed_cn[59],\
speed_cn[60],	speed_cn[61],	speed_cn[62],	speed_cn[63],	speed_cn[64],	speed_cn[65],	speed_cn[66],	speed_cn[67],	speed_cn[68],	speed_cn[69],\
speed_cn[70],	speed_cn[71],	speed_cn[72],	speed_cn[73],	speed_cn[74],	speed_cn[75],	speed_cn[76],	speed_cn[77],	speed_cn[78],	speed_cn[79],\
speed_cn[80],	speed_cn[81],	speed_cn[82],	speed_cn[83],	speed_cn[84],	speed_cn[85],	speed_cn[86],	speed_cn[87],	speed_cn[88],	speed_cn[89],\
speed_cn[90],	speed_cn[91],	speed_cn[92],	speed_cn[93],	speed_cn[94],	speed_cn[95],	speed_cn[96],	speed_cn[97],	speed_cn[98],	speed_cn[99],\
speed_cn[100],	speed_cn[101],	speed_cn[102],	speed_cn[103],	speed_cn[104],	speed_cn[105],	speed_cn[106],	speed_cn[107],	speed_cn[108],	speed_cn[109],\
speed_cn[110],	speed_cn[111],	speed_cn[112],	speed_cn[113],	speed_cn[114],	speed_cn[115],	speed_cn[116],	speed_cn[117],	speed_cn[118],	speed_cn[119],\
speed_cn[120],	speed_cn[121],	speed_cn[122],	speed_cn[123],	speed_cn[124],	speed_cn[125],	speed_cn[126],	speed_cn[127],	speed_cn[128],	speed_cn[129],\
speed_cn[130],	speed_cn[131],	speed_cn[132],	speed_cn[133],	speed_cn[134])	

html = html + shm_html + sht_html + shu_html + gdm_html + gdt_html + gdu_html + own_html + footer

web = open("/root/report.html","w")

web.write(html)

web.close()
