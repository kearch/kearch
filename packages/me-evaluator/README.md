---
title: kearch meta search engine evaluator API
language_tabs: []
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<h1 id="kearch-meta-search-engine-evaluator-api">kearch meta search engine evaluator API v0.1.0</h1>

> Scroll down for example requests and responses.

kearch meta search engine evaluator API

Base URLs:

* <a href="http://{me_host}:{port}/me/evaluator">http://{me_host}:{port}/me/evaluator</a>

    * **me_host** -  Default: me-evaluator.kearch.svc.cluster.local

    * **port** -  Default: 10080

<h1 id="kearch-meta-search-engine-evaluator-api-default">Default</h1>

## get__evaluate

`GET /evaluate`

<h3 id="get__evaluate-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|query|query|string|true|none|

> Example responses

> 200 Response

```json
{
  "192.168.99.100": 0.91
}
```

<h3 id="get__evaluate-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|An info about specialist servers for a given query.|[Evaluation](#schemaevaluation)|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocSevaluation">Evaluation</h2>

<a id="schemaevaluation"></a>

```json
{
  "192.168.99.100": 0.91
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|**additionalProperties**|number(float)|false|none|none|

