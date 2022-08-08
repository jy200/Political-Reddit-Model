# Report on Classifiers
Results for SGDClassifier:
* Accuracy: 0.3691
* Recall: [0.4905, 0.1246, 0.8032, 0.0502]
* Precision: [0.5142, 0.4729, 0.3088, 0.3224]

Confusion Matrix: 
[[ 978   74  899   43]
 [ 309  253 1398   70]
 [ 212   93 1624   93]
 [ 403  115 1338   98]]

Results for GaussianNB:
* Accuracy: 0.3479
* Recall: [0.7222, 0.0621, 0.1533, 0.4642]
* Precision: [0.3665, 0.2944, 0.4984, 0.3002]

Confusion Matrix: 
[[1440   37   89  428]
 [1019  126   98  787]
 [ 639  174  310  899]
 [ 831   91  125  907]]

Results for RandomForestClassifier:
* Accuracy: 0.4396
* Recall: [0.5757, 0.3473, 0.5861, 0.2451]
* Precision: [0.5415, 0.404, 0.4303, 0.3469]

Confusion Matrix: 
[[1148  225  328  293]
 [ 366  705  611  348]
 [ 236  340 1185  261]
 [ 370  475  630  479]]

Results for MLPClassifier:
* Accuracy: 0.4491
* Recall: [0.7111, 0.4527, 0.4179, 0.2103]
* Precision: [0.4815, 0.397, 0.5335, 0.3555]

Confusion Matrix: 
[[1418  238  102  236]
 [ 553  919  288  270]
 [ 410  528  845  239]
 [ 564  630  349  411]]

Results for AdaBoostClassifier:
* Accuracy: 0.4871
* Recall: [0.6163, 0.3675, 0.5208, 0.4447]
* Precision: [0.6223, 0.4599, 0.4735, 0.3988]

Confusion Matrix: 
[[1229  207  205  353]
 [ 273  746  499  512]
 [ 220  304 1053  445]
 [ 253  365  467  869]]

# Report on amount of training data
1000: 0.4218

5000: 0.4587

10000: 0.4736

15000: 0.4781

20000: 0.4793

Observed trend tells us that the the accuracy of the classifier increases as the sample size increases.
This is because we have more data, which makes our estimate more precise. In other words, greater sample sizes decrease the standard deviation and increases accuracy.

# Report on feature analysis

5 p-values: ['0.0', '0.0', '0.0', '0.0', '0.0']

50 p-values: ['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '1.299254e-318', '1.1390672768724132e-298', '4.418101073785867e-282', '1.2236900950959972e-280', '3.93323333091639e-277', '6.413930550197132e-269', '4.28900116978717e-261', '8.579503701918315e-246', '3.374066653924117e-241', '9.486518301664556e-236', '1.6504477132017061e-233', '3.185077502785087e-216', '2.2458715112939776e-208', '7.99207631879245e-197', '2.297318594644837e-187', '1.4179619209547032e-179', '2.011729628380683e-178', '7.760850235669144e-174', '2.2707820563142038e-172', '1.0052833164242313e-163', '2.6953282645307003e-163', '3.5924208987830235e-162', '1.3206535549735825e-158', '2.4153362466114776e-154', '1.1814377035415396e-153', '1.0197964398046966e-152', '3.1567334231426135e-151', '1.6023990769408108e-148', '2.524654712597233e-147', '2.3482600522156913e-146', '3.2961712953143947e-144', '9.65215881454409e-141', '4.620869973542296e-134', '1.592504769540035e-133', '1.9186752052719136e-133', '1.4238033031602166e-132', '4.944402919939052e-132', '1.0260722203387049e-131', '1.2157361977897299e-131', '1.1470894005074633e-118', '1.1611297389370851e-110', '8.735409648742486e-108', '4.140960305714248e-101', '8.551252860555295e-101']

Accuracy for 1k: 0.3578

Accuracy for full dataset: 0.3736

Chosen feature intersection: [ 1  2 11]

Top-5 at higher: [  1   2  11  21 163]

### a) What features, if any, are chosen at both the low and high(er) amounts of input data? Also provide a possible explanation as to why this might be.

Number of first-person pronouns, number of second-person pronouns, number of adverbs.

A high number of first-person pronouns may indicate that the person is self-centered.

A high number of second-person pronouns tells us that the person often addresses other people. (verbal attacks, often tries convincing other people)

Adverbs tell us how, when, or where something happened. A high number of adverbs can tell us that the commentor is opinionated.

### b) Are p-values generally higher or lower given more or less data? Why or why not?

Generally speaking, larger sample sizes result in smaller p-values because our population will normalize to a value (thus decreasing our uncertainty), telling us we can reject the null hypothesis.

### c) Name the top 5 features chosen for the 32K training case.

Number of first-person pronouns, second person, pronouns, adverbs. Familiarity standard deviation and receptiviti_self_conscious.
* High # of first-person pronouns and second-person pronouns may reflect in one's political leaning, such as a greater probality they lean to the alt/right due to a high number of verbal attacks, persuasion attempts and egocentrism as according to feature descriptions.
* High number of adverbs tells us they are opinionated which may possibly indicate a left-ish leaning (a trend seen in processed data)
* Greater familiarity standard deviation indicates that they use a large range of words. Trend possibily indicates likely left-leaning. Contrary, lower standard deviation means they use very familiar words (low vocabulary), indicating possible alt/right leaning.
* Greater receptiviti_self_conscious value means greater egocentrism. Likelihood in classified data indicates higher possibility of being alt/right.



# Report on 5-fold cross validation

Kfold Accuracies: [0.4422, 0.3452, 0.4444, 0.483, 0.474]

Kfold Accuracies: [0.3628, 0.3431, 0.4379, 0.4559, 0.4745]

Kfold Accuracies: [0.4088, 0.362, 0.46, 0.4435, 0.4745]

Kfold Accuracies: [0.3924, 0.3544, 0.4388, 0.4758, 0.4816]

Kfold Accuracies: [0.3782, 0.3619, 0.4531, 0.4356, 0.4885]

p-values: [0.4512, 0.2998, 0.433, 0.6361]
