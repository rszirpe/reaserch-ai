# 🔄 How to Restart Everything After Computer Reboot

## What Happens When You Restart Your Computer?

❌ **These processes will STOP:**
- Background trainer (stops learning)
- Flask app (website goes offline)

✅ **These files are SAFE (won't be lost):**
- All training data in database
- Model weights and checkpoints
- Vocabulary file
- Training history

---

## 🚀 Quick Restart (After Reboot)

Open Terminal and run these commands:

```bash
# 1. Navigate to project
cd "/Users/rishi/reserch ai"

# 2. Activate virtual environment
source venv/bin/activate

# 3. Start background trainer (24/7 learning)
python -u background_trainer.py > training.log 2>&1 &

# 4. Start Flask app (website)
python app.py &

# 5. Done! Check it's working
open http://localhost:8080
```

---

## 📋 Copy-Paste One-Liner

```bash
cd "/Users/rishi/reserch ai" && source venv/bin/activate && python -u background_trainer.py > training.log 2>&1 & python app.py &
```

---

## ✅ Verify It's Running

```bash
# Check if both processes are running
ps aux | grep -E "(background_trainer|app.py)" | grep -v grep

# Check training log
tail -f training.log

# Check web interface
curl http://localhost:8080/model-status
```

---

## 💡 Pro Tip: Auto-Start on Boot (Optional)

If you want the training to start automatically when your computer boots:

### Create Launch Agent:

```bash
cat > ~/Library/LaunchAgents/com.researchai.trainer.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.researchai.trainer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd "/Users/rishi/reserch ai" && source venv/bin/activate && python -u background_trainer.py > training.log 2>&1</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/Users/rishi/reserch ai/trainer_error.log</string>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.researchai.trainer.plist
```

Then create another for Flask:

```bash
cat > ~/Library/LaunchAgents/com.researchai.flask.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.researchai.flask</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd "/Users/rishi/reserch ai" && source venv/bin/activate && python app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.researchai.flask.plist
```

Now it will auto-start on every boot! 🎉

---

## 🛑 To Disable Auto-Start:

```bash
launchctl unload ~/Library/LaunchAgents/com.researchai.trainer.plist
launchctl unload ~/Library/LaunchAgents/com.researchai.flask.plist
```

---

## ❓ FAQ

**Q: Will I lose my training progress?**  
A: No! All training data is saved in the database. The model will continue from where it left off.

**Q: How long does it take to restart?**  
A: About 10-15 seconds for both processes to start.

**Q: What if I forget to restart it?**  
A: No problem! Your progress is saved. Just restart when you remember.

---

🎯 **TL;DR**: Restarting is safe, but you need to manually restart the processes after reboot. Use the one-liner above!




