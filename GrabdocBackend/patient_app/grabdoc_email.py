from django.core.mail import send_mail


def send(subject,message,to):

    try:

        send_mail(
            subject,
            message,
            "pudaykumar@eitacies.com",
            [to],
            fail_silently=False,
        )
    except  Exception as e:
        print(e)
        

