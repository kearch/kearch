---
title: kearch specialist search engine admin API
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - javascript--nodejs: Node.JS
  - ruby: Ruby
  - python: Python
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<h1 id="kearch-specialist-search-engine-admin-api">kearch specialist search engine admin API v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

kearch specialist search engine admin API

Base URLs:

* <a href="{scheme}://{sp_host}:{port}/sp/admin">{scheme}://{sp_host}:{port}/sp/admin</a>

    * **scheme** -  Default: http

        * http

        * https

    * **sp_host** -  Default: localhost

    * **port** -  Default: 32600

<h1 id="kearch-specialist-search-engine-admin-api-default">Default</h1>

## get__login

`GET /login`

<h3 id="get__login-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|username|query|string|true|none|
|password|query|string|true|none|

<h3 id="get__login-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## get__logout

`GET /logout`

<h3 id="get__logout-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__update_password

`POST /update_password`

> Body parameter

```json
{
  "required": null,
  "password": "string",
  "password_again": "string"
}
```

<h3 id="post__update_password-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="post__update_password-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__init_crawl_urls

`POST /init_crawl_urls`

> Body parameter

```json
{
  "required": null,
  "urls": "www.google.com\\nwww.facebook.com"
}
```

<h3 id="post__init_crawl_urls-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="post__init_crawl_urls-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__learn_params_from_url

`POST /learn_params_from_url`

> Body parameter

```json
{
  "required": null,
  "topic_urls": "www.google.com\\nwww.facebook.com",
  "random_urls": "www.google.com\\nwww.facebook.com"
}
```

<h3 id="post__learn_params_from_url-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="post__learn_params_from_url-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__learn_params_from_dict

`POST /learn_params_from_dict`

> Body parameter

```json
{
  "language": "string",
  "use_default_dict": "string",
  "topic_dict": {
    "lisp": 91
  },
  "random_dict": {
    "OCaml": 91
  }
}
```

<h3 id="post__learn_params_from_dict-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Dict](#schemadict)|true|none|

<h3 id="post__learn_params_from_dict-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__update_config

`POST /update_config`

> Body parameter

```json
{
  "connection_policy": "string",
  "host_name": "string",
  "engine_name": "string"
}
```

<h3 id="post__update_config-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|Designated configs(connection_policy, host_name or engine_name) are updated|

<h3 id="post__update_config-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__approve_a_connection_request

`POST /approve_a_connection_request`

> Body parameter

```json
{
  "required": null,
  "me_host": "string"
}
```

<h3 id="post__approve_a_connection_request-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="post__approve_a_connection_request-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## delete__delete_a_connection_request

`DELETE /delete_a_connection_request`

> Body parameter

```json
{
  "required": null,
  "me_host": "string"
}
```

<h3 id="delete__delete_a_connection_request-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="delete__delete_a_connection_request-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__send_a_connection_request

`POST /send_a_connection_request`

> Body parameter

```json
{
  "required": null,
  "me_host": "string"
}
```

<h3 id="post__send_a_connection_request-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="post__send_a_connection_request-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocSdict">Dict</h2>

<a id="schemadict"></a>

```json
{
  "language": "string",
  "use_default_dict": "string",
  "topic_dict": {
    "lisp": 91
  },
  "random_dict": {
    "OCaml": 91
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|language|string|false|none|none|
|use_default_dict|string|false|none|none|
|topic_dict|object|false|none|none|
|» **additionalProperties**|number(integer)|false|none|none|
|random_dict|object|false|none|none|
|» **additionalProperties**|number(integer)|false|none|none|

