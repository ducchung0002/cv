import smtplib
from email.mime.text import MIMEText

email = "102210030@sv1.dut.udn.vn"
recovery_code = 123456

msg = MIMEText(f"Mã khôi phục mật khẩu của bạn là {recovery_code}. Mã này chỉ có hiệu lực trong vòng 2 phút.")
msg["Subject"] = "Mã khôi phục mật khẩu"
msg["From"] = "ducchung2444@gmail.com"
msg["To"] = email
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login("ducchung2444@gmail.com", "fymizjaxqsrqfjzb")
smtp.send_message(msg)
smtp.quit()