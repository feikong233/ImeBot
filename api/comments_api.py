from botiime.api_get_comments import api_random_ruiping, api_random_charter_ruiping, api_comments_upload

from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI()


# 一个简单的api实现，可以让其他人通过http或者https访问到瑞萍接口，并且从瑞萍接口拉取瑞萍或者上传瑞萍
# 直接运行这个py文件就可以启动api，默认地址为 127.0.0.1:8091
# 修改ip端口等请见下方uvicorn相关
# -----
# 函数定义在botiime/api_get_comments.py
# -----

# 根目录被访问时返回的提示信息
@app.get('/')
def api_default():
    hello = "很显然，你访问到了这个接口的根目录，但是很sad的是，访问这里不会让你获得任何信息。\n" \
            "这个接口来自ImeBot项目，这是一个实现了瑞平和计数功能的Bot库。\n" \
            "访问 https://github.com/feikong233/ImeBot 这个仓库可以获取更多信息！\n" \
            "By Botiime 2023.4.24"
    return hello


# 实现拉取一条随机瑞萍的接口，不需要传入参数，直接拉取就会返回一组数据，包括谱师、瑞萍内容、qq号码、qq群昵称、日期
# 如果抽取到了没有被瑞萍过的谱师则会返回一个"is_commented" = False，请注意对布尔值的判定
@app.get('/sjrp')
def api_sjrp():
    # 如果抽取到了瑞萍，则返回一个包含charter, member_name, qq_id, date, comments的列表
    # 如果抽取到了没有被瑞萍过的谱师，则返回一个列表
    result = api_random_ruiping()
    return result


# 实现拉取指定谱师的一条随机瑞萍的接口，传入的字符串会在本地进行比对并返回合适的结果
@app.get('/sjcharter/charter={charter}')
def api_sjcharter(charter: str = None):
    result = api_random_charter_ruiping(charter)
    return result


# 创建数据模型Item
class Item(BaseModel):
    # 定义传入信息的类型
    inp_charter: str = None
    qq_id: str = None
    comments: str = None
    member_name: str = None


# 实现上传针对指定谱师的一条瑞平，如果匹配成功则上传True，匹配失败则返回False
@app.post('/charter_upload/')
def api_charter_comments(requested_data: Item):
    # 初始化变量
    inp_charter = requested_data.inp_charter
    qq_id = requested_data.qq_id
    comments = requested_data.comments
    member_name = requested_data.member_name
    # 执行函数
    result = api_comments_upload(inp_charter, qq_id, comments, member_name)
    return result


uvicorn.run(
	
    app=app,
    host="0.0.0.0", # 这里对应你的本机ip地址，一般默认即可
    port=8091, # 这里对应你的api端口，如果你需要从外部访问api那么请务必对外网开放你设置的端口
    workers=1
)
