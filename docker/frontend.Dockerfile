FROM node:18-alpine

ENV NODE_ENV=production

WORKDIR /app


# Install dependencies with lockfile for reproducible builds
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . .
RUN npm run build

# Cloud Run expects the container to listen on $PORT (default 8080)
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "npm start -- -p ${PORT}"]
=======
