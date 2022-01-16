Zucc自动打卡

1. `config.json`中配置学号、密码、疫苗情况等

   ```json
   {
     "user": [
       {
         "username": "xxxxxxxx",
         "password": "xxxxxx",
         "vaccine": "1",
         "address": "浙江省 杭州市 西湖区",
         "tag": "张三",
         "email": "xxxx@qq.com"
       },
       {
         "username": "xxxxxxxx",
         "password": "xxxxxx",
         "vaccine": "2",
         "address": "",
         "tag": "李四",
         "email": ""
       }
     ],
     "email": {
       "host": "smtp.qq.com",
       "username": "xxxxx@qq.com",
       "password": "xxxxxxx",
       "receiver": "xxxxx@qq.com"
     }
   }
   ```

   （必填）**`vaccine`（疫苗）选项**(2021-12-31)更新

   > 1. 已接种两针剂疫苗（科兴、生物等）第一针
   > 2. 已接种两针剂疫苗（科兴、生物等）第二针
   > 3. 已接种两针剂疫苗（科兴、生物等）加强针
   > 4. 已接种三针剂疫苗（安徽智飞）第一针
   > 5. 已接种三针剂疫苗（安徽智飞）第二针
   > 6. 已接种三针剂疫苗（安徽智飞）第三针
   > 7. 未接种疫苗

   （选填）**`address` 选项**填写假期时所在地，具体格式遵循 `省 市 区`（建议先手动打卡再准确填入，注意空格！），默认空字符串为学校地址

   （选填）**`tag` 选项**填写学号对应的姓名或联系方式等，方便辨识，只在日志输出时起作用

   （选填）**`email` 选项**填写当前打卡人的邮箱，通知对方打卡成功（`email -> receiver` 是自动打卡服务部署者邮箱，推送所有人打卡情况及服务启动异常）

2. 服务器中配置计划任务

   ```bash
   crontab -e
   # 写入
   0 9 * * * cd /path/to && /usr/bin/python3 main.py >> log
   # 每天9点执行一次脚本
   # 注意目录和文件的权限足够
   ```

**打卡的具体信息可能更新，代码也需要更新**
