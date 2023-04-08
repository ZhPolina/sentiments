FROM mysql:5.7

# Copy custom MySQL configuration file
COPY my.cnf /etc/mysql/conf.d/

# Copy the database dump file to the container's /docker-entrypoint-initdb.d directory
COPY flask.sql /docker-entrypoint-initdb.d/

# Set environment variables for the MySQL database
ENV MYSQL_DATABASE flask
ENV MYSQL_ROOT_PASSWORD 9156
ENV MYSQL_CHARSET utf8
ENV MYSQL_COLLATION utf8_general_ci
