#! /bin/bash
# We use widdershins in this script.
# You must install widdershins by "npm install -g widdershins".

widdershins -cl packages/sp-gateway/sp_gateway_spec.yaml -o packages/sp-gateway/README.md
widdershins -cl packages/me-gateway/me_gateway_spec.yaml -o packages/me-gateway/README.md
widdershins -cl packages/sp-classifier/sp_classifier_spec.yaml -o packages/sp-classifier/README.md
widdershins -cl packages/sp-admin/sp_admin_spec.yaml -o packages/sp-admin/README.md
widdershins -cl packages/sp-crawler-child/sp_crawler_child_spec.yaml packages/sp-crawler-child/README.md
widdershins -cl packages/me-admin/me_admin_spec.yaml -o packages/me-admin/README.md
widdershins -cl packages/sp-front/sp_front_spec.yaml -o packages/sp-front/README.md
widdershins -cl packages/me-front/me_front_spec.yaml -o packages/me-front/README.md
widdershins -cl packages/me-evaluater/me_evaluater_spec.yaml -o packages/me-evaluater/README.md
widdershins -cl packages/sp-query-processor/sp_query_processor_spec.yaml -o packages/sp-query-processor/README.md
