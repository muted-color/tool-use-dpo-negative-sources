# s4r002 Pairwise Bootstrap CI

Status: `complete`
Bootstrap iterations: `1000`

Primary resampling unit: shared `prompt_id` between compared evaluation detail files.

Use this as directional evidence only for metrics where the 95% CI excludes zero.

- `clean_vs_unfiltered_step50` `r028/step50` minus `s3d001/step50` BFCL_core_accuracy: point `0.0033333333333334103`, CI95 [`0.0`, `0.010791366906474864`].
- `clean_vs_unfiltered_step50` `r028/step50` minus `s3d001/step50` When2Call_behavior_accuracy: point `-0.010000000000000009`, CI95 [`-0.022950819672131084`, `0.0`].
- `clean_vs_unfiltered_step50` `r028/step50` minus `s3d001/step50` When2Call_macro_F1: point `-0.005501689955910161`, CI95 [`-0.014910088465275306`, `0.0008401147049755808`].
- `clean_vs_unfiltered_step50` `r029/step50` minus `s3d002/step50` BFCL_core_accuracy: point `-0.0033333333333332993`, CI95 [`-0.014869888475836479`, `0.006779661016949157`].
- `clean_vs_unfiltered_step50` `r029/step50` minus `s3d002/step50` When2Call_behavior_accuracy: point `0.006666666666666599`, CI95 [`-0.009740259740259827`, `0.023333333333333428`].
- `clean_vs_unfiltered_step50` `r029/step50` minus `s3d002/step50` When2Call_macro_F1: point `0.005537898859417356`, CI95 [`-0.00827615304619822`, `0.018058472315438223`].
- `clean_vs_unfiltered_final` `r028/final` minus `s3d001/final` BFCL_core_accuracy: point `-0.0033333333333332993`, CI95 [`-0.014234875444839812`, `0.006968641114982521`].
- `clean_vs_unfiltered_final` `r028/final` minus `s3d001/final` When2Call_behavior_accuracy: point `-0.01666666666666672`, CI95 [`-0.03202846975088969`, `-0.003355704697986628`].
- `clean_vs_unfiltered_final` `r028/final` minus `s3d001/final` When2Call_macro_F1: point `-0.007307615067476236`, CI95 [`-0.020103189492320928`, `0.0035829314432671566`].
- `clean_vs_unfiltered_final` `r029/final` minus `s3d002/final` BFCL_core_accuracy: point `-0.0033333333333332993`, CI95 [`-0.010600706713780883`, `0.0`].
- `clean_vs_unfiltered_final` `r029/final` minus `s3d002/final` When2Call_behavior_accuracy: point `0.0`, CI95 [`-0.009868421052631526`, `0.009646302250803873`].
- `clean_vs_unfiltered_final` `r029/final` minus `s3d002/final` When2Call_macro_F1: point `-0.0013808031049410419`, CI95 [`-0.010995553833687777`, `0.006943472428775577`].
- `step50_vs_final` `r028/step50` minus `r028/final` BFCL_core_accuracy: point `0.020000000000000018`, CI95 [`0.0030674846625767804`, `0.038461538461538436`].
- `step50_vs_final` `r028/step50` minus `r028/final` When2Call_behavior_accuracy: point `-0.010000000000000009`, CI95 [`-0.035598705501618144`, `0.012987012987012991`].
- `step50_vs_final` `r028/step50` minus `r028/final` When2Call_macro_F1: point `-0.0029208766086734617`, CI95 [`-0.02098264863434751`, `0.013933210384042605`].
- `step50_vs_final` `r029/step50` minus `r029/final` BFCL_core_accuracy: point `0.020000000000000018`, CI95 [`0.0`, `0.039999999999999925`].
- `step50_vs_final` `r029/step50` minus `r029/final` When2Call_behavior_accuracy: point `-0.00666666666666671`, CI95 [`-0.02960526315789469`, `0.01577287066246058`].
- `step50_vs_final` `r029/step50` minus `r029/final` When2Call_macro_F1: point `0.0018606335766224724`, CI95 [`-0.016589726576404118`, `0.019603933366037718`].
- `step50_vs_final` `s3d001/step50` minus `s3d001/final` BFCL_core_accuracy: point `0.013333333333333308`, CI95 [`-0.0064102564102563875`, `0.03412969283276457`].
- `step50_vs_final` `s3d001/step50` minus `s3d001/final` When2Call_behavior_accuracy: point `-0.01666666666666672`, CI95 [`-0.03819444444444453`, `0.003597122302158251`].
- `step50_vs_final` `s3d001/step50` minus `s3d001/final` When2Call_macro_F1: point `-0.004726801720239537`, CI95 [`-0.020954117379192838`, `0.011432027115112597`].
- `step50_vs_final` `s3d002/step50` minus `s3d002/final` BFCL_core_accuracy: point `0.020000000000000018`, CI95 [`0.006535947712418277`, `0.03623188405797095`].
- `step50_vs_final` `s3d002/step50` minus `s3d002/final` When2Call_behavior_accuracy: point `-0.013333333333333308`, CI95 [`-0.0383386581469648`, `0.009933774834437137`].
- `step50_vs_final` `s3d002/step50` minus `s3d002/final` When2Call_macro_F1: point `-0.005058068387735926`, CI95 [`-0.024992086824439097`, `0.013922925451259172`].
- `source_axis_step50` `r028/step50` minus `r029/step50` BFCL_core_accuracy: point `0.033333333333333326`, CI95 [`0.015337423312883458`, `0.05666666666666664`].
- `source_axis_step50` `r028/step50` minus `r029/step50` When2Call_behavior_accuracy: point `-0.06666666666666665`, CI95 [`-0.10752688172043012`, `-0.030201342281879207`].
- `source_axis_step50` `r028/step50` minus `r029/step50` When2Call_macro_F1: point `-0.05310632480624111`, CI95 [`-0.0884699042263416`, `-0.023391204562596135`].
- `source_axis_step50` `s3d001/step50` minus `s3d002/step50` BFCL_core_accuracy: point `0.026666666666666616`, CI95 [`0.01016949152542379`, `0.04861111111111116`].
- `source_axis_step50` `s3d001/step50` minus `s3d002/step50` When2Call_behavior_accuracy: point `-0.050000000000000044`, CI95 [`-0.08695652173913049`, `-0.013986013986013957`].
- `source_axis_step50` `s3d001/step50` minus `s3d002/step50` When2Call_macro_F1: point `-0.042066735990913595`, CI95 [`-0.07479866147771586`, `-0.012340294401863128`].
