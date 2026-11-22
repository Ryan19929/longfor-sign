# 懒猫微服构建用。与根目录 Dockerfile 相同，只是换成微服能访问的镜像源：
# 微服访问不了 Docker Hub 和 PyPI。构建上下文是仓库根目录（见 lzc-build.yml）。
FROM docker.m.daocloud.io/library/python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATA_DIR=/data
WORKDIR /app
COPY requirements.txt requirements-server.txt ./
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements-server.txt \
    && groupadd --gid 10001 longfor \
    && useradd --uid 10001 --gid 10001 --no-create-home longfor \
    && mkdir /data && chown 10001:10001 /data && chmod 700 /data
COPY core/ ./core/
COPY server/ ./server/
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3)"
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "--timeout", "180", "--graceful-timeout", "180", "server.app:create_app()"]
