for n in `seq 200 10 301`
do
    echo ntopic = ${n}
    python3 ./topic_detect.py ./computer_science_url_list ./random_url_list --ntopic ${n}
done
