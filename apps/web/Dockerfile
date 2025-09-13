FROM node:20-alpine
WORKDIR /app
COPY package.json pnpm-workspace.yaml turbo.json ./
COPY pnpm-lock.yaml ./
COPY apps/web/package.json apps/web/package.json
COPY packages ./packages
RUN corepack enable && pnpm i --no-frozen-lockfile
COPY apps/web ./apps/web
EXPOSE 3000
CMD ["pnpm", "--filter", "web", "dev"]


