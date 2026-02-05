from django.core.mail import send_mail


def send_email(subject, message, from_email, to_email):
    to_email = to_email if isinstance(to_email, list) else [to_email,]
    # to_email(수신자)이 list형태면 to_email그대로 반환, 아니라면 []로 감싸준다!
    send_mail(subject, message, from_email, to_email)
    # 발신자

