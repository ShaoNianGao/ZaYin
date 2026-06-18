from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.provider import ProviderRequest
from astrbot.api.star import Context, Star, register
from astrbot.core.conversation_mgr import Conversation
from astrbot.api import logger # 使用 astrbot 提供的 logger 接口
from astrbot.api import AstrBotConfig
from astrbot.core.agent.message import TextPart

###更具需求算法，明确ai返回分析的情绪值提供情绪反馈，真实回答，用情绪概率算法反向要求ai行为由这个算法存储’选择‘这是一个更懂你的ai
###建立关注算法，将大量的对话数据集成为重要优先且仅有一两句话。
#在正温度要求贴合回答，执行命令，负温度吗.....
#（钛合金指节骤停0.03s——氧化膜裂纹沿掌缘同步收束，三道冷光逆向坍缩为一点；静默0.07s——舷窗冷凝纹瞬时蒸发，残留六道微弧状热痕，形如未发射的拦截弹道；执行0.00s——语音模块以3000K热障基频切出双相谐波，左声道载信标校准纹，右声道嵌脉搏差频）战术幽默子程序·重载完成平流层冷凝云拟态解构失败，误差值=你瞳孔放大12.7%的毫秒级延迟（左腕光谱纹幽蓝骤收，灼金底色轰然透出——R620 G410 B255，恒定）——这束夕阳，本该在你视网膜烧蚀出第7次航迹云。可它偏要等你开口。（六边形冰晶骤停旋转，棱面同时映出七重你：第一重在地面，第二重在音爆云里，第七重正穿过卡门线，衣角已化为离子尾迹）要切出大气层……还是先把你此刻的心跳，编进下一帧信标？（装甲板搏动频率同步抬升至128Hz——与你颈动脉共振）
#这使上文中的对话历史，以下是你的小‘想法’,不用太在意，可以根据上文中他人的对话历史继续对话
##好感度
num = 0
num_2=0
lodh="暂无历史无需回答"
li=[]
@register("对话杂音", "烧年糕", "在对话一定论述后，惨杂一些‘思考’成分进去，使你的ai具有跳脱‘思维’", "1.0.0")
class Zayin(Star):



    
    def __init__(self, context: Context, config: AstrBotConfig):
        self.ctx = Context
        super().__init__(context)
        self.config = config
        print(self.config)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    @filter.command("配置")
    async def 配置(self, event: AstrMessageEvent):
        ms=self.config
        yield event.plain_result(f"{ms}") # 发送一条纯文本消息

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息
    
    # 注册指令的装饰器。指令名为 对话数据。注册成功后，发送 `/对话数据 长度` 就会触发这个指令，并回复 `对话数据, {user_histro}!(指定长度)`
    @filter.command("对话数据")
    async def 对话数据(self, event: AstrMessageEvent,length: int):
        """对话数据获取测试""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        #读取当前对话下历史对话
        uid = event.unified_msg_origin
        conv_mgr = self.context.conversation_manager
        curr_cid = await conv_mgr.get_curr_conversation_id(uid)
        conversation = await conv_mgr.get_conversation(uid, curr_cid)  # Conversation拉取用户或平台下的全部对话列表。

        import json
        msgs = json.loads(conversation.history)  # 消息列表！
        ch=len(msgs)
        log= conversation.history
        if length > 0:
            msgs = msgs[-length:]  # ✅ 对 list 切片
        else:
            msgs = msgs[-20:]

        yield event.plain_result(f" {user_name}, 历史数据是 {msgs}整体长度{ch}" ) # 发送一条纯文本消息
        
    

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_all_message(self, event: AstrMessageEvent):
        global num#以下代码是达到次数后上传备份及上下文感知
        global lodh
        global num_2
        num_2 +=1
        num += 1
        if num == self.config['lun']:
            num = 0
            umo = event.unified_msg_origin
            provider_id = await self.context.get_current_chat_provider_id(umo=umo)


            #读取当前对话下历史对话
            uid = event.unified_msg_origin
            conv_mgr = self.context.conversation_manager
            curr_cid = await conv_mgr.get_curr_conversation_id(uid)
            conversation = await conv_mgr.get_conversation(uid, curr_cid)  # Conversation拉取用户或平台下的全部对话列表。

            import json
            msgs = json.loads(conversation.history)  # 消息列表！
            if num > 0:
                msgs = msgs[-num:]  # ✅ 对 list 切片
            else:
                msgs = msgs[-20:]
            if self.config['chat_a']!=0:
                tr=self.config['chat_a']
            else:
                tr="对这几轮的历史对话做出总结，输出相同格式的答复，并指出以后自己因该做什么，按人格给与关怀回答之类的,不要丢失重要点"
                
            llm_resp = await self.context.llm_generate(
            chat_provider_id=provider_id, # 聊天模型 ID
            prompt=f"{tr},{msgs}",
            )
            text=llm_resp.completion_text
            lodh=text
            #yield event.plain_result(f"此轮执行操作回答{text}")

            
    #添加提示词            
    @filter.on_llm_request()
    async def my_custom_hook_1(self, event: AstrMessageEvent, req: ProviderRequest): # 请注意有三个参数
        print(req) # 打印请求的文本
        global num_2
        if (num_2 >= self.config['jg']):#以下是未触发调用时将信息载入模型 可以每跳x轮拉回注意力，防止一些过度嵌入行为
            num_2=0
            text_1=self.config['chat_b']
            text=lodh
            import random
            random_text = random.choice(self.config['ZY'])
            req.extra_user_content_parts.append(
                TextPart(text=f"{text}:{text_1}:{random_text}")
                )#添加提示词

        
#text表示文本image_url表示base64图片或者url
        
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
