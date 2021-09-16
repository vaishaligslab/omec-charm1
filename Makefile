SHELL = bash -o pipefail

.PHONY: build

build: build-hss build-mme

build-hss:
	echo "bundling hss charm"
	cd charm/hss && charmcraft pack -v
build-mme:
	echo "bundling mme charm"
	cd charm/mme && charmcraft pack -v

deploy: deploy-hss deploy-mme

deploy-hss:
	juju add-model development
	juju deploy cassandra-k8s
	echo "deploying hss charm"
	cd charm/hss && juju deploy ./hss_ubuntu-20.04-amd64.charm --resource hss-image=vaishalinicky/cqlshimage:v5 
deploy-mme:
	echo "deploying mme charm"
	cd charm/mme && juju deploy ./mme_ubuntu-20.04-amd64.charm --resource mme-image=amitinfo2k/nucleus-mme:9f86f87

cleanup:
	juju remove-application mme
	juju remove-application hss
	juju remove-application cassandra-k8s
	juju destroy-model development


