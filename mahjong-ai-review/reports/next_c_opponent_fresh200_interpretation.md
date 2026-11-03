# Frozen shared-tile candidate: independent200game result

Actual one registered evaluation exit0,12.158seconds CPU2; command saved next_c_opponent_fresh200_command.txt. No training,calibration,epochselection orbaselinechange. Two frozen checkpointSHAs match pre-generation chiefapproval;200new seeds7120000..199 andindependentdataaudit bound.2395states/329true-tenpai targets produce8883conditionaltilelabels/556positive; sample JSONL has explicitseed/turn/observer/relativeopponent/absolutetarget/tile/label/knowncount andall5predictions. Replay independently rebuilt all27/allowed18 metrics exactly.

| Predictor | All27 Brier | All27 LogLoss | All27 AUC | Allowed18 AUC |
|---|---:|---:|---:|---:|
| Sharedtilev2 | .055697 | .201828 | .773593 | .648660 |
| Frozenflatv1 | .059905 | .243437 | .511750 | .506504 |
| Frozenflat+missingzero | .057890 | .219089 | .681987 | .506504 |
| Trainmissing/tile/knownprior | .056213 | .204365 | .759588 | .626927 |
| Publicunknowncopyweight | .054663 | .227173 | .789636 | .685962 |

Primary pre-registered Brier/LogLoss v2-minusflat+rule95%whole-game paired bootstrap CIs are[-.002744,-.001613]/[-.022555,-.011754]. Allowed18 also improves beyond rule-only oldhead: AUCdifference+.14216,CI[+.09786,+.18110]. Thus sharedexplicitrepresentation has evidence for better structuralwaitprediction than frozenflat, beyond trivialmissingmask. This is a combinedarchitecture/inputdirection using15918vs19563parameters,not an isolated causal attribution to sharing.

Against train-only statisticalprior,primarydifferences are-.000516 Brier/-.002538LogLoss withCIs[-.001664,+.000882]/[-.008427,+.003999],bothcrosszero. Superior to simple statistical prediction is NOT established. Against publiccopyweight,Brier is worse by+.001034(CI[-.000151,+.002131]),LogLoss better by-.02535(CI[-.05171,-.00474]); allowed18AUC islower by-.03730,CI[-.05717,-.01415]. No uniform dominance or promotion. Copyweight zeroes structurallypossibleknown4tiles and can incurlogloss; network retains suchcases. Rank vs probabilityscores tell different aspects.

Secondary neural-only tenpaiAUC.79231v2/.79499v1;legalrisk.74537/.73443 from114positives. These are descriptive (no pairedsecondaryCI registered/computed),not confirmed improvement or usable riskcertification. Multihuwinner remains0positive,unvalidated. No policy-strength experiment or Mahjong expert claim follows from conditionalstructuralwaitgain.

300whole-game bootstrap replicates,nominal95%intervals,correlated repeatedstates,simulator-limited200games,multiplecomparators without multiplicityadjustment. Holdout used once as registered; retain artifacts anddo not tune against it. Currentstrongchampion unchanged. A futureclaim must rely on a newlyfrozencandidate plus newdata; no additional trainingproposed here.
