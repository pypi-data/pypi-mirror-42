

# v-0.0.9

修改 sms 和 email 模板 同时支持 python2 和  python3


# v-0.0.10

修改钉钉模板，支持Markdown 消息类型

# v-0.0.11

dingding 模块中 关于python2 和Python3支持 configparser 的问题

# v-0.0.12

邮件发送附件支持各类压缩格式


# v1.0.0

修改短信、钉钉、邮件发送结果为 json 格式

# v1.0.2

添加七牛上传功能, 
默认一般文件上传之后存放在
    files/20190213/xxxx.txt
图片/js/css 上传之后存放在 （images/js/css）
    static/images/20190213/xxxx    

首先需要自定义配置文件：

    cat xx.conf
    [bucketname]
    bucket_name = bucketname
    access_key = xxxxx
    secret_key = xxxx

Demo:

from cwstools.Qiniu import qiniuInstance

demo = qiniuInstance()
demo.configfile = xx.conf
demo.section = bucketname
demo.local_filename = real_local_file.txt
demo.filetype = "file" 
demo.upload_file()


