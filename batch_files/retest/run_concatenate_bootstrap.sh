cd /home/groups/russpold/ian_home/uh2/fmri_data/aim1_mturk_behavioral_data/mturk_retest_output/bootstrap_output
cat *.csv > /oak/stanford/groups/russpold/users/henrymj/uh2/Self_Regulation_Ontology/Data/Retest_01-05-2020/Local/bootstrap_merged.csv
cd /oak/stanford/groups/russpold/users/henrymj/uh2/Self_Regulation_Ontology/Data/Retest_01-05-2020/Local
awk '!a[$0]++' bootstrap_merged.csv > bootstrap_merged_clean.csv
rm bootstrap_merged.csv
mv bootstrap_merged_clean.csv ./bootstrap_merged.csv
gzip bootstrap_merged.csv
