import logging

from django.core.mail import send_mail

class_docs = {'dress': 'https://petitballetacademy.com/static/docs/Dress%20&%20Conduct%20Code.pdf',
              'payment': 'https://petitballetacademy.com/static/docs/PaymentandAttendancePolicy.pdf',
              'Pre-Ballet': 'https://petitballetacademy.com/static/docs/Pre-Ballet%20Curriculum.pdf',
              'Kinder Ballet': 'https://petitballetacademy.com/static/docs/Kinder%20Ballet%20Curriculum.pdf',
              'Beginning Ballet': 'https://petitballetacademy.com/static/docs/Beginning%20Ballet%202%20Curriculum.pdf'}

logger = logging.getLogger('ballet')

def registration_email(enrollment):
    logger.info("Sending registration email.")
    subject = 'Petit Ballet Academy Registration'
    from_email = 'petitballetacademy@gmail.com'

    parent = enrollment.student.parent.name
    student = enrollment.student.name
    ballet_class = enrollment.dance_class.title
    day_of_week = enrollment.dance_class.day_of_week
    start_time = enrollment.dance_class.start_time

    location_address = enrollment.dance_class.location.street
    location_city = enrollment.dance_class.location.city
    location_code = enrollment.dance_class.location.zipcode

    to_email = [enrollment.student.parent.email]
    email = """
<img src="https://petitballetacademy.com/static/img/email_header.jpg" width="400" alt="Petit Ballet Header" title="Petit Ballet Header" style="display:block"></img>
<p>Hey %s,</p>

<p>We are so excited to have %s join our %s class! We wanted to let you know that %s is officially registered to join the %s class at %s. Classes begin the week of September 9th. %s's classes will be held at the following address:</p>
<p>
%s
<br/>
%s, Utah, %s
</p>

<p>Also, if %s has any friends that sign up that you've referred, we will give you $15 off your second month's tuition per new student (make sure they add you to the \"Referred By\" entry on the registration page)! Below, you will find documents relevant to the class:</p>

<p>
<a href="%s">Dress Code</a><br/>
<a href="%s">Attendance and Payment Policy</a><br/>
<a href="%s">Curriculum</a>
</p>

<p>If you have any questions about anything, please let us know.</p>

<p>We really look forward to seeing %s in class!</p>

<p>Best Regards,</p>

Marybeth Wilde (Dance Director)<br/>
385-404-8687""" % ( parent, student, ballet_class, student, ballet_class, str(start_time), student, location_address, location_city, location_code, student, class_docs.get('dress'), class_docs.get('payment'), class_docs.get( ballet_class, None), student )

    send_mail(subject,
              email,
              from_email,
              to_email,
              fail_silently=False,
              html_message=email)


    print "Sent email to %s" % str(to_email)
