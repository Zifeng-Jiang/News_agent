# News Agent 🌌🛰️

A Python-based project designed to collect and summarize recent news about space and satellites. The project categorizes news by country/region and selects the top news for each region, providing a concise summary for easy reading.

## Features ✨

- 📰 Collects news articles about space and satellites from the past week
- 🌍 Categorizes news by country/region
- 🏆 Utilizes a Pitcher Agent to select the top news for each region
- 📝 Uses a Scripter Agent to summarize the selected news in under 150 words
- ⚙️ Compiles the Pitcher Agent & Scripter Agent by LangGraph
- 🌐 Develops a Streamlit web interface
- 📄 Generates a downloadable user-friendly docx document with summarized news

## Installation (Python/Conda) 🛠️

To install and set up the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Zifeng-Jiang/News_agent.git
    ```
2. Navigate to the project directory:
    ```bash
    cd News_agent
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Make sure you have Google Chrome browser and the corresponding version of ChromeDriver.
5. Ensure you have an LLM API that can be invoked by LangChain.

## Usage 🚀

To start using the News Agent, run the following command:

```bash
streamlit run main.py
```

## Installation(Docker) 🐳 *Recomanded*
Write a docker file and run the project in container
Example:
```
# Use the official Python base image
FROM python:3.11-bullseye

# Switch the APT source to Tsinghua source and install necessary system dependencies and Chrome browser (optional)
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian bullseye main" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian bullseye-updates main" >> /etc/apt/sources.list

# Update the APT cache and install dependencies
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

# Download and install Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -fy install && \
    rm google-chrome-stable_current_amd64.deb

# Setting the working directory
WORKDIR /app

# Copy the project files to the working directory
COPY . .

# Set permissions for chromedriver and move to system path
RUN chmod +x /app/chromedriver_linux64/chromedriver && \
    mv -f /app/chromedriver_linux64/chromedriver /usr/local/bin/chromedriver

# Make sure google-chrome is in PATH
RUN ln -s /usr/bin/google-chrome /usr/local/bin/google-chrome

# Output Chrome and ChromeDriver version information
RUN google-chrome --version
RUN chromedriver --version

# Setting Environment Variables
ENV DISPLAY=:99
ENV DASHSCOPE_API_KEY=<YOUR_API_KEY>

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start Xvfb and run the application
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & echo | streamlit run main.py --server.port 8502 --server.enableCORS false "]
```
## Contributing 🤝
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch  `git checkout -b feature-branch`
3. Commit your changes  `git commit -m 'Add new feature`
4. Push to the branch  `git push origin feature-branch`
5. Open a pull request

## Contact 📧

For any inquiries or feedback, please contact Zifeng Jiang at [jzf.job@gmail.com].
