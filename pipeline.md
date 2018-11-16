## pipeline
component | student | dependencies | sql table
--- | --- | --- | ---
channel scores for EEG | David | none | scores
skull stripping | Yannan | none | subjects
speech correlation | Ge | none | scores
bad channel identification | Amy | none | 
phase amplitude coupling | Mohammadali | none | scores
power analysis/signal processing | Jake | none | scores
CT to MR registration | Joseph | skull stripping | channels
ECOG labeling | James | skull stripping, CT to MR registration | channels
heatmap plotting | Zhaoqiang | everything |

## files to be prepopulated in the database
- Standard MR data file, for EEG subjects
- EEG coordinates csv file, for EEG subjects 
