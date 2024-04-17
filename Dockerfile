# 使用官方Python运行时作为父镜像
FROM python:3.8

# 设置工作目录为/app
WORKDIR /app

# 将当前目录内容复制到位于/app中的容器中
COPY . /app

# 设置国内的pip下载源，例如使用清华大学的源
RUN pip install --upgrade pip 
  

# 安装项目依赖
RUN pip install --no-cache-dir edge-tts gradio asyncio

# 使端口7860可供外界访问
EXPOSE 7860


# 在容器启动时运行app.py
CMD ["python", "app.py"]
