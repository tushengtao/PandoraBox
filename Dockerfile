# 从docker hub官方同步的 image python:3.10-slim
FROM registry.cn-shanghai.aliyuncs.com/self_images/python:3.10-slim

WORKDIR /PandoraBox

COPY . .

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ENV TZ = Asia/Shanghai

EXPOSE 9501

# 设置入口点为 app.py
ENTRYPOINT ["python", "pdbox/app.py"]

# 默认的 CMD 指令，启动服务器
CMD ["s", "--server", "0.0.0.0", "--port", "9501"]
