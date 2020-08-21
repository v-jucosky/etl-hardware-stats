docker stop etl_hardware_stats || true
docker rm etl_hardware_stats || true
mysql -u${sql_uid} -p${sql_pwd} -e "CREATE SCHEMA IF NOT EXISTS RASPBERRY;"
docker build --build-arg arg_uid=${sql_uid} --build-arg arg_pwd=${sql_pwd} -t etl_hardware_stats .
docker run -d --name etl_hardware_stats --restart on-failure etl_hardware_stats