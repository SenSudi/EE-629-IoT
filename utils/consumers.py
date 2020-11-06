from channels.sessions import enforce_ordering
from channels import Group
from channels.sessions import channel_session
from channels.auth import (
    http_session_user,
    channel_session_user,
    channel_session_user_from_http,
)

# @enforce_ordering(slight=True)
@channel_session_user_from_http
def ws_connect(message):
    if message.channel_session["group"] == "":
        message.reply_channel.send({"accept": True})
        message.channel_session["group"] = group = "testers"
        Group("%s" % group).add(message.reply_channel)
        # Group('%s'%message.channel_session['group']).send({
        # 	'text': '%s has logged in'%message.user,
        # })


# @enforce_ordering(slight=True)
@channel_session_user
def ws_message(message):
    # "Echoes messages back to the client"
    # message.reply_channel.send({
    #     "text": message['text'],
    # })
    Group("%s" % message.channel_session["group"]).send({"text": message["text"]})


# @enforce_ordering(slight=True)
@channel_session_user
def ws_disconnect(message):
    Group("%s" % message.channel_session["group"]).discard(message.reply_channel)
    Group("%s" % message.channel_session["group"]).send(
        {"text": "%s has logged out" % message.user}
    )
