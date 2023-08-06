#!/usr/bin/env bash
while getopts ":m:b:c:" opts
do
    case $opts in
        m)
        update_info=$OPTARG;;
        b)
        echo "参数b的值$OPTARG";;
        c)
        echo "参数c的值$OPTARG";;
        ?)
        echo "未知参数"
        exit 1;;
    esac
done

git pull
git add *
git commit -m "$update_info"
git push
pip uninstall restful_api -y \
&& pip install git+https://github.com/Jie-Yuan/RestfulApi.git -U -i https://pypi.tuna.tsinghua.edu.cn/simple

exit 0