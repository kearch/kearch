<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/dev/logo-text-side-white.png" width="400"/></div>

# kearch: Open and distributed search engine

## How to deploy kearch to your kubernetes cluster

```
git clone https://github.com/kearch/kearch.git
cd kearch
./sp_deploy.sh spdb spes all
./me_deploy.sh medb all
```

## How to deploy kearch to your server using Ansible playbook

### Deploy specialist search engine

```
ansible-playbook sp-playbook.yml -i <HOSTNAME>, -u <USERNAME> --ask-become-pass -vvv
```

### Deploy meta search engine

```
ansible-playbook me-playbook.yml -i <HOSTNAME>, -u <USERNAME> --ask-become-pass -vvv
```

## Port numbers for services
- 32700: Admin setting page port of specialist search engines
- 32600: Admin setting page port of meta search engines
- 32500: Gateway port of specialist search engines
- 32400: Gateway port of meta search engines
- 32550: Search engine front page port of specialist search engines
- 32450: Search engine front page port of meta search engines

## Check your DB in kearch

Check the specialist DB.
```
./sp_db_checker.sh
```
Check the meta DB.
```
./me_db_checker.sh
```
