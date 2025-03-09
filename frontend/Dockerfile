# Utilisation de Node.js pour build l'app Vue.js
FROM node:18 as build

WORKDIR /app

# Installation des dépendances
COPY package.json .
RUN npm install

COPY . .
RUN npm run build

# Utilisation de Nginx pour servir l’app Vue.js
FROM nginx
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
