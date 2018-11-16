## pipeline
- channel scores for EEG (David), independent, writes to `scores` table
- skull stripping (Yannan), independent, writes to `subjects` table
- speech correlation (Ge), independent, write to `scores` table
- bad channel identification (Amy), independent
- phase amplitude coupling (Mohammadali), independent, writes to `scores` table
- power analysis/signal processing (Jake), independent, writes to `scores` table
- CT to MR registration (Joseph), depends on skull stripping, writes to `channels` table
- ECOG labeling (James), depends on skull stripping, CT to MR registration, writes to `channels` table
- heatmap plotting (Zhaoqiang), depends on everything

## files to be prepopulated in the database
- Standard MR data file, for EEG subjects
- EEG coordinates csv file, for EEG subjects 
