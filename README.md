# kearch
Open and distributed search engine

## How to deploy kearch to your kubernetes cluster
```
git clone https://github.com/kearch/kearch.git
cd kearch
./sp_deploy.sh spdb
./sp_deploy.sh all
./me_deploy.sh spdb
./me_deploy.sh all
```
## Check your DB in kearch
Check the specialist DB.
```
./sp_db_checker.sh
```
Check the meta DB.
```
./me_db_checker.sh
```
