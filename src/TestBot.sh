#!/bin/bash

defaultRunMode=native

function usage()
{
	echo Usage:
	echo -e "\t$0 <docker|native*>"
	echo -e "\t\t docker\t run contents curator server on docker."
	echo -e "\t\t native\t run contents curator server on local-machine."
}

#
# check argument 1
#
varRunMode=$1
if [ -z ${varRunMode} ] ; then
	varRunMode=defaultRunMode
fi

case $varRunMode in
	docker)
		cp *.py docker/copy/.
		cp *.sh docker/copy/.

		CC_DOCKER_NAME=contents-curator
		CC_DOCKER_TAG=0.0.1
		CC_DOCKER_CONTAINER=${CC_DOCKER_NAME}
		CC_DOCKER_IMAGE=${CC_DOCKER_NAME}:${CC_DOCKER_TAG}

		docker rm -f ${CC_DOCKER_CONTAINER}
		docker rm ${CC_DOCKER_IMAGE}
		docker build -t ${CC_DOCKER_IMAGE} docker/
		docker run -it -p 8888:8888 --name ${CC_DOCKER_CONTAINER} ${CC_DOCKER_IMAGE}
		;;
	native)
		while :
		do
			echo '[INFO] python3 BotServer.py block'
			python3 BotServer.py block
		done
		;;
	*)
		usage
		exit 1
		;;
esac

