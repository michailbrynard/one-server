from allauth.account.adapter import DefaultAccountAdapter

class MessageFreeAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template,
                        message_context=None, extra_tags=''):
        pass