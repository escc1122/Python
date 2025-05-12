執行方式

```bash
# 建立 image
docker build -t playwright_docker .

# 執行 container，掛載所有需要的外部檔案
docker run --rm \
  --env-file .env \
  -v $(pwd)/main.py:/app/main.py \
  -v $(pwd)/site_urls.txt:/app/site_urls.txt \
  -v $(pwd)/logs:/app/logs \
  playwright_docker

```
or

```bash
docker-compose up --build --remove-orphans
```



