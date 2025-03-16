# Vietnamese Event Extraction Project

## Overview

This project implements a comprehensive event extraction system for Vietnamese text, comparing three different approaches: Conditional Random Fields (CRF), BiLSTM-CRF, and PhoBERT. The system can identify three types of events: Leader-Activity, Policy-Announcement, and Emergency-Event, along with their triggers and arguments.

## Features

- **Multiple Event Extraction Models**: Implements and evaluates CRF, BiLSTM-CRF, and PhoBERT models
- **Detailed Performance Analysis**: Provides comprehensive comparison metrics and visualizations
- **Real-time Demo Interface**: Web-based application for testing and visualizing event extraction
- **Vietnamese Language Support**: Specialized for Vietnamese text processing

## Dataset

The project uses a custom dataset containing Vietnamese news and social media content labeled with three types of events:
- **Leader-Activity**: Events related to activities of political and organizational leaders
- **Policy-Announcement**: Events related to policy and regulation announcements
- **Emergency-Event**: Events related to emergencies, disasters, and crises

## Model Performance

| Model | Precision | Recall | F1 Score |
|-------|-----------|--------|----------|
| CRF | 56.4% | 59.6% | 53.1% |
| BiLSTM-CRF | 54.8% | 54.7% | 50.1% |
| PhoBERT | 67.1% | 60.4% | 70.1% |

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/vietnamese-event-extraction.git
cd vietnamese-event-extraction
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Download required resources (if not included):
```bash
python download_resources.py
```

## Usage

### Data Preprocessing
```bash
python pre-data.py
```

### Train and Evaluate Models

#### CRF Model
```bash
python CRF.py
```

#### BiLSTM-CRF Model
```bash
python BiLSTM-CRF.py
```

#### PhoBERT Model
```bash
python PhoBERT.py
```

### Interactive Demo
```bash
python RealTime.py
```
Access the demo interface through the link provided in the terminal.

## Project Structure

```
vietnamese-event-extraction/
├── data/
│   ├── data1.json              # Raw data
│   └── tagged_events.json      # Processed data with annotations
├── models/
│   ├── CRF.py                  # CRF model implementation
│   ├── BiLSTM-CRF.py           # BiLSTM-CRF model implementation
│   └── PhoBERT.py              # PhoBERT model implementation
├── utils/
│   ├── pre-data.py             # Data preprocessing utilities
│   └── vizualize.py            # Visualization utilities
├── results/
│   ├── crf_confusion_matrix.png        # CRF evaluation results
│   ├── event_confusion_matrix.png      # BiLSTM-CRF evaluation results
│   ├── phobert_confusion_matrix.png    # PhoBERT evaluation results
│   ├── crf_loss_history.png            # CRF training progress
│   ├── loss_history.png                # BiLSTM-CRF training progress
│   └── phobert_loss_history.png        # PhoBERT training progress
├── RealTime.py                 # Interactive demo application
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Demo Application

The interactive demo application (RealTime.py) provides a user-friendly interface to:

1. Input Vietnamese text for event extraction
2. Select a model (CRF, BiLSTM-CRF, PhoBERT)
3. Visualize extraction results with confidence scores
4. Compare performance metrics across models

## Key Findings

- PhoBERT outperforms traditional models (CRF and BiLSTM-CRF) in all metrics
- All models struggle with the "Emergency-Event" type due to data imbalance
- Context understanding is crucial for accurate event extraction in Vietnamese
- Pre-trained language models show significant advantages for this task

## Future Work

- Expand dataset with more examples of underrepresented event types
- Explore hybrid approaches combining PhoBERT with CRF
- Implement domain-specific fine-tuning
- Integrate with real-time news and social media monitoring systems

## Contributors

- Nguyễn Nam: Data processing, CRF and BiLSTM-CRF models, demo interface
- Phạm Hoàng: Data collection, PhoBERT model, performance benchmarking

## Citation

If you use this code or data in your research, please cite:
```
@misc{vietnameseeventextraction2025,
  author = {Nguyen Nam and Pham Hoang},
  title = {Vietnamese Event Extraction with CRF, BiLSTM-CRF, and PhoBERT},
  year = {2025},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/your-username/vietnamese-event-extraction}}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [VinAI Research](https://github.com/VinAIResearch/PhoBERT) for the PhoBERT model
- [sklearn-crfsuite](https://github.com/TeamHG-Memex/sklearn-crfsuite) for the CRF implementation
- [Gradio](https://www.gradio.app/) for the interactive demo interface