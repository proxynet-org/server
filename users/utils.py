from content.models import Message, Publication, Comment, PrivateMessage
from zone.models import Chatroom, ChatroomMessages

def delete_user_data(user):
    messages = Message.objects.filter(user=user)
    messages.delete()
    chatroomMessages = ChatroomMessages.objects.filter(user=user)
    chatroomMessages.delete()
    publications = Publication.objects.filter(user=user)
    publications.delete()
    comments = Comment.objects.filter(user=user)
    comments.delete()
    privateMessages = PrivateMessage.objects.filter(sender=user)
    privateMessages.delete()
    chatroom = Chatroom.objects.filter(owner=user)
    chatroom.delete()