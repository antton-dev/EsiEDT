# Étape 1 : Construction statique
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# S'assure que adapter-static génère le dossier /build
RUN npm run build 

# Étape 2 : Serveur web léger
FROM nginx:alpine
# Copie les fichiers statiques générés vers le dossier public de Nginx
COPY --from=builder /app/build /usr/share/nginx/html
# Redirige les requêtes non trouvées vers index.html (pour le routage SvelteKit)
RUN sed -i '/index  index.html index.htm;/a \        try_files $uri $uri/ /index.html;' /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]