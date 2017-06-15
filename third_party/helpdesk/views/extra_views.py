from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from helpdesk.models import (Ticket, FollowUp, Attachment,
                             TicketChange,Attachment)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from helpdesk.helpers import send_reply_email


@login_required
def reply_ticket(request,ticket_id):
    """reply ticket to the client"""
    if not (request.user.is_authenticated() and
            request.user.is_active and (
                request.user.is_staff )):
        return HttpResponseRedirect('%s?next=%s' %
                                    (reverse('staff/login'), request.path))
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        comment = request.POST.get('comment', '')
        new_status = int(request.POST.get('new_status', ticket.status))
        if not all([title, comment]):
            return render(request, 'helpdesk/reply_ticket.html',
                  {'ticket': ticket,})
        #save models
        f = FollowUp(public=True,ticket=ticket, date=timezone.now(), comment=comment,user=request.user)
        f.title = 'Email:{}'.format(title)
        if new_status != ticket.status:
            ticket.status = new_status
            ticket.save()
            f.new_status = new_status
        f.save()
        #save attachment
        files = []
        if request.FILES:
            import mimetypes
            for file in request.FILES.getlist('attachment'):
                print(dir(file))
                filename = file.name
                a = Attachment(
                    followup=f,
                    filename=filename,
                    mime_type=mimetypes.guess_type(filename)[0] or 'application/octet-stream',
                    size=file.size,
                    )
                a.file.save(filename, file, save=False)
                a.save()
                files.append([a.filename, a.file])
        if new_status in [ Ticket.RESOLVED_STATUS, Ticket.CLOSED_STATUS ]:
            if new_status == Ticket.RESOLVED_STATUS:
                ticket.resolution = comment
                ticket.save()
        #send email
        send_reply_email(
            files=files,
            subject = title,
            body = comment,
            recipients=[ticket.submitter_email],
            sender = ticket.queue.from_address,
            fail_silently=True
        )
        return HttpResponseRedirect(ticket.get_absolute_url())
    return render(request, 'helpdesk/reply_ticket.html',
                  {'ticket': ticket,})