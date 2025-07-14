FROM python:3.10-slim

# Wroking directory

WORKDIR /app

# COPY PROJECT FILES
COPY requirnments.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirnments.txt


# COPY SOURCE CODE
COPY src .

CMD ["uvicorn","poc.kite_oauth_poc.controllers.auth_server_redirect:app","--host","0.0.0.0","--port","8080"]
