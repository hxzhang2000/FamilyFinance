# Dockerfile-flask

# Simply inherit the Python 3 image.
FROM python:3

# Set an environment variable
ENV APP /FamilyFinance

# Create the directory
RUN mkdir $APP
WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5000

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

# Install Python dependencies #-i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt

# We copy the rest of the codebase into the image
COPY . .

# Finally, we run uWSGI with the ini file
# 指定容器启动时执行的命令
CMD ["python", "app.py"]
