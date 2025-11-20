# 🧠 24/7 AI Training System - Setup Guide

## 🚀 Quick Start

### 1. Install PyTorch Dependencies

```bash
cd "/Users/rishi/reserch ai"
source venv/bin/activate
pip install torch nltk numpy
```

### 2. Start the Background Trainer (24/7)

```bash
# Start training in the background
nohup python background_trainer.py > training.log 2>&1 &

# Check if it's running
ps aux | grep background_trainer
```

### 3. Start the Flask App

```bash
# In a separate terminal or the same one
python app.py
```

### 4. Open the App

Navigate to: **http://localhost:8080**

You'll see the training status in the top-right corner!

---

## 📊 What Happens

### Phase 1: TRAINING (0-100+ examples)
- 🌐 **Uses Gemini API** for all answers
- 🕷️ **Background trainer scrapes** web every 30 seconds
- 💾 **Builds training dataset** automatically
- 🧠 **Model improves** with each example
- 📈 **Status shows**: `TRAINING: X examples | Quality: Y%`

### Phase 2: READY (Quality > 85%)
- 🧠 **Switches to LOCAL MODEL** automatically
- ✍️ **Gemini corrects grammar** after generation
- 💪 **Model handles** most queries
- 📈 **Status shows**: `LOCAL AI: Quality 87% ✓`

### Phase 3: EXPERT (Grammar > 90%)
- 🎯 **100% Local Model** - no Gemini needed
- ⚡ **Faster responses** (no API calls)
- 🔒 **Complete privacy** - all local
- 📈 **Status shows**: `EXPERT MODE: 100% Independent 🧠`

---

## 🔧 Monitoring

### Check Training Progress

```bash
# View live training logs
tail -f training.log

# Check database
sqlite3 model/training_data.db "SELECT COUNT(*) FROM training_examples;"

# View model status
cat model/model_status.json
```

### Stop Training

```bash
# Find and stop the background trainer
ps aux | grep background_trainer
kill <PID>

# Or kill all Python processes (if safe)
pkill -f background_trainer
```

---

## 📁 Files Created During Training

- `model/training_data.db` - Training examples database
- `model/vocab.pkl` - Tokenizer vocabulary
- `model/checkpoints/model_latest.pth` - Model weights
- `model/model_status.json` - Current training status
- `training.log` - Training logs

---

## 🎯 Expected Timeline

| Time | Status | Description |
|------|--------|-------------|
| **Hour 1** | TRAINING 20% | Collecting initial data |
| **Hour 6** | TRAINING 50% | 200+ examples, vocab built |
| **Day 1** | TRAINING 70% | 500+ examples, basic answers |
| **Day 3** | READY 85% | Auto-switches to local AI |
| **Week 1** | EXPERT 95% | Grammar mastered, fully independent |
| **Ongoing** | EXPERT 100% | Continues learning forever |

---

## 💡 Tips

1. **Let it run 24/7** - The longer it trains, the better it gets
2. **Use the app regularly** - User queries are high-quality training data
3. **Check status periodically** - Watch it improve over time
4. **Be patient** - Good AI takes time to train

---

## 🐛 Troubleshooting

### Training Not Starting
```bash
# Check if PyTorch is installed
python -c "import torch; print(torch.__version__)"

# Manually start training
python background_trainer.py
```

### Model Not Improving
- Need more training data (aim for 500+ examples)
- Let it train for at least 24 hours
- Check `training.log` for errors

### High Memory Usage
- Reduce `BATCH_SIZE` in `config.py`
- Reduce `VOCAB_SIZE` in `config.py`

---

🎉 **Your AI is now learning 24/7!** Watch it evolve from beginner to expert! 🧠🚀

