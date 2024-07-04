# 从docker hub官方同步的 image python:3.10-slim
FROM registry.cn-shanghai.aliyuncs.com/self_images/python:3.10-slim

WORKDIR /PandoraBox

ENV PYTHONPATH "${PYTHONPATH}:/PandoraBox"

COPY . .

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple  \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

ENV TZ = Asia/Shanghai

EXPOSE 9501

# 设置入口点为 app.py
ENTRYPOINT ["python", "pbox/app.py"]

# 默认的 CMD 指令，启动服务器
CMD ["s", "--server", "0.0.0.0", "--port", "9501"]
