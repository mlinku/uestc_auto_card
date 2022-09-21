#### uestc学号自动健康填报

#### 配置流程

1.  点击右上角Fork本项目到你自己的库中

2.  点击你库中的本项目，开启Action中的工作流（点击Action，再点击工作流列表中的Daily autoCard将其启动）

3.  点击Settings，找到Secrets中的Actions，分别添加`USERNAME`和`PASSWORD`属性，输入`学号`和`信息门户密码`

4. 如果需要打卡后的wx推送服务，本项目提供了`WxPusher`接口，可以注册后同样在3中添加`TOKEN`和`UIDS`属性。（相关文档链接：https://wxpusher.dingliqc.com/docs/）




