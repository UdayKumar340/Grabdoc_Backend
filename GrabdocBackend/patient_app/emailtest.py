from django.core.mail import send_mail


result = send_mail(
    "Subject here",
    "Here is the message.",
    "pudaykumar@eitacies.com",
    ["udaykumarpanasam@gmail.com"],
    fail_silently=False,
)

print(result)