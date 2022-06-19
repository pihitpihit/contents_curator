#!/bin/bash

function usage()
{
	echo Usage:
	echo -e "\t$0 <native|docker|docker-rt>"
	echo -e "\t\t native     run contents curator server on local-machine."
	echo -e "\t\t docker     run contents curator server on docker."
	echo -e "\t\t docker-rt  run contents curator server on docker. (realtime-modifiable)"
	exit 1
}

function exec()
{
	echo -e "\033[0;36m[EXEC]\033[0m" -----
	echo -e "\033[0;36m[EXEC]\033[0m" $@
	echo -e "\033[0;36m[EXEC]\033[0m" -----
	$@
}

function checkArgumentCount()
{
	argcER=$1
	argcAR=$2

	if [ ${argcER} != $argcAR ] ; then
		echo Insufficient Argument Count \(function ${FUNCNAME[1]}\)
		exit 1
	fi
}

function runOnDocker()
{
	checkArgumentCount 1 $#

	isModifiable=$1
	case $isModifiable in
		true|false)
			;;
		*)
			echo Invalid Argument \(function runOnDocker\)
			exit 1
			;;
	esac

	exec cp *.py docker/copy/.
	exec cp *.sh docker/copy/.

	CC_DOCKER_NAME=contents-curator
	CC_DOCKER_TAG=0.0.1
	CC_DOCKER_CONTAINER=${CC_DOCKER_NAME}
	CC_DOCKER_IMAGE=${CC_DOCKER_NAME}:${CC_DOCKER_TAG}

	exec docker rm -f ${CC_DOCKER_CONTAINER}
	exec docker image rm ${CC_DOCKER_IMAGE}
	exec docker build -t ${CC_DOCKER_IMAGE} docker/

	CC_DOCKER_RUN_OPTS=
	CC_DOCKER_RUN_OPTS="${CC_DOCKER_RUN_OPTS} -it"
	CC_DOCKER_RUN_OPTS="${CC_DOCKER_RUN_OPTS} -p 8888:8888"
	CC_DOCKER_RUN_OPTS="${CC_DOCKER_RUN_OPTS} --name ${CC_DOCKER_CONTAINER}"

	case $isModifiable in
		true)
			CC_DOCKER_RUN_OPTS="${CC_DOCKER_RUN_OPTS} -v $PWD:/root/contents-curator"
			;;
	esac

	exec docker run ${CC_DOCKER_RUN_OPTS} ${CC_DOCKER_IMAGE}
}

function runOnLocal()
{
	while :
	do
		echo '[INFO] python3 BotServer.py block'
		python3 BotServer.py block
	done
}

#
# check argument 1
#
varRunMode=$1
case $varRunMode in
	docker)
		runOnDocker false
		;;
	docker-rt)
		runOnDocker true
		;;
	native)
		runOnLocal
		;;
	*)
		usage
		;;
esac

