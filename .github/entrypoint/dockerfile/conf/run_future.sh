docker build -t dbs .
docker run --name dbs -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -d dbs

# Wait for the container to be in a running state
# sleep 3
# Wait for the container to be ready
docker cp init-db.sql dbs:init-db.sql
docker cp query-db.sql dbs:query-db.sql
# echo "Waiting for PostgreSQL container to be ready..."
# while true; do
#     docker logs dbs | grep "dbs system is ready to accept connections"
#     if [ $? -eq 0 ]; then
#         break
#     fi
#     sleep 1
# done
# echo "PostgreSQL container is ready."
sleep 5

docker exec -i dbs psql -U user -f init-db.sql
docker exec -i dbs psql -U user -f query-db.sql
