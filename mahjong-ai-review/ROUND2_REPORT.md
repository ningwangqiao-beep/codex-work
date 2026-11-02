# �ڶ����Զ�ʵ����

������Ϊʵ��������ָ����ܣ����ʵ�鲻����ģ�͸��ơ���������齫AI��δ���ա�

```json
{
  "reports\\round2_c_new_final.json": {
    "tenpai": {
      "model": {
        "n": 30422,
        "positive": 1298,
        "roc_auc": 0.7567731142044067,
        "average_precision": 0.1203063353896141,
        "brier": 0.03932987153530121,
        "log_loss": 0.15784922242164612,
        "ece": 0.004458544572116807
      },
      "baseline": {
        "n": 30422,
        "positive": 1298,
        "roc_auc": 0.5167489051818848,
        "average_precision": 0.04418020695447922,
        "brier": 0.04099947586655617,
        "log_loss": 0.17790523171424866,
        "ece": 0.012649007141590118
      }
    },
    "conditional_wait": {
      "model": {
        "n": 35046,
        "positive": 2193,
        "roc_auc": 0.6616250276565552,
        "average_precision": 0.11256780475378036,
        "brier": 0.05751872435212135,
        "log_loss": 0.22444266080856323,
        "ece": 0.003923165117157623
      },
      "baseline": {
        "n": 35046,
        "positive": 2193,
        "roc_auc": 0.566082775592804,
        "average_precision": 0.08089389652013779,
        "brier": 0.05846002325415611,
        "log_loss": 0.23238754272460938,
        "ece": 0.00045934319496154785
      }
    },
    "deal_in": {
      "model": {
        "n": 54305,
        "positive": 515,
        "roc_auc": 0.7716768980026245,
        "average_precision": 0.038492266088724136,
        "brier": 0.009268920868635178,
        "log_loss": 0.048713285475969315,
        "ece": 0.0007361753723671427
      },
      "baseline": {
        "n": 54305,
        "positive": 515,
        "roc_auc": 0.582435667514801,
        "average_precision": 0.013515764847397804,
        "brier": 0.009386463090777397,
        "log_loss": 0.05325748771429062,
        "ece": 0.0009081047028303146
      }
    },
    "expected_loss_mae": 0.03551848605275154,
    "scope": "configured_simulator_only",
    "groups_tenpai": {
      "game_phase:0": {
        "n": 9927,
        "positive": 47,
        "roc_auc": 0.7539968490600586,
        "average_precision": 0.08116459101438522,
        "brier": 0.004671144764870405,
        "log_loss": 0.027908185496926308,
        "ece": 0.0014702626504004002
      },
      "style:['pure', 'defensive', 'random']": {
        "n": 7544,
        "positive": 230,
        "roc_auc": 0.7630268335342407,
        "average_precision": 0.12999466061592102,
        "brier": 0.028705978766083717,
        "log_loss": 0.12444406747817993,
        "ece": 0.014779511460801587
      },
      "style:['defensive', 'random', 'shape']": {
        "n": 7373,
        "positive": 255,
        "roc_auc": 0.7377697825431824,
        "average_precision": 0.08127286285161972,
        "brier": 0.03314392268657684,
        "log_loss": 0.13956959545612335,
        "ece": 0.012058435218932573
      },
      "style:['random', 'shape', 'pure']": {
        "n": 7690,
        "positive": 365,
        "roc_auc": 0.7422184944152832,
        "average_precision": 0.10301753133535385,
        "brier": 0.04395752027630806,
        "log_loss": 0.17365401983261108,
        "ece": 0.007810021321347449
      },
      "style:['shape', 'pure', 'defensive']": {
        "n": 7815,
        "positive": 448,
        "roc_auc": 0.7711918354034424,
        "average_precision": 0.17398416996002197,
        "brier": 0.05086781084537506,
        "log_loss": 0.19178974628448486,
        "ece": 0.0067951702803839
      },
      "game_phase:1": {
        "n": 10665,
        "positive": 410,
        "roc_auc": 0.6244729161262512,
        "average_precision": 0.07313264906406403,
        "brier": 0.036600951105356216,
        "log_loss": 0.1593950241804123,
        "ece": 0.0011648646905086935
      },
      "game_phase:2": {
        "n": 9830,
        "positive": 841,
        "roc_auc": 0.6020814776420593,
        "average_precision": 0.14269500970840454,
        "brier": 0.07729131728410721,
        "log_loss": 0.2873953878879547,
        "ece": 0.013577395089669153
      }
    },
    "per_tile_conditional_wait": [
      {
        "n": 1298,
        "positive": 65,
        "roc_auc": 0.6077359914779663,
        "average_precision": 0.07725303620100021,
        "brier": 0.047256533056497574,
        "log_loss": 0.1957700401544571,
        "ece": 0.01027404807973653
      },
      {
        "n": 1298,
        "positive": 104,
        "roc_auc": 0.782115638256073,
        "average_precision": 0.22352880239486694,
        "brier": 0.07095526158809662,
        "log_loss": 0.25662970542907715,
        "ece": 0.027424488216638565
      },
      {
        "n": 1298,
        "positive": 104,
        "roc_auc": 0.7616850137710571,
        "average_precision": 0.2171103060245514,
        "brier": 0.07044096291065216,
        "log_loss": 0.2555120885372162,
        "ece": 0.02770349010825157
      },
      {
        "n": 1298,
        "positive": 68,
        "roc_auc": 0.5980989336967468,
        "average_precision": 0.06855928897857666,
        "brier": 0.04970375820994377,
        "log_loss": 0.2038048952817917,
        "ece": 0.006202411954291165
      },
      {
        "n": 1298,
        "positive": 44,
        "roc_auc": 0.6038857698440552,
        "average_precision": 0.043398745357990265,
        "brier": 0.03326035663485527,
        "log_loss": 0.14984381198883057,
        "ece": 0.016875450033694506
      },
      {
        "n": 1298,
        "positive": 94,
        "roc_auc": 0.7783186435699463,
        "average_precision": 0.30825990438461304,
        "brier": 0.06367886066436768,
        "log_loss": 0.23696871101856232,
        "ece": 0.03169961553066969
      },
      {
        "n": 1298,
        "positive": 53,
        "roc_auc": 0.7055845856666565,
        "average_precision": 0.07653830200433731,
        "brier": 0.038581058382987976,
        "log_loss": 0.16302205622196198,
        "ece": 0.00820984735400998
      },
      {
        "n": 1298,
        "positive": 41,
        "roc_auc": 0.6865358948707581,
        "average_precision": 0.08685218542814255,
        "brier": 0.03056555613875389,
        "log_loss": 0.1403542011976242,
        "ece": 0.020203233332722448
      },
      {
        "n": 1298,
        "positive": 24,
        "roc_auc": 0.6368393301963806,
        "average_precision": 0.04546551778912544,
        "brier": 0.018881920725107193,
        "log_loss": 0.09970996528863907,
        "ece": 0.025559954054187983
      },
      {
        "n": 1298,
        "positive": 77,
        "roc_auc": 0.5470925569534302,
        "average_precision": 0.0783054381608963,
        "brier": 0.055823784321546555,
        "log_loss": 0.22603526711463928,
        "ece": 0.006558146909810603
      },
      {
        "n": 1298,
        "positive": 46,
        "roc_auc": 0.5475760698318481,
        "average_precision": 0.04162684082984924,
        "brier": 0.03455899655818939,
        "log_loss": 0.1564658135175705,
        "ece": 0.015123417193535715
      },
      {
        "n": 1298,
        "positive": 93,
        "roc_auc": 0.6989604234695435,
        "average_precision": 0.15309450030326843,
        "brier": 0.06597563624382019,
        "log_loss": 0.25303998589515686,
        "ece": 0.032105723163113
      },
      {
        "n": 1298,
        "positive": 59,
        "roc_auc": 0.7150107622146606,
        "average_precision": 0.11908450722694397,
        "brier": 0.04229016974568367,
        "log_loss": 0.17374810576438904,
        "ece": 0.0019371435919310898
      },
      {
        "n": 1298,
        "positive": 67,
        "roc_auc": 0.5675885677337646,
        "average_precision": 0.059770144522190094,
        "brier": 0.04933154210448265,
        "log_loss": 0.20439091324806213,
        "ece": 0.014642613474279642
      },
      {
        "n": 1298,
        "positive": 99,
        "roc_auc": 0.6800364255905151,
        "average_precision": 0.18697690963745117,
        "brier": 0.06995784491300583,
        "log_loss": 0.26601532101631165,
        "ece": 0.03184867987874895
      },
      {
        "n": 1298,
        "positive": 65,
        "roc_auc": 0.6682013869285583,
        "average_precision": 0.10591717809438705,
        "brier": 0.04678356647491455,
        "log_loss": 0.19072049856185913,
        "ece": 0.004760154173709452
      },
      {
        "n": 1298,
        "positive": 53,
        "roc_auc": 0.6443888545036316,
        "average_precision": 0.05487856641411781,
        "brier": 0.03912881761789322,
        "log_loss": 0.1678774356842041,
        "ece": 0.01301314658485353
      },
      {
        "n": 1298,
        "positive": 74,
        "roc_auc": 0.6981208920478821,
        "average_precision": 0.12173520028591156,
        "brier": 0.05305369198322296,
        "log_loss": 0.2105173021554947,
        "ece": 0.014906775206327438
      },
      {
        "n": 1298,
        "positive": 80,
        "roc_auc": 0.573706865310669,
        "average_precision": 0.08218516409397125,
        "brier": 0.05817003548145294,
        "log_loss": 0.2351931631565094,
        "ece": 0.022658340632915497
      },
      {
        "n": 1298,
        "positive": 105,
        "roc_auc": 0.6611943244934082,
        "average_precision": 0.13482649624347687,
        "brier": 0.07362223416566849,
        "log_loss": 0.27543389797210693,
        "ece": 0.017936922755325213
      },
      {
        "n": 1298,
        "positive": 188,
        "roc_auc": 0.5762603282928467,
        "average_precision": 0.17607447504997253,
        "brier": 0.1273166984319687,
        "log_loss": 0.43509554862976074,
        "ece": 0.06575536169111729
      },
      {
        "n": 1298,
        "positive": 92,
        "roc_auc": 0.7053049802780151,
        "average_precision": 0.14637546241283417,
        "brier": 0.0641772672533989,
        "log_loss": 0.24425846338272095,
        "ece": 0.023661437444388866
      },
      {
        "n": 1298,
        "positive": 117,
        "roc_auc": 0.5857269763946533,
        "average_precision": 0.12304296344518661,
        "brier": 0.08145402371883392,
        "log_loss": 0.29978200793266296,
        "ece": 0.005578934797085822
      },
      {
        "n": 1298,
        "positive": 109,
        "roc_auc": 0.6697595119476318,
        "average_precision": 0.17004507780075073,
        "brier": 0.07484257966279984,
        "log_loss": 0.2756612002849579,
        "ece": 0.012240751064382493
      },
      {
        "n": 1298,
        "positive": 96,
        "roc_auc": 0.5849799513816833,
        "average_precision": 0.15029211342334747,
        "brier": 0.06843312829732895,
        "log_loss": 0.2643921673297882,
        "ece": 0.024699755405890755
      },
      {
        "n": 1298,
        "positive": 110,
        "roc_auc": 0.6362718343734741,
        "average_precision": 0.11391019076108932,
        "brier": 0.07707430422306061,
        "log_loss": 0.2856665849685669,
        "ece": 0.020500750571954995
      },
      {
        "n": 1298,
        "positive": 66,
        "roc_auc": 0.6744269132614136,
        "average_precision": 0.07791835814714432,
        "brier": 0.047686900943517685,
        "log_loss": 0.19404251873493195,
        "ece": 0.0017910791939357296
      }
    ],
    "tenpai_brier_delta_game_bootstrap_95ci": [
      -0.002382298497409464,
      -0.0009587216380495592
    ],
    "bootstrap_games": 180,
    "calibration_scope": "new_validation_groups_only",
    "checkpoint_epoch": 7,
    "calibration_decisions": {
      "tenpai": true,
      "wait": true,
      "risk": true
    },
    "dataset_fingerprint": "b1d361764dfb067ba6875140db8b874a02d3cf2a9adb535a65a52bd296fd71e9",
    "limitations": [
      "no real-player validation",
      "empirical score support; tails unvalidated",
      "independent wait/joint marginal disagreement",
      "no complete A-F full-history study"
    ]
  },
  "reports\\round2_c_new_calibration.json": {
    "scope": "validation_only_game_split",
    "dataset_version": "round2",
    "fit_games": 195,
    "eval_games": 165,
    "tasks": {
      "tenpai": {
        "parameters": {
          "slope": 1.042968988418579,
          "intercept": -0.2612549066543579
        },
        "fit_positive": 1898,
        "fit_n": 33026,
        "before": {
          "n": 27998,
          "positive": 1619,
          "roc_auc": 0.7786185145378113,
          "average_precision": 0.1878104954957962,
          "brier": 0.05157013237476349,
          "log_loss": 0.19516734778881073,
          "ece": 0.020816276875848416
        },
        "after": {
          "n": 27998,
          "positive": 1619,
          "roc_auc": 0.778618574142456,
          "average_precision": 0.1878105103969574,
          "brier": 0.050714053213596344,
          "log_loss": 0.1917366236448288,
          "ece": 0.004494985205383273
        },
        "accepted": true,
        "selection_rule": "validation_eval_half_brier_and_logloss_nonworse_at_least_one_better"
      },
      "wait": {
        "parameters": {
          "slope": 0.6419644951820374,
          "intercept": -1.0898325443267822
        },
        "fit_positive": 3076,
        "fit_n": 51246,
        "before": {
          "n": 43713,
          "positive": 2698,
          "roc_auc": 0.6580621004104614,
          "average_precision": 0.1050686314702034,
          "brier": 0.05739115923643112,
          "log_loss": 0.22452668845653534,
          "ece": 0.01255745850630774
        },
        "after": {
          "n": 43713,
          "positive": 2698,
          "roc_auc": 0.6580621004104614,
          "average_precision": 0.10506860911846161,
          "brier": 0.056895360350608826,
          "log_loss": 0.2228889763355255,
          "ece": 0.0019573017216316657
        },
        "accepted": true,
        "selection_rule": "validation_eval_half_brier_and_logloss_nonworse_at_least_one_better"
      },
      "risk": {
        "parameters": {
          "slope": 0.7911221981048584,
          "intercept": -1.2680069208145142
        },
        "fit_positive": 600,
        "fit_n": 58225,
        "before": {
          "n": 49138,
          "positive": 611,
          "roc_auc": 0.7643540501594543,
          "average_precision": 0.04221953824162483,
          "brier": 0.012222964316606522,
          "log_loss": 0.0621485598385334,
          "ece": 0.004705950996140018
        },
        "after": {
          "n": 49138,
          "positive": 611,
          "roc_auc": 0.7643540501594543,
          "average_precision": 0.04221952706575394,
          "brier": 0.012107003480196,
          "log_loss": 0.061322685331106186,
          "ece": 0.0022441308601628407
        },
        "accepted": true,
        "selection_rule": "validation_eval_half_brier_and_logloss_nonworse_at_least_one_better"
      }
    },
    "seconds": 4.551727600002778
  },
  "reports\\round2_d_policy_evaluation.json": {
    "simulation_only": true,
    "not_for_tuning": true,
    "seed_groups": 100,
    "executed_games": 1200,
    "means": {
      "heuristic": 0.4225,
      "old_reading_risk": -0.975,
      "trained_policy_value": -0.8275
    },
    "comparisons": {
      "old_reading_risk": {
        "mean_difference": -1.3975,
        "paired_seed_cluster_bootstrap_95ci": [
          -1.6875,
          -1.12
        ]
      },
      "trained_policy_value": {
        "mean_difference": -1.25,
        "paired_seed_cluster_bootstrap_95ci": [
          -1.5425,
          -0.9525
        ]
      }
    },
    "per_game": [
      {
        "policy": "heuristic",
        "seed": 1200000,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200000,
        "seat": 1,
        "net_score": 1,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200000,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200000,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200001,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          3,
          1,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200001,
        "seat": 1,
        "net_score": 12,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200001,
        "seat": 2,
        "net_score": -1,
        "scores": [
          0,
          3,
          -1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200001,
        "seat": 3,
        "net_score": 2,
        "scores": [
          1,
          3,
          -6,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200002,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          2,
          -1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200002,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -6,
          1,
          4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200002,
        "seat": 2,
        "net_score": 1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200002,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200003,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -4,
          2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200003,
        "seat": 1,
        "net_score": 4,
        "scores": [
          -5,
          4,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200003,
        "seat": 2,
        "net_score": 6,
        "scores": [
          -4,
          -4,
          6,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200003,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200004,
        "seat": 0,
        "net_score": 8,
        "scores": [
          8,
          2,
          -5,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200004,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200004,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -2,
          -1,
          2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200004,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200005,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          1,
          -2,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200005,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200005,
        "seat": 2,
        "net_score": 3,
        "scores": [
          -1,
          0,
          3,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200005,
        "seat": 3,
        "net_score": -4,
        "scores": [
          4,
          0,
          0,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200006,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          4,
          -3,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200006,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200006,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          -4,
          -1,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200006,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200007,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200007,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200007,
        "seat": 2,
        "net_score": -2,
        "scores": [
          0,
          -2,
          -2,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200007,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200008,
        "seat": 0,
        "net_score": 4,
        "scores": [
          4,
          2,
          -4,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200008,
        "seat": 1,
        "net_score": 3,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200008,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200008,
        "seat": 3,
        "net_score": 4,
        "scores": [
          0,
          -4,
          0,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200009,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          2,
          -1,
          -3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200009,
        "seat": 1,
        "net_score": 6,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200009,
        "seat": 2,
        "net_score": 8,
        "scores": [
          4,
          -4,
          8,
          -8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200009,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200010,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200010,
        "seat": 1,
        "net_score": -5,
        "scores": [
          8,
          -5,
          -4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200010,
        "seat": 2,
        "net_score": 2,
        "scores": [
          4,
          2,
          2,
          -8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200010,
        "seat": 3,
        "net_score": 1,
        "scores": [
          8,
          -5,
          -4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200011,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200011,
        "seat": 1,
        "net_score": -2,
        "scores": [
          3,
          -2,
          1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200011,
        "seat": 2,
        "net_score": 1,
        "scores": [
          3,
          -2,
          1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200011,
        "seat": 3,
        "net_score": -2,
        "scores": [
          1,
          0,
          1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200012,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          1,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200012,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200012,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -5,
          1,
          2,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200012,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200013,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200013,
        "seat": 1,
        "net_score": 3,
        "scores": [
          -2,
          3,
          3,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200013,
        "seat": 2,
        "net_score": 0,
        "scores": [
          3,
          -1,
          0,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200013,
        "seat": 3,
        "net_score": 2,
        "scores": [
          1,
          -2,
          -1,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200014,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200014,
        "seat": 1,
        "net_score": 4,
        "scores": [
          -6,
          4,
          -2,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200014,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -1,
          1,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200014,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -1,
          3,
          -3,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200015,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200015,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200015,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200015,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200016,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200016,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200016,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -3,
          4,
          1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200016,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200017,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200017,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -1,
          1,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200017,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200017,
        "seat": 3,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200018,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200018,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -1,
          1,
          -2,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200018,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200018,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -2,
          1,
          -2,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200019,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200019,
        "seat": 1,
        "net_score": -8,
        "scores": [
          -8,
          -8,
          -8,
          24
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200019,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          -4,
          0,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200019,
        "seat": 3,
        "net_score": 12,
        "scores": [
          -3,
          -6,
          -3,
          12
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200020,
        "seat": 0,
        "net_score": -3,
        "scores": [
          -3,
          -2,
          4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200020,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200020,
        "seat": 2,
        "net_score": 8,
        "scores": [
          -4,
          -6,
          8,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200020,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200021,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          7,
          1,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200021,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -2,
          0,
          2,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200021,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -5,
          12,
          -2,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200021,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -7,
          8,
          -2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200022,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200022,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200022,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -2,
          -2,
          2,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200022,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200023,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200023,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200023,
        "seat": 2,
        "net_score": 1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200023,
        "seat": 3,
        "net_score": 1,
        "scores": [
          4,
          -2,
          -3,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200024,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200024,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -3,
          0,
          3,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200024,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -3,
          2,
          2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200024,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200025,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200025,
        "seat": 1,
        "net_score": -6,
        "scores": [
          8,
          -6,
          4,
          -6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200025,
        "seat": 2,
        "net_score": 2,
        "scores": [
          8,
          -5,
          2,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200025,
        "seat": 3,
        "net_score": 2,
        "scores": [
          8,
          -11,
          1,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200026,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200026,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200026,
        "seat": 2,
        "net_score": 4,
        "scores": [
          -4,
          0,
          4,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200026,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200027,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200027,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200027,
        "seat": 2,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200027,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200028,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          2,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200028,
        "seat": 1,
        "net_score": 2,
        "scores": [
          -3,
          2,
          -3,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200028,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200028,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -1,
          2,
          -2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200029,
        "seat": 0,
        "net_score": 7,
        "scores": [
          7,
          -5,
          3,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200029,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200029,
        "seat": 2,
        "net_score": 1,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200029,
        "seat": 3,
        "net_score": -2,
        "scores": [
          4,
          -1,
          -1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200030,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200030,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          -2,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200030,
        "seat": 2,
        "net_score": 1,
        "scores": [
          1,
          -2,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200030,
        "seat": 3,
        "net_score": -2,
        "scores": [
          4,
          0,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200031,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200031,
        "seat": 1,
        "net_score": 3,
        "scores": [
          1,
          3,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200031,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200031,
        "seat": 3,
        "net_score": 2,
        "scores": [
          2,
          -2,
          -2,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200032,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200032,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200032,
        "seat": 2,
        "net_score": 1,
        "scores": [
          3,
          -2,
          1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200032,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200033,
        "seat": 0,
        "net_score": -8,
        "scores": [
          -8,
          15,
          1,
          -8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200033,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200033,
        "seat": 2,
        "net_score": 8,
        "scores": [
          1,
          7,
          8,
          -16
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200033,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200034,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          4,
          -1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200034,
        "seat": 1,
        "net_score": 6,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200034,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -1,
          -1,
          1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200034,
        "seat": 3,
        "net_score": 2,
        "scores": [
          2,
          -1,
          -3,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200035,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -5,
          -4,
          8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200035,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200035,
        "seat": 2,
        "net_score": 0,
        "scores": [
          6,
          -8,
          0,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200035,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200036,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -1,
          -2,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200036,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200036,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200036,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          2,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200037,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          -3,
          -1,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200037,
        "seat": 1,
        "net_score": 1,
        "scores": [
          2,
          1,
          0,
          -3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200037,
        "seat": 2,
        "net_score": 1,
        "scores": [
          2,
          -3,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200037,
        "seat": 3,
        "net_score": -3,
        "scores": [
          4,
          -3,
          2,
          -3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200038,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          1,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200038,
        "seat": 1,
        "net_score": 4,
        "scores": [
          -3,
          4,
          -3,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200038,
        "seat": 2,
        "net_score": 3,
        "scores": [
          1,
          -2,
          3,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200038,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200039,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -1,
          0,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200039,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200039,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200039,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200040,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          2,
          -2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200040,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200040,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200040,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200041,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200041,
        "seat": 1,
        "net_score": -2,
        "scores": [
          2,
          -2,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200041,
        "seat": 2,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200041,
        "seat": 3,
        "net_score": 4,
        "scores": [
          -3,
          0,
          -1,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200042,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200042,
        "seat": 1,
        "net_score": 2,
        "scores": [
          16,
          2,
          -9,
          -9
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200042,
        "seat": 2,
        "net_score": -1,
        "scores": [
          4,
          -1,
          -1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200042,
        "seat": 3,
        "net_score": -1,
        "scores": [
          1,
          -2,
          2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200043,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          -5,
          -1,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200043,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200043,
        "seat": 2,
        "net_score": 0,
        "scores": [
          1,
          -2,
          0,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200043,
        "seat": 3,
        "net_score": 6,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200044,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200044,
        "seat": 1,
        "net_score": 3,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200044,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200044,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200045,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          -2,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200045,
        "seat": 1,
        "net_score": -2,
        "scores": [
          1,
          -2,
          2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200045,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200045,
        "seat": 3,
        "net_score": 1,
        "scores": [
          3,
          -2,
          -2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200046,
        "seat": 0,
        "net_score": 4,
        "scores": [
          4,
          4,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200046,
        "seat": 1,
        "net_score": 0,
        "scores": [
          4,
          0,
          -4,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200046,
        "seat": 2,
        "net_score": -4,
        "scores": [
          4,
          -2,
          -4,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200046,
        "seat": 3,
        "net_score": -4,
        "scores": [
          4,
          0,
          0,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200047,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200047,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200047,
        "seat": 2,
        "net_score": 2,
        "scores": [
          1,
          -2,
          2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200047,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200048,
        "seat": 0,
        "net_score": -6,
        "scores": [
          -6,
          1,
          4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200048,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200048,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -1,
          1,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200048,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -1,
          -1,
          1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200049,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200049,
        "seat": 1,
        "net_score": 6,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200049,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200049,
        "seat": 3,
        "net_score": 1,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200050,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200050,
        "seat": 1,
        "net_score": 1,
        "scores": [
          4,
          1,
          -1,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200050,
        "seat": 2,
        "net_score": 4,
        "scores": [
          -3,
          -3,
          4,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200050,
        "seat": 3,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200051,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -2,
          2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200051,
        "seat": 1,
        "net_score": -2,
        "scores": [
          2,
          -2,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200051,
        "seat": 2,
        "net_score": 3,
        "scores": [
          1,
          -2,
          3,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200051,
        "seat": 3,
        "net_score": -4,
        "scores": [
          1,
          -5,
          8,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200052,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          8,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200052,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200052,
        "seat": 2,
        "net_score": 2,
        "scores": [
          0,
          -3,
          2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200052,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -4,
          0,
          4,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200053,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200053,
        "seat": 1,
        "net_score": 1,
        "scores": [
          1,
          1,
          1,
          -3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200053,
        "seat": 2,
        "net_score": -1,
        "scores": [
          0,
          3,
          -1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200053,
        "seat": 3,
        "net_score": 2,
        "scores": [
          -2,
          1,
          -1,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200054,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          1,
          -2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200054,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -4,
          1,
          -1,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200054,
        "seat": 2,
        "net_score": -9,
        "scores": [
          15,
          3,
          -9,
          -9
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200054,
        "seat": 3,
        "net_score": -4,
        "scores": [
          4,
          0,
          0,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200055,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200055,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -2,
          1,
          3,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200055,
        "seat": 2,
        "net_score": -2,
        "scores": [
          0,
          -1,
          -2,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200055,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200056,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200056,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200056,
        "seat": 2,
        "net_score": 6,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200056,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200057,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          1,
          -1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200057,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200057,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200057,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200058,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -2,
          -1,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200058,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200058,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200058,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200059,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -6,
          1,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200059,
        "seat": 1,
        "net_score": 1,
        "scores": [
          4,
          1,
          -2,
          -3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200059,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200059,
        "seat": 3,
        "net_score": -3,
        "scores": [
          4,
          -2,
          1,
          -3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200060,
        "seat": 0,
        "net_score": -6,
        "scores": [
          -6,
          4,
          4,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200060,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -3,
          1,
          7,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200060,
        "seat": 2,
        "net_score": 8,
        "scores": [
          -4,
          2,
          8,
          -6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200060,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          1,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200061,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200061,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200061,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200061,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200062,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200062,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200062,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200062,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200063,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200063,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200063,
        "seat": 2,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200063,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200064,
        "seat": 0,
        "net_score": -6,
        "scores": [
          -6,
          0,
          12,
          -6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200064,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -2,
          1,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200064,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -2,
          2,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200064,
        "seat": 3,
        "net_score": -4,
        "scores": [
          0,
          2,
          2,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200065,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          7,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200065,
        "seat": 1,
        "net_score": 1,
        "scores": [
          0,
          1,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200065,
        "seat": 2,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200065,
        "seat": 3,
        "net_score": -3,
        "scores": [
          1,
          1,
          1,
          -3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200066,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200066,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200066,
        "seat": 2,
        "net_score": 4,
        "scores": [
          -4,
          0,
          4,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200066,
        "seat": 3,
        "net_score": 1,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200067,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200067,
        "seat": 1,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200067,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200067,
        "seat": 3,
        "net_score": 6,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200068,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200068,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200068,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          0,
          -1,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200068,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -4,
          7,
          -4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200069,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200069,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200069,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200069,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200070,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200070,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200070,
        "seat": 2,
        "net_score": 1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200070,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200071,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200071,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -4,
          0,
          1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200071,
        "seat": 2,
        "net_score": 4,
        "scores": [
          -3,
          -3,
          4,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200071,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200072,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200072,
        "seat": 1,
        "net_score": 4,
        "scores": [
          0,
          4,
          4,
          -8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200072,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -1,
          1,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200072,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -3,
          4,
          1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200073,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200073,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200073,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -3,
          2,
          2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200073,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200074,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200074,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200074,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200074,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200075,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          -4,
          -2,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200075,
        "seat": 1,
        "net_score": -3,
        "scores": [
          -1,
          -3,
          1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200075,
        "seat": 2,
        "net_score": 4,
        "scores": [
          -2,
          1,
          4,
          -3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200075,
        "seat": 3,
        "net_score": 2,
        "scores": [
          1,
          -3,
          0,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200076,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          3,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200076,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200076,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200076,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200077,
        "seat": 0,
        "net_score": 4,
        "scores": [
          4,
          -5,
          2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200077,
        "seat": 1,
        "net_score": 1,
        "scores": [
          4,
          1,
          1,
          -6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200077,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200077,
        "seat": 3,
        "net_score": -6,
        "scores": [
          4,
          1,
          1,
          -6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200078,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          -1,
          -3,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200078,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200078,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200078,
        "seat": 3,
        "net_score": -4,
        "scores": [
          4,
          0,
          0,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200079,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200079,
        "seat": 1,
        "net_score": 4,
        "scores": [
          0,
          4,
          0,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200079,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200079,
        "seat": 3,
        "net_score": 2,
        "scores": [
          1,
          2,
          -5,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200080,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          2,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200080,
        "seat": 1,
        "net_score": 6,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200080,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200080,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200081,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          4,
          1,
          -8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200081,
        "seat": 1,
        "net_score": 0,
        "scores": [
          4,
          0,
          -4,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200081,
        "seat": 2,
        "net_score": -4,
        "scores": [
          0,
          4,
          -4,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200081,
        "seat": 3,
        "net_score": 0,
        "scores": [
          4,
          4,
          -8,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200082,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200082,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200082,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -2,
          -1,
          2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200082,
        "seat": 3,
        "net_score": 1,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200083,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -6,
          3,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200083,
        "seat": 1,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          1,
          7
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200083,
        "seat": 2,
        "net_score": -8,
        "scores": [
          -8,
          -8,
          -8,
          24
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200083,
        "seat": 3,
        "net_score": 8,
        "scores": [
          -4,
          -5,
          1,
          8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200084,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          1,
          -2,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200084,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -5,
          0,
          4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200084,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          1,
          -1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200084,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -5,
          1,
          3,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200085,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200085,
        "seat": 1,
        "net_score": 8,
        "scores": [
          -5,
          8,
          -4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200085,
        "seat": 2,
        "net_score": 1,
        "scores": [
          0,
          4,
          1,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200085,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200086,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200086,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200086,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200086,
        "seat": 3,
        "net_score": -8,
        "scores": [
          8,
          8,
          -8,
          -8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200087,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200087,
        "seat": 1,
        "net_score": 3,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200087,
        "seat": 2,
        "net_score": 12,
        "scores": [
          -4,
          -4,
          12,
          -4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200087,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200088,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -1,
          -1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200088,
        "seat": 1,
        "net_score": -4,
        "scores": [
          -6,
          -4,
          8,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200088,
        "seat": 2,
        "net_score": 6,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200088,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -1,
          -1,
          1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200089,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200089,
        "seat": 1,
        "net_score": 3,
        "scores": [
          1,
          3,
          -2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200089,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200089,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200090,
        "seat": 0,
        "net_score": 7,
        "scores": [
          7,
          -5,
          -5,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200090,
        "seat": 1,
        "net_score": -3,
        "scores": [
          -1,
          -3,
          1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200090,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -7,
          3,
          1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200090,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -2,
          1,
          -2,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200091,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -3,
          -3,
          6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200091,
        "seat": 1,
        "net_score": 2,
        "scores": [
          1,
          2,
          -2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200091,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -1,
          -3,
          2,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200091,
        "seat": 3,
        "net_score": 2,
        "scores": [
          -1,
          -1,
          0,
          2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200092,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -5,
          12,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200092,
        "seat": 1,
        "net_score": 8,
        "scores": [
          -4,
          8,
          4,
          -8
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200092,
        "seat": 2,
        "net_score": 1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200092,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200093,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          -2,
          1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200093,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200093,
        "seat": 2,
        "net_score": 1,
        "scores": [
          0,
          1,
          1,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200093,
        "seat": 3,
        "net_score": 1,
        "scores": [
          1,
          2,
          -4,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200094,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200094,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -1,
          1,
          -1,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200094,
        "seat": 2,
        "net_score": 3,
        "scores": [
          3,
          0,
          3,
          -6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200094,
        "seat": 3,
        "net_score": -5,
        "scores": [
          8,
          1,
          -4,
          -5
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200095,
        "seat": 0,
        "net_score": 4,
        "scores": [
          4,
          -5,
          2,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200095,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200095,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200095,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200096,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          2,
          2,
          -2
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200096,
        "seat": 1,
        "net_score": 4,
        "scores": [
          -4,
          4,
          -4,
          4
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200096,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200096,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -5,
          1,
          3,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200097,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200097,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200097,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200097,
        "seat": 3,
        "net_score": 1,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200098,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200098,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200098,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -2,
          -1,
          2,
          1
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200098,
        "seat": 3,
        "net_score": 6,
        "scores": [
          2,
          -1,
          -7,
          6
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200099,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200099,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200099,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "heuristic",
        "seed": 1200099,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200000,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200000,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200000,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200000,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200001,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          2,
          0,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200001,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200001,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200001,
        "seat": 3,
        "net_score": -5,
        "scores": [
          1,
          4,
          0,
          -5
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200002,
        "seat": 0,
        "net_score": -9,
        "scores": [
          -9,
          2,
          -9,
          16
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200002,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200002,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -8,
          0,
          0,
          8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200002,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200003,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          2,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200003,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200003,
        "seat": 2,
        "net_score": 6,
        "scores": [
          -4,
          -4,
          6,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200003,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200004,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200004,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200004,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200004,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -2,
          1,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200005,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200005,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200005,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200005,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200006,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200006,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200006,
        "seat": 2,
        "net_score": -3,
        "scores": [
          1,
          -2,
          -3,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200006,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200007,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          3,
          1,
          -5
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200007,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200007,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200007,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200008,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200008,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200008,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200008,
        "seat": 3,
        "net_score": -2,
        "scores": [
          6,
          -2,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200009,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200009,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200009,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200009,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200010,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200010,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200010,
        "seat": 2,
        "net_score": 1,
        "scores": [
          4,
          -6,
          1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200010,
        "seat": 3,
        "net_score": -2,
        "scores": [
          6,
          -2,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200011,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200011,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200011,
        "seat": 2,
        "net_score": 1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200011,
        "seat": 3,
        "net_score": -2,
        "scores": [
          3,
          -2,
          1,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200012,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          3,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200012,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200012,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200012,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200013,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200013,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200013,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200013,
        "seat": 3,
        "net_score": -3,
        "scores": [
          -3,
          4,
          2,
          -3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200014,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200014,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -1,
          1,
          -2,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200014,
        "seat": 2,
        "net_score": -1,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200014,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200015,
        "seat": 0,
        "net_score": -3,
        "scores": [
          -3,
          -3,
          4,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200015,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          1,
          -3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200015,
        "seat": 2,
        "net_score": -3,
        "scores": [
          4,
          -3,
          -3,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200015,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200016,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -5,
          3,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200016,
        "seat": 1,
        "net_score": -3,
        "scores": [
          2,
          -3,
          -3,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200016,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200016,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200017,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200017,
        "seat": 1,
        "net_score": -6,
        "scores": [
          4,
          -6,
          4,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200017,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200017,
        "seat": 3,
        "net_score": -2,
        "scores": [
          3,
          -1,
          0,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200018,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200018,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200018,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -4,
          4,
          -4,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200018,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200019,
        "seat": 0,
        "net_score": 7,
        "scores": [
          7,
          -13,
          3,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200019,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -1,
          -2,
          0,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200019,
        "seat": 2,
        "net_score": 0,
        "scores": [
          2,
          -6,
          0,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200019,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200020,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -4,
          4,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200020,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200020,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200020,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200021,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          7,
          1,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200021,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200021,
        "seat": 2,
        "net_score": 1,
        "scores": [
          0,
          1,
          1,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200021,
        "seat": 3,
        "net_score": 1,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200022,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200022,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200022,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200022,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200023,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200023,
        "seat": 1,
        "net_score": 1,
        "scores": [
          1,
          1,
          0,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200023,
        "seat": 2,
        "net_score": -6,
        "scores": [
          2,
          -4,
          -6,
          8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200023,
        "seat": 3,
        "net_score": 0,
        "scores": [
          4,
          0,
          -4,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200024,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          2,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200024,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200024,
        "seat": 2,
        "net_score": 1,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200024,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -2,
          2,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200025,
        "seat": 0,
        "net_score": -9,
        "scores": [
          -9,
          -8,
          16,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200025,
        "seat": 1,
        "net_score": -6,
        "scores": [
          4,
          -6,
          4,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200025,
        "seat": 2,
        "net_score": -8,
        "scores": [
          24,
          -8,
          -8,
          -8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200025,
        "seat": 3,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200026,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200026,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200026,
        "seat": 2,
        "net_score": -6,
        "scores": [
          1,
          1,
          -6,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200026,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200027,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200027,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200027,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200027,
        "seat": 3,
        "net_score": -3,
        "scores": [
          4,
          -3,
          2,
          -3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200028,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200028,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200028,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -2,
          2,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200028,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200029,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200029,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200029,
        "seat": 2,
        "net_score": -1,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200029,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200030,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          2,
          -2,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200030,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200030,
        "seat": 2,
        "net_score": 0,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200030,
        "seat": 3,
        "net_score": -2,
        "scores": [
          1,
          3,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200031,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200031,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200031,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200031,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200032,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -1,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200032,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200032,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200032,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200033,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          2,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200033,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200033,
        "seat": 2,
        "net_score": -8,
        "scores": [
          -8,
          24,
          -8,
          -8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200033,
        "seat": 3,
        "net_score": -1,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200034,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200034,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200034,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200034,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200035,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          -5,
          -3,
          12
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200035,
        "seat": 1,
        "net_score": -1,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200035,
        "seat": 2,
        "net_score": -1,
        "scores": [
          6,
          -7,
          -1,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200035,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200036,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200036,
        "seat": 1,
        "net_score": -2,
        "scores": [
          1,
          -2,
          -1,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200036,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200036,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          2,
          2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200037,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200037,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200037,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200037,
        "seat": 3,
        "net_score": -1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200038,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          1,
          -2,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200038,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200038,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200038,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200039,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -1,
          0,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200039,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200039,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200039,
        "seat": 3,
        "net_score": -2,
        "scores": [
          2,
          2,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200040,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200040,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200040,
        "seat": 2,
        "net_score": 1,
        "scores": [
          1,
          -2,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200040,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200041,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200041,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200041,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200041,
        "seat": 3,
        "net_score": -2,
        "scores": [
          2,
          -2,
          2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200042,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200042,
        "seat": 1,
        "net_score": -9,
        "scores": [
          16,
          -9,
          -9,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200042,
        "seat": 2,
        "net_score": 0,
        "scores": [
          4,
          -5,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200042,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200043,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -8,
          3,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200043,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          3,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200043,
        "seat": 2,
        "net_score": -3,
        "scores": [
          4,
          -2,
          -3,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200043,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200044,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200044,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200044,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200044,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200045,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          1,
          0,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200045,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200045,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200045,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200046,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200046,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -3,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200046,
        "seat": 2,
        "net_score": -4,
        "scores": [
          4,
          0,
          -4,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200046,
        "seat": 3,
        "net_score": 0,
        "scores": [
          4,
          0,
          -4,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200047,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200047,
        "seat": 1,
        "net_score": 2,
        "scores": [
          2,
          2,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200047,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200047,
        "seat": 3,
        "net_score": -2,
        "scores": [
          6,
          -2,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200048,
        "seat": 0,
        "net_score": -6,
        "scores": [
          -6,
          1,
          4,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200048,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200048,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200048,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200049,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200049,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200049,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200049,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200050,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200050,
        "seat": 1,
        "net_score": -5,
        "scores": [
          8,
          -5,
          -4,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200050,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200050,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200051,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -2,
          2,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200051,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200051,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200051,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200052,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          8,
          -6
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200052,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          8,
          -8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200052,
        "seat": 2,
        "net_score": 2,
        "scores": [
          0,
          0,
          2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200052,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -4,
          0,
          4,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200053,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200053,
        "seat": 1,
        "net_score": -2,
        "scores": [
          3,
          -2,
          1,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200053,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200053,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          1,
          0,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200054,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200054,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200054,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200054,
        "seat": 3,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200055,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -2,
          3,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200055,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200055,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          -1,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200055,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200056,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200056,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200056,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200056,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -9,
          4,
          4,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200057,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200057,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200057,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200057,
        "seat": 3,
        "net_score": -1,
        "scores": [
          2,
          -2,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200058,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          -4,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200058,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200058,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          -2,
          0,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200058,
        "seat": 3,
        "net_score": -2,
        "scores": [
          6,
          -2,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200059,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200059,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -3,
          -1,
          1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200059,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200059,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200060,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          2,
          -4,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200060,
        "seat": 1,
        "net_score": 4,
        "scores": [
          0,
          4,
          4,
          -8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200060,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200060,
        "seat": 3,
        "net_score": -8,
        "scores": [
          -8,
          1,
          15,
          -8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200061,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200061,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200061,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200061,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200062,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200062,
        "seat": 1,
        "net_score": 1,
        "scores": [
          1,
          1,
          1,
          -3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200062,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200062,
        "seat": 3,
        "net_score": -1,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200063,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200063,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200063,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200063,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200064,
        "seat": 0,
        "net_score": -6,
        "scores": [
          -6,
          0,
          12,
          -6
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200064,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200064,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200064,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -5,
          -4,
          8,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200065,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200065,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200065,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200065,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200066,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200066,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200066,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200066,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200067,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200067,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200067,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200067,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200068,
        "seat": 0,
        "net_score": -8,
        "scores": [
          -8,
          24,
          -8,
          -8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200068,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200068,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200068,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -1,
          1,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200069,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200069,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200069,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200069,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200070,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          0,
          0,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200070,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200070,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200070,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200071,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -1,
          1,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200071,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200071,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200071,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200072,
        "seat": 0,
        "net_score": -10,
        "scores": [
          -10,
          16,
          4,
          -10
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200072,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200072,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -2,
          1,
          -1,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200072,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -4,
          4,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200073,
        "seat": 0,
        "net_score": -5,
        "scores": [
          -5,
          8,
          -5,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200073,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200073,
        "seat": 2,
        "net_score": -1,
        "scores": [
          2,
          1,
          -1,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200073,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200074,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200074,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200074,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -2,
          1,
          -2,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200074,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200075,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -4,
          -5,
          8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200075,
        "seat": 1,
        "net_score": -3,
        "scores": [
          -3,
          -3,
          3,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200075,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -8,
          -8,
          1,
          15
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200075,
        "seat": 3,
        "net_score": 1,
        "scores": [
          1,
          -3,
          1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200076,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200076,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200076,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200076,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200077,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200077,
        "seat": 1,
        "net_score": -5,
        "scores": [
          4,
          -5,
          2,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200077,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200077,
        "seat": 3,
        "net_score": -3,
        "scores": [
          4,
          1,
          -2,
          -3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200078,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200078,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          -2,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200078,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -4,
          4,
          -4,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200078,
        "seat": 3,
        "net_score": -5,
        "scores": [
          2,
          1,
          2,
          -5
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200079,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200079,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200079,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200079,
        "seat": 3,
        "net_score": -8,
        "scores": [
          24,
          -8,
          -8,
          -8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200080,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          3,
          1,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200080,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200080,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          -2,
          0,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200080,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200081,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          4,
          0,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200081,
        "seat": 1,
        "net_score": -4,
        "scores": [
          4,
          -4,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200081,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200081,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          -2,
          2,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200082,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200082,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200082,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200082,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200083,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          -4,
          12
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200083,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200083,
        "seat": 2,
        "net_score": -1,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200083,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -1,
          -1,
          1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200084,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200084,
        "seat": 1,
        "net_score": -4,
        "scores": [
          0,
          -4,
          4,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200084,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -2,
          2,
          -2,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200084,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200085,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          4,
          1,
          -5
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200085,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200085,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -3,
          4,
          1,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200085,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200086,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200086,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          -1,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200086,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200086,
        "seat": 3,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200087,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200087,
        "seat": 1,
        "net_score": -9,
        "scores": [
          2,
          -9,
          8,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200087,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200087,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200088,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200088,
        "seat": 1,
        "net_score": -5,
        "scores": [
          -5,
          -5,
          7,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200088,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -2,
          0,
          0,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200088,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200089,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200089,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200089,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200089,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200090,
        "seat": 0,
        "net_score": -3,
        "scores": [
          -3,
          3,
          -3,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200090,
        "seat": 1,
        "net_score": -3,
        "scores": [
          -1,
          -3,
          1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200090,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -6,
          2,
          1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200090,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -2,
          1,
          -2,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200091,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200091,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -4,
          0,
          0,
          4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200091,
        "seat": 2,
        "net_score": -4,
        "scores": [
          4,
          -2,
          -4,
          2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200091,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200092,
        "seat": 0,
        "net_score": -5,
        "scores": [
          -5,
          2,
          8,
          -5
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200092,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -4,
          0,
          4,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200092,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200092,
        "seat": 3,
        "net_score": -8,
        "scores": [
          0,
          0,
          8,
          -8
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200093,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200093,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200093,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200093,
        "seat": 3,
        "net_score": 1,
        "scores": [
          1,
          4,
          -6,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200094,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200094,
        "seat": 1,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200094,
        "seat": 2,
        "net_score": 3,
        "scores": [
          -2,
          1,
          3,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200094,
        "seat": 3,
        "net_score": -5,
        "scores": [
          8,
          2,
          -5,
          -5
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200095,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200095,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200095,
        "seat": 2,
        "net_score": -8,
        "scores": [
          1,
          -8,
          -8,
          15
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200095,
        "seat": 3,
        "net_score": 6,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200096,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200096,
        "seat": 1,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          12,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200096,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200096,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          3,
          1,
          -2
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200097,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          12,
          -4
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200097,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200097,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200097,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200098,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          1,
          -2,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200098,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200098,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200098,
        "seat": 3,
        "net_score": -1,
        "scores": [
          4,
          -2,
          -1,
          -1
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200099,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200099,
        "seat": 1,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          -4,
          12
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200099,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "old_reading_risk",
        "seed": 1200099,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200000,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          1,
          -2,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200000,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200000,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200000,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200001,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          1,
          -1,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200001,
        "seat": 1,
        "net_score": 1,
        "scores": [
          2,
          1,
          -2,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200001,
        "seat": 2,
        "net_score": 2,
        "scores": [
          1,
          -2,
          2,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200001,
        "seat": 3,
        "net_score": -1,
        "scores": [
          1,
          1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200002,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200002,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200002,
        "seat": 2,
        "net_score": -6,
        "scores": [
          8,
          -6,
          -6,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200002,
        "seat": 3,
        "net_score": 8,
        "scores": [
          0,
          1,
          -9,
          8
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200003,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200003,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200003,
        "seat": 2,
        "net_score": 6,
        "scores": [
          -4,
          -4,
          6,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200003,
        "seat": 3,
        "net_score": -2,
        "scores": [
          1,
          -2,
          3,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200004,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200004,
        "seat": 1,
        "net_score": -1,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200004,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -1,
          4,
          -4,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200004,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200005,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200005,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200005,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200005,
        "seat": 3,
        "net_score": -1,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200006,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200006,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200006,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200006,
        "seat": 3,
        "net_score": -1,
        "scores": [
          1,
          2,
          -2,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200007,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -2,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200007,
        "seat": 1,
        "net_score": -5,
        "scores": [
          -2,
          -5,
          -5,
          12
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200007,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200007,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200008,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200008,
        "seat": 1,
        "net_score": 1,
        "scores": [
          0,
          1,
          0,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200008,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200008,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200009,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200009,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200009,
        "seat": 2,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200009,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200010,
        "seat": 0,
        "net_score": -3,
        "scores": [
          -3,
          -1,
          1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200010,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200010,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200010,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200011,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          -2,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200011,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200011,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200011,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200012,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200012,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200012,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200012,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200013,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200013,
        "seat": 1,
        "net_score": 3,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200013,
        "seat": 2,
        "net_score": 1,
        "scores": [
          1,
          0,
          1,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200013,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          1,
          0,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200014,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200014,
        "seat": 1,
        "net_score": -2,
        "scores": [
          2,
          -2,
          -2,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200014,
        "seat": 2,
        "net_score": -3,
        "scores": [
          1,
          1,
          -3,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200014,
        "seat": 3,
        "net_score": -3,
        "scores": [
          12,
          -3,
          -6,
          -3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200015,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -1,
          -2,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200015,
        "seat": 1,
        "net_score": -3,
        "scores": [
          0,
          -3,
          6,
          -3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200015,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200015,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200016,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200016,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200016,
        "seat": 2,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200016,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200017,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          0,
          2,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200017,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200017,
        "seat": 2,
        "net_score": 1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200017,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200018,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200018,
        "seat": 1,
        "net_score": -3,
        "scores": [
          4,
          -3,
          -3,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200018,
        "seat": 2,
        "net_score": -3,
        "scores": [
          4,
          -3,
          -3,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200018,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200019,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200019,
        "seat": 1,
        "net_score": -10,
        "scores": [
          2,
          -10,
          1,
          7
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200019,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200019,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200020,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          -1,
          4,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200020,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200020,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200020,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200021,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200021,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -2,
          0,
          2,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200021,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          4,
          0,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200021,
        "seat": 3,
        "net_score": -5,
        "scores": [
          1,
          2,
          2,
          -5
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200022,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200022,
        "seat": 1,
        "net_score": -9,
        "scores": [
          4,
          -9,
          1,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200022,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200022,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200023,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200023,
        "seat": 1,
        "net_score": 1,
        "scores": [
          1,
          1,
          0,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200023,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200023,
        "seat": 3,
        "net_score": -2,
        "scores": [
          6,
          -2,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200024,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200024,
        "seat": 1,
        "net_score": 3,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200024,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200024,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200025,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200025,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200025,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200025,
        "seat": 3,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200026,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200026,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200026,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200026,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200027,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200027,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200027,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200027,
        "seat": 3,
        "net_score": 2,
        "scores": [
          1,
          -1,
          -2,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200028,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200028,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200028,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200028,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200029,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200029,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200029,
        "seat": 2,
        "net_score": 0,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200029,
        "seat": 3,
        "net_score": -1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200030,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200030,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200030,
        "seat": 2,
        "net_score": -6,
        "scores": [
          4,
          1,
          -6,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200030,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200031,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200031,
        "seat": 1,
        "net_score": 4,
        "scores": [
          -3,
          4,
          -3,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200031,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200031,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200032,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200032,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200032,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200032,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200033,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200033,
        "seat": 1,
        "net_score": -2,
        "scores": [
          1,
          -2,
          4,
          -3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200033,
        "seat": 2,
        "net_score": -8,
        "scores": [
          -8,
          24,
          -8,
          -8
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200033,
        "seat": 3,
        "net_score": 0,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200034,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -2,
          -3,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200034,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200034,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200034,
        "seat": 3,
        "net_score": -8,
        "scores": [
          16,
          1,
          -9,
          -8
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200035,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          -7,
          2,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200035,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200035,
        "seat": 2,
        "net_score": -10,
        "scores": [
          4,
          -10,
          -10,
          16
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200035,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200036,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200036,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200036,
        "seat": 2,
        "net_score": 0,
        "scores": [
          1,
          -3,
          0,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200036,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200037,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200037,
        "seat": 1,
        "net_score": -2,
        "scores": [
          1,
          -2,
          3,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200037,
        "seat": 2,
        "net_score": -3,
        "scores": [
          1,
          4,
          -3,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200037,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -3,
          -1,
          1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200038,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          2,
          -3,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200038,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200038,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200038,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200039,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          -1,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200039,
        "seat": 1,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          -4,
          12
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200039,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200039,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200040,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200040,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200040,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200040,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200041,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200041,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200041,
        "seat": 2,
        "net_score": -1,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200041,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200042,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200042,
        "seat": 1,
        "net_score": -9,
        "scores": [
          16,
          -9,
          -9,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200042,
        "seat": 2,
        "net_score": -2,
        "scores": [
          0,
          0,
          -2,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200042,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200043,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          0,
          0,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200043,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -2,
          -1,
          2,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200043,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          -4,
          12
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200043,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200044,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200044,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200044,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200044,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200045,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200045,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200045,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200045,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200046,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200046,
        "seat": 1,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200046,
        "seat": 2,
        "net_score": -8,
        "scores": [
          3,
          4,
          -8,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200046,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200047,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200047,
        "seat": 1,
        "net_score": -1,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200047,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200047,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200048,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200048,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200048,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200048,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200049,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200049,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200049,
        "seat": 2,
        "net_score": -1,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200049,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200050,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          0,
          0,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200050,
        "seat": 1,
        "net_score": 1,
        "scores": [
          4,
          1,
          -1,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200050,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          -4,
          12
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200050,
        "seat": 3,
        "net_score": -2,
        "scores": [
          3,
          1,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200051,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200051,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200051,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200051,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200052,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          0,
          4,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200052,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          8,
          -8
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200052,
        "seat": 2,
        "net_score": 2,
        "scores": [
          0,
          -3,
          2,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200052,
        "seat": 3,
        "net_score": -8,
        "scores": [
          0,
          0,
          8,
          -8
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200053,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200053,
        "seat": 1,
        "net_score": 0,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200053,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -2,
          1,
          2,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200053,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200054,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -2,
          -2,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200054,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          -1,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200054,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200054,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          1,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200055,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          -4,
          12
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200055,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200055,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200055,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200056,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200056,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200056,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200056,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200057,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200057,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -1,
          1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200057,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200057,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200058,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200058,
        "seat": 1,
        "net_score": -1,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200058,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200058,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200059,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          -4,
          12
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200059,
        "seat": 1,
        "net_score": -2,
        "scores": [
          6,
          -2,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200059,
        "seat": 2,
        "net_score": 1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200059,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200060,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200060,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -6,
          -2,
          12,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200060,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -3,
          4,
          2,
          -3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200060,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200061,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200061,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200061,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200061,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200062,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200062,
        "seat": 1,
        "net_score": -2,
        "scores": [
          1,
          -2,
          -2,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200062,
        "seat": 2,
        "net_score": -6,
        "scores": [
          1,
          1,
          -6,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200062,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200063,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200063,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200063,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200063,
        "seat": 3,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200064,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200064,
        "seat": 1,
        "net_score": 1,
        "scores": [
          -2,
          1,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200064,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200064,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200065,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200065,
        "seat": 1,
        "net_score": -1,
        "scores": [
          1,
          -1,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200065,
        "seat": 2,
        "net_score": -3,
        "scores": [
          1,
          1,
          -3,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200065,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200066,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200066,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200066,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200066,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200067,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          1,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200067,
        "seat": 1,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200067,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200067,
        "seat": 3,
        "net_score": 6,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200068,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200068,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200068,
        "seat": 2,
        "net_score": -3,
        "scores": [
          -3,
          2,
          -3,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200068,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200069,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200069,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200069,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200069,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200070,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200070,
        "seat": 1,
        "net_score": -4,
        "scores": [
          1,
          -4,
          -4,
          7
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200070,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200070,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200071,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200071,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200071,
        "seat": 2,
        "net_score": -2,
        "scores": [
          6,
          -2,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200071,
        "seat": 3,
        "net_score": -3,
        "scores": [
          4,
          -3,
          2,
          -3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200072,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200072,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          -1,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200072,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -2,
          1,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200072,
        "seat": 3,
        "net_score": 2,
        "scores": [
          -5,
          4,
          -1,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200073,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200073,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200073,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -3,
          6,
          -1,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200073,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200074,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200074,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200074,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200074,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200075,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          0,
          0,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200075,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200075,
        "seat": 2,
        "net_score": -3,
        "scores": [
          3,
          -3,
          -3,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200075,
        "seat": 3,
        "net_score": -2,
        "scores": [
          2,
          0,
          0,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200076,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          4,
          1,
          -3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200076,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200076,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200076,
        "seat": 3,
        "net_score": -2,
        "scores": [
          -2,
          6,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200077,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200077,
        "seat": 1,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200077,
        "seat": 2,
        "net_score": 2,
        "scores": [
          4,
          -4,
          2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200077,
        "seat": 3,
        "net_score": 0,
        "scores": [
          4,
          -4,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200078,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200078,
        "seat": 1,
        "net_score": -2,
        "scores": [
          -3,
          -2,
          -1,
          6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200078,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200078,
        "seat": 3,
        "net_score": 1,
        "scores": [
          -2,
          2,
          -1,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200079,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          0,
          0,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200079,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200079,
        "seat": 2,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200079,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200080,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200080,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200080,
        "seat": 2,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200080,
        "seat": 3,
        "net_score": -2,
        "scores": [
          1,
          1,
          0,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200081,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          4,
          1,
          -6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200081,
        "seat": 1,
        "net_score": 0,
        "scores": [
          4,
          0,
          -4,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200081,
        "seat": 2,
        "net_score": -4,
        "scores": [
          0,
          4,
          -4,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200081,
        "seat": 3,
        "net_score": -6,
        "scores": [
          3,
          3,
          0,
          -6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200082,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          2,
          -2,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200082,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200082,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200082,
        "seat": 3,
        "net_score": -2,
        "scores": [
          1,
          2,
          -1,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200083,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200083,
        "seat": 1,
        "net_score": -5,
        "scores": [
          -4,
          -5,
          1,
          8
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200083,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -4,
          0,
          0,
          4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200083,
        "seat": 3,
        "net_score": 1,
        "scores": [
          0,
          -1,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200084,
        "seat": 0,
        "net_score": -5,
        "scores": [
          -5,
          1,
          3,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200084,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          4,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200084,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -2,
          1,
          -1,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200084,
        "seat": 3,
        "net_score": -1,
        "scores": [
          -2,
          0,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200085,
        "seat": 0,
        "net_score": -4,
        "scores": [
          -4,
          12,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200085,
        "seat": 1,
        "net_score": -1,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200085,
        "seat": 2,
        "net_score": 1,
        "scores": [
          -3,
          4,
          1,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200085,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200086,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200086,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200086,
        "seat": 2,
        "net_score": 3,
        "scores": [
          1,
          -2,
          3,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200086,
        "seat": 3,
        "net_score": 0,
        "scores": [
          1,
          0,
          -1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200087,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          0,
          1,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200087,
        "seat": 1,
        "net_score": -1,
        "scores": [
          -1,
          -1,
          3,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200087,
        "seat": 2,
        "net_score": 2,
        "scores": [
          -1,
          1,
          2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200087,
        "seat": 3,
        "net_score": -2,
        "scores": [
          0,
          0,
          2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200088,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          -2,
          6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200088,
        "seat": 1,
        "net_score": 0,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200088,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -1,
          0,
          -1,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200088,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200089,
        "seat": 0,
        "net_score": 3,
        "scores": [
          3,
          -1,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200089,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200089,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200089,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200090,
        "seat": 0,
        "net_score": -3,
        "scores": [
          -3,
          3,
          -3,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200090,
        "seat": 1,
        "net_score": -3,
        "scores": [
          -1,
          -3,
          1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200090,
        "seat": 2,
        "net_score": -1,
        "scores": [
          -5,
          3,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200090,
        "seat": 3,
        "net_score": -1,
        "scores": [
          0,
          2,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200091,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -2,
          2,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200091,
        "seat": 1,
        "net_score": -6,
        "scores": [
          -6,
          -6,
          0,
          12
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200091,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200091,
        "seat": 3,
        "net_score": 3,
        "scores": [
          -1,
          -1,
          -1,
          3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200092,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          -2,
          4,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200092,
        "seat": 1,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          12,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200092,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200092,
        "seat": 3,
        "net_score": -8,
        "scores": [
          -8,
          -8,
          24,
          -8
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200093,
        "seat": 0,
        "net_score": 2,
        "scores": [
          2,
          2,
          1,
          -5
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200093,
        "seat": 1,
        "net_score": -2,
        "scores": [
          6,
          -2,
          -2,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200093,
        "seat": 2,
        "net_score": 4,
        "scores": [
          1,
          -2,
          4,
          -3
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200093,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200094,
        "seat": 0,
        "net_score": 1,
        "scores": [
          1,
          1,
          -2,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200094,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200094,
        "seat": 2,
        "net_score": -1,
        "scores": [
          4,
          2,
          -1,
          -5
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200094,
        "seat": 3,
        "net_score": -5,
        "scores": [
          8,
          2,
          -5,
          -5
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200095,
        "seat": 0,
        "net_score": -2,
        "scores": [
          -2,
          -2,
          6,
          -2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200095,
        "seat": 1,
        "net_score": -2,
        "scores": [
          2,
          -2,
          -2,
          2
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200095,
        "seat": 2,
        "net_score": -4,
        "scores": [
          -4,
          -4,
          -4,
          12
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200095,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200096,
        "seat": 0,
        "net_score": -1,
        "scores": [
          -1,
          3,
          -1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200096,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200096,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200096,
        "seat": 3,
        "net_score": -6,
        "scores": [
          -6,
          4,
          8,
          -6
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200097,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200097,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          1,
          -1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200097,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200097,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200098,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200098,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200098,
        "seat": 2,
        "net_score": 0,
        "scores": [
          -1,
          0,
          0,
          1
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200098,
        "seat": 3,
        "net_score": -4,
        "scores": [
          12,
          -4,
          -4,
          -4
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200099,
        "seat": 0,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200099,
        "seat": 1,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200099,
        "seat": 2,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      },
      {
        "policy": "trained_policy_value",
        "seed": 1200099,
        "seat": 3,
        "net_score": 0,
        "scores": [
          0,
          0,
          0,
          0
        ]
      }
    ],
    "flags": [
      "OLD_MODEL_NEW_CONCEALED_KONG_AND_ACTION_DISTRIBUTION_SHIFT",
      "PAIRED_INITIAL_DEAL_NOT_IDENTICAL_FUTURE_TRAJECTORY",
      "SMALL_SAMPLE_NO_STRENGTH_CLAIM"
    ],
    "checkpoint_sha256": "1f051771341ee2e046c567f1d754a797bd5ef8fd6c3f6fb3b394c21338ac05ad",
    "old_checkpoint_sha256": "0f60b0ceeb9cfd2ce14d381e5d584102eb341968551956b95ff546115b695549"
  },
  "reports\\round2_d_trained_policy_eval.json": {
    "simulation_only": true,
    "paired_seed_and_rotated_seats": true,
    "results": {
      "baseline": {
        "games": 80,
        "mean_net_score": 0.2125,
        "scores": [
          3,
          0,
          1,
          -2,
          -1,
          0,
          6,
          8,
          0,
          1,
          -1,
          -1,
          0,
          16,
          12,
          -3,
          0,
          -1,
          -2,
          -5,
          8,
          -2,
          -2,
          0,
          0,
          0,
          0,
          0,
          0,
          3,
          -1,
          0,
          -1,
          2,
          -1,
          1,
          1,
          -1,
          2,
          -2,
          -2,
          0,
          0,
          0,
          1,
          1,
          0,
          0,
          -7,
          -9,
          0,
          0,
          7,
          0,
          -1,
          -2,
          -3,
          1,
          1,
          0,
          -6,
          2,
          -1,
          0,
          0,
          0,
          0,
          -2,
          0,
          1,
          -5,
          -1,
          -1,
          12,
          -1,
          -1,
          -1,
          -2,
          0,
          -2
        ]
      },
      "public_count": {
        "games": 80,
        "mean_net_score": -0.425,
        "scores": [
          7,
          0,
          -1,
          -4,
          0,
          0,
          6,
          -3,
          -1,
          1,
          -1,
          -1,
          0,
          -2,
          0,
          0,
          -1,
          0,
          -1,
          -1,
          -1,
          -2,
          -2,
          -1,
          0,
          0,
          0,
          4,
          0,
          -2,
          0,
          -1,
          -1,
          -1,
          0,
          6,
          0,
          -1,
          -1,
          0,
          2,
          0,
          -3,
          -4,
          6,
          3,
          0,
          3,
          -1,
          0,
          0,
          0,
          2,
          -4,
          0,
          -1,
          -3,
          -4,
          -2,
          -1,
          3,
          -3,
          -1,
          0,
          -4,
          -4,
          0,
          0,
          -1,
          0,
          -1,
          -2,
          -1,
          -1,
          1,
          0,
          -1,
          -1,
          -4,
          -2
        ]
      },
      "learned": {
        "games": 80,
        "mean_net_score": -0.8375,
        "scores": [
          -1,
          0,
          -1,
          0,
          -1,
          -4,
          6,
          0,
          -1,
          0,
          -4,
          0,
          0,
          3,
          -1,
          0,
          -6,
          0,
          -5,
          0,
          -1,
          -2,
          0,
          -1,
          4,
          0,
          -1,
          0,
          -1,
          -5,
          0,
          0,
          -1,
          0,
          0,
          0,
          1,
          -1,
          -1,
          -1,
          0,
          -5,
          0,
          -4,
          1,
          -2,
          -3,
          -2,
          -1,
          -4,
          0,
          0,
          3,
          0,
          -1,
          -2,
          1,
          1,
          -1,
          0,
          0,
          -2,
          0,
          0,
          -4,
          0,
          2,
          -5,
          -1,
          0,
          -2,
          -3,
          0,
          2,
          0,
          0,
          0,
          -1,
          0,
          -9
        ]
      }
    }
  },
  "experiments\\round2_c\\A\\validation.json": {
    "variant": "A",
    "seed": 42,
    "epochs_limit": 2,
    "seconds": 42.291788800001086,
    "scope": "train_validation_only",
    "features": "public counts",
    "not_full_requested_ablation": "D uses last11 history, not complete discard sequence; E differs by several feature groups",
    "validation_tenpai": {
      "n": 61936,
      "positive": 3437,
      "roc_auc": 0.7850570678710938,
      "average_precision": 0.15767227113246918,
      "brier": 0.049313757568597794,
      "log_loss": 0.18557147681713104,
      "ece": 0.0018382687121629715
    }
  },
  "experiments\\round2_c\\B\\validation.json": {
    "variant": "B",
    "seed": 42,
    "epochs_limit": 2,
    "seconds": 41.4027367000017,
    "scope": "train_validation_only",
    "features": "counts+missing",
    "not_full_requested_ablation": "D uses last11 history, not complete discard sequence; E differs by several feature groups",
    "validation_tenpai": {
      "n": 61936,
      "positive": 3437,
      "roc_auc": 0.7845945954322815,
      "average_precision": 0.1560364067554474,
      "brier": 0.049328479915857315,
      "log_loss": 0.18574240803718567,
      "ece": 0.0024311338074767264
    }
  },
  "experiments\\round2_c\\C\\validation.json": {
    "variant": "C",
    "seed": 42,
    "epochs_limit": 2,
    "seconds": 42.80772409999918,
    "scope": "train_validation_only",
    "features": "counts+missing+meld counts",
    "not_full_requested_ablation": "D uses last11 history, not complete discard sequence; E differs by several feature groups",
    "validation_tenpai": {
      "n": 61936,
      "positive": 3437,
      "roc_auc": 0.7885702848434448,
      "average_precision": 0.16917254030704498,
      "brier": 0.04910062998533249,
      "log_loss": 0.18480508029460907,
      "ece": 0.004524177755229175
    }
  },
  "experiments\\round2_c\\D\\validation.json": {
    "variant": "D",
    "seed": 42,
    "epochs_limit": 2,
    "seconds": 41.723876000003656,
    "scope": "train_validation_only",
    "features": "C+last11 encoded actions",
    "not_full_requested_ablation": "D uses last11 history, not complete discard sequence; E differs by several feature groups",
    "validation_tenpai": {
      "n": 61936,
      "positive": 3437,
      "roc_auc": 0.786962628364563,
      "average_precision": 0.16430546343326569,
      "brier": 0.04919775575399399,
      "log_loss": 0.18531294167041779,
      "ece": 0.004824408155400306
    }
  },
  "experiments\\round2_c\\E\\validation.json": {
    "variant": "E",
    "seed": 42,
    "epochs_limit": 2,
    "seconds": 42.15765410000313,
    "scope": "train_validation_only",
    "features": "all128 incl own/wall/turn/seats/active",
    "not_full_requested_ablation": "D uses last11 history, not complete discard sequence; E differs by several feature groups",
    "validation_tenpai": {
      "n": 61936,
      "positive": 3437,
      "roc_auc": 0.784256100654602,
      "average_precision": 0.15050658583641052,
      "brier": 0.04942696541547775,
      "log_loss": 0.18620984256267548,
      "ece": 0.0054673050181008875
    }
  },
  "experiments\\round2_c\\F\\validation.json": {
    "variant": "F",
    "seed": 42,
    "epochs_limit": 2,
    "seconds": 43.788400500001444,
    "scope": "train_validation_only",
    "features": "E+GRU over last11 actions",
    "not_full_requested_ablation": "D uses last11 history, not complete discard sequence; E differs by several feature groups",
    "validation_tenpai": {
      "n": 61936,
      "positive": 3437,
      "roc_auc": 0.7865005135536194,
      "average_precision": 0.16186439990997314,
      "brier": 0.04926715046167374,
      "log_loss": 0.18566744029521942,
      "ece": 0.00681340794380958
    }
  }
}
```
