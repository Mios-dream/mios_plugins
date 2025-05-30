from Core.Plugin import Plugin
from functools import singledispatchmethod
from Models.Context.GroupMessageContext import GroupMessageContext
from Models.MessageChain.Message import Text, Reply
from Models.MessageChain.MessageChain import MessageChain
from Plugins.AiChat.fastchat import chat_fastapi


class AiChat(Plugin):

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):
        # 以/开头为指令
        if context.Event.Message[0]:
            if context.Event.Message[0][0] == "/":
                # 调用fastchat进行回复
                response = await chat_fastapi(context.Event.Message[0][1:])
                # 如果回复超过30字或者随机数小于0.3则只回复文字
                # if len(response.encode("utf-8")) // 4 < 30:
                messageChain = (
                    MessageChain()
                    .add(Reply(context.Event.Message_ID))
                    .add(Text(response))
                )
                await context.Command.Reply(messageChain)

        # 以@机器人 为指令
        if context.Event.At:
            if context.Event.At[0] == context.Event.Robot:

                # 调用fastchat进行回复
                response = await chat_fastapi(context.Event.Message[0])
                messageChain = (
                    MessageChain()
                    .add(Reply(context.Event.Message_ID))
                    .add(Text(response))
                )
                await context.Command.Reply(messageChain)

    def dispose(self):
        pass
