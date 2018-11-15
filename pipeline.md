## pipeline
- channel scores for EEG (David), independent, writes to `scores` table
- skull stripping (Yannen), independent, writes to `subjects` table
- speech correlation (Ge), independent, write to `scores` table
- bad channel identification (Amy), independent
- phase amplitude coupling (Mohammadali), independent, writes to `scores` table
- power analysis/signal processing (Jake), independent, writes to `scores` table
- CT to MR registration (Joseph), depends on skull stripping, writes to `channels` table
- ECOG labeling (James), depends on skull stripping, CT to MR registration, writes to `channels` table
- heatmap plotting (Zhaoquiang), depends on everything
