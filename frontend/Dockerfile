FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Compile l'application React pour la production
RUN npm run build

# Expose le port sur lequel l'application s'exécutera
EXPOSE 3000

# Démarre l'application avec un serveur statique
CMD ["npm", "start"]
