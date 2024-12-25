from django.shortcuts import render
from django.http import JsonResponse
import random
from .models import Notification
from django.contrib import messages



# create notificatoion model and embed it in all the views
# create a mark as read and delete notification view
# delete notification not requeired just create a mark as read which will just mark the notification as read and remove it from the fronend and



# front end done embed notifications model in all the views
# generate notifications and test the mark as read and delete notification view




def getNotifications(request):
    # send only the unread notifications
    user = request.user
    notifications = Notification.objects.filter(user=user,read=False)
    data = []
    for notification in notifications:
        data.append({
            'content':notification.content,
            'id':notification.id
        })
    print(list(notifications.values()))
    return JsonResponse({
        'notifications':data})

    # return JsonResponse({
    #     'content':"You have 5 new notifications",
    #     'id':id,})


def markAsRead(request,id):
    try:
        notification = Notification.objects.get(id=id)
        if request.user != notification.user:
            return JsonResponse({
                'Error':"You are not authorized to perform this action"})
        notification.read = True
        notification.save()
        return JsonResponse({
            'Success':"Marked as read"})
    except:
        pass
        return JsonResponse({
            'Error':"Notification not found"})
    
