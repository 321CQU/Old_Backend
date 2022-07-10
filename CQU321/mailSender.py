import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header


class mailSender():
    def __init__(self, receiver, file_paths, receiver_name):
        self.SMTP_host = 'mail.zhulegend.com'
        self.sender = '321cqu@zhulegend.com'
        self.password = 'CQUz5321'
        self.receiver = [receiver]
        self.name = receiver_name
        self.message = MIMEMultipart()
        self.file_paths = file_paths
        self.is_success = False

        self.message['From'] = Header("321CQU团队", 'utf-8')
        self.message['To'] = Header(self.name, 'utf-8')
        subject = '个人志愿时长文件'
        self.message['Subject'] = Header(subject, 'utf-8')
        content = self.name + '同学： \r\n    你好！\r\n    以下是您选择的个人志愿时长相关pdf，感谢您对321CQU小程序的支持，如果有任何问题请在反馈界面反馈或者加入321CQU反馈qq' \
                              '群：101158269进行反馈，谢谢！'
        self.message.attach(MIMEText(content, 'plain', 'utf-8'))
        self._add_attach()
        try:
            smtpObj = smtplib.SMTP(self.SMTP_host, 25)
            smtpObj.login(self.sender, self.password)
            smtpObj.sendmail(self.sender, self.receiver, self.message.as_string())
            smtpObj.quit()
            self.is_success = True
        except smtplib.SMTPException:
            self.is_success = False

    def _add_attach(self):
        if len(self.file_paths) == 0:
            return

        for file_path in self.file_paths:
            att = MIMEApplication(open(file_path, 'rb').read())
            att["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            file_name = file_path.split('/')[-1]
            att.add_header("Content-Disposition", 'attachment', filename=('utf-8', '', file_name))
            self.message.attach(att)

    def get_response(self):
        return self.is_success



if __name__ == '__main__':
    sender = mailSender('2961163526@qq.com', ['./刘泯杉+王超+朱子骏+重庆大学.pdf'], "朱子骏")

