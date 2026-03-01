---
title: Render.com Deployment Guide - Flask App
description: Passo a passo completo para hospedar o Downloader de Graça na Render
---

# 🚀 Como hospedar o seu Downloader na Render.com (De Graça)

A plataforma [Render.com](https://render.com) é a melhor alternativa 100% gratuita para rodar aplicações Python pesadas que precisam processar vídeo com o FFmpeg e fazer downloads longos.

Siga os passos exatamente como descritos abaixo e o servidor ficará pronto em **5 a 10 minutos**.

---

## Passo 1: Limpar os arquivos no seu Computador
1. Vá até a pasta `PROJETO-DOWNLOADER-main` no seu computador.
2. **Apague** as seguintes pastas/arquivos, pois não precisamos e só vão atrasar o upload:
   * A pasta `.venv` ou `venv` (se houver).
   * A pasta `__pycache__` ou `.pytest_cache`.
   * O arquivo `ffmpeg.exe` ou `ffprobe.exe` (A Render roda em Linux e vai instalar a versão original automaticamente através do nosso `render.yaml`).
   * Arquivos pesados dentro de `downloads/`, deixe a pasta `downloads` vazia.
   * Você pode apagar tudo que for relacionado à "HostGator", como o `passenger_wsgi.py` ou os tutoriais.

---

## Passo 2: Subir o código para o GitHub (A Render lê o código de lá)
A Render.com não tem um "Painel de upload de arquivos" como a HostGator. Eles são mágicos: você manda o arquivo pro GitHub e a Render puxa sozinho toda vez que você atualiza o código.

1. Se você não tem conta no **GitHub**, acesse [github.com](https://github.com/) e crie uma.
2. Faça o login na sua conta do GitHub.
3. No canto superior direito da tela do GitHub, clique no **Símbolo de +** (Mais) e selecione **New repository** (Novo repositório).
4. Em "Repository name", digite `meu-downloader-app`.
5. Marque a caixa de "Private" (Privado) para ninguém ver seu código.
6. Clique no botão verde **Create repository**.
7. Na página seguinte, você vai ver um link azul lá em cima que fala "uploading an existing file". **Clique em "uploading an existing file"**.
8. Arraste TODOS os arquivos da sua pasta `PROJETO-DOWNLOADER-main` (incluindo `app.py`, `render.yaml`, pastas `templates`, `static`, etc.) para o quadro do GitHub no navegador.
9. No fim da página, clique no botão verde **Commit changes**.

---

## Passo 3: Colocar o site online na Render.com
1. Acesse [dashboard.render.com](https://dashboard.render.com/) e faça o login escolhendo a opção **"GitHub"**.
2. Após o login, clique no botão superior **"New +"** e selecione **"Blueprint"** (ou "Web Service", se Blueprint não aparecer logo de cara).
3. Na página que abrir, a Render pedirá permissão para acessar o seu GitHub. Permita e **Klique no botão verde "Connect"** ao lado do seu repositório `meu-downloader-app`.
4. É só isso!
5. A Render vai ler o arquivo mágico chamado `render.yaml` que nós criamos dentro desse projeto. Ali dentro eu já disse pra Render que o projeto é: Python 3.10, que ela precisa instalar o FFmpeg, rodar o `pip install -r requirements.txt` e iniciar o servidor via `gunicorn`.

---

## Passo 4: Esperar a Mágica e Acessar
1. Assim que clicar em conectar/deploy, você verá uma tela preta cheia de letrinhas passarem. É o servidor Linux da Render baixando suas dependências de graça.
2. Aguarde entre 2 a 5 minutos.
3. Quando as últimas linhas falarem algo como `Build successful` e `Starting service...`, aparecerá um selo verde "Live".
4. Vá no topo da página à esquerda, sob o nome do seu projeto, e **clique no link (ex: `https://meu-downloader-app.onrender.com`)**.

**🎉 SEU SITE ESTÁ NO AR E PRONTO PARA BAIXAR QUALQUER VÍDEO NO MUNDO!**

---

## 🛠 Como atualizar os Cookies no Servidor (Muito Importante!)
Lembra que o botão "Cookies" lá no topo do seu site abre a caixa de texto? **Use isso no site ao vivo (onrender.com) toda vez que o Instagram travar sua conta**.
Quando você salva lá, o próprio servidor Python da Render salva o token dentro dele mesmo. Se der 10 downloads com erro direto do Insta, vá no seu navegador (com o Insta aberto e logado), exporte os novos Cookies e cole via botão na Navbar do seu novo site hospedado!
