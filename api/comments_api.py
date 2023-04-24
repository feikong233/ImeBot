from botiime.api_get_comments import api_random_ruiping, api_random_charter_ruiping

from fastapi import FastAPI
import uvicorn

app = FastAPI()


# 一个简单的api实现，可以让其他人通过http或者https访问到瑞萍接口，并且从瑞萍接口拉取瑞萍或者上传瑞萍
# -----
# 函数定义在botiime/api_get_comments.py
# -----


# 实现拉取一条随机瑞萍的接口，不需要传入参数，直接拉取就会返回一组数据，包括谱师、瑞萍内容、qq号码、qq群昵称、日期
# 如果抽取到了没有被瑞萍过的谱师则会返回一个False，请注意对布尔值的判定
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


uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=8091,
    workers=1
)
