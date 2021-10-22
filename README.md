Zucc自动打卡

1. `config.json`中配置学号密码

2. 服务器中配置计划任务

   ```bash
   crontab -e
   # 写入
   0 9 * * * python /path/to/main.py > /path/to/log
   # 每天9点执行一次脚本
   
   # exmaple
   0 9 * * * python3 /root/repo/ZUCC_clock_in/main.py > /root/repo/ZUCC_clock_in/log
   ```

   

**打卡的具体信息可能更新，代码也需要更新**
