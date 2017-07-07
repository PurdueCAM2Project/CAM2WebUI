# Contact Us

## Goal
Under email_system app, creating a page for user to contact our website.

## Approach
Using a form that requires user to input "Name, email, subject and message" and the content into an email template. And then email admin. 
In `forms.py`:
```
    class ContactForm(forms.Form):
        name = forms.CharField(required=True)
        from_email = forms.EmailField(required=True)
        subject = forms.CharField(required=True)
        message = forms.CharField(widget=forms.Textarea, required=True)
```
2 new urls needed to be linked: one for contact us, and one for notifying user the email has been sent.
In `urls.py`, add:
```
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^email_sent/$', views.email_sent, name='email_sent'),
```
2 new views corresponding to the two urls are added.
The one that tells user email has been seet only needs a template:
```
    def email_sent(request):
        return render(request, 'email_system/email_sent.html')
```
The second one is the view for contact us page:
First we get everything user input and add them into our email template. And then we email our website host.
```
    def contact(request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                #get info from form
                name = form.cleaned_data['name']
                from_email = form.cleaned_data['from_email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                #add info to email template
                content = render_to_string('email_system/contact_email_template.html', {
                    'name': name,
                    'from_email': from_email,
                    'message': message,
                })
                try:
                     send_mail(subject, content, from_email, [EMAIL_HOST_USER])#email admin
                except:
                    messages.error(request, 'Email sent failed.')  # error message

                return redirect('email_sent')
        else:
            form = ContactForm()
        return render(request, "email_system/contact.html", {'form': form})
```

### Template
Email template:
`contact_email_template.html`
```
    Contact Name:
    {{ name }}

    Email:
    {{ from_email }}

    Content:
    {{ message }}
```

Tempalte for web page that tells user the email has been sent:
```
    {% block content %}
        <h4 id="emailconfirm">Email Successfully sent</h4>
        <p>Thank you for your message. <br>
        We will read it as soon as possible!</p>
        <p><a style="color: deepskyblue" href="/">Go back to home page</a></p>
    {% endblock %}
```  

Template for contact us page:
```
    {% extends "app/base.html" %} 
    {% block title %}Contact us{% endblock %}
    {% load static %} 
    {% block css %}
    <link rel="stylesheet" href="{% static "app/css/contact.css" %}" />
    {% endblock %} 
    {% block content %}
    <div class="container">
      <hr class="divide-divider">
      <div class="center">Contact Us </div>
      <hr class="divide-divider">
      <form id="contact-us" method="post" action="/email/contact/">
        {% csrf_token %}
        <div class="col-xs-6 wow animated slideInLeft" data-wow-delay=".5s">
          <input type="text" name="name" id="name" required="required" class="form" placeholder="Your Name" />
          <input type="email" name="from_email" id="from_email" required="required" class="form" placeholder="Your Email" />
          <input type="text" name="subject" id="subject" required="required" class="form" placeholder="Subject" /> </div>
        <div class="col-xs-6 wow animated slideInRight" data-wow-delay=".5s">
          <textarea name="message" id="message" class="form textarea" placeholder="Message"></textarea>
        </div>
        <div class="relative fullwidth col-xs-12">
          <button type="submit" id="submit" name="submit" class="form-btn semibold">Send Message</button>
        </div>
        <div class="clear"></div>
        {% for error in field.errors %}
            <p id="emailerror" style="color: red">{{ error }}</p>
        {% endfor %}
      </form>
    </div>
    {% endblock %}
```
