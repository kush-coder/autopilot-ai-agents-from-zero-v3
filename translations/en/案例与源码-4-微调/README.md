# Keyword Fine-Tuning: Course Data and Configuration

Chapters 29-33 use the `keywords-clean` data here. First complete the data preparation, training, evaluation, and export according to the chapters; when you need to compare answers or curves, open `examples/` and `results/`.

## Where to Start

| Learning Step | What to Use |
| ------------------------------- | --------------------------------------------------------------------------- |
| Chapter 29: Clean and split data | `keywords_data_sharegpt_small.jsonl`, `prepare_keywords_dataset.py` |
| Chapter 29: Document Q&A exercises | `product-manual.md` and `product_qa_reviewed.jsonl` in `document-qa-demo/` |
| Chapter 30: Understand model inputs and labels | `audit_keywords_preprocessing.py`, `examples/preprocessing/` |
| Chapter 31: Training | `processed/keywords-clean/`, `configs/keywords_clean_train.yaml` |
| Chapter 32: Prediction and scoring | Two prediction YAML files, prediction verification script, conversion script, and scoring script |
| Chapter 32: Export the model | `configs/keywords_clean_export.yaml` |
| Chapter 33 (optional): Compare batch and VRAM | `compare_batch_resources.py`, `results/batch-comparison/` |

## Data Files

| File | Purpose |
| ---------------------------------------------------------------- | ---------------------------------------- |
| `keywords_data_sharegpt_small.jsonl` | 2,000 keyword exercise samples |
| `keywords_data_sharegpt.jsonl` | 49,499 complete records for extended practice |
| `processed/keywords-clean/keywords_train.jsonl` | 1,600 training records |
| `processed/keywords-clean/keywords_validation.jsonl` | 200 validation records for tuning the approach and selecting checkpoints |
| `processed/keywords-clean/keywords_test.jsonl` | 200 test records, used only after the approach is finalized |
| `processed/keywords-clean/dataset_info.json` | Registry table required by LLaMA-Factory to read the three datasets |
| `processed/keywords-clean/cleaning_report.json`, `manifest.json` | Processing details, source, and split notes |

To reproduce the processing in this directory, save the results to a directory that does not yet exist:

```bash
python3 prepare_keywords_dataset.py \
  --source keywords_data_sharegpt_small.jsonl \
  --seed chapter-29-v1 \
  --output-dir processed/keywords-clean-repro
```

The seed `chapter-29-v1` is used to fix the grouping; keep this value when following along. The script checks the single-turn ShareGPT structure, normalizes keyword formatting, and deduplicates; it stops if it encounters conflicting answers or remaining formatting problems. It is not a substitute for content review, nor can it identify all similar inputs. Reference answers may still contain questionable content; when preparing your own data, you should continue to review the wording against the original sources.

Both the full dataset and the small files are in this directory; use the small files for the main course flow. The full dataset contains all small samples; do not treat the two as independent training and test sets.

## Scripts and Configurations

| File | Purpose |
| ------------------------------------------ | ---------------------------------------------------------------- |
| `prepare_keywords_dataset.py` | Checks, cleans, and splits keyword samples; reuses the format checks from the scoring script |
| `audit_keywords_preprocessing.py` | Verifies token lengths, labels, and truncation in the LLaMA-Factory environment |
| `audit_keywords_prediction.py` | Runs predictions according to YAML, verifies actual FP16, data fingerprints, and complete record counts |
| `convert_keywords_predictions.py` | Converts prediction files to scoring format while preserving the model's original answers |
| `evaluate_keywords_predictions.py` | Checks format against reference answers and computes keyword metrics |
| `compare_batch_resources.py` | Compares single-GPU batch 4 / accumulation 8 with batch 2 / accumulation 16, recording elapsed time and VRAM samples |
| `configs/keywords_clean_train.yaml` | Chapter 31 LoRA training configuration |
| `configs/keywords_clean_predict_base.yaml` | Chapter 32 base-model test prediction configuration |
| `configs/keywords_clean_predict_lora.yaml` | Chapter 32 Adapter test prediction configuration; must complete training first |
| `configs/keywords_clean_export.yaml` | Chapter 32 merge export configuration |

Following [Chapter 31](../31-LLaMA-Factory%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E4%B8%8E%E5%BE%AE%E8%B0%83%E5%AE%9E%E6%88%98.md), upload the six files in `processed/keywords-clean/` to `LLaMA-Factory/data/keywords-clean/` on AutoDL. Before uploading the YAML files, enter `LLaMA-Factory/` in the AutoDL terminal and run `mkdir -p configs`, then upload them to that directory. Adjust the configuration to your own model and output locations, and use a new output directory.

## Example Materials and Results

| What to Check | Where to Look |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Prompts, thinking mode, reference annotations | [Example reading and recalculation entry](examples/README.md) |
| Training logs, Loss curves, and statistics | `results/keywords-clean/training/`; the corresponding training configuration is `configs/keywords_clean_train.yaml` |
| Model responses for three validation inputs | [Validation and merged model comparison](../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/results/keywords-clean/%E9%AA%8C%E8%AF%81%E4%B8%8E%E5%90%88%E5%B9%B6%E6%A8%A1%E5%9E%8B%E5%AF%B9%E7%85%A7.json ":ignore"): common settings, three model states, and original answers |
| 200 test predictions and scores for each | `generated_predictions.jsonl` and `report.json` in `results/keywords-clean/base/` and `lora/` |
| Actual prediction configurations and precision | `actual-config.yaml` and `prediction-evidence.json` in the above `base/` and `lora/` |
| Exported files and independent loading results | [Export file list](../../../%E6%A1%88%E4%BE%8B%E4%B8%8E%E6%BA%90%E7%A0%81-4-%E5%BE%AE%E8%B0%83/results/keywords-clean/%E5%AF%BC%E5%87%BA%E6%96%87%E4%BB%B6%E6%B8%85%E5%8D%95.json ":ignore") and the above validation comparison; the export configuration is `configs/keywords_clean_export.yaml` |
| Batch and VRAM comparison | Configuration, logs, GPU samples, curves, and `comparison.json` in `results/batch-comparison/` |
| WebUI pages and training status | Page configuration, training parameters, status, and curves in `results/keywords-clean-webui-20260908/` |

**Note the correspondence between examples:** Chapter 30 log analysis, Chapter 32 prediction, scoring, and export correspond to the CLI example `results/keywords-clean/`; Chapter 31 WebUI screenshots correspond to a different training result. Both groups use the same data and core parameters, but the Adapter and output directories are saved separately. When following along yourself, use your own set of artifacts.

These materials contain problems such as formatting issues, missing words, and duplicates, and can be used for analysis practice; they do not indicate that the model has met business requirements. The directory contains no model weights or complete continued pre-training checkpoints, and the example paths cannot be entered into WebUI as Adapter paths.

Use Python 3.10 or later; following [Chapter 32, Section 4.4](../32-%E5%BE%AE%E8%B0%83%E6%95%88%E6%9E%9C%E8%AF%84%E4%BC%B0%E4%B8%8E%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md?id=_44-running-the-conversion-and-scoring-scripts), you can reproduce the scoring locally. The converted JSONL and new scoring reports are generated by the scripts and saved to an unused directory such as `results/keywords-clean-rescore/`.
