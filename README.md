<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/dev/logo-text-side-white.png" width="400"/></div>

kearch is a distributed search engine. You can set up your own search engine using kearch and connect your search engine to another search engine.

There are two types of search engines in kearch. One is **specialist search engine** and another is **meta search engine**. A **specialist search engine** is a specialized search engine for a topic. For example, a search engine for history, programming language ... anything you want. 

On the other side, a **meta search engine** is used for connecting specialized search engines. You can conect any specialist search engines using a meta search engine. For example, you can get search engine about some programming languages when you connect specialized search engines about Lisp, Haskell, C#, etc..

## 1. How to deploy and configure a specialist search engine 
#### 1.1 Prepare a server for a specialist search engine
First of all, you need to prepare a server for a specialist search engine. Minimum spec for a specialist search engine is following.
- RAM: 8GiB
- SSD/HDD: 100GiB
- CPU: Dual core processor
- OS: Ubuntu 18.04
- Global IP adress or domain 

You can get a qualified server using [Sakura Cloud](https://cloud.sakura.ad.jp/), [AWS](https://aws.amazon.com/), [GCP](https://cloud.google.com/) or [Microsoft Azure](https://azure.microsoft.com/).
#### 1.2 Deploy a specialist search engine to your server using Ansible
Second, deploy a specialist search engine using Ansible. If you don't install Ansible to your **local machine**, please install it first. You can install Ansible by following commands.
- Debian/Ubuntu: `sudo apt install ansible`
- Mac: `brew install ansible`

And then clone this repository your **local machine** by the following command.
```
~$ git clone https://github.com/kearch/kearch.git
```
Finally, deploy a specialist search engine using Ansible. Please replace `<HOSTNAME>` and `<USERNAME>` depending on your environment. (In most cases, `<HOSTNAME>` is the IP adress of your server.) This takes some time to finish. I recommend you to take a coffee brake.
```
~/kearch$ ansible-playbook sp-playbook.yml -i <HOSTNAME>, -u <USERNAME> --ask-become-pass -vvv
```
#### 1.3 Confiure a topic on your specialist search engine and start crawling
Please access [http://HOSTNAME-OR-IP-ADRESS-OFYOUR-SERVER:32700](http://HOSTNAME-OR-IP-ADRESS-OFYOUR-SERVER:32700). You can see this screen if you succeeded to set up. 
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-signin.png" width="200"/></div>

The default Username and Password are "root" and "password". We strongly recommend you to **update password** immdiately after login.

After updating password, Please **set engine name** here.
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-set-engine-name.png" width="300"/></div>

And **set the global IP adress** of your server here.
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-set-ip-adress.png" width="300"/></div>

Now, you can **set a topic to your specialist search engine**. There are two way to set a topic. One is using word frequency dictionary and another is using URLs. You must choose one of them. I think word frequency dictionary is better.
###### Method A: using word frequency dictionary

###### Method B: using word frequency dictionary

## 2. How to connect your specialist search engine to a meta search engine

## Appendix
#### Appendix 1. How to deploy kearch to your kubernetes cluster

```
git clone https://github.com/kearch/kearch.git
cd kearch
./sp_deploy.sh spdb spes all
./me_deploy.sh medb all
```

#### Appendix 2. Port numbers for services
- 32700: Admin setting page port of specialist search engines
- 32600: Admin setting page port of meta search engines
- 32500: Gateway port of specialist search engines
- 32400: Gateway port of meta search engines
- 32550: Search engine front page port of specialist search engines
- 32450: Search engine front page port of meta search engines

#### Appendix 3. Check your DB in kearch

Check the specialist DB.
```
./sp_db_checker.sh
```
Check the meta DB.
```
./me_db_checker.sh
```
