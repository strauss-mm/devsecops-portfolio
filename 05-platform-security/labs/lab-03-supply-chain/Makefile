.PHONY: all build sign sbom verify attest diff clean

IMAGE := lab03-app
TAG_V1 := v1.0
TAG_V2 := v2.0

all: build sbom sign attest

build:
	docker build -t $(IMAGE):$(TAG_V1) app/
	docker build -f app/Dockerfile.v2 -t $(IMAGE):$(TAG_V2) app/

sbom:
	mkdir -p sbom
	syft $(IMAGE):$(TAG_V1) -o cyclonedx-json > sbom/app-$(TAG_V1)-cyclonedx.json
	syft $(IMAGE):$(TAG_V2) -o cyclonedx-json > sbom/app-$(TAG_V2)-cyclonedx.json
	syft $(IMAGE):$(TAG_V1) -o spdx-json > sbom/app-$(TAG_V1)-spdx.json

sign:
	@test -f cosign.key || cosign generate-key-pair
	cosign sign --key cosign.key $(IMAGE):$(TAG_V1)
	cosign sign --key cosign.key $(IMAGE):$(TAG_V2)

verify:
	cosign verify --key cosign.pub $(IMAGE):$(TAG_V1)
	cosign verify --key cosign.pub $(IMAGE):$(TAG_V2)

attest:
	cosign attest --key cosign.key --predicate sbom/app-$(TAG_V1)-cyclonedx.json \
		--type cyclonedx $(IMAGE):$(TAG_V1)

diff:
	python3 scripts/sbom-diff.py sbom/app-$(TAG_V1)-cyclonedx.json sbom/app-$(TAG_V2)-cyclonedx.json

deploy:
	cd terraform && terraform init && terraform apply -auto-approve

clean:
	docker rmi $(IMAGE):$(TAG_V1) $(IMAGE):$(TAG_V2) 2>/dev/null || true
	rm -rf sbom/*.json cosign.key cosign.pub
	cd terraform && terraform destroy -auto-approve 2>/dev/null || true
