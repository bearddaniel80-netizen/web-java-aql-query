# syntax=docker/dockerfile:1.7
# ---------- deps ----------
FROM node:22-alpine AS deps

WORKDIR /build

COPY package.json .

RUN --mount=type=cache,target=/root/.npm \
    npm install

# ---------- runtime ----------
FROM deps AS runtime

WORKDIR /app

COPY --from=deps /build/node_modules ./node_modules

COPY . .

CMD ["npm", "run", "dev"]