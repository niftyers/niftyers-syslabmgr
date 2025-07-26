# Stage 1: Build frontend and backend
FROM node:22.17-alpine AS builder

WORKDIR /app
COPY . .

RUN mkdir -p server/web && cd vue && yarn && yarn build
RUN apk add --no-cache go && cd server && go build -o ../syslabmgr

FROM alpine:3.22

WORKDIR /app

COPY --from=builder /app/syslabmgr .
COPY --from=builder /app/server/web ./web

CMD ["./syslabmgr"]
