# kearch
Open and distributed search engine

## How to deploy kearch to your kubernetes cluster
```
git clone https://github.com/kearch/kearch.git
cd kearch
./sp_deploy.sh spdb all
./me_deploy.sh medb all
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
