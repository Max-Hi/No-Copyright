# pull official base image
FROM node:16

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

RUN npm install -g @vue/cli

# install app dependencies
COPY package.json ./
#COPY package-lock.json ./
RUN npm install
# install tailwind
RUN npx tailwindcss init -p

# start app
CMD ["npm", "run", "serve"]
