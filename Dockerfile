# 使用官方的Python基础镜像
FROM python:3.11-bullseye

# 切换APT源到清华源并安装必要的系统依赖和Chrome浏览器
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian bullseye main" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian bullseye-updates main" >> /etc/apt/sources.list

# # 设置代理环境变量
# ENV http_proxy=http://192.168.147.48:7890
# ENV https_proxy=http://192.168.147.48:7890
# ENV ftp_proxy=http://192.168.147.48:7890
# ENV no_proxy=127.0.0.1,localhost

# ENV export HTTP_PROXY=http://192.168.147.48:7890
# ENV HTTPS_PROXY=192.168.147.48:7890
# ENV FTP_PROXY=192.168.147.48:7890
# ENV NO_PROXY=127.0.0.1,localhost

# 更新APT缓存并安装依赖包
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libappindicator1 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    libasound2 \
    libgbm1 \
    libu2f-udev && apt-get clean && rm -rf /var/lib/apt/lists/*

# 下载和安装Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -fy install && \
    rm google-chrome-stable_current_amd64.deb

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . .

# 设置chromedriver的权限并移动到系统路径
RUN chmod +x /app/chromedriver_linux64/chromedriver && \
    mv -f /app/chromedriver_linux64/chromedriver /usr/local/bin/chromedriver

# 确保google-chrome在PATH中
RUN ln -s /usr/bin/google-chrome /usr/local/bin/google-chrome

# 输出Chrome和ChromeDriver的版本信息
RUN google-chrome --version
RUN chromedriver --version

# 设置环境变量
ENV DISPLAY=:99
ENV DASHSCOPE_API_KEY=sk-4a6d7c3447314975bcebf0b2f1e1e29e
ENV QIANFAN_AK=3i1j7bH7HwrjBnkomhHs5UjJ
ENV QIANFAN_SK=b4JaljmauCABb2UUw8DKYtsO9KnaZnus

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 启动Xvfb并运行应用程序
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & echo | streamlit run main.py --server.port 8502 --server.enableCORS false "]