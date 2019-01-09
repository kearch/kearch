#! /bin/bash

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i https://raw.githubusercontent.com/kearch/kearch/dev/me_gateway_spec.yaml -g python -o /local/me-gateway-client
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i https://raw.githubusercontent.com/kearch/kearch/dev/me_gateway_spec.yaml -g python-flask -o /local/me-gateway-server
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i https://raw.githubusercontent.com/kearch/kearch/dev/sp_gateway_spec.yaml -g python -o /local/sp-gateway-client
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i https://raw.githubusercontent.com/kearch/kearch/dev/sp_gateway_spec.yaml -g python-flask -o /local/sp-gateway-server
