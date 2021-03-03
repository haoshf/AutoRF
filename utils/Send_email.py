#coding=utf8
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from repository import models

# 第三方 SMTP 服务
mail_host = "smtp.mxhichina.com" # SMTP服务器
mail_user = "haosf@jvtd.cn" # 用户名
mail_pass = "Lu201314" # 授权密码，非登录密码
sender = 'haosf@jvtd.cn'# 发件人邮箱(最好写全, 不然会失败)
#邮件配置
receivers = ['haosf@jvtd.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

def sendEmail(project_id,log_path):

    date = datetime.datetime.now().strftime('%Y-%m-%d %X')
    smtp = models.Smtp.objects.filter(project_name=project_id).first()
    if smtp.enable:

        title = smtp.title.replace('${date}',date).replace('${project}',smtp.project_name.project_name)  # 邮件主题
        # message = MIMEText(content, 'plain', 'utf-8') # 内容, 格式, 编码
        message = MIMEMultipart()
        message['From'] = "{}".format(smtp.mail_user)
        message['Subject'] = title
        message.attach(MIMEText(smtp.documentation.replace('${date}',date).replace('${project}',smtp.project_name.project_name), 'html', 'utf-8'))
        att1 = MIMEText(open('%slog.html'%log_path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="log.html"'
        message.attach(att1)
        att2 = MIMEText(open('%sreport.html'%log_path, 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="report.html"'
        message.attach(att2)

        try:
            smtpObj = smtplib.SMTP_SSL(smtp.mail_host, 465) # 启用SSL发信, 端口一般是465
            smtpObj.login(smtp.mail_user, smtp.mail_pass) # 登录验证
            message['To'] = smtp.receivers.replace('\n','').replace('\t','')
            receivers = message['To'].split(',')
            smtpObj.sendmail(smtp.mail_user, receivers, message.as_string()) # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)

# def send_email2(SMTP_host, from_account, from_passwd, to_account, subject, content):
#     email_client = smtplib.SMTP(SMTP_host)
#     email_client.login(from_account, from_passwd) # create msg
#     msg = MIMEText(content, 'plain', 'utf-8')
#     msg['Subject'] = Header(subject, 'utf-8') # subject
#     msg['From'] = from_account
#     msg['To'] = to_account
#     email_client.sendmail(from_account, to_account, msg.as_string())
#     email_client.quit()

# if __name__ == '__main__':
#     sendEmail()

    return True