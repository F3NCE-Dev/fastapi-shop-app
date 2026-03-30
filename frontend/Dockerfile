FROM node:20 as build

COPY package.json package.json
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /dist /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 4000

CMD ["nginx", "-g", "daemon off;"]
