# Stable-Diffusion-ChatBot
This is a stable diffusion chatbot

## Concepts Used
- LangChain
- OpenAI API
- Google-Drive API
- E-Mail Services
- Stable Diffusion-XL

## Brief Overview
- The client sends an email along with an image to aour mail server
- Our mail server then sends the mail to our LangChain server, which then computes the text prompt in the email
- From the LangChain results based on the prompt a specifc function( toolkit ) is selected
- This toolkit then hits a SD server and sends the image from the client and computes as per the toolkit's requirement
- Finally our server sends back an image to the client via an email

