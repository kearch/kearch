<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/dev/logo-text-side-white.png" width="400"/></div>

# What is kearch?
kearch is a distributed search engine. You can set up your own search engine using kearch and connect your search engine to another search engine.

There are two types of search engines in kearch. One is **specialist search engine** and another is **meta search engine**. A **specialist search engine** is a specialized search engine for a topic. For example, a search engine for history, programming language ... anything you want. 

On the other side, a **meta search engine** is used for connecting specialized search engines. You can conect any specialist search engines using a meta search engine. For example, you can get search engine about some programming languages when you connect specialized search engines about Lisp, Haskell, C#, etc..

## How to deploy and configure a specialist search engine 
#### Prepare a server for a specialist search engine
First of all, you need to prepare a server for a specialist search engine. Minimum spec for a specialist search engine is following.
- RAM: 8GiB
- SSD/HDD: 100GiB
- CPU: Dual core processor
- OS: Ubuntu 18.04
- Global IP adress or domain 

You can get a qualified server using [Sakura Cloud](https://cloud.sakura.ad.jp/), [AWS](https://aws.amazon.com/), [GCP](https://cloud.google.com/) or [Microsoft Azure](https://azure.microsoft.com/).
#### Deploy a specialist search engine to your server using Ansible
Second, deploy a specialist search engine using Ansible. If you don't install Ansible to your **local machine**, please install it first. You can install Ansible by following commands.
- Debian/Ubuntu: `sudo apt install ansible`
- Mac: `brew install ansible`

And then clone this repository your **local machine** by the following command.
```
~$ git clone https://github.com/kearch/kearch.git
```
Finally, deploy a specialist search engine using Ansible. Please replace `<HOSTNAME>` and `<USERNAME>` depending on your environment. This takes some time to finish. I recommend you to take a coffee brake.
```
~/kearch$ ansible-playbook sp-playbook.yml -i <HOSTNAME>, -u <USERNAME> --ask-become-pass -vvv
```
#### Confiure a topic on your specialist search engine and start crawling
## How to deploy a meta search engine 

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
