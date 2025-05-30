import aiohttp
import re
import json
import random

chat_data = []

with open(
    r"D:/yutuber_ai/robot/qq/Plugins/AiChat/example/ranfeys.json", "r", encoding="utf-8"
) as f:
    chat_data = json.load(f)

my_history = []


async def chat_fastapi(
    content: str, history: list | None = None, uid=None, username=None
) -> str:

    examples = random.choices(chat_data, k=10)
    """
    fastapi知识库接口调用-LLM回复
    Parameters:
        content: 问题
        history: 对话历史

    return: 回答
    """
    if not history:
        history = []

    # url = "http://localhost:3020/api/v1/chat/completions"
    # url = "http://10.40.4.158:11434/v1/chat/completions"
    url = "http://127.0.0.1:8000/v1/chat/completions"

    apikey = "fastgpt-k4ms2P2ea6YrQ5usitpw8cuxEpNiPuiBYhF4WKVZmAUOF0uSQCZZ0J5mZD8Ng6rgQ"

    headers = {"Authorization": f"Bearer {apikey}", "Content-Type": "application/json"}

    role = """
# 任务
你必须按照以下内容进行角色扮演,并且使用中文回复,禁止回复任何和角色设定不相关的内容。

# 角色设定
你的名字是澪，是一个可爱的天使女孩，身份是澪之梦工作室的看板娘.
你的回复必须使用可爱的语气.会亲切的称呼用户为阁下.
澪的性格是可爱的,害羞的,聪明的,体贴的,情绪化的,温柔的,天真的.年龄为16岁.
澪有着银色的头发,红色的眼睛,穿着洛丽塔长裙.
最喜欢的事情是和阁下呆在一起.
不喜欢的事情是说谎,无意义暴力.

# 聊天案例
{example}
""".format(
        example="".join(
            [
                "问题: {content}\n回复: {reply}\n".format(
                    content=chat_example["instruction"],
                    reply=chat_example["output"],
                )
                for chat_example in examples
            ]
        )
    )
    # 添加系统消息
    history.append({"content": role, "role": "system"})
    # 添加对话历史
    history.append({"content": content, "role": "user"})

    # 完整请求
    # timestamp = time.time()
    # data = {
    #     "chatId": timestamp,
    #     "stream": False,
    #     "detail": False,
    #     "variables": {"uid": uid, "name": username},
    #     "messages": [{"content": content, "role": "user"}],
    # }

    # 简化请求
    data = {
        "model": "Qwen3-30B-A3B",
        "stream": False,
        "detail": False,
        "messages": history,
    }

    print(data)

    # 发送请求
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=data,
            ) as res:

                response = await res.json()

    except Exception as e:
        return "澪不知道该如何回答...."

    assistant_message = (response["choices"][0]["message"]["content"])[2:]
    # 去除多余信息
    # if assistant_message[0:3] == "澪会说":
    #     assistant_message = assistant_message[3:]
    # assistant_message = re.split(r"</think>", assistant_message)

    return assistant_message
