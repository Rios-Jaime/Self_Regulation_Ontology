for subset in task survey
do
    # run each classification after bash run_dim_struct.sh
    for classifier in lasso ridge rf svm
    do
        sed  -e "s/{SUBSET}/$subset/g" -e "s/{CLASSIFIER}/$classifier/g" dimensional_structure.batch | sbatch
    done
done
