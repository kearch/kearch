<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/dev/logo-text-side-white.png" width="400"/></div>

kearch is a distributed search engine. You can set up your own search engine using kearch and connect your search engine to another search engine.

You can access our search engine from [https://kearch.info](https://kearch.info).

There are two types of search engines in kearch. One is **specialist search engine** and the other is **meta search engine**. A **specialist search engine** is a specialized search engine for a topic. For example, a search engine for history, programming language ... anything you want.

On the other hand, a **meta search engine** is used for connecting specialized search engines. You can conect any specialist search engines using a meta search engine. For example, you can get search engine about some programming languages when you connect specialized search engines about Lisp, Haskell, C#, etc..

If you want to set up your own **specialist search engine**, please read from [1. Specialist search engine](#1-Specialist-search-engine). If you want to set up your own **meta search engine**, please read from [2. Meta search engine](#2-Meta-search-engine). 

## 1. Specialist search engine
### 1.1 Prepare a server for a specialist search engine
First of all, you need to prepare a server for a specialist search engine. Minimum spec for a specialist search engine is as follows.
- RAM: 8GiB
- SSD/HDD: 100GiB
- CPU: Dual core processor
- OS: Ubuntu 18.04
- Global IP adress or domain 
- SSH login using public key authentication

You can get a qualified server using [Sakura Cloud](https://cloud.sakura.ad.jp/), [AWS](https://aws.amazon.com/), [GCP](https://cloud.google.com/) or [Microsoft Azure](https://azure.microsoft.com/).
### 1.2 Deploy a specialist search engine to your server using Ansible
Second, deploy a specialist search engine using Ansible. If you don't install Ansible to your **local machine**, please install it first. You can install Ansible by following commands.
- Debian/Ubuntu: `sudo apt install ansible`
- Mac: `brew install ansible`

And then clone this repository your **local machine** by the following command.
```
~$ git clone https://github.com/kearch/kearch.git
```
Finally, deploy a specialist search engine using Ansible. Please replace `<HOSTNAME>` and `<USERNAME>` depending on your environment. (In most cases, `<HOSTNAME>` is the IP adress of your server. **Don't forget a comma after `<HOSTNAME>`.** ) This takes some time to finish. I recommend you to take a coffee break.
```
~/kearch$ ansible-playbook sp-playbook.yml -i <HOSTNAME>, -u <USERNAME> --ask-become-pass -vvv
```
### 1.3 Configuration of your specialist search engine
Please access [http://HOSTNAME-OR-IP-ADRESS-OF-YOUR-SERVER:32700](http://HOSTNAME-OR-IP-ADRESS-OFYOUR-SERVER:32700). You can see this screen if you succeeded to set up. 
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-signin.png" width="200"/></div>

The default Username and Password are "root" and "password". We strongly recommend you to **update password** immdiately after login.

After updating password, Please **set engine name** here.
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-set-engine-name.png" width="300"/></div>

And **set the global IP adress** of your server here.
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-set-ip-adress.png" width="300"/></div>

### 1.4 Set a topic to your specialist search engine and start crawling
Now, you can **set a topic to your specialist search engine**. There are two way to set a topic. One is using word frequency dictionary (Method A) and the other is using URLs (Method B). You must choose one of them. **I think word frequency dictionary ([Method A](#141A-Use-word-frequency-dictionary)) is better**.
#### 1.4.1.A Use word frequency dictionary
You must choose a **language** and then input **word frequencies in your crawling topic** and **Word frequencies in random topic**.

You shoud input characteristic words and their ratio in **word frequencies in your crawling topic**. If you feel troublesome to input, please have a look [Appendix4](#Appendix-4-Generate-word-frequencies-from-URLs). You can find easy way to generate text to input there.

You should input all words and their ratio in the Web in **word frequencies in random topic**. But it is very difficult. So I recommend you to check **use default dict**.

<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-frequency.png" width="500"/></div>

#### 1.4.1.B Use URLs
You must choose a **language** and input some URLs related your own topic in **URLs in your crawling topic**. And then, input some URLs about random topics in **URLs in random topic**.

Though this method is easier than frequency dictionary one, it is rougher. This is because I recommend you to use [Method A](#141A-Use-word-frequency-dictionary).

<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-urls.png" width="500"/></div>

#### 1.4.2 Start crawling
Then, you can start crawling from some URLs. Please specify some URLs from here.
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-init-crawl.png" width="500"/></div>

### 1.5 Use your specialist search engine
Now, you can use your specialist search engine from [http://HOSTNAME-OR-IP-ADRESS-OF-YOUR-SERVER:32550](http://HOSTNAME-OR-IP-ADRESS-OFYOUR-SERVER:32550).
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-front.png" width="500"/></div>

### 1.6 Connect your specialist search engine to a meta search engine
There are two cases for connecting a specialist search engine and a meta search engine. One is sending a **connection request** from a specialist search and another is sendinf from a meta search engine.
#### 1.6.1.A Connect from your specialist search engine to a meta search engine
In this case, you **send** a **connection request** from your specialist search engine.

<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-send-req.png" width="500"/></div>

After sending a connection request, the administrator of the meta search engine will approve your request. Then, two search engines are connected. You can confirm it by check here.

<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-from-req-status.png" width="500"/></div>

#### 1.6.1.B Connect from a meta search engine to your specialist search engine
In this case, you **receive** a **connection request** from a specialist search engine. When a specialist search engine send a connection request to your meta search engine, it is displayed in this way.

<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-received-req-status.png" width="500"/></div>

You can approve a connection request just pushing **approve** button.

## 2. Meta search engine
### 2.1 Prepare a server for a meta search engine
First of all, you need to prepare a server for a specialist search engine. Minimum spec for a specialist search engine is following.
- RAM: 4GiB
- SSD/HDD: 100GiB
- CPU: Dual core processor
- OS: Ubuntu 18.04
- Global IP adress or domain 
- SSH login using public key authentication

You can get a qualified server using [Sakura Cloud](https://cloud.sakura.ad.jp/), [AWS](https://aws.amazon.com/), [GCP](https://cloud.google.com/) or [Microsoft Azure](https://azure.microsoft.com/).

### 2.2 Deploy a meta search engine to your server using Ansible
Second, deploy a meta search engine using Ansible. If you don't install Ansible to your **local machine**, please install it first. You can install Ansible by following commands.
- Debian/Ubuntu: `sudo apt install ansible`
- Mac: `brew install ansible`

And then clone this repository your **local machine** by the following command.
```
~$ git clone https://github.com/kearch/kearch.git
```
Finally, deploy a meta search engine using Ansible. Please replace `<HOSTNAME>` and `<USERNAME>` depending on your environment. (In most cases, `<HOSTNAME>` is the IP adress of your server. **Don't forget a comma after `<HOSTNAME>`.** ) This takes some time to finish. I recommend you to take a coffee brake.
```
~/kearch$ ansible-playbook me-playbook.yml -i <HOSTNAME>, -u <USERNAME> --ask-become-pass -vvv
```

### 2.3 Configuration of your meta search engine
Please access [http://HOSTNAME-OR-IP-ADRESS-OF-YOUR-SERVER:32700](http://HOSTNAME-OR-IP-ADRESS-OFYOUR-SERVER:32700). You can see this screen if you succeeded to set up. 
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-signin.png" width="200"/></div>

The default Username and Password are "root" and "password". We strongly recommend you to **update password** immdiately after login.

And **set the global IP adress** of your server here.
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/sp-admin-set-ip-adress.png" width="300"/></div>

### 2.4 Connect your meta search engine to a specialist search engine
There are two cases for connecting a meta search engine and a specialist search engine. One is sending a **connection request** from a meta search and another is sending from a specialist search engine.
#### 2.4.1.A Connect from your meta search engine to a specialist search engine
In this case, you **send** a **connection request** from your meta search engine.

<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/me-admin-send-req.png" width="500"/></div>

After sending a connection request, the administrator of the specialist search engine will approve your request. Then, two search engines are connected. You can confirm it by check here.

<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/me-admin-from-req-status.png" width="500"/></div>

#### 2.4.1.B Connect from a meta search engine to your specialist search engine
In this case, you **receive** a **connection request** from a meta search engine. When a meta search engine send a connection request to your specialist search engine, it is displayed in this way.

<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/me-admin-received-req-status.png" width="500"/></div>

You can approve a connection request just pushing **approve** button.

### 2.5 Use your meta search engine
Now, you can use your meta search engine from [http://HOSTNAME-OR-IP-ADRESS-OF-YOUR-SERVER:32450](http://HOSTNAME-OR-IP-ADRESS-OFYOUR-SERVER:32450).
<div align="center"><img src="https://raw.githubusercontent.com/kearch/kearch/feature/improve-top-README/figure/me-front.png" width="500"/></div>

## Appendix
### Appendix 1. How to deploy kearch to your kubernetes cluster

```
git clone https://github.com/kearch/kearch.git
cd kearch
./sp_deploy.sh spdb spes all
./me_deploy.sh medb all
```

### Appendix 2. Port numbers for services
- 32700: Admin setting page port of specialist search engines
- 32600: Admin setting page port of meta search engines
- 32500: Gateway port of specialist search engines
- 32400: Gateway port of meta search engines
- 32550: Search engine front page port of specialist search engines
- 32450: Search engine front page port of meta search engines

### Appendix 3. Check your DB in kearch

Check the specialist DB.
```
./sp_db_checker.sh
```
Check the meta DB.
```
./me_db_checker.sh
```
### Appendix 4. Generate word frequencies from URLs
You can generate frequencies from URLs easily using `generate_frequencies_from_URLs.py` in `utils` dicrtory.
```
$ cd utils
$ python3 generate_frequencies_from_URLs.py haskell_list
haskell 213
language 55
programming 43
ghc 42
...
```
Please replace `haskell_list` with your own URL list and generate your frequencies. URL list is just only a text file of newline-separated URLs.
