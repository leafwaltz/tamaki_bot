from nonebot import on_command, CommandSession

from .config import redis_port
from .config import default_boss_hp

import redis

__plugin_name__ = 'guild_war_manager'
__plugin_usage__ = ''

r = redis.StrictRedis(host='localhost', port=redis_port, db=0)

# command: '/报刀 <伤害数值> <阵容类型>'
@on_command('report_damage', aliases=('报刀'))
async def report_damage(session: CommandSession):
    damage = session.get('damage')
    user = session.get('user')
    damage_type = session.get('damage_type')

    if damage == "" or damage_type == "":
        await session.send("@%s 请填写伤害数值和阵容类型并用空格分开喵。"%user)
        return

    if not damage.isdigit():
        await session.send("@%s 报刀数值不正确呢，请重新填写喵。"%user)
    elif damage_type.isspace():
        await session.send("@%s 您使用的阵容类型珠希不知道呢喵。"%user)
    else:
        await session.send("@%s 造成伤害：%s，阵容类型：%s。"%(user, damage, damage_type))
    
    session.finish()
    
@report_damage.args_parser
async def report_damage_args_parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    args = stripped_arg.split()

    if 'card' in session.event['sender'].keys():
        user = session.event['sender']['card']
    else:
        user = ""

    if session.is_first_run:
        if len(args) == 2:
            session.state['damage'] = args[0]
            session.state['damage_type'] = args[1]
        elif len(args) == 1:
            session.state['damage'] = args[0]
            session.state['damage_type'] = ""
        else:
            session.state['damage'] = ""
            session.state['damage_type'] = ""
        
        session.state['user'] = user