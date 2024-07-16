##
# NAME             :
# VERSION          : 1.0
# DOCKER-VERSION   : 1.12
# DESCRIPTION      : A container with maven and postgres to execute Bdd tests
# TO_BUILD         : docker build --pull=true --no-cache --rm -t adrienpessu/docker-maven-postgres:master . && docker tag adrienpessu/docker-maven-postgres:master adrienpessu/docker-maven-postgres:1.1 && docker tag adrienpessu/docker-maven-postgres:1.1 adrienpessu/docker-maven-postgres:latest
# TO_RUN           : docker run -it --volume=/Users/adrien/workspaces/kconnect/app-service:/localDebugRepo --workdir="/localDebugRepo" --memory=4g --entrypoint=/bin/bash adrienpessu/docker-maven-postgres
##


# extend the most recent long term support Ubuntu version
FROM ubuntu:latest

MAINTAINER Adrien PESSU

# this is a non-interactive automated build - avoid some warning messages
ENV DEBIAN_FRONTEND noninteractive

# update dpkg repositories
RUN apt-get update

# install wget
RUN apt-get install -y wget curl

# get maven 3.2.2
RUN wget --no-verbose -O /tmp/apache-maven-3.2.2.tar.gz http://archive.apache.org/dist/maven/maven-3/3.2.2/binaries/apache-maven-3.2.2-bin.tar.gz

# verify checksum
RUN echo "87e5cc81bc4ab9b83986b3e77e6b3095 /tmp/apache-maven-3.2.2.tar.gz" | md5sum -c

# install maven
RUN tar xzf /tmp/apache-maven-3.2.2.tar.gz -C /opt/
RUN ln -s /opt/apache-maven-3.2.2 /opt/maven
RUN ln -s /opt/maven/bin/mvn /usr/local/bin
RUN rm -f /tmp/apache-maven-3.2.2.tar.gz
ENV MAVEN_HOME /opt/maven

# install git
RUN apt-get install -y git

# install nano
RUN apt-get install -y nano

# remove download archive files
RUN apt-get clean

# set shell variables for java installation
ENV java_version 1.8.0_11
ENV filename jdk-8u11-linux-x64.tar.gz
ENV downloadlink http://download.oracle.com/otn-pub/java/jdk/8u11-b12/$filename

# download java, accepting the license agreement
#RUN wget --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" -O /tmp/$filename $downloadlink

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN mkdir /docker-entrypoint-initdb.d

ENV PG_MAJOR 9.6
ENV PG_VERSION 9.6.1-2.pgdg80+1

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main' $PG_MAJOR > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update \
   && apt-get install -y \
		postgresql-$PG_MAJOR \
		postgresql-contrib-$PG_MAJOR \
	&& rm -rf /var/lib/apt/lists/*

# make the sample config easier to munge (and "correct by default")
RUN mv -v /usr/share/postgresql/$PG_MAJOR/postgresql.conf.sample /usr/share/postgresql/ \
	&& ln -sv ../postgresql.conf.sample /usr/share/postgresql/$PG_MAJOR/ \
	&& sed -ri "s!^#?(listen_addresses)\s*=\s*\S+.*!\1 = '*'!" /usr/share/postgresql/postgresql.conf.sample

RUN mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql && chmod g+s /var/run/postgresql

ENV PATH /usr/lib/postgresql/$PG_MAJOR/bin:$PATH
ENV PGDATA /var/lib/postgresql/data
RUN mkdir -p "$PGDATA" && chown -R postgres:postgres "$PGDATA" && chmod 777 "$PGDATA" # this 777 will be replaced by 700 at runtime (allows semi-arbitrary "--user" values)
VOLUME /var/lib/postgresql/data


#RUN wget -O /tmp/sonar-scanner-2.8.zip "https://sonarsource.bintray.com/Distribution/sonar-scanner-cli/sonar-scanner-2.8.zip" \
#    && unzip /tmp/sonar-scanner-2.8.zip -d /etc/lib/ \
#    && rm /tmp/sonar-scanner-2.8.zip \
#    && ln -s /etc/lib/sonar-scanner-2.8//bin/sonar-scanner /usr/local/bin/sonar-scanner

RUN apt-get purge -y --auto-remove ca-certificates wget

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 5432
CMD ["pg_ctlcluster", "$PG_MAJOR", "main", "start"]
