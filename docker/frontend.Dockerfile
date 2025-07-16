FROM node:18-alpine

ENV NODE_ENV=production

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci --omit=dev \
    && adduser -D appuser \
    && chown -R appuser /app

COPY . .
RUN npm run build && npm prune --omit=dev

USER appuser

EXPOSE 3000

CMD ["npm", "start"]
