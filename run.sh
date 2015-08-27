#/bin/sh
function run_demo()
{
    python test/kcrossing/main.py -i test/kcrossing/fakedata.conll
}

function run_conllx()
{
    . run/common/get_conllx_filepath.sh
    python test/kcrossing/main.py -i $TRAIN 
}

if [ $# -eq 0 ] ;then
    run_demo
elif [ $# -eq 1 ] ;then
    run_conllx $1
else 
    echo "usage: $0 [language]" >> /dev/stderr
fi

