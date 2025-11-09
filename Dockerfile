FROM python //imagem base

WORKDIR /app // diretório de trabalho dentro do container.

COPY requirements.txt /app  // Copia o arquivo requirements.txt do seu computador para dentro do container.

RUN pip install -r requirements.txt // Instala as dependências do seu projeto (Django, etc.) dentro do container.

COPY . . //Copia todo o código do seu projeto para dentro do container.

EXPOSE 8000 // Informa ao Docker que o container vai usar a porta 8000.

CMD ["python", "manage.py", "runserver","0.0.0.0:8000"] // Define o comando que o container executa ao iniciar.