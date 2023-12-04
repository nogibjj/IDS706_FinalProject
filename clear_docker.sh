docker images prune
docker containers prune
docker rm $(docker images -a -q)
docker rm -f $(docker ps -a -q)
# 清理 Docker 缓存
docker system prune

# 清理未使用的系统资源
docker system prune -a --volumes