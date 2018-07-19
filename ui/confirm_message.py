from discord import Client, Channel, User

from ui.reaction import Reaction
from ui.reaction_message import ReactionMessage


class ConfirmMessage(ReactionMessage):
    def __init__(self, client: Client, channel: Channel, messages: list):
        super().__init__(client, channel, messages, [Reaction.DISMISS.value, Reaction.CONFIRM.value])

    async def wait_for_user_reaction(self, target_user: User=None):
        if self.message_literal is None:
            raise ValueError('message has not been sent yet')

        def check(reaction, user):
            if user:
                return str(reaction.emoji) in self.reactions and user == target_user
            return str(reaction.emoji) in self.reactions

        response = await self.client.wait_for_reaction(message=self.message_literal, check=check)
        if response:
            emoji_code = str(response.reaction.emoji)
            await self.client.edit_message(self.message_literal,
                                           self.reaction_messages.get(emoji_code))
            return emoji_code == Reaction.CONFIRM.value  # if the confirm button was clicked, then return truen
        else:
            await self.client.delete_message(self.message_literal)
            return None
