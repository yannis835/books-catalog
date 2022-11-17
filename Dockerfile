Use Alpine as a base Operating System
FROM docker.io/alpine
# Add python3 and Tornado
# and create a 'runner' user for running the app (instead of root)
RUN apk update && \
apk add python3 py-pip && \
pip3 install tornado && \
adduser -D -s /bin/ash runner
# Copy the source files of the micro-services
COPY src/*.py /home/runner/booksCatalog/
# Copy the default configuration file of the micro-services
COPY config/BooksCatalog.properties /home/runner/booksCatalog/config/
# Micro-service files shall belong to 'runner' user
RUN chown -R runner:runner /home/runner/booksCatalog/
# Expose micro-service port
EXPOSE 9990
# As 'runner' user...
USER runner
# ...position in the micro-service directory...
WORKDIR /home/runner/booksCatalog/
# ...run the micro-service!
ENTRYPOINT ["python3", "-u", "main.py", "--config", "config/BooksCatalog.properties"]
