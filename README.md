# Bootstrapping Your Own Representations for Fake News Detection
## Data Preparation. 
The organization of the data folder is as follows：
```
--GossipCop
  --top_img
    --xx.jpg
    ......
  --gossipcop_v3-1_style_based_fake.json
  --gossipcop_v3-2_content_based_fake.json
  --gossipcop_v3-3_integration_based_fake_tn200.json
  --gossipcop_v3-4_story_based_fake.json
  --gossipcop_v3-5_style_based_legitimate.json
  --gossipcop_v3-7_integration_based_legitimate_tn300.json
--datasets
  --gossip
    --gossip_test.xlsx
    --gossip_test_no_filt.xlsx
    --gossip_train.xlsx
    --gossip_train_no_filt.xlsx
```
## Pre-training
The pre-training models of MAE can be downloaded from ["Masked Autoencoders: A PyTorch Implementation"](https://github.com/facebookresearch/mae).

Because of the restriction on upload size, we are unable to upload pretrained models and the processed data. We will further open-source them on GitHub after the anonymous reviewing process.

## Run
	python UAMFD.py

## Result
```
--outputs
  --gossip
    ----xx.pkl

--groupshare
  --mae-main
    --example
      --gossip_experiment.xlsx
--log.txt
--npresultf.txt
--npresulti.txt
--npresultm.txt
--npresultt.txt
--npresultv.txt
```