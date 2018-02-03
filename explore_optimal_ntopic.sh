for n in `seq 50 25 501`
do
    echo ntopic = ${n}
    python3 ./topic_detect.py ./computer_science_url_list ./random_url_list --ntopic ${n}
done
