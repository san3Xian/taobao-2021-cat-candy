# 淘宝2021 双十一预热 喵糖活动 python脚本
- 无售后支持
- 纯属无聊玩玩
- python新手基于精度玄学的OpenCV实现
- 只支持浏览15秒和逛逛类型的任务

# 环境准备
- python3
- python3 module: opencv-python
- adb (需要已写入PATH环境变量中，即在cmd或者shell中可直接执行`adb`)
- macos(windows 没完全测过，理论上可以,在等待淘宝执行任务过程中倒计时日志输出可能会重复输出)

# 食用姿势
1. 安卓打开usb调试，在电脑使用`adb devices`确保能看到相应的设备
2. 手机进入淘宝，进入喵糖活动页
3. `python3 view-task.py`
4. 如果已经打开了任务列表，可以使用命令 `python3 view-task.py {任意参数}` 直接开始搜索可执行任务
5. 当搜索不到可执行任务以后，终端日志会提示`runable task not found`,此时在python弹出的图片窗口中按下任意按钮结束程序

# 暂时不支持的任务 / 行为
- 游戏小互动 (可能会写)
- 跳转到支付宝的一切活动
- 滚动任务列表中的任务

# 常见异常
- 更换手机使用脚本的时候，需要根据log回显调整`view-task.py`中的`thresold`（阈值）以匹配到相应的目标，`thresold`（阈值）取值根据log回显中的`max_loc:`最后的数字调整即可
- 每天第一次做任务遇到'天天好房'引导页还不会识别退出