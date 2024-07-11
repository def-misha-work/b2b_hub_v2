#!/bin/bash

# Имя контейнера
CONTAINER_NAME="infra-db-1"
# Имя базы данных
DATABASE_NAME="django"
# Имя пользователя базы данных
DB_USER="django_user"
# Имя файла бекапа
BACKUP_FILE="django_backup_$(date +%Y%m%d).dump"

# Создание бекапа
sudo docker exec -t $CONTAINER_NAME pg_dump -U $DB_USER -Fc $DATABASE_NAME > $BACKUP_FILE

# Копирование бекапа на хост-машину
# sudo docker cp $CONTAINER_NAME:/$BACKUP_FILE .

# Удаление бекапа из контейнера (опционально)
# sudo docker exec -t $CONTAINER_NAME rm $BACKUP_FILE
