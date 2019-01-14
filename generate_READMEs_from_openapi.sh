#! /bin/bash

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/sp-gateway/sp_gateway_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/sp-gateway/README.md

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/me-gateway/me_gateway_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/me-gateway/README.md

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/sp-classifier/sp_classifier_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/sp-classifier/README.md

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/sp-admin/sp_admin_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/sp-admin/README.md

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/sp-crawler-child/sp_crawler_child_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/sp-crawler-child/README.md

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/me-admin/me_admin_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/me-admin/README.md

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/sp-front/sp_front_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/sp-front/README.md

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/me-front/me_front_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/me-front/README.md

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/packages/me-evaluater/me_evaluater_spec.yaml -g html -o /local/
sudo chown $USER:$USER index.html
mv index.html packages/me-evaluater/README.md

sudo rm -rf ./.openapi-generator-ignore ./.openapi-generator
